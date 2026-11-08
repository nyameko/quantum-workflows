# Learning and Research Path

`quantum-workflows` is intended to support users from a first quantum-computing notebook through advanced hybrid CPU/GPU/QPU research.

The repository should not force one linear curriculum. Instead it provides a set of progressive tracks with shared environment, execution and provenance conventions.

## Entry levels

### Beginner

Start with:

- classical bit vs qubit;
- single-qubit gates;
- Bloch sphere;
- superposition and interference;
- measurement;
- Bell states and entanglement;
- shot statistics.

The first notebook is:

```text
labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb
```

### Intermediate

Progress into:

- Qiskit primitives and transpilation;
- noise and sampling;
- variational algorithms;
- OpenQASM;
- portability between SDKs;
- local simulator vs remote execution;
- CPU/GPU simulation.

### Advanced

Progress into:

- Suzuki–Trotter product formulas;
- Hamiltonian simulation;
- SQD/SKQD;
- quantum chemistry;
- QML/QINNs;
- HEP/nuclear/medical domain examples;
- QRMI/QDMI;
- heterogeneous CPU/GPU/QPU workflows.

## Classical HPC bridge

The repository also needs an explicit classical scaling journey because QCSC users must understand the systems around the QPU.

Planned sequence:

```text
single-core CPU
   ↓
multicore CPU
   ↓
two-node MPI
   ↓
multi-node HPL
   ↓
A100 HPL
   ↓
H200 HPL
   ↓
multi-H200 HPL
```

The HPL track is a flagship teaching workflow because it connects notebooks, Slurm, observability, performance tuning and persistent agent projects before introducing a QPU.

## Quantum acceleration bridge

The corresponding quantum-simulation journey is:

```text
Qiskit Aer CPU
    ↓
Qiskit Aer GPU
    ↓
PennyLane Lightning CPU
    ↓
PennyLane Lightning GPU
    ↓
CUDA-Q
    ↓
provider emulator
    ↓
QPU hardware
```

## Vendor-neutral teaching rule

Vendor-neutral does not mean hiding provider-native concepts.

For each supported ecosystem:

1. teach the native SDK and execution model;
2. provide a credential-free simulator/emulator path;
3. provide the hardware path where available;
4. record the target capability and provenance;
5. provide equivalent examples in other SDKs where the semantics genuinely map;
6. document information loss when translation is not exact.

Candidate ecosystems include:

- IBM / Qiskit;
- PennyLane;
- CUDA-Q;
- IQM;
- Pasqal / Pulser;
- D-Wave / Ocean;
- Cirq;
- Braket;
- Azure Quantum / QDK;
- maintained open interchange layers such as OpenQASM/QIR where applicable.

## Notebook quality contract

Every canonical lab/notebook should state:

- audience/level;
- prerequisites;
- expected runtime;
- local credential-free path;
- optional Slurm/GPU/QPU path;
- environment/kernel;
- learning outcomes;
- result/provenance path;
- references;
- known limitations;
- expected cleanup.

## Batch-first simulator academy (M5 entry sequence)

> **Scientific preparation is cheap; expensive execution is scheduled.**

The short [00–07 simulator academy](../labs/01-intro-quantum-computing/batch-first/README.md) is the recommended *first-use* path alongside the existing comprehensive Bell-state notebook; it does **not** replace the established classical HPC track or the chemistry/finance/nuclear/photonics research tracks.

| Lab | Method | Default and advanced path |
| --- | --- | --- |
| 00 | Bell circuit | Qiskit Aer CPU, small JupyterHub workbench |
| 01 | First GPU Slurm batch | authenticated native `sbatch` → Aer GPU A100/H200 |
| 02 | Quantum simulation performance | `16 * 2**n` bytes complex128 statevector storage; CPU then scheduled GPU benchmark |
| 03 | PennyLane Lightning | lightning.qubit gradients → validated lightning.gpu image |
| 04 | Cirq/qsim/cuQuantum | Cirq/qsim CPU → separate CUDA/cuStateVec/cuTensorNet GPU runners |
| 05 | IQM architectures | local IQM fake backend (no QPU expenditure) |
| 06 | Pasqal neutral atoms | Pulser/Qutip CPU → separately validated emu-sv/emu-mps |
| 07 | Real quantum hardware | Aer baseline → **explicitly approved** remote QPU, with quota and provenance |

**Concept rule:** a development framework, a simulator backend, a CPU/GPU execution resource and a physical QPU provider are distinct. Real device emulation requires modality-specific assumptions and scientific checks. Native scheduler jobs survive the Jupyter kernel; GPU access is never held simply for reading or editing.

## Persistent-agent integration

The future Agent Control Plane should guide users through the same material rather than replacing it.

For example:

```text
user opens HPL notebook
      ↓
agent explains parameters
      ↓
user submits durable run
      ↓
agent records experiment context
      ↓
run finishes on Slurm/GPU
      ↓
agent compares result with previous runs
      ↓
user continues from SSH/TUI or portal
```

The scientific notebook remains reproducible without the agent. The agent adds continuity, tutoring and experiment memory.
