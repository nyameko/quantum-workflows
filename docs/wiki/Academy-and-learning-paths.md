# Academy and research learning paths

## How to navigate

The academy should be a prerequisite/equivalence graph, not a forced sequence or a list of every planned notebook. Learners can enter as beginners, computational physicists, engineering students, advanced quantum researchers or HPC scientists.

| Track | Foundations | Progression and capstone |
|---|---|---|
| Scientific foundations | Python, linear algebra, numerics, uncertainty | verified classical reference, uncertainty and reproducibility |
| Classical HPC | CPU, profiling, parallel algorithms, MPI | Slurm, GPU portability, strong/weak scaling, HPL measurements |
| Quantum computing core | states, gates, channels, circuits, measurement | simulation, noise, transpilation, ISA, Hamiltonians, QEC |
| Algorithms | Grover, QFT, phase estimation, VQE, HHL | error/resource analysis, hardware-aware comparisons |
| QML / neural networks | classical ML baselines, kernel methods | QCNN/QSVM/QINN, trainability, data encoding and rigorous benchmarks |
| Finance | probability, derivatives, PDE, portfolio optimization | classical pricing/optimization -> HPC/ML -> quantum comparisons |
| Nuclear / HEP / medicine | Hamiltonians, nuclear methods, Monte Carlo | lattice/spin/field models, nuclear simulation, validated domain cases |
| CFD / PDE | finite difference/volume/element, solvers | HPC benchmark -> quantum linear systems/resource estimation |
| Photonics / quantum optics | Maxwell/Jones/diffraction, detectors | PhotonicsLab bench, coherence, single photons, QKD, noise |
| QPU modalities | superconducting, ions, neutral atoms, photonic, spins | native SDK, controls, error models, QEC and resource estimates |

Hardware and software tracks should retain distinct foundations: classical engineering first, then quantum modeling, then resource/performance evidence. Planned modality tracks include analog/digital ions and neutral atoms, superconducting circuits, photonics, semiconductors, dual rail and qudits. QEC includes surface and LDPC/bicycle-type codes and relevant fault-tolerance overhead.

## Availability labels

**Committed now:** the intro notebook, Bell CPU/GPU/QPU reference notebook where dependencies permit, three computational photonics N01–N03 notebooks, and core runner source. **Historical/staged, not guaranteed in main:** the larger Zero-to-Hero and QEC curriculum archives referred to by planning docs. **Proposed:** full domain academies and capstones. Count notebook files on the actual commit before asserting delivery.

## Learning outcome contract

Each reviewed lesson needs audience, prerequisites, theory/derivation, CPU credential-free path, expected outputs, analytic checks, numerical convergence, tests, optional authorized accelerated/hardware path, safety/cost estimate, references and exercises. An LLM can offer tutoring but cannot certify mastery by itself.

See [master academy](https://github.com/nyameko/quantum-workflows/blob/main/docs/MASTER-ACADEMY-AND-RESEARCH-TRACKS.md), [learning path](https://github.com/nyameko/quantum-workflows/blob/main/docs/LEARNING_PATH.md), and [curriculum ingestion policy](https://github.com/nyameko/quantum-workflows/blob/main/docs/ACADEMY-PATHWAYS-AND-INGESTION.md).