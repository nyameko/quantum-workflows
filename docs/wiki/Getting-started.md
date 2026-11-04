# Getting started

## Prerequisites

The current `pyproject.toml` requires **Python 3.14** (`>=3.14,<3.15`). Install from a supported Python 3.14 environment, use a virtualenv and keep remote QPU credentials out of Git. Ordinary reference CPU work needs no GPU allocation, proprietary service or paid API.

```sh
git clone https://github.com/nyameko/quantum-workflows.git
cd quantum-workflows
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev,notebooks]'
qw --help
qw cpu-smoke --iterations 100000 --output results
qw hello --executor aer --shots 1024 --seed 42 --output results
```

The command creates a result tree, not just printed output. Inspect `manifest.json`, `summary.json` and `data/` in the directory reported by the runner. Preserve the complete result folder for debugging and science review.

## First notebook

Open `labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb` using a compatible Jupyter kernel and the notebook requirements. Work through state preparation, measurement, Bell-state correlations and shot statistics. Compare simulation to mathematical expectations rather than treating any one histogram as a theorem.

## Choose your next path

Run `qw trotter --executor aer --qubits 4 --output results` for Ising dynamics. The `sqd` example has additional scientific dependencies and heavier cost; install the `sqd` extra into a dedicated environment before attempting it. For physical hardware use the explicit provider extra/allocation pathway; no remote credentials are needed for the simulator path.

## Managed environment

The portal's JupyterHub single-user server is a lightweight KubeSpawner workbench. Large CPU/GPU/QPU experiments are scheduled separately, with durable results. A notebook is not a resource reservation.

See [Quick Start](https://github.com/nyameko/quantum-workflows/blob/main/docs/QUICK_START.md), [first lab](https://github.com/nyameko/quantum-workflows/blob/main/labs/01-intro-quantum-computing/README.md) and [scientific environments](https://github.com/nyameko/quantum-workflows/blob/main/docs/ENVIRONMENTS.md).