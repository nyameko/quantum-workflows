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
