# Lab 01 — A Very Basic Introduction to Quantum Computing

This introductory lab is adapted from the CHPC SCC `Day4_QC_Demo.ipynb`.
It introduces classical bits, a single qubit, superposition, measurement,
interference, two-qubit entanglement and a coin-flip analogy using Qiskit and
Qiskit Aer.

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

Then open `Day4_QC_Demo.ipynb` and select **Python (Qiskit Intro)** as the
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
and is not a unitary statevector instruction. This is retained as a useful
discussion point; the following section creates a fresh circuit before
continuing.

## Platform direction

This venv/kernel workflow is appropriate for the introductory lab and teaches
students Python environment isolation. A later platform milestone can publish a
prebuilt **Intro Qiskit** workbench/kernel so large cohorts do not each download
the same packages independently.
