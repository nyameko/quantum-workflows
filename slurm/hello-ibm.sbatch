#!/usr/bin/env bash
#SBATCH --job-name=qw-hello-ibm
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:20:00
#SBATCH --output=qw-hello-ibm-%j.log
# Request at submission time after QRMI/SPANK is installed:
# sbatch --gres=qpu:1 --qpu=ibm_resource_name slurm/hello-ibm.sbatch

set -euo pipefail

: "${QUANTUM_WORKFLOWS_IMAGE:?Set QUANTUM_WORKFLOWS_IMAGE to an immutable .sif path}"
result_root="${QUANTUM_WORKFLOWS_RESULTS:-${SLURM_SUBMIT_DIR}/results}"
mkdir -p "${result_root}"

module load apptainer
srun apptainer exec \
  --bind "${result_root}:/results" \
  "${QUANTUM_WORKFLOWS_IMAGE}" \
  qw hello --executor qrmi --shots 1024 --output /results
