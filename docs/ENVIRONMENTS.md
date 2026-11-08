# Scientific Environments

Scientific environments are a product contract shared by notebooks, durable Slurm execution and future GPU/QPU providers.

## Why prebuilt environments matter

Manual virtual environments are useful for teaching environment isolation, but a cohort should not independently download the same SDK stack into NFS-backed homes.

The platform should therefore publish versioned, tested environments for common SDKs.

## Initial environment catalogue

CPU:

- Intro Qiskit;
- Qiskit / Aer CPU;
- PennyLane CPU;
- interoperability / translation;
- MPI/HPL CPU.

GPU:

- Qiskit Aer GPU — A100;
- Qiskit Aer GPU — H200;
- PennyLane Lightning GPU — A100;
- PennyLane Lightning GPU — H200;
- CUDA-Q — A100;
- CUDA-Q — H200;
- Pasqal emulation — H200;
- HPL / HPL-MxP — A100/H200.

QPU/provider environments:

- IBM / Qiskit Runtime;
- IQM;
- Pasqal / Pulser;
- D-Wave / Ocean;
- other provider-specific SDKs as maintained.

## Environment is not the execution target

Keep these concepts separate:

```text
workflow
  +
environment
  +
execution provider
  +
resource profile
```

Example:

```text
workflow:   hpl
environment:nvidia-hpl
provider:   axis-atmos-h200
profile:    h200-multi
```

A user-facing offering such as “HPL — H200” may resolve to those four internal objects.

## OCI and Apptainer

Versioned OCI images are the common build artifact.

For Slurm:

```text
OCI image
  ↓
Apptainer SIF/cache
  ↓
Slurm job
```

The image is not a substitute for the facility software stack. Lmod remains appropriate for compilers, MPI, CUDA/ROCm and shared applications where native integration/performance matters.

## Immutable image generation and ownership (batch-first M5)

**Quantum Workflows** owns the versioned scientific Dockerfile/OCI source, SDK dependency choices, numerical smoke tests and runner provenance. The existing `.github/workflows/images.yml` builds source-controlled images; new GPU runner targets should only enter its publishing matrix after isolated builds and compatibility checks. **Infrastructure/Axis operator** owns OCI digest promotion, site-visible SIF conversion/cache, NVIDIA driver and library compatibility, GPU cgroups/GRES, storage quota and deployment. **Quantum Platform** presents an approved environment/offering—not an image build UI. ACP guides, without building images or impersonating users.

| Image family | Scientific SDK/backend | Promotion |
| --- | --- | --- |
| `qiskit-cpu` | Qiskit/Aer CPU | reuse existing tested image |
| `qiskit-aer-gpu` | Qiskit Aer GPU 0.18.2, Python 3.14 candidate | candidate Dockerfile in `runners/qiskit-aer-gpu`; **not yet site/CI validated** |
| `pennylane-lightning-gpu` | PennyLane Lightning, NVIDIA cuQuantum | separate CUDA/GPU compatibility gate |
| `cirq-qsim-gpu` | Cirq/qsim CUDA | separate qsim build/benchmark gate |
| `cuquantum-gpu` | NVIDIA cuStateVec/cuTensorNet | separate method/correctness gate |
| `pulser-neutral-atom` | Pulser/Qutip, optional emu-sv/emu-mps | distinct CPU/GPU backends; do not assume API equivalence |
| `iqm-fake-cpu` | qiskit-iqm local fake backends | CPU and no credentials |
| `provider-qpu-client` | official native QPU SDKs | credential/quotas must be authorized independently |

Build once as OCI and publish by digest; convert or retrieve as Apptainer SIF on **approved site storage**, running as a regular Slurm user under `srun apptainer exec --nv` when allocated. An OCI image/SIF is not a Kubernetes Pod. Choose upstream-maintained images only when their provenance, licensing, known vulnerabilities, host drivers, Python 3.14 support and numerical fixtures pass review. Never promote images just because a `pip install` succeeds.

## Compatibility

Avoid one giant “all vendors” environment when SDK constraints conflict.

Prefer small purpose-built images implementing the same workflow/result contract.

Every image should record:

- source commit;
- image digest;
- Python version;
- SDK versions;
- GPU/CUDA requirements;
- supported executor types;
- smoke-test status.
