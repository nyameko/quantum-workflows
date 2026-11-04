# Designing research curricula and coherent learning pathways

## Philosophy

A full hybrid quantum-centric supercomputing curriculum should **not** be a queue of 87 notebooks or merely a sequence of popular quantum algorithms. Begin with mathematical foundations and classical scientific truth; then explore high-performance implementations and only then introduce quantum reformulations whose accuracy and resources can be meaningfully compared. Each module should be independently usable by a beginner, HPC engineer or domain specialist with the necessary prerequisites.

## Curriculum graph

The curriculum should describe prerequisites as an explicit graph: Python/numerical methods, probability/linear algebra, basic quantum mechanics and computing, classical modeling, HPC scaling, scientific ML, circuit compilation, noise, QEC, hardware modality and domain application. A researcher in nuclear physics can enter through Hamiltonians; a finance student through stochastic processes/PDEs; a photonics researcher through Maxwell/Jones optics. Common validation/provenance standards unify the paths without requiring all learners to complete identical courses.

## Domain academy requirements

**Financial engineering:** classical statistics, Black–Scholes/PDE and Monte Carlo, portfolio optimization, GPU/HPC baselines, QAOA/amplitude estimation/HHL where justified, cost/resource metrics. **Nuclear and HEP:** conservation, nuclear many-body Hamiltonians, transport, lattice models and selected quantum simulation with independent high-precision references. **CFD/PDE:** discretization, convergence, conditioning, sparse solvers, hardware scaling and full quantum linear-system resource costs. **QML:** classical baselines, data encoding, reproducibility, trainability, no unsupported speedup claims. **Photonics:** optical fields, detectors, coherent/incoherent regimes, quantum states and measured validation.

## Hardware-specific tracks

Each modality deserves a substantial native-SDK and hardware model, including superconducting circuits, trapped ions, neutral atoms, semiconductor spins, photonic CV/DV states, analog simulators, qudits and dual-rail schemes. Include device physics, control/measurement, calibration, noise, error correction, ISA/compilation and resource estimates. A conceptual overview notebook is not a completed modality programme.

## Lesson release criteria

Require explicit learning outcomes, skill graph placement, reading prerequisites, runnable credential-free CPU path, known expected answers, mathematical derivations, numerical/statistical validation, runnable tests, references/license, limitations, cost estimate, optional QPU step and teaching feedback. Keep a separate content-development status from published curriculum approval.

Sources: [master curriculum 2026–31](https://github.com/nyameko/quantum-workflows/blob/main/docs/MASTER-ACADEMY-AND-RESEARCH-TRACKS.md), [learning path](https://github.com/nyameko/quantum-workflows/blob/main/docs/LEARNING_PATH.md), [pathways and ingestion plan](https://github.com/nyameko/quantum-workflows/blob/main/docs/ACADEMY-PATHWAYS-AND-INGESTION.md).