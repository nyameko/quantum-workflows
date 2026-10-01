#!/usr/bin/env bash
#SBATCH --job-name=jhub-cpu-smoke
#SBATCH --partition=cpu-small
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

set -euo pipefail

: "${QUANTUM_WORKFLOWS_IMAGE:?Set QUANTUM_WORKFLOWS_IMAGE to an immutable qiskit-cpu .sif path}"
result_root="${QUANTUM_WORKFLOWS_RESULTS:-${SLURM_SUBMIT_DIR}/results}"
mkdir -p "${result_root}"

module load apptainer
srun apptainer exec \
  --bind "${result_root}:/results" \
  "${QUANTUM_WORKFLOWS_IMAGE}" \
  cpu-smoke \
    --iterations "${CPU_SMOKE_ITERATIONS:-100000}" \
    --output /results
