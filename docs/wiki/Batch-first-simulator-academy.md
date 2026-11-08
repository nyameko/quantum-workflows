# Batch-first simulator academy

> **Scientific preparation is cheap; expensive execution is scheduled.**

Open the [eight introductory notebooks](../../labs/01-intro-quantum-computing/batch-first/README.md), starting with credential-free Aer CPU and moving to a separately authorised, one-GPU Slurm job. The **workbench remains a small JupyterHub/KubeSpawner CPU pod**; its lifetime does not own a Slurm GPU allocation.

The official upstream SDKs are taught natively: Qiskit/Aer, PennyLane/Lightning, Cirq/qsim/cuQuantum, IQM fake backends, Pasqal/Pulser neutral-atom emulation, and approved physical provider SDKs. Frameworks, simulator backends, execution resources and QPUs are distinct. No default QPU credits or GPU interactive session.

- Read [M5 batch-first design and acceptance](../M5-BATCH-FIRST-SIMULATOR-PATH.md).
- Read [scientific environments](../ENVIRONMENTS.md).
- Read [Slurm runner contract](Slurm-runner-contract.md).
- **Status:** notebook/runner **source only** until native researcher Slurm access, GPU GRES, image build and site tests are independently observed.
