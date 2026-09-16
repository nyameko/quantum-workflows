#!/usr/bin/env bash
#SBATCH --job-name=qw-sqd-n2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=qw-sqd-n2-%j.log
# For QPU execution submit with:
# sbatch --gres=qpu:1 --qpu=ibm_resource_name --export=ALL,QUANTUM_EXECUTOR=qrmi slurm/sqd.sbatch

set -euo pipefail

: "${QUANTUM_WORKFLOWS_IMAGE:?Set QUANTUM_WORKFLOWS_IMAGE to an immutable SQD .sif path}"
result_root="${QUANTUM_WORKFLOWS_RESULTS:-${SLURM_SUBMIT_DIR}/results}"
executor="${QUANTUM_EXECUTOR:-statevector}"
mkdir -p "${result_root}"

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
module load apptainer
srun apptainer exec \
  --bind "${result_root}:/results" \
  "${QUANTUM_WORKFLOWS_IMAGE}" \
  qw sqd \
    --executor "${executor}" \
    --shots "${SHOTS:-20000}" \
    --samples-per-batch "${SAMPLES_PER_BATCH:-1000}" \
    --num-batches "${NUM_BATCHES:-3}" \
    --max-iterations "${MAX_ITERATIONS:-5}" \
    --max-dim "${MAX_DIM:-50}" \
    --output /results
