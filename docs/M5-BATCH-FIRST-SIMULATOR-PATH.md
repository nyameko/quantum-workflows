# M5 — Batch-first simulator academy and single-GPU acceptance path

**Status:** source/design implementation proposal; **not a live A100/H200 deployment or authorized scheduler change**.

> **Scientific preparation is cheap; expensive execution is scheduled.**

## Invariants

- Keep the existing Quantum Platform UI and lightweight JupyterHub/KubeSpawner CPU workbench. No SSH terminal, filesystem browser or new Open OnDemand portal is required.
- CPU notebooks are directly interactive; expensive A100/H200 computation is a **durable, independently scheduled Slurm batch job**, not a long-lived interactive Jupyter reservation. The notebook may exit while the job runs.
- Distinguish **framework/SDK**, **simulator backend**, **GPU/CPU execution target**, and **real QPU provider**. The same nominal circuit does not imply equivalent noise, physical semantics or device capability.
- Native `sbatch`, `squeue`, `sacct`, `scancel` run as the **authenticated researcher**. For ACE Kubernetes notebooks, the first path is native `ssh researcher@approved-login sbatch ...` with a *researcher-owned* private key and out-of-band verified host key. OpenSSH on the login tier maps the actual user to their POSIX principal. Workbench pods need only the OpenSSH client, not MUNGE keys. See [infra P0 PR #290](https://github.com/nyameko/infra-hpc-qc-k8s/pull/290). Reject shared/root service identity, `runuser`, passwordless-sudo Slurm helpers and any application-selected identity switch. Remove obsolete helpers only after replacement CPU path passes owner-observed acceptance.
- Slurm or the provider is authoritative for scheduling/accounting; Quantum Platform for resource offerings, entitlements and ExecutionRecord; Workflow for scientific code, numerical checks and artifacts; ACP for explanations/context (not another scheduler).

## Exact initial eight teaching notebooks

| Lab | SDK / backend | Baseline → expensive execution | Teaching outcome |
| --- | --- | --- | --- |
| 00 | Qiskit Aer | CPU workbench | Bell measurement, shot statistics |
| 01 | Qiskit Aer GPU | per-user sbatch → A100/H200 1 GPU | persist job ID, reconcile result |
| 02 | Aer statevector | CPU → GPU batch | raw memory `16 * 2**n` B, scalability and benchmarking |
| 03 | PennyLane Lightning | lightning.qubit → lightning.gpu via Slurm | Ising energy and gradients |
| 04 | Cirq/qsim/cuQuantum | CPU qsim → validated GPU image | circuit vs simulator vs cuStateVec/cuTensorNet |
| 05 | IQM qiskit adapter | fake backend CPU | native compilation, architecture/noise |
| 06 | Pulser/Pasqal | QutipEmulator CPU → emu-sv/emu-mps optional GPU | Rydberg/neutral-atom analogue emulation |
| 07 | physical provider | Aer CPU → separately authorized QPU | explicit quota, physical device/cost, native SDK and provenance |

Existing Bell/QPU learning notebooks remain canonical advanced references; the new `labs/01-intro-quantum-computing/batch-first/` sequence is a navigable on-ramp.

## Single-GPU runner and environment ownership

Scientific image *source* and dependency/physics tests: **quantum-workflows**. OCI image build/CI artifact publication: existing `quantum-workflows/.github/workflows/images.yml` pattern, extended in reviewed PR after first image builds and site tests. Image digest promotion, Apptainer SIF distribution/cache, CUDA-driver compatibility, Slurm GRES, remote stage service and storage quotas: **infra-hpc-qc-k8s** or Axis site operator. Quantum Platform displays approved logical `environment + execution provider + resource profile`, **never** builds user images ad hoc. ACP only recommends reviewed images.

Build separate immutable environments: (1) Qiskit/Aer CPU; (2) Qiskit Aer GPU; (3) PennyLane Lightning GPU; (4) Cirq/qsim CUDA; (5) cuQuantum/cuStateVec/cuTensorNet; (6) Pulser/neutral-atom; plus IQM fake/QPU-only native client as appropriate. Do not combine all vendor dependencies or assume any untested package supports Python 3.14/CUDA at both sites. Prefer existing tested upstream OCI images where provenance, licensing, compat and maintenance pass; otherwise build small project-owned runners. Source manifests must record image digest, Python/SDK/CUDA matrix, supported methods, numeric test fixture and accelerator/driver metadata. An Apptainer SIF is a **container image**, not a Kubernetes Pod; Slurm allocates the host GPU and `srun apptainer exec --nv` executes the SIF.

First candidate `runners/qiskit-aer-gpu/Dockerfile` pins `qiskit-aer-gpu==0.18.2` and targets Python 3.14. It must pass actual image build + CUDA-compatible A100/H200 allocation before promotion; this PR does not automatically alter the existing image-publishing matrix.

## Cross-site scratch and transfer

No remote H200 path is assumed to be mounted under ACE NFS. A symbolic link to an SSHFS mount is merely a pointer to a fragile FUSE filesystem and cannot guarantee the compute node will see it. SSHFS is acceptable **only as an optional human convenience for small files**, not the default data plane for large GPU simulations, high-throughput checkpoints, live HDF5 or large parallel I/O.

Instead: `/home/research/<user>/projects/<experiment>` on ACE for notebook/source/provenance; a per-user **site-approved H200 scratch directory** for staged input, local computation/checkpoints and output; transfer via authenticated, site-approved `rsync -e ssh`, SFTP or object-store multipart transfer using short-lived scoped credentials. **Site-initiated outbound** links or an approved relay are needed if Atmos cannot accept inbound SSH. Stage input before submission, checksum and preserve UID/GID mapping/ACLs, use local scratch on allocated GPU node if available, stage outputs back after completion, compare SHA256/byte count and mark artifact `available` only when reconciled. Avoid automatically copying full training/checkpoint datasets: transfer explicit manifests and outputs or object-store URIs; incremental sync, batching/compression only where beneficial, retention/cleanup rules and resumable transfer for TB-sized datasets. Never send protected datasets through a third-party relay without approval.

`ExecutionRecord` must retain `site + cluster + scheduler_job_id + user/programme + artifact URI/digest + Slurm TRES/accounting`, not merely an integer job ID; accounting and provenance are distinct. Prefer an explicit stage-in/compute/stage-out state machine; do not claim automatic recovery yet. Slurm burst-buffer integration is a *future option* only if the site supports it.

## Accepted implementation order (P0–P6)

| Gate | Owner | Observable acceptance |
| --- | --- | --- |
| P0 | Infra + Platform | replace privileged helper with native authenticated researcher Slurm path; `nlisa` own job submit/cancel succeeds, cross-user denial (operator test) |
| P1 | Infra / Axis operator | approved A100/H200 Slurm GRES/cgroups/TRES; inference GPUs excluded |
| P2 | Workflow | CPU Bell baseline and **real A100** Aer GPU batch: scientific JSON + Slurm accounting |
| P3 | Infra + Workflow | same verified job on **remote H200**, staged data/checksums, no unapproved resource sharing |
| P4 | Platform | programme-only offerings/status/quotas in **existing** Runs UI; no UI redesign |
| P5 | Workflow | separate Lightning, qsim/cuQuantum, IQM/Pulser numerical + image compatibility gates |
| P6 | ACP | Guide teaches/diagnoses reviewed jobs and retrieves already-authorized status/metrics |

**First full milestone:** researcher opens CPU Qiskit notebook → submits *real A100 batch job* → closes notebook → returns → sees scientifically verified outputs and accounted GPU use → repeats at Axis H200. Only actual operator-observed A100/H200 jobs may close P2/P3. This source PR cannot claim these gates pass.
