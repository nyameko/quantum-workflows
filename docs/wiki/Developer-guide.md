# Scientific developer guide

## Development environment

Use a Python 3.14 virtual environment and isolate optional provider extras; IBM Runtime, QRMI, IQM and GPU dependencies can conflict. For the core development checkout:

```sh
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
ruff check src tests
ruff format --check src tests
pytest -m 'not hardware'
```

Hardware tests must be explicitly opt-in and separately budgeted; never run them automatically on a pull request.

## Architecture

`src/quantum_workflows/` contains `cli.py`, `executors.py`, `artifacts.py`, and experiment modules. `labs/` owns notebooks and teaching material; `slurm/` has reference sbatch templates; `runners/` builds versioned OCI images; `catalog/` supplies reviewed metadata; `configs/` stores examples. The CLI is a minimal reference runner, not an alternative to the official scientific packages.

## Add a workflow

1. Name the scientific problem and independent reference solution.
2. Define SI units or explicitly stated natural units, input schema, sampling, tolerances, failure modes and resource estimates.
3. Start with a deterministic credential-free CPU implementation and tests.
4. Add backend adapter(s) only when physics/SDK semantics map faithfully.
5. Emit structured provenance and guard against collisions/idempotency problems.
6. Supply a lesson (theory, notebook, exercises) and one reproducible CLI/Slurm reference where useful.
7. Document concurrency, GPU/QPU entitlements and costs. Add negative tests for missing credentials and unsupported hardware.

See [contribution guide](https://github.com/nyameko/quantum-workflows/blob/main/CONTRIBUTING.md), [architecture](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md) and [tests](https://github.com/nyameko/quantum-workflows/tree/main/tests).