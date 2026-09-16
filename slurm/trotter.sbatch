#!/usr/bin/env bash
#SBATCH --job-name=qw-trotter
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=qw-trotter-%j.log

set -euo pipefail

: "${QUANTUM_WORKFLOWS_IMAGE:?Set QUANTUM_WORKFLOWS_IMAGE to an immutable .sif path}"
result_root="${QUANTUM_WORKFLOWS_RESULTS:-${SLURM_SUBMIT_DIR}/results}"
executor="${QUANTUM_EXECUTOR:-aer}"
mkdir -p "${result_root}"

module load apptainer
srun apptainer exec \
  --bind "${result_root}:/results" \
  "${QUANTUM_WORKFLOWS_IMAGE}" \
  qw trotter \
    --executor "${executor}" \
    --qubits "${QUBITS:-6}" \
    --final-time "${FINAL_TIME:-3.0}" \
    --time-points "${TIME_POINTS:-13}" \
    --trotter-steps "${TROTTER_STEPS:-4}" \
    --shots "${SHOTS:-4096}" \
    --output /results
