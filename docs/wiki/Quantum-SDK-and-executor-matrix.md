# Quantum SDKs, simulators and execution backends

## Preserve scientific semantics

The choice of SDK, simulator method, hardware modality and target backend changes available gates, noise, topology, precision, shot handling and compilation options. Do not assume that the same Python circuit object transparently maps to every QPU. Teach native SDKs first, and use adapters only for a genuinely common scientific contract. Never claim equivalent physical behavior without independent comparison.

## Current CLI executor capabilities

| Reference command | Implemented executor choices in CLI | Requirements |
|---|---|---|
| `qw cpu-smoke` | local CPU path | supported Python and core dependencies |
| `qw hello` | `aer`, `aer-gpu`, `lightning-cpu`, `lightning-gpu`, `ibm`, `qrmi` | optional compatible SDK, GPU or remote credentials |
| `qw trotter` | `aer`, `ibm`, `qrmi` | Qiskit; remote access only if authorized |
| `qw sqd` | `statevector`, `ibm`, `qrmi` | optional `sqd` scientific extra, chemistry dependencies |

This reflects parser options in `src/quantum_workflows/cli.py` on the reviewed source revision; **an available parser option does not prove that its environment or provider is deployed**.

## Optional and proposed ecosystems

The academy roadmap includes IBM/Qiskit, PennyLane Lightning, NVIDIA cuQuantum/CUDA-Q, IQM, Pasqal/Pulser, D-Wave/Ocean, Cirq, AWS Braket, Azure Quantum and native analog/digital hardware modes. Some have conflicting Qiskit or Python version requirements. Plan independent, pinned environments with their own tests; mark unimplemented gateways **planned**.

## CPU/GPU cross-check

Run a small circuit with known outcome on credential-free CPU first. Compare statevector or measured observable against analytical exact results and then repeat on a GPU simulator using a compatible wheel on an allocated A100/H200. Record backend version, GPU driver, simulation method, precision, number of qubits, memory usage and error. A GPU path may be faster at large scale but slower for tiny examples due to overhead; benchmark rather than assume.

## Hardware evaluation

For real QPUs, log modality, native topology, calibration window, transpiler and mitigation strategy, shots/credits, queue time and the circuit's actual implemented form. Provider QPU access is opt-in, subject to research entitlement and budget. A simulator result is not evidence of a physical experiment.

See [CLI executor map](https://github.com/nyameko/quantum-workflows/blob/main/src/quantum_workflows/cli.py), [environment catalogue](https://github.com/nyameko/quantum-workflows/blob/main/docs/ENVIRONMENTS.md), [IBM handshake](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/01-IBM-QPU-HANDSHAKE.md) and [academy roadmap](https://github.com/nyameko/quantum-workflows/blob/main/docs/MASTER-ACADEMY-AND-RESEARCH-TRACKS.md).