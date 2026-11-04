# Lab 01 — A Very Basic Introduction to Quantum Computing

This introductory lab is adapted from the CHPC Student Cluster Competition quantum-computing demonstration notebook.
It introduces classical bits, a single qubit, superposition, measurement,
interference, two-qubit entanglement and a coin-flip analogy using Qiskit and
Qiskit Aer.

## Independent workstation installation

A personal laptop/workstation can run this notebook without a CHPC or Quantum Platform account. Install Python, create a local virtual environment, install `requirements.txt` and `jupyterlab` in that environment, and open `Intro_QC_Demo.ipynb` with its kernel. The full `02-bell-cpu-gpu-qpu.ipynb` lesson additionally requires the `quantum-workflows` Python 3.14 package. Follow [the self-hosted workstation and GPU guide](../../docs/wiki/Standalone-workstation-GPU-and-notebooks.md). GPU and QPU access are not required for beginner CPU lessons.

## One-time environment setup in Quantum Platform

The Jupyter workbench home is persistent at `/home/research/<username>`.
Create the virtual environment there so it survives workbench Pod replacement.

From a JupyterLab Terminal:

```bash
mkdir -p ~/.venvs
python -m venv ~/.venvs/qiskit-intro
source ~/.venvs/qiskit-intro/bin/activate

python -m pip install --upgrade pip
python -m pip install -r /path/to/quantum-workflows/labs/01-intro-quantum-computing/requirements.txt

python -m ipykernel install \
  --user \
  --name qiskit-intro \
  --display-name "Python (Qiskit Intro)"
```

Then open `Intro_QC_Demo.ipynb` and select **Python (Qiskit Intro)** as the
kernel.

You do not need to install JupyterLab inside this venv: JupyterLab is already
provided by the managed Quantum Platform workbench. The venv only needs the
scientific packages plus `ipykernel` so the environment can appear as a
selectable kernel.

## Dependencies

The notebook imports:

- `qiskit.QuantumCircuit`;
- `qiskit.quantum_info.Statevector`;
- Qiskit Bloch/state-city/circuit visualisation;
- `qiskit_aer.AerSimulator`.

The requirements therefore install Qiskit with its visualization extra,
Qiskit Aer, Matplotlib and IPython kernel support. Avoid installing both
`qiskit` and `qiskit[visualization]` separately; the latter already
installs Qiskit with the visualization dependencies.

## Verify the environment

```bash
source ~/.venvs/qiskit-intro/bin/activate
python - <<'PY'
import qiskit
import qiskit_aer
import matplotlib

print("qiskit:", qiskit.__version__)
print("qiskit-aer:", qiskit_aer.__version__)
print("matplotlib:", matplotlib.__version__)
PY
```

## Teaching note: statevector after measurement

The source SCC notebook contains a cell that calls
`Statevector.from_instruction(qc0)` after `qc0.measure_all()`. Current
Qiskit raises a `QiskitError` because measurement introduces classical bits
and is not a unitary statevector instruction. The error is now **caught and explained inside the cell** so a clean top-to-bottom run succeeds; an unmeasured copy of the preparation circuit provides the statevector visualization. This remains a discussion point rather than a hard failure.

## Platform direction

This venv/kernel workflow is appropriate for the introductory lab and teaches
students Python environment isolation. A later platform milestone can publish a
prebuilt **Intro Qiskit** workbench/kernel so large cohorts do not each download
the same packages independently.
