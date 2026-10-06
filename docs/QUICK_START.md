# Quick Start

## Local package

```bash
git clone https://github.com/nyameko/quantum-workflows.git
cd quantum-workflows
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
qw --help
```

Credential-free smoke:

```bash
qw cpu-smoke --iterations 100000 --output results
```

## Intro notebook

The introductory notebook is:

```text
labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb
```

For a personal Jupyter environment:

```bash
python -m venv ~/.venvs/qiskit-intro
source ~/.venvs/qiskit-intro/bin/activate
python -m pip install --upgrade pip
python -m pip install -r labs/01-intro-quantum-computing/requirements.txt
python -m ipykernel install   --user   --name qiskit-intro   --display-name "Python (Qiskit Intro)"
```

On the managed Quantum Platform, prebuilt kernels/environments are the preferred long-term cohort experience.

## Durable platform execution

The validated M3 path is:

```text
Quantum Platform /runs/
   ↓
cpu-smoke
   ↓
restricted gateway
   ↓
Slurm
   ↓
Apptainer
   ↓
qw cpu-smoke
   ↓
shared result/provenance
```

The reference acceptance run completed successfully as Slurm job 15 with exit code `0:0`.

## Results

Every canonical workflow writes:

```text
<output>/<workflow>/<run-id>/
├── manifest.json
├── summary.json
└── data/
```

The manifest is part of the scientific result, not optional logging.
