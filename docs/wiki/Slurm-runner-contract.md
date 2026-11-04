# Slurm submission, runner images and durable artifacts

## Runtime contract

Quantum Workflows owns scientific code, tests, notebook environments, Slurm entry points and reproducible artifacts. Infrastructure owns Slurm/accounting, compute nodes, NFS and container build/deployment; Quantum Platform owns access/entitlement and `ExecutionRecord`. A user can explore methods in a cheap Jupyter workbench, but jobs that should survive the notebook are submitted as durable scheduler allocations.

The repository currently includes `slurm/cpu-smoke.sbatch`, `slurm/hello-ibm.sbatch`, `slurm/trotter.sbatch`, `slurm/sqd.sbatch` and OCI build contexts `runners/qiskit-cpu/` and `runners/sqd/`. These are reference templates, not a universal configuration for every HPC facility. Review site partitions, walltime and job-name policy, environment modules, Apptainer availability, container permissions and shared data paths first.

## Safe user execution

1. Select an approved workflow, environment and offering in Quantum Platform; choose the smallest CPU baseline before GPU/QPU allocation.
2. Inspect requested cores, memory, duration, credentials, provider target and expected artifact path.
3. Submit through the restricted gateway or authorized site `sbatch`; never invoke Slurm commands directly from an unprivileged web request with arbitrary shell arguments.
4. Track Slurm job ID, queued/running/completed state, exit code and elapsed time.
5. Retrieve `manifest.json`, `summary.json` and data; confirm scientific validity and image digest. A process exit code of zero does not prove the physics.

## Container and reproducibility requirements

A runner should be an immutable purpose-built OCI image runnable via Apptainer as an ordinary user, with no embedded model keys, SSH material, patient datasets or provider credentials. Document Python/SDK version, compatible GPU driver/CUDA if relevant, the code commit/image digest, supported methods, resources and scientific checks. Do not hide incompatible provider SDK dependencies inside a single “all-in-one” image.

## Job debugging

A job may be rejected before allocation because of requested partition, walltime, QOS, reservation or invalid name. A completed job can still write failed numerical checks or no artifacts due to storage/permission errors. Inspect `squeue`, `scontrol show job <ID>`, `sacct`, scheduler stderr, and the exact output directory. The portal can report its own error even if a Slurm job is still running.

See [Slurm templates](https://github.com/nyameko/quantum-workflows/tree/main/slurm), [runner images](https://github.com/nyameko/quantum-workflows/tree/main/runners), [execution architecture](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md) and [workbench tutorial](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/04-JUPYTER-WORKBENCH-TO-HYBRID-EXECUTION.md).