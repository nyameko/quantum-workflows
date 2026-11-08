# M5 — Scientific Workflows and Reproducible Hybrid Quantum-Centric Computing

**Planning status:** architecture and acceptance roadmap. **Not a deployment claim,
approved H200 allocation, completed M5 workflow, or replacement for the existing
V0.1–V2 Quantum Workflows roadmap.**

**Predecessor:** [ACP M4a–M4g integrated release gate](https://github.com/nyameko/agent-control-plane/issues/45).
Do not re-scope M4 to include H200 scientific execution. M4's goal is a portable,
usable, authorised research assistant. Older documents called the scientific
workflow work *M4* and the agent control plane *M5*; the project subsequently
locked M4a–M4g as persistent ACP and uses *M5* for the science-delivery handoff.
The existing workflow **V0.1–V2 versions remain unchanged**.

## A. The real research outcome

A researcher should be able to ask:

> How do I run a PennyLane portfolio-optimisation / chemistry / nuclear
> Hamiltonian simulation with Lightning on an available H200 allocation?

And receive **a usable, inspectable execution path**, not an invented cluster
command or a model claiming to have executed it. The Guide may explain and
select a *reviewed* workflow; the researcher explicitly authorises a specific
compute offering, requested time/resource budget and input parameters; an
approved scheduler runs ordinary scientific code; a durable result is returned
with numerical validation and provenance.

The same contract must support other scientific domains without treating
different physical representations or vendor QPUs as interchangeable devices.

## B. Current source baseline (not a fresh live cluster acceptance)

- `src/quantum_workflows/lightning.py`: two-qubit Bell example with explicit
  `lightning.qubit` vs `lightning.gpu` selection and no implicit GPU fallback.
- `labs/01-intro-quantum-computing/`: comprehensive introductory Qiskit and
  multi-backend Bell notebooks; `src/quantum_workflows` includes existing
  IBM Bell, Ising/Trotter, SQD, provenance and CPU-smoke examples.
- `slurm/*.sbatch` and `runners/qiskit-cpu/`, `runners/sqd/`:
  patterns for Slurm/Apptainer execution. Prior M3 evidence reports a completed
  CPU-smoke job, but it is **not H200 verification**.
- `quantum-platform`: identity/programmes, workbench and restricted Slurm
  execution APIs; `ACP`: projects, conversations, memory, owner-bound
  reviewed references, audited task/run correlation.
- `photonicslab`: independently tested coherent Jones/polarisation optics,
  scalar diffraction, detector time-tagging, coincidences and **idealised**
  BB84 alpha examples; laser cavities, SPDC/Fock quantum states, realistic
  detectors and H200 acceleration remain separately validated future work.
- A100/H200 scientific ownership, Axis Atmos provider and CUDA/cuQuantum
  software compatibility require **actual site-operator evidence**.
  Inference-serving capacity is not automatically an HPC GPU allocation.

## C. One authority per subsystem

| Authority | Responsibility in M5 | Must not do |
| --- | --- | --- |
| `quantum-workflows` | Reviewed scientific scripts/notebooks; input and output schemas; numerical tests; runner images; experiment provenance | Create a new identity store, GPU scheduler or universal provider SDK |
| `infra-hpc-qc-k8s` | Slurm/QRMI/Axis resource integration; GPU allocations; CUDA/MPI/Apptainer images; storage; GitOps | Let inference and Slurm independently allocate the same GPU; live changes without operator review |
| `quantum-platform` | Authenticate user/programme; resource catalog; quotas, cost consent, submit/status/cancel; Jupyter and result UI | Run arbitrary shell command supplied by an agent or bypass scheduler entitlements |
| `agent-control-plane` | Canonical researcher context, approved skills and policies, authorised task and run association, model explanation and audit | Own scientific state instead of workflow manifest; create a second Slurm/provider scheduler |
| `photonicslab` | Versioned numerical optics models, physical accuracy checks, validated experiments | Claim unimplemented nonlinear/quantum optics or automatic GPU deployment |

Canonical scientific outcomes stay in the `quantum-workflows` **experiment
manifest and artifacts**. ACP stores references/associations to those records;
the provider and Slurm retain authoritative scheduling/job states.

## D. Existing Quantum Workflows V0.1–V2 scope, preserved

| Existing version | Existing intent | M5 action |
| --- | --- | --- |
| V0.1 Foundation | Bell/Ising/Trotter/N2 SQD + CPU reference and manifests | Keep as science baselines, fix failed regression |
| V0.2 Facility | Slurm, QRMI, pinned images, user workbench handoff | Test missing integration contracts |
| V0.3 Acceleration | A100/H200 Aer/PennyLane Lightning/CUDA-Q, benchmarks | **First M5 hardware priority** once allocated |
| V0.4 Chemistry | Larger N2 cc-pVDZ SQD/SKQD, MPI/OpenMP | Domain follow-on, not required for first release |
| V0.5 Provider breadth | IBM, IQM, Pasqal/Pulser, D-Wave and QDMI/QRMI | Add each with modality-native tests and authorised access |
| V0.6 Applied corpus | Finance, CFD/PDE, HEP/nuclear/medical, optics/photonics, QML | Grow as independently validated science families |
| V1 Platform workflow | Authorized submit → durable status/results, credentials, telemetry | **Core integrated M5 acceptance** |
| V2 Intelligent QCSC | Evidence-based resource/model/workflow optimisation | Subsequent research, not MVP blocker |

## Batch-first access pilot: P0–P6 (new first-user milestone, 8 November 2026)

This access-first sequence operationalises the existing M5 scientific ambition without discarding the prior domain-specific M5a–M5e Lightning/Ising/finance/chemistry science roadmap below.

> **Scientific preparation is cheap; expensive execution is scheduled.**

**P0** replace the privileged helper with approved native *per-researcher* Slurm submit/status/cancel; deny cross-user access and preserve existing CPU service. **P1** isolate approved ACE A100 and Axis H200 science GPUs through authoritative GRES/cgroups/accounting, excluding inference allocations. **P2** run first Aer GPU batch on a real A100 from a small KubeSpawner CPU Jupyter notebook, capture scientific validation and `sacct` usage. **P3** repeat independently on the remote Axis H200 after explicit input/output staging and checksum reconciliation. **P4** expose programme-scoped, site-qualified offering/status/results in the **existing** Quantum Platform Runs UI (no redesign). **P5** qualify distinct Lightning, Cirq/qsim/cuQuantum, IQM and Pulser images and modality-correct numerical tests. **P6** allow ACP Guide to tutor, inspect authorized progress and interpret returned science, without becoming scheduler.

These gates must not be marked complete based on source alone or on the existing CPU-only smoke test. The first acceptance demonstration is notebook opened → GPU batch submitted → browser/notebook closed → result and GPU usage observed after return → H200 repetition. See [detailed batch-first M5 plan](M5-BATCH-FIRST-SIMULATOR-PATH.md) and [eight short lessons](../labs/01-intro-quantum-computing/batch-first/README.md). The Lightning M5a–M5e work below remains a separate scientific correctness programme; the P0–P3 path validates access and GPU utilisation first.

## E. Concrete implementation gates (ordered, evidence-based)

### M5a — One reproducible CPU scientific reference

Use an ordinary Python script and notebook with upstream PennyLane /
`lightning.qubit` and NumPy/SciPy. The **first domain fixture** is a small
portfolio/QUBO mapped to a Pauli-Z Ising Hamiltonian, with fixed inputs,
independently enumerated optimum for small N and defined objective tolerance.
Track analytic expectation and finite-shot samples separately. Reuse the
existing multi-backend Bell sanity circuit and Ising/Trotter reference where
relevant, rather than duplicating them.

**Pass:** clean CPU environment, pinned versions and source SHA; deterministic
reference input; numerical tests; resulting `manifest.json`,
`summary.json` and data/hashes from existing artifact contract. No GPU
or QPU claimed.

### M5b — An actual authorised H200 Lightning GPU allocation

Build a narrowly scoped immutable GPU runner using compatible
`pennylane`, `pennylane-lightning`, NVIDIA driver/CUDA/cuQuantum and
Apptainer runtime. Discover the real site scheduler/Axis resource contract;
do not hardcode a fictitious partition. Start on **one GPU** in an exclusive
approved allocation. Verify `lightning.gpu` availability; **fail closed** if
CUDA devices/plugin are unavailable. Do not pretend eight GPUs on one H200
host are eight separate compute nodes.

**Pass:** real approved scheduler/provider job ID, GPU device UUID,
driver/toolkit/plugin versions, immutable OCI/SIF digest, measured runtime and
peak VRAM, CPU/GPU scientific agreement under stated tolerance. Slurm/Axis
status, resource accounting and isolation demonstrated. No double
allocation with vLLM/inference service.

### M5c — End-to-end authorised platform scientific run

Expose one approved, version-pinned logical offering in Quantum Platform,
such as `pennylane-lightning-h200`, only after resource availability is
verified. Reuse existing researcher identity, programme entitlements,
JupyterHub, Slurm gateway and ExecutionRecord/RunArtifacts; integrate ACP
task/run/experiment references without making ACP a scheduler.

**Pass:** researcher previews exact experiment/parameters/quota/cost,
explicitly submits, sees queued/running/failed/completed/cancelled states,
reads validated artifacts after notebook/browser restart. Independent user
cannot inspect or cancel the job. Invalid input, unavailable quota, absent
GPU and expired session return actionable errors.

### M5d — Asynchronous hybrid CPU/GPU/QPU workflow

Reuse IBM/Qiskit Aer and QRMI patterns for a single optional authorised
provider. Use stages **prepare → simulate/sample → postprocess → persist**.
Persist provider job ID, compilation/device/calibration metadata, queue
time, result digest and provider-specific units/charges. Release scarce
GPU resources while waiting on a remote QPU. Test mock/provider dry-run
first, then actual user-authorised QPU access.

**Pass:** restart-safe queued/poll/cancel/retrieve, protected credentials,
no duplicate provider submission, scientifically validated result. IBM is
the first *candidate*, not a hidden bias in future fair multi-modality
evaluation.

### M5e — Application and modality expansion, one vertical slice at a time

Each domain carries its own independently checked problem model,
references, tolerance and reproducibility:
- **Finance/optimisation:** Ising/QUBO, QAOA/VQE, classical exact/heuristic
  comparison, constraints and scaling;
- **Chemistry/nuclear/HEP:** documented Hamiltonian encodings, truncated
  bases, SQD/Trotter, conservation laws and classical reference;
- **CFD/PDE:** discretisation, condition numbers, boundary conditions,
  error/speed comparison; no implied generic quantum speedup;
- **Photonics/QKD:** version-pinned `photonicslab` alpha CPU examples
  first; detectors/coincidences/polarisation, then independently validated
  Fock/Gaussian, HOM/SPDC, nonlinear crystals, birefringence and cavities;
- **Modalities/QEC/QML:** trapped ions and neutral atoms, annealers,
  bosonic/photonics platforms, qudits/QLDPC and QML only with native
  scientific representations and domain specialists.

The six-month domain research rotation and PhD/procurement collaborations
may guide choice of *subsequent* domain slices but are not infrastructure
dependencies for M5a–M5c.

### M5f — Intelligent science assistance (after deterministic execution)

A reviewed Guide/ACP skill can propose a workflow and explain results,
grounded in the experiment manifest and source. Model routing / local
research agent teams may compare CPU/GPU/QPU evidence or suggest research
questions. **Never silently install tools, spend provider credits, submit
GPU jobs, assert scientific speedups or self-approve a PR.**

## F. The first complete researcher demonstration

1. User signs into Quantum Platform and asks how to run their PennyLane
   portfolio Hamiltonian on the H200. Guide links an approved immutable
   notebook/script and correctly distinguishes GPU availability from model
   inference.
2. User runs and verifies the CPU `lightning.qubit` reference with a
   small analytic benchmark; records source commit and results.
3. User chooses the permitted H200 offering; reviews bounded parameters
   and consumption, explicitly approves a scheduler run.
4. Slurm/Axis **actually allocates** one H200 GPU; approved pinned runner
   runs `lightning.gpu`; captures device, CUDA/plugin and job provenance.
5. Result manifest, summary, numeric accuracy, timing and artifacts
   persist independently of Jupyter and model sessions. User can revisit
   results and ask Guide for an evidence-grounded explanation.
6. Negative controls: no entitlement, wrong user, revoked skill binding,
   unavailable GPU, incompatible plugin, cancellation and retry.
7. The same contract can then receive a chemistry or nuclear Hamiltonian
   while requiring separate physical validation.

**M5 MVP passes only on an observed science result and live user journey**,
not a GitHub image build, assumed H200 accessibility or a plausible
assistant response.

## G. Explicit exclusions and dependencies

- **M4 closeout first**: M4a–M4g source, compatible deployed schema/Pod
  images, approved destructive continuity and **human-operated** `nlisa`
  cross-interface tests. Coding agents never impersonate `nlisa`.
- No manual checkout on `k8s-cp-01`; read-only assessments through
  `kubectl`. No direct ArgoCD CLI or auto-sync/privileged cluster mutation
  by development agents. Production changes require reviewed GitOps and
  human approval.
- No rebuild of Paperclip, Letta, LiteLLM, Slurm, Qiskit, PennyLane,
  cuQuantum, vendor SDKs, a universal `qw` platform SDK, or user identity.
  Existing `qw` commands are compatibility/reference surfaces, not a
  requirement for researchers to adopt new scientific APIs.
- Full A100/H200 inference-fabric expansion, dynamic GPU sharing/MIG
  experiments, multi-H200-node MPI, virtual QPU zoo, automated procurement,
  unrestricted agent teams, national facility BFI capital projects and
  first-class Discord/Telegram social bots are **independent programmes**,
  not M5 MVP acceptance criteria.

## Linked evidence and issues

- [Quantum Workflows README V0.1–V2 roadmap](../README.md)
- [Workflow/runner architecture](ARCHITECTURE.md)
- [Slurm runner contract](wiki/Slurm-runner-contract.md)
- [ACP integration boundary](agent-control-plane-integration.md)
- [M5 PennyLane H200 vertical slice #46](https://github.com/nyameko/quantum-workflows/issues/46)
- [Hybrid Ising reference #27](https://github.com/nyameko/quantum-workflows/issues/27)
- [Axis H200 AccessProvider #82](https://github.com/nyameko/infra-hpc-qc-k8s/issues/82)
- [GPU inference-vs-Slurm allocation #124](https://github.com/nyameko/infra-hpc-qc-k8s/issues/124)
- [PhotonicsLab physical regime boundaries](https://github.com/nyameko/photonicslab/blob/main/docs/ARCHITECTURE.md)
- [ACP M4 integrated release gate #45](https://github.com/nyameko/agent-control-plane/issues/45)
