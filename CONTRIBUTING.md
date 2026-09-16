# Contributing

Contributions should preserve three properties: the local path must remain runnable without a
provider account, hardware execution must never require credentials in Git, and every run must
emit a provenance manifest.

1. Create a focused branch and install `.[all,dev]`.
2. Add or update tests and tutorial documentation with the code.
3. Run `make check` before opening a pull request.
4. Never commit `.env`, provider tokens, result directories, private data, or container secrets.

Generic capabilities belong upstream when possible. Deployment-specific Slurm/QRMI installation
belongs in `infra-hpc-qc-k8s`; portal and identity features belong in `quantum-platform`.
