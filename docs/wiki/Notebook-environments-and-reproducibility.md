# Notebooks, kernels and reproducible software environments

## Environment model

A notebook is a teaching and interactive scientific interface; a Python virtualenv/kernel is a software environment; a scheduler allocation is a compute resource; a runner image is a versioned execution artifact. These must not be conflated. The current source requires **Python 3.14** for `quantum-workflows` and isolates optional extras such as `ibm`, `sqd`, `lightning-cpu` and `lightning-gpu`.

## Local interactive environment

```sh
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[notebooks,dev]'
python -m ipykernel install --user --name quantum-workflows --display-name "Python (Quantum Workflows)"
jupyter lab
```

Only run kernel installation in a user-controlled development machine; managed Jupyter cohorts should prefer prebuilt, tested kernels. A large shared NFS environment should not require every student to independently download conflicting SDK stacks. Native SDK notebooks remain primary teaching material; `qw` supplies reference durable workflow runs, not an alternative to Qiskit/PennyLane.

## Reproducible notebook acceptance

Run top-to-bottom with a clean kernel, no hidden earlier state, explicit seed and local writable output path. Make network/hardware steps optional and clearly consented. Plot axes with units, compare derived results to analytical reference/tolerance, and keep the exported notebook clear of huge outputs/secrets. A reproducible lesson can be tested in CI using an isolated CPU environment; hardware QPU tests should never be on the normal PR path.

## Managed HPC submission

Keep the notebook light; submit substantial compute via an approved offering and run image. Preserve parameter JSON, code revision, image digest, backend, job ID, numerical checks and result path. When re-running on A100/H200, compare physics to CPU first and only then benchmark speed/memory; do not assume GPU equals improved accuracy.

## Troubleshooting

Wrong Python minor version, incompatible optional extras, stale kernel registration, missing GPU drivers and insufficient NFS permission are separate failures. Use `python --version`, `python -m pip list`, `jupyter kernelspec list`, test imports and small reference circuit before escalating.

References: [environment plan](https://github.com/nyameko/quantum-workflows/blob/main/docs/ENVIRONMENTS.md), [quickstart](https://github.com/nyameko/quantum-workflows/blob/main/docs/QUICK_START.md), [learning lab](https://github.com/nyameko/quantum-workflows/blob/main/labs/01-intro-quantum-computing/README.md), [project dependencies](https://github.com/nyameko/quantum-workflows/blob/main/pyproject.toml).