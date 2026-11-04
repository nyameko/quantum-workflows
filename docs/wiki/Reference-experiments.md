# Reference scientific experiments

All commands assume the project's supported Python 3.14 environment, installed extras and appropriate working directory. The `qw` wrapper exists for durable reference runs; **notebooks should teach and use native Qiskit/PennyLane/etc. SDKs directly** instead of inventing a separate science SDK.

## CPU smoke: platform acceptance, not quantum pedagogy

```sh
qw cpu-smoke --iterations 100000 --output results
```

This validates a simple CPU execution/result path, including scientific artifact emission. It does not demonstrate quantum advantage or entanglement.

## Bell handshake: Aer CPU

```sh
qw hello --executor aer --shots 2048 --seed 42 --output results
```

Validate ideal Bell correlations statistically; deviations at finite shots follow sampling uncertainty. Optional `lightning-cpu`, `aer-gpu`, `lightning-gpu`, `ibm` and `qrmi` executors have separate environment and authorization requirements. A backend string does not itself establish hardware access.

## Transverse-field Ising Trotter dynamics

```sh
qw trotter --executor aer --qubits 4 --coupling 1.0 --field 0.7 --trotter-steps 4 --output results
```

Compare exact and digitized time-evolution where possible. Study Trotter step error, time discretization, shot noise and circuit depth. The source also supports `ibm`/`qrmi` execution with external requirements.

## N₂ sample-based quantum diagonalization

Install a compatible optional `sqd` environment first:

```sh
python -m pip install -e '.[sqd]'
qw sqd --executor statevector --shots 20000 --output results
```

This is a chemistry/sample-processing workflow with heavier scientific dependencies, not a first-day lab. Track reference energy, recovery strategy, batch sizes, truncation and convergence, rather than inferring chemical accuracy from mere job completion.

Inspect [CLI argument definitions](https://github.com/nyameko/quantum-workflows/blob/main/src/quantum_workflows/cli.py), [Trotter tutorial](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/02-TROTTERIZED-DYNAMICS.md), [SQD tutorial](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/03-SAMPLE-BASED-QUANTUM-DIAGONALIZATION.md) and [IBM handshake](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/01-IBM-QPU-HANDSHAKE.md).