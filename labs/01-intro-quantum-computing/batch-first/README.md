# Batch-first quantum simulator academy (00–07)

> **Scientific preparation is cheap; expensive execution is scheduled.**

These eight *new short entry labs* complement, not replace, `../Intro_QC_Demo.ipynb` and `../02-bell-cpu-gpu-qpu.ipynb`.

| Lab | Topic | Local baseline | Optional expensive backend |
| --- | --- | --- | --- |
| 00 | Bell circuit | Qiskit Aer CPU | None |
| 01 | First Slurm GPU batch | Native Slurm submit/status/result only | Aer GPU A100/H200, 1 GPU |
| 02 | Simulator scaling | Aer CPU + statevector memory model | Aer GPU Slurm comparison |
| 03 | PennyLane Lightning | lightning.qubit | lightning.gpu Slurm |
| 04 | Cirq + qsim + cuQuantum | Cirq, optional qsim CPU | separate qsim/CUDA/cuStateVec/cuTensorNet runners |
| 05 | IQM architectures | IQMFakeAdonis CPU | physical IQM only after approval |
| 06 | Pulser/Pasqal | QutipEmulator CPU | emu-sv/emu-mps after validated setup |
| 07 | Real QPU | Aer CPU | provider-native approved remote QPU, disabled by default |

Workbenches are Kubernetes/JupyterHub CPU pods. Native Slurm and the provider control plane own *all* scarce allocations. Never reserve a GPU for time spent reading, writing or inspecting results. Lab 01 has a deliberate prerequisite: a reviewed **per-user** Slurm client path on the submit host, not the currently deployed privileged gateway helper. Current notebooks are examples/source, **not evidence that A100/H200/QPU execution is live**.

## Software environment notes

Lab 00/01/02/07: Qiskit, Qiskit Aer; Lab 03: PennyLane + Lightning CPU; Lab 04: Cirq, qsimcirq optional; Lab 05: qiskit-iqm fake backends; Lab 06: Pulser + pulser-simulation. Use **separate vetted kernels/images** rather than `pip install` every SDK in an NFS home. `docs/ENVIRONMENTS.md` describes the promoted image catalogue.

Submission conventions: for CPU Jupyter → ACE login use the researcher's own SSH identity (not a shared gateway): `SLURM_LOGIN_HOST` is the approved login FQDN, `SLURM_RESEARCHER_SSH_KEY` defaults to `~/.ssh/id_ed25519` (owned by the user, mode 0600), and `SLURM_RESEARCHER_KNOWN_HOSTS` defaults to `~/.ssh/known_hosts` with its host key verified out of band. This reuses ordinary `ssh` + **native** remote `sbatch/squeue/sacct`; no client SDK, browser terminal, MUNGE secret in Kubernetes, or `runuser` helper. Site public SSH key admission is prepared in [infra P0 PR #290](https://github.com/nyameko/infra-hpc-qc-k8s/pull/290); the portal's legacy shared-gateway API has a [separate P0 blocker](https://github.com/nyameko/quantum-platform/issues/162). **Do not retire a live portal gateway until that compatibility issue is resolved.** Configure `SLURM_GPU_PARTITION` and absolute `QISKIT_AER_GPU_IMAGE` from the approved **site**; launch notebook 01 from a checkout visible to the submit node; independently stage inputs/results across sites. `slurm/aer-gpu.sbatch` and `runners/qiskit-aer-gpu/aer_gpu_run.py` are the first runnable reference, subject to resource admission. If the site supports no native per-user submit path yet, STOP: do not substitute `runuser`, sudo or an agent-selected UID.

## Acceptance evidence

1. Baseline CPU notebook passes without GPU or credentials.
2. `nlisa` (human operator acceptance) runs `sbatch` as their own authorized POSIX principal; cannot cancel other users' jobs.
3. One real A100 GPU run exits with scientific verification, `sacct` TRES/accounting and returned JSON result; notebook restarts independently.
4. Repeat on separately authorized remote Axis H200 with checksum-verified stage-in/out and no overlapping inference GPU allocation.
5. Separate optional notebook/backends are promoted only after isolated scientific and CUDA compatibility tests. Physical QPU requires an independently approved quota and charge.

Other references: [M5 architecture](../../../docs/M5-BATCH-FIRST-SIMULATOR-PATH.md), [scientific environments](../../../docs/ENVIRONMENTS.md), [workbench guide](../../../docs/wiki/Execution-environments.md).
