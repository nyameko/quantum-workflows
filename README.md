# quantum-workflows

Vendor-neutral reference workflows for **hybrid quantum-classical computing** and
**quantum-centric supercomputing (QCSC)**.

This repository is the executable research and teaching layer of a three-repository system:

| Repository | Question it answers | Owns |
| --- | --- | --- |
| [`infra-hpc-qc-k8s`](https://github.com/nyameko/infra-hpc-qc-k8s) | How is the facility built and operated? | OpenStack, Terraform, Ansible, Kubernetes, Slurm, QRMI/SPANK, MPI, GPUs, storage, observability |
| [`quantum-platform`](https://github.com/nyameko/quantum-platform) | How do people securely use the facility? | identity, programmes, portal, JupyterHub experience, backend catalog, credentials, jobs and results |
| **`quantum-workflows`** | What scientific work can the facility execute and reproduce? | runners, algorithms, tutorials, benchmarks, Slurm entry points, result and provenance contracts |

The name is intentionally broader than “QC”. The project includes gate-based quantum computing,
Hamiltonian simulation, quantum emulation, quantum-inspired algorithms and neural networks,
annealing, neutral atoms, classical simulation, and heterogeneous CPU–GPU–QPU workflows. The
repository description carries the hybrid/QCSC precision without making the name cumbersome or
conflating it with quantum chemistry or quality control.

## Philosophy

1. **One scientific intent, many execution targets.** A workflow begins on a laptop simulator,
   progresses to CPU/GPU HPC, and can reach an emulator or QPU without becoming a different lesson.
2. **QPU as one resource in a heterogeneous system.** CPU preprocessing, GPU simulation, QPU
   sampling, and MPI/OpenMP postprocessing are explicit stages rather than hidden behind “run”.
3. **Local-first and hardware-ready.** Every workflow has a credential-free local path. Remote
   hardware is opt-in and never runs in CI.
4. **Scheduler-mediated production.** Direct provider access is useful for development. The target
   facility path is Slurm + QRMI/SPANK with just-in-time resources and credentials.
5. **Upstream first.** Integrate maintained Qiskit, QRMI, QDMI, ffsim and vendor SDK capabilities;
   contribute generally useful missing pieces upstream rather than forking an ecosystem.
6. **Provenance is a result.** Every execution writes a redacted manifest with source, software,
   resource, circuit, timing and result metadata.
7. **Teach the boundary conditions.** Queue time, shots, transpilation, simulator memory,
   classical postprocessing and approximation error are part of the curriculum.

## Initial release

The initial commit contains a complete vertical slice:

- **IBM QPU handshake** — Bell-state execution on local Aer, directly through IBM Quantum Compute
  Service, or through QRMI when Slurm has injected a QPU allocation.
- **Trotterized dynamics** — transverse-field Ising dynamics with configurable lattice size,
  couplings, time grid and second-order Suzuki–Trotter steps; local exact comparison and sampled
  execution paths produce approximation/shot metrics.
- **Sample-based quantum diagonalization (SQD)** — an N₂/STO-6G workflow using PySCF, ffsim,
  Qiskit primitives and `qiskit-addon-sqd`: classical molecular preparation → LUCJ sampling →
  configuration recovery/subspace diagonalization → energy and orbital-occupancy results.
- OCI runners for the base Qiskit and SQD stacks.
- Slurm scripts designed for Apptainer execution and a future QRMI/SPANK `--qpu` allocation.
- Unit tests, GitHub Actions, documentation and a stable result layout.

## Execution model

```text
researcher / notebook / quantum-platform
                  │
                  ▼
       versioned workflow + runner
                  │
        ┌─────────┴─────────┐
        │                   │
 local development      Slurm allocation
 Aer / statevector      CPU / A100 / H200
                            │
                         QRMI/SPANK
                            │
                  IBM / IQM / Pasqal / ...
        │                   │
        └─────────┬─────────┘
                  ▼
       immutable result directory
       manifest + raw + processed
```

Kubernetes hosts control-plane services and the OCI registry. Slurm executes HPC runners through
Apptainer on compute nodes. A container image is a reproducible artifact, not a reason to place
multi-node HPC execution inside Kubernetes.

## Quick start

Python 3.11–3.13 is supported.

```bash
git clone https://github.com/nyameko/quantum-workflows.git
cd quantum-workflows
make install

# Credential-free IBM Bell workflow on Aer
make hello-local

# Four-qubit Ising dynamics, including exact-vs-Trotter comparison
make trotter
```

Install the chemistry stack and run the local SQD example:

```bash
make install-all
make sqd
```

All commands write a timestamped run below `results/`:

```text
results/<workflow>/<run-id>/
├── manifest.json
├── summary.json
└── data/
    └── workflow-specific artifacts
```

The short and long CLI names are equivalent:

```bash
qw --help
quantum-workflow --help
```

## IBM Quantum hardware handshake

Use Qiskit's normal secure account store:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    token="<API key>",
    instance="<service CRN>",  # optional for an Open Plan account
)
```

Then submit the two-qubit handshake:

```bash
qw hello --executor ibm --shots 1024
```

To pin a target rather than select the least-busy eligible QPU:

```bash
qw hello --executor ibm --backend ibm_backend_name --shots 1024
```

The workflow succeeds only when the result contains the expected Bell correlations above the
configured threshold. It records the IBM job ID and backend name, but never serializes credentials.
Remote execution consumes QPU time and is intentionally excluded from automated tests.

For the facility path, the Slurm script requests the logical QPU resource:

```bash
sbatch --gres=qpu:1 --qpu=ibm_resource_name slurm/hello-ibm.sbatch
```

The SPANK plugin injects `QRMI_JOB_QPU_RESOURCES` and `QRMI_JOB_QPU_TYPES`; application source does
not contain a physical backend name or provider token.

## Reference workflows

### 1. Trotterized transverse-field Ising dynamics

```bash
qw trotter \
  --executor aer \
  --qubits 6 \
  --coupling 1.0 \
  --field 0.7 \
  --final-time 3.0 \
  --time-points 13 \
  --trotter-steps 4 \
  --shots 4096
```

The Hamiltonian is

$$H=-J\sum_{i=0}^{N-2} Z_i Z_{i+1}-h\sum_{i=0}^{N-1}X_i.$$

For each time point the workflow records exact and product-formula magnetization, absolute Trotter
error, sampled magnetization and sampling error. This makes algorithmic approximation, finite-shot
statistics and later device noise separately visible.

### 2. N₂ sample-based quantum diagonalization

```bash
qw sqd \
  --executor statevector \
  --shots 20000 \
  --samples-per-batch 1000 \
  --num-batches 3 \
  --max-iterations 5
```

The initial teaching workload uses a tractable STO-6G active space so the full workflow runs without
hardware credentials. It performs:

```text
PySCF RHF/CASCI + CCSD amplitudes
                │
                ▼
        ffsim LUCJ ansatz
                │
                ▼
   StatevectorSampler / IBM / QRMI
                │
                ▼
       measured configurations
                │
                ▼
 qiskit-addon-sqd recovery + SCI
                │
                ▼
 energy error + orbital occupancies
```

The deliberately larger N₂/cc-pVDZ QRMI/HPC variant is a roadmap milestone after the baseline
Slurm/QRMI deployment is accepted. It requires materially more QPU time and classical postprocessing.

## Runners

Build locally:

```bash
docker build -f runners/qiskit-cpu/Dockerfile -t quantum-workflows:qiskit-cpu .
docker build -f runners/sqd/Dockerfile -t quantum-workflows:sqd .
```

The CI workflow publishes immutable `sha-<commit>` GHCR tags after tests pass. Production Slurm
jobs should pin an image digest or immutable tag, pull it into Apptainer, and record the digest in
the manifest. Mutable `main` tags are for integration only.

## Repository layout

```text
quantum-workflows/
├── src/quantum_workflows/       CLI, executors, workflows, provenance
├── configs/                     documented example inputs
├── runners/                     versioned OCI execution environments
├── slurm/                       batch entry points; infrastructure-neutral
├── tests/                       credential-free tests
├── docs/
│   ├── ARCHITECTURE.md
│   └── tutorials/
│       ├── 01-IBM-QPU-HANDSHAKE.md
│       ├── 02-TROTTERIZED-DYNAMICS.md
│       └── 03-SAMPLE-BASED-QUANTUM-DIAGONALIZATION.md
└── .github/workflows/           CI and runner publication
```

## Security boundary

Never commit or bake the following into an image:

- IBM, IQM, Pasqal, D-Wave or other provider tokens;
- SSH or WireGuard private keys;
- `.env` files, Qiskit account stores, kubeconfigs or Slurm credentials;
- raw multi-user research data not cleared for publication.

SealedSecrets are appropriate for static platform/service secrets in the GitOps deployment. They
are not the per-user provider-token database. The target platform uses an encrypted credential
broker and ephemeral job injection; PostgreSQL stores ciphertext metadata/references, not plaintext
bearer tokens.

## Roadmap

| Phase | Deliverable |
| --- | --- |
| **V0.1 — foundation** | IBM Bell handshake; Trotter dynamics; local N₂ SQD; manifests; CPU runners; Slurm templates |
| **V0.2 — facility integration** | QRMI/SPANK validation; JupyterHub profiles; immutable GHCR/Apptainer images; Slurm DAGs |
| **V0.3 — accelerated simulation** | Aer GPU on A100/H200; PennyLane Lightning GPU; CUDA-Q; simulator benchmarks |
| **V0.4 — QCSC chemistry** | N₂ cc-pVDZ through QRMI; `qiskit-addon-sqd-hpc`; MPI/OpenMP postprocessing; SQD/SKQD |
| **V0.5 — vendor breadth** | IQM/QDMI, Pasqal Pulser emulator/QPU, D-Wave Ocean, backend-capability contracts |
| **V0.6 — applied corpus** | photonics, nuclear/medical, HEP, finance, optimization, QML/QINNs and PDE demonstrators |
| **V1 — platform workflow** | submit from `quantum-platform`; live stage state; credentials; provenance catalog; Grafana telemetry |
| **V2 — intelligent QCSC** | evidence-based resource/model placement above deterministic Slurm/QRMI/QDMI foundations |

Candidate curriculum namespaces will grow as numbered workflow families rather than unrelated demo
scripts: foundations, simulation, dynamics, variational algorithms, SQD/SKQD, neutral atoms,
annealing, QML, PDEs, and domain applications.

## Definition of done for a workflow

A workflow is not complete merely because a notebook ran once. It must have:

- a credential-free local execution path;
- typed/configurable inputs and deterministic seeds where meaningful;
- a documented remote resource path when supported;
- an immutable runner definition;
- a Slurm entry point for HPC stages;
- redacted provenance and structured results;
- unit/smoke tests that do not consume QPU time;
- scientific references, assumptions and known limits;
- a tutorial that explains both the physics/algorithm and the systems path.

## Documentation

- [Architecture and contracts](docs/ARCHITECTURE.md)
- [IBM QPU handshake](docs/tutorials/01-IBM-QPU-HANDSHAKE.md)
- [Trotterized dynamics](docs/tutorials/02-TROTTERIZED-DYNAMICS.md)
- [Sample-based quantum diagonalization](docs/tutorials/03-SAMPLE-BASED-QUANTUM-DIAGONALIZATION.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License

Apache-2.0. Individual upstream packages and scientific datasets retain their own licenses and
citation requirements.

## Agent integration

[Agent Control Plane boundary and roadmap](docs/agent-control-plane-integration.md)
defines future authorized submissions and provenance. Phase 1 adds infrastructure
diagnostics only; scientific runners remain independent.
