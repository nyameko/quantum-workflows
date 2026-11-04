# Execution environments: local CPU, Slurm, GPU and QPU

## Four independent choices

A run is identified by **workflow + software environment + execution provider + resource profile**. Changing GPU node or QPU backend is not equivalent to changing the scientific method. The portal owns authorization/catalog; this repository owns runner software and scientific results.

| Execution target | Expected path | Caveat |
|---|---|---|
| Local laptop / Jupyter CPU | Python 3.14 venv, native scientific SDKs | Good for notebooks and small references |
| Slurm CPU | authorized submission, versioned OCI→Apptainer runner | Separate workbench from durable job |
| A100/H200 simulator | GPU-enabled image and scheduler allocation | CUDA/runtime/driver and dependency compatibility essential |
| Remote QPU | explicit provider credential and allocation | Provider availability, queue, shots/credits and calibration vary |

## Current templates

The source tree contains Slurm templates under `slurm/cpu-smoke.sbatch`, `hello-ibm.sbatch`, `trotter.sbatch`, and `sqd.sbatch`; current OCI build contexts are `runners/qiskit-cpu/` and `runners/sqd/`. Treat GPU runners/accelerators and vendor SDK matrices in planning docs as target environments until an actual image, resource policy and acceptance result exist.

## CPU → GPU comparison

Run the same circuit, observable, seed/shot plan, tolerance and input with CPU reference first. Pin the correct CUDA-compatible `qiskit-aer` GPU or PennyLane Lightning GPU dependency in a **dedicated** runner; default `pip install` may install a CPU-only wheel. Run inside an allocated GPU node, not a cheap web workbench. Report accelerator model, driver/CUDA versions, method, precision, runtime, memory, power if measured and numerical agreement.

## Hardware access

Use a real provider entitlement and official SDK credentials through protected providers/secret brokers. Never paste tokens into notebooks, issues or an agent chat. Reserve hardware use as a deliberate opt-in; plan finite shot budgets, queue delays, noisy baselines and reproducible calibration references.

See [environments](https://github.com/nyameko/quantum-workflows/blob/main/docs/ENVIRONMENTS.md), [workbench-to-execution tutorial](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/04-JUPYTER-WORKBENCH-TO-HYBRID-EXECUTION.md) and [run architecture](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md).