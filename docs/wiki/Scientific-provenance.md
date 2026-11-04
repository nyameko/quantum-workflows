# Scientific reproducibility and provenance

## Required result contract

Canonical `qw` experiments write a structured run directory with `manifest.json`, `summary.json` and optional `data/`. The result is not an untracked notebook screenshot. Keep input parameters, source revision, installed SDK versions, engine, backend, exact simulator method, seed, shot count, build digest, hardware profile, timestamps, validity checks and hashes where applicable.

## Scientific validity

A `COMPLETED` Slurm job only proves a scheduled process exited; it cannot prove that a numerical method approximates the intended physics. Verify a known analytical or independent reference, quantify convergence with time steps, mesh/grid and sampling, and report statistical confidence. Quantify truncation and hardware noise; do not conflate simulator success, provider queue success, noise-model agreement and claimed quantum advantage.

## Data management

Use versioned, redistributable input datasets or record restricted datasets with controlled references and access policies. Keep units, coordinate conventions and random seeds explicit. Avoid committing huge binary results or personally identifying research data. Record the platform ExecutionRecord, Slurm/provider ID and workflow run ID separately.

## Publishing and peer review

A useful computational paper or reproducible teaching lesson includes problem statement, independent baseline, algorithms/approximations, runtime/hardware, cost, acceptance thresholds, failed experiments, limitations, exact source and artifact versions. Peer review must inspect physics and numerical assumptions, not only test coverage.

See [runner contract](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md) and [artifacts implementation](https://github.com/nyameko/quantum-workflows/blob/main/src/quantum_workflows/artifacts.py).