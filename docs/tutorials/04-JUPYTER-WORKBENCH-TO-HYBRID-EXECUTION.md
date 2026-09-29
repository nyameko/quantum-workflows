# Tutorial — From a cheap notebook to burst CPU/GPU/QPU execution

This tutorial defines the intended researcher interaction pattern.

## 1. Start the workbench

The user starts a low-cost Jupyter workbench. It mounts the same `/home/research/<user>` seen through SSH and contains the client libraries needed to prepare work.

The workbench is suitable for circuit construction, light local tests, plots, Git, documentation, agent chat and inspecting prior results.

## 2. Submit substantial work

Do not request physical Slurm partitions from ordinary notebook code. Submit a logical target through the platform/workflow client.

Illustrative future interface:

```python
from quantum_platform import compute

job = compute.submit(
    "qiskit-aer-large",
    script="simulate.py",
    inputs={"shots": 100000},
)
```

The backend resolves entitlement, environment, resource class and scheduler placement.

## 3. Notebook lifetime is independent

The workbench may be disconnected or culled. The run remains persisted and queryable. Reconnect later and recover it by run/job ID.

## 4. Hybrid workflow

A more advanced run can acquire and release resources stage-by-stage:

```text
CPU preprocessing
  -> release CPU
GPU simulation
  -> release GPU
QPU submission / wait / retry under policy
  -> release QPU/provider allocation
CPU/GPU postprocess
  -> release
structured result + provenance
```

## 5. Interactive exception

If the algorithm genuinely requires live GPU/HPC interaction, use an explicitly entitled BatchSpawner/interactive-HPC session instead. The higher cost and walltime should be visible to the user.
