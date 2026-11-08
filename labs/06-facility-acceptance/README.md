# Lab 06 — Facility backend readiness and hands-on scientific acceptance

**Status:** source-only, review required; no H200/A100/IBM/IQM/Pasqal hardware result is implied.

Start with [00-backend-readiness.ipynb](00-backend-readiness.ipynb). It is a
small diagnostic for the **current** notebook kernel, not a universal
environment installer, scheduler, credential broker or vendor SDK replacement.

## What the notebook does

- Records Python, installed SDK distribution versions and visible NVIDIA
  devices (presence is **not** proof of allocated GPU isolation).
- Performs a real, seeded **Qiskit Aer CPU Bell circuit** and checks that
  only correlated `00` and `11` outcomes occur.
- Optionally reuses `quantum_workflows.lightning.sample_bell` to test
  Lightning CPU without duplicating a circuit implementation.
- Has **disabled-by-default** Aer GPU and Lightning GPU Bell smoke checks;
  enable only inside an exclusive, operator-approved GPU allocation.
- Has **disabled-by-default** IBM Quantum account/backend *discovery*, using
  `IBM_QUANTUM_API_KEY` and `IBM_QUANTUM_INSTANCE_CRN` supplied from a
  protected service. It submits **zero** QPU jobs.
- Reports PASS, FAIL, SKIP or TODO distinctly. Package detection for Cirq,
  IQM, Pulser and cuQuantum is inventory only, not a scientific result.
- Optionally writes `results/backend-readiness.json` containing no tokens
  or instance identifiers. Do not interpret this as an experiment manifest.

The notebook does **not** need or request sudo, host driver installation,
GPU provisioning or internet credentials for the default CPU run.

## Delivery matrix (gates to complete, not claims)

| Workload | Workbench/CPU | Slurm CPU | A100 | H200 (science GPU 4–7) | External QPU |
| --- | --- | --- | --- | --- | --- |
| Qiskit statevector/Bell | Existing lesson | Run reference under job allocation | Aer GPU runner (pending) | Aer GPU runner (pending) | IBM opt-in job |
| PennyLane Lightning Bell | CPU kernel | CPU job | Lightning GPU runner (pending) | Lightning GPU runner (pending) | Not equivalent |
| Portfolio Ising / VQE reference | [M5a CPU notebook](../05-quantum-finance/01-portfolio-ising-lightning-cpu.ipynb) | Capture exact reference | Compare against CPU (pending) | First M5b target (pending) | Future evaluated variant |
| Cirq | Simple CPU circuit and measurement | CPU runner | Only where supported by actual backend | No GPU claimed by importing Cirq | Provider-specific integration |
| NVIDIA cuQuantum | No CUDA acceleration | N/A | cuStateVec/cuTensorNet device tests | cuStateVec/cuTensorNet tests, then 2/4-GPU scaling | Not a QPU |
| IQM | Native Qiskit-IQM local/mock or authorised emulator | Prep/transpile | N/A for first test | N/A for first test | Entitlement-required IQM backend |
| Pasqal / Pulser | Pulse/register/Rydberg-blockade simulator | Pulse emulator | Optimise only if proven | Optimise only if proven | Entitlement-required neutral-atom QPU |
| IBM Classroom Account | Credential-free Aer first | Offline prep and job manifest | Simulator before QPU | Simulator before QPU | **Per-student** instances/quotas |

The remote providers **must not** be treated as interchangeable Bell-state
backends. IQM gate topology and Pasqal analog pulse semantics need separate
validated native experiments. For NVIDIA, explicit simulator GPU execution is
necessary: `pip install qiskit-aer` ordinarily gives the CPU build; Linux
CUDA 12 uses `qiskit-aer-gpu` in a *separate pinned runner environment*.
PennyLane Lightning GPU needs a compatible cuQuantum/CUDA stack. Do not
install GPU SDKs into every lightweight Kubernetes workbench.

## Practical acceptance order

1. Run this notebook from the ordinary JupyterHub workbench. Verify the CPU
   Bell check; record the missing optional SDKs without counting them as
   failures of the base workbench.
2. Re-run the same notebook from an authorised Slurm **CPU** job or kernel;
   retain the job ID, Python environment digest and result directory.
3. Build and test one pinned H200 science-GPU runner, limiting visibility to
   exactly one allocated GPU from 4–7. Switch `ENABLE_GPU_SMOKES=True`
   only inside that allocation; run Aer GPU and Lightning GPU independently
   and capture versions, GPU UUID, result and runtime.
4. Repeat on a genuine A100 allocation; compare numerics, not guessed
   speedups. Only then evaluate multi-GPU capability using upstream
   documented APIs, scheduler allocation and actual measured scaling.
5. Connect JupyterHub's approved submission/status/result path to Slurm
   without keeping a GPU allocated to an idle browser session. Exercise
   stop/reconnect/results and other-user access denial.
6. Enable IBM Classroom **backend discovery only**, scoped to the individual
   student instance; explicitly approve any actual QPU submission with a
   shot budget, remaining quota check and persistent provider job ID.
7. Add separate Cirq, IQM, Pulser and cuQuantum scientific experiments with
   an independent expected result; don't label package presence PASS.

The first deep GPU scientific demonstration should reuse the existing
PennyLane portfolio Ising reference and match its exact classical baseline
within explicit tolerance, not add another toy-specific research framework.

## IBM Classroom Accounts

IBM's published Classroom Account procedure creates an education account
and lets the owner invite students. Its recommended default allocates
**one IBM Cloud instance per student**. The documentation currently states
**up to 10 minutes of QPU usage per 28-day rolling window per instance**
under the Open Plan; confirm the account's actual limits before class.

Each student should own their IBM credentials and instance CRN. The
Quantum Platform entitlement layer can record an approved, non-secret
instance association, but never copy a classroom token into source code,
a notebook, a Git issue, or another student's environment. Use a
credential broker/Vault for approved compute jobs, and never consume
credits automatically during discovery.

Official references:
- [IBM Classroom Accounts](https://quantum.cloud.ibm.com/docs/en/guides/classroom-accounts)
- [IBM credentials and instance CRNs](https://quantum.cloud.ibm.com/docs/en/guides/initialize-account)
- [Qiskit Aer GPU](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)
- [PennyLane Lightning GPU](https://docs.pennylane.ai/projects/lightning/en/latest/lightning_gpu/device.html)
- [IQM Qiskit provider](https://docs.iqm.tech/iqm-client/api/iqm.qiskit_iqm.iqm_provider.IQMProvider.html)
- [Pasqal Pulser](https://docs.pasqal.com/pulser/)

## Honest acceptance language

Passing local CPU checks, or passing a CDI one-GPU `nvidia-smi` check, does
not establish that Slurm can allocate an H200 GPU, that student device
confinement is safe, that a scientific GPU plugin executes, or that remote
hardware can be submitted. Each is a separate operator-observed milestone.

No live JupyterHub/Slurm/IBM acceptance, GPU consumption, Kubernetes change,
or credentials were used to author this lab.
