#!/usr/bin/env bash
#SBATCH --job-name=jhub-aer-gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --output=jhub-aer-gpu-%j.log

set -euo pipefail
: "${QISKIT_AER_GPU_IMAGE:?Site must publish the approved immutable Apptainer SIF}"
: "${SLURM_SUBMIT_DIR:?Slurm submit directory is required}"
: "${SLURM_JOB_ID:?Slurm job identity is required}"
cd "${SLURM_SUBMIT_DIR}"
mkdir -p results
# Run only in a scheduler-authorised GPU allocation.
# Site must enforce GRES device cgroups; CUDA_VISIBLE_DEVICES alone is not isolation.
srun apptainer exec --nv \
  --bind "${SLURM_SUBMIT_DIR}:/workspace" --pwd /workspace \
  "${QISKIT_AER_GPU_IMAGE}" \
  python /workspace/runners/qiskit-aer-gpu/aer_gpu_run.py \
  --qubits "${AER_QUBITS:-22}" --shots "${AER_SHOTS:-2048}" \
  --output "/workspace/results/aer-gpu-${SLURM_JOB_ID}.json"
