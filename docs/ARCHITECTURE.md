# Architecture

## Scope and repository boundaries

`quantum-workflows` is an experimental corpus and runner catalog. It does not provision OpenStack,
install Slurm, operate Kubernetes, authenticate users, or become a second backend registry.

| Concern | Authoritative repository |
| --- | --- |
| Terraform, OpenStack VMs/networks, Ansible, Slurm, QRMI/SPANK, GPU drivers, MPI, Apptainer | `infra-hpc-qc-k8s` |
| Identity, programmes, JupyterHub UX, job API, credential broker, backend registry, results catalog | `quantum-platform` |
| Scientific code, runner images, workflow parameters, Slurm entry points, tutorials, benchmarks | `quantum-workflows` |

The infrastructure repository may deploy a platform release; the platform may reference a workflow
runner and schema. Neither should copy the scientific environment definitions.

## Control plane and compute plane

```text
Kubernetes control plane                 Slurm compute plane
────────────────────────                 ───────────────────
quantum-platform portal                  login/submit nodes
JupyterHub hub                    sbatch  CPU compute nodes
job/credential services  ──────────────► A100/H200 nodes
backend registry                         Apptainer runners
PostgreSQL                               QRMI/SPANK
Prometheus/Grafana                            │
                                              ▼
                                         remote/local QPU
```

JupyterHub is a platform experience deployed through Argo CD. The default path is a lightweight
KubeSpawner workbench; durable CPU/GPU/QPU work is submitted separately through Quantum Platform
and Slurm/provider adapters. BatchSpawner remains an explicit secondary mode when the notebook
kernel itself must run inside a scarce Slurm allocation.

## Runner contract

A runner is a versioned OCI image that can also be consumed by Apptainer. Each production runner:

- has a narrow SDK/algorithm purpose;
- runs as a non-root user;
- contains no credentials or research data;
- exposes `qw` as the stable command;
- uses immutable tags/digests in Slurm and provenance;
- writes only below the caller-provided output directory;
- keeps provider-specific optional dependencies isolated when dependency sets conflict.

This last point is important: current QRMI IBM and IQM extras may require incompatible Qiskit
versions. One “everything” image would be fragile and impossible to reproduce. Separate IBM, IQM,
Pasqal and D-Wave runners can implement the same workflow/result contract.

## Workflow contract

Every workflow has four logical phases even when they execute in one process locally:

1. **Prepare** — validate inputs, construct the physical/mathematical problem and circuit.
2. **Compile and execute** — transpile against a target and simulate/sample.
3. **Postprocess** — calculate observables, recover configurations, diagonalize or optimize.
4. **Persist** — emit the summary, raw/processed data and redacted provenance.

At scale these phases become separate Slurm jobs with `afterok` dependencies so scarce resources
are allocated just in time:

```text
CPU/GPU prepare ──► release resource ──► QPU sample ──► CPU/MPI postprocess
```

Cloud QPU queue time must never strand an H200 reservation. Tight CPU/GPU/QPU co-scheduling is a
future concern for a co-located low-latency QPU, not a simulation of tight coupling over the public
internet.

## Executor model

The initial executors are intentionally explicit:

| Executor | Purpose | Credential path |
| --- | --- | --- |
| `aer` | credential-free sampled circuit baseline | none |
| `statevector` | exact/noiseless SQD sample generation | none |
| `ibm` | direct development and hardware validation | Qiskit account store or ephemeral env |
| `qrmi` | production scheduler-mediated IBM execution | Slurm SPANK injection |

“Vendor-neutral” does not mean every provider accepts the same circuit or payload. QRMI unifies the
resource/job lifecycle; compilation, native instructions, payload construction and result decoding
remain provider-aware. Pasqal pulse sequences and D-Wave BQMs should be taught natively instead of
being disguised as Qiskit gate backends.

## Result contract

Each execution creates:

```text
<output>/<workflow>/<UTC timestamp>-<random id>/
├── manifest.json
├── summary.json
└── data/
```

`manifest.json` schema version 1.0 records:

- experiment ID, workflow, status and UTC timestamps;
- repository commit and dirty state;
- Python and relevant package versions;
- executor, host and redacted Slurm/QRMI allocation metadata;
- workflow parameters;
- logical/transpiled circuit hashes, qubits, depth and operation counts;
- provider, logical backend and provider job ID;
- artifact paths, sizes and SHA-256 digests;
- wall time and a sanitized failure type/message when applicable.

Credentials and full environment dumps are forbidden. Environment capture is an allowlist, never
“serialize `os.environ` and redact known tokens”, because unknown future secrets would leak.

## Backend registry integration

`quantum-platform` will own the authoritative registry. A workflow requests capabilities or a
logical resource, not a machine name:

```text
provider=ibm, modality=gate, minimum_qubits=16
```

or:

```text
resource=ibm-production
```

Slurm/QRMI resolves the physical target and injects it. Direct `--backend` remains a development and
diagnostic escape hatch.

## Credential architecture

```text
user ─HTTPS─► credential broker ─► encrypted secret store
                         │
                         └─ just in time ─► Slurm/QRMI job environment
```

For the MVP, envelope-encrypted ciphertext may live in PostgreSQL while a SealedSecret provisions
the service's wrapping key. Longer term, Vault/KMS/HSM can replace the key layer without changing
the portal data model. SealedSecrets remain suitable for static deployment secrets, not dynamic
per-user provider tokens.

## Observability

The workflow result manifest is the durable scientific record. Prometheus/Grafana is the live
operational view. Planned platform metrics include job outcomes, Slurm/provider queue time,
execution and postprocessing time, circuit depth/two-qubit count/shots, backend calibration age,
and CPU/GPU resource seconds. Labels must remain bounded: provider job IDs and experiment IDs belong
in logs/traces/catalog records, not unbounded Prometheus labels.

## Upstream policy

1. If upstream implements a capability, integrate it.
2. If a missing feature is generally useful, implement it with the upstream project and submit it.
3. Keep platform-specific behavior in `quantum-platform`.
4. Keep deployment-specific behavior in `infra-hpc-qc-k8s`.
5. Keep scientific reference implementations here.

Examples: a generic QRMI D-Wave adapter belongs upstream; an Astro result page belongs in the
platform; a Rocky Linux SPANK role belongs in infrastructure; an SQD lesson belongs here.

## Interactive workbench versus execution lifecycle

The user-facing Jupyter process and the scientific execution lifecycle are separate concerns.

### Default

A KubeSpawner notebook pod is a lightweight client with the user's persistent home, selected software workbench and authenticated execution client. It may perform trivial local checks, but substantial simulation/training/postprocessing work is submitted as a durable workflow/job.

### Durable workflow state

A workflow run owns stage state independently of notebook lifetime:

```text
PREPROCESS -> SIMULATE -> WAIT_QPU -> QPU_RUN -> POSTPROCESS -> COMPLETE
```

Each stage records its immutable environment, requested logical resource, resolved scheduler/provider placement, timestamps, identifiers, result references and release outcome. Resource acquisition is per stage. Do not keep an H200, large CPU allocation or QPU reservation alive merely because a notebook is open.

### Logical targets

Clients ask for logical targets such as `qiskit-aer-large`, `pennylane-lightning-h200` or a provider-capability class. The platform/execution layer resolves these to Slurm/QPU details under entitlement and quota policy. The workflow manifest records the resolved placement for provenance without requiring the researcher to program against physical partitions.

### Interactive HPC exception

BatchSpawner or an equivalent remote-kernel path is retained for workloads that need an interactive kernel inside an HPC allocation. Such sessions have explicit walltime/concurrency policy and are not the default execution architecture.


## Validated M3 execution contract

The first production vertical slice has now been proven:

```text
Quantum Platform
  ↓
restricted SSH gateway
  ↓
Slurm
  ↓
Apptainer
  ↓
qw cpu-smoke
  ↓
structured result + provenance
```

Reference acceptance:

```text
Slurm job:   15
partition:   cpu-small
state:       COMPLETED
exit code:   0:0
workflow:    cpu-smoke
passed:      true
```

This establishes the execution contract that later CPU, MPI, A100, H200, emulator and QPU workflows should preserve.

## HPL and heterogeneous benchmark progression

A flagship systems curriculum should progress through:

```text
small CPU HPL
  ↓
large single-node HPL
  ↓
multi-node MPI/HPL
  ↓
A100 HPL
  ↓
H200 HPL
  ↓
multi-H200 HPL
```

Each experiment should emit the same kind of structured parameters, environment metadata, scheduler/provider state and result provenance as quantum workflows.

This track becomes a natural persistent-agent project: an agent can compare previous parameter sets and benchmark results while the user moves between Jupyter, the portal and an SSH/TUI client.
