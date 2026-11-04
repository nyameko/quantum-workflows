# Troubleshooting Quantum Workflows

## Installation/import failure

Confirm interpreter is Python 3.14, active venv and installed extras; inspect `python --version`, `python -m pip show quantum-workflows` and `qw --help`. An old environment or mixed provider extras can cause incompatible Qiskit/SciPy dependency resolutions. Start from a fresh isolated environment.

## GPU executor not available

Check actual `nvidia-smi` in the allocated GPU node, container runtime, CUDA/driver versions, optional simulator wheel and GPU method support. A GPU-enabled Python package on a CPU-only workbench is not a GPU allocation. Do not force GPU simulator flags when the build cannot provide them.

## QPU provider fails

Separate authentication, plan/allocation, backend selection, provider downtime, queueing, API/SDK compatibility and resource cap. Never post tokens. Reproduce the same circuit locally before escalating hardware service faults.

## Slurm job rejected

Inspect job name, partition, QOS, walltime and reservation policies. A site may allow only specific names and fixed walltimes; use facility-approved templates rather than altering application authorization. Confirm `sacct` exit code and artifact directory after completion.

## Results do not agree with theory

Check seed/shot uncertainty, Hamiltonian convention, coupling units, time-step error, qubit ordering, normalization, backend noise and exact reference. An altered experiment can pass the execution smoke but fail scientific acceptance; report both.

See [scientific checks](Scientific-provenance.md) and [reference commands](Reference-experiments.md).