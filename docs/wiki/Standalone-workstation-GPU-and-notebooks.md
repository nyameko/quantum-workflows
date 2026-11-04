# Standalone Jupyter notebooks and a personal GPU workstation

**Audience:** independent student/researcher or instructor with a Linux workstation, desktop or single GPU server. **No CHPC/Quantum Platform account, Kubernetes, Slurm, ACP, paid provider account or remote QPU is needed for the CPU examples.** The currently committed lessons are the two introductory quantum notebooks and three CPU PhotonicsLab notebooks (N01–N03); the proposed academy is not an installed set of notebooks.

## 1. Choose the Python environment

| Lesson / task | Python / packages | GPU needed? |
| --- | --- | --- |
| `Intro_QC_Demo.ipynb` only | Standalone `labs/01-intro-quantum-computing/requirements.txt`; a compatible Python interpreter | No |
| `02-bell-cpu-gpu-qpu.ipynb`, `qw hello`, `qw trotter` | `quantum-workflows` package **Python 3.14**, Qiskit/Aer, notebook extras | No for CPU; optional NVIDIA for GPU |
| `qw sqd` | Python 3.14 and dedicated `sqd` extra; additional scientific dependencies | No for the reference local run |
| Photonics N01–N03 | NumPy, Matplotlib, nbclient and the **pinned PhotonicsLab revision**, in a separate environment | No; these are currently CPU lessons |

For early experiments, use one Python 3.14 virtual environment for Qiskit notebooks, and a separate photonics environment if needed. Notebook files are ordinary Jupyter notebooks, not tied to the project's portal. To run *only* the original introductory Qiskit notebook, `quantum-workflows` package installation is not necessary; use its standalone requirements instead.

## 2. Clone and run locally on Linux

Install Git, Python **3.14**, python3.14-venv/ensurepip, and a Python-compatible C/C++ toolchain if any required scientific package lacks a wheel for your platform. Use a published commit or tag for a stable cohort, or `dev` to evaluate current development documentation:

```bash
git clone --branch dev https://github.com/nyameko/quantum-workflows.git
cd quantum-workflows
git rev-parse HEAD

python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[notebooks]'
python -m pip install 'qiskit[visualization]>=2.5,<3' 'nbclient>=0.10,<1' 'nbformat>=5,<6'
python -m ipykernel install --user --name qw-local --display-name 'Python (Quantum Workflows Local)'
```

If your OS does not package Python 3.14, install an isolated interpreter with a trusted Python version manager or container; **do not replace your operating system's Python**. If a wheel does not exist for your OS/CPU/architecture, installation may fail; use a supported Linux x86-64 environment or compatible version instead of claiming automatic portability.

Validate the exact committed introductory and Bell CPU notebooks with clean kernels (the validator never selects a QPU):

```bash
MPLBACKEND=Agg python scripts/validate_local_notebooks.py
qw hello --executor aer --shots 1024 --seed 42 --output results
qw trotter --executor aer --qubits 4 --output results
jupyter lab --no-browser --ip 127.0.0.1
```

Use the Jupyter URL and token printed in the terminal. Select the **Python (Quantum Workflows Local)** kernel for:
- `labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb`
- `labs/01-intro-quantum-computing/02-bell-cpu-gpu-qpu.ipynb`

If using Jupyter over SSH, bind Jupyter to `127.0.0.1` on the remote host and forward its port with `ssh -L 8888:127.0.0.1:8888 user@your-host`; retain Jupyter authentication. Do not expose the unauthenticated notebook server to the Internet.

## 3. Enable an NVIDIA GPU only when compatible

The simple Bell demonstration will not meaningfully benchmark a powerful GPU. Larger circuit simulations can benefit, but memory, circuit structure, GPU occupancy, precision and host-device transfer govern performance. A statevector of `n` qubits uses at least `16 × 2^n` bytes at complex128 precision before temporary workspaces and simulator overhead.

```bash
nvidia-smi
python -V
python -m pip show qiskit-aer
```

Create a **separate GPU virtualenv** so that incompatible Aer CPU/GPU wheels cannot accidentally share a kernel. Inside that environment, use the same Python 3.14 source checkout and install the base package and notebook extras. Then **replace** the CPU-only Aer distribution with the GPU distribution supported by your exact Python, CUDA and NVIDIA driver combination:

```bash
python3.14 -m venv .venv-aer-gpu
source .venv-aer-gpu/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[notebooks]'
python -m pip uninstall -y qiskit-aer
python -m pip install 'qiskit-aer-gpu>=0.17,<0.19'
python - <<'PY'
from qiskit_aer import AerSimulator
devices = AerSimulator().available_devices()
print('Aer devices:', devices)
assert 'GPU' in devices, 'GPU is not available; check wheel/driver/CUDA compatibility'
PY
qw hello --executor aer-gpu --shots 1024 --output results
python -m ipykernel install --user --name qw-aer-gpu --display-name 'Python (Aer GPU)'
python -m pip install 'nbclient>=0.10,<1' 'nbformat>=5,<6'
python scripts/validate_local_gpu_notebook.py --executor aer-gpu --kernel qw-aer-gpu
```

**Compatibility is conditional, not guaranteed.** If the GPU wheel has no Python 3.14/platform-compatible build, or CUDA/cuQuantum libraries do not support your GPU generation (including some consumer RTX models), this install will fail. Stop there; use `aer` CPU for the lessons or a verified GPU environment with a matching interpreter and driver. Do not interpret `nvidia-smi` alone as proof that Aer GPU works.

PennyLane Lightning GPU is a **different executor**: in a fresh compatible environment, install `.[notebooks,lightning-gpu]`, verify `qw hello --executor lightning-gpu`, register a dedicated `qw-lightning-gpu` ipykernel, then run `python scripts/validate_local_gpu_notebook.py --executor lightning-gpu --kernel qw-lightning-gpu`. It depends on a compatible PennyLane Lightning GPU and cuQuantum installation; it should not be assumed interchangeable with Aer GPU. The `02-bell-cpu-gpu-qpu.ipynb` notebook allows switching executors after installation. Physical `ibm` and `qrmi` remain **explicitly opt-in** and may require credentials, provider quota, money or institutional allocation.

## 4. Run the Computational Photonics lessons without GPU or CHPC

Photonics N01–N03 use the pinned object-oriented `photonicslab` dependency, not a CUDA backend. Follow [the photonics lab README](https://github.com/nyameko/quantum-workflows/blob/dev/labs/04-zero-to-hero-photonics/README.md) and run `python scripts/validate_photonics_lessons.py` in its dedicated environment. Its referenced PhotonicsLab commit is part of the reproducibility contract; a newer `main` checkout may change physics behavior.

## 5. Troubleshooting and reproducibility

| Symptom | Check |
| --- | --- |
| `qw: command not found` | Activate Python 3.14 venv and `python -m pip show quantum-workflows` |
| Notebook imports missing | Notebook's kernel and `sys.executable`; register `ipykernel` from the correct venv |
| `No module named qiskit_aer` | Install environment requirements in the *active kernel*, not system Python |
| `Aer devices: ('CPU',)` | GPU wheel, NVIDIA driver/CUDA compatibility and `nvidia-smi` |
| GPU out-of-memory | Smaller circuit/qubit count or a lower-memory simulation method; distinguish VRAM from RAM |
| `Statevector` rejects measurement | The introductory lesson now catches this as a teaching example and visualizes the unmeasured preparation |
| `Permission denied` / kernel times out | Writable directory, process/kernel isolation, available system RAM and user permissions |
| Photonics library import fails | Use the course's pinned PhotonicsLab revision in a separate environment |
| Real QPU asks for a token | Remain on local `aer`; hardware use is optional and never a precondition |

Record `git rev-parse HEAD`, `python --version`, `python -m pip freeze`, `nvidia-smi` (if GPU), input parameters, seeds, simulator method, result manifests and any physical assumptions. Never commit QPU tokens, personal datasets or large notebook outputs. The CPU notebook validator is automated in CI; the optional GPU notebook validator executes the Bell notebook on the selected dedicated GPU kernel but **still requires a real compatible GPU machine**, and a passing Bell test alone does not establish speedup or scientific accuracy of a larger workflow.

See [notebook reproducibility](Notebook-environments-and-reproducibility.md), [execution environments](Execution-environments.md), [reference experiments](Reference-experiments.md), and [GPU/QPU simulator matrix](Quantum-SDK-and-executor-matrix.md).
