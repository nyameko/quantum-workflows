# Quantum Workflows — Master Academy and Research Curriculum (2026–2031)

**Status:** proposed architectural curriculum (not a claim of implemented notebooks). **Owner:** \`quantum-workflows\` for science/content, with \`quantum-platform\` and \`agent-control-plane\` as consumers. **Base principle:** "classical truth first; HPC scaling next; ML where justified; quantum implementation only where semantics and physical access permit; measurement, resource accounting and reproducibility throughout."

This document corrects the too-narrow interpretation of the 87 staged notebooks as the entirety of the academy. It consolidates the original hybrid-HPC/QC and PhD research scope (2025–2026), including numerical methods, **finance from first principles**, nuclear/HEP/medicine, CFD/PDEs, optics/photonic systems, QML/AI, algorithms and circuit engineering, compilers/logical ISA, quantum simulation, all major physical QPU modalities, QEC, open systems, energy/resource estimation, and scholarly teaching. It captures a **roadmap**, not a requirement to build all subjects before one student can use Jupyter.

## 0. Distinguish implemented, staged and planned

- **Committed in repo:** \`labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb\`; existing Bell, Ising/Trotter and SQD runners and scientific workflows documented elsewhere. These do not constitute the whole academy.
- **Staged archive, pending import and scientific review:** \`labs/02-zero-to-hero\` (24), \`labs/03-zero-to-hero-qec\` (29), \`labs/04-zero-to-hero-photonics\` (34): **87 notebook files**. These include individual Grover, VQE and HHL demonstrations and some modality overviews. A one-notebook demonstration is **not** a comprehensive quantum-algorithms or modality course.
- **Proposed herein:** modular families and dedicated domain academies with their own prerequisite chains, testable notebook specifications, textbook references, datasets, benchmarks and research capstones. Counts listed as *planned modules*, not implemented files.
- **Independently runnable:** every foundational notebook must have a local, credential-free CPU path. GPU, high-memory Slurm, remote QPUs and expensive experiments remain opt-in and policy authorised.

## 1. Pedagogical architecture: shared trunks plus branching specialisations

A user should NOT receive "all notebooks." A curriculum is a **directed prerequisite/equivalence graph**. A motivated beginner, graduate, experimental scientist or established PI enters via an optional diagnostic or a user-selected goal. A user may jump into their own field, revisit foundations, choose different hardware backends, or pursue multiple research applications. A PI can fork/edit an approved pathway and publish a reviewed version. Never assert a student's competence based solely on an LLM interaction.

\`\`\`text
scientific literacy / Python / mathematics / reproducibility
         |                          |
  classical domain science      quantum information / QM
         |                          |
 numerical algorithms --> CPU/HPC/GPU scaling --> robust ML/AI baselines
         |                          |
         +---- quantum algorithm / circuit / QEC / ISA foundations ----+
         |                          |                                  |
   domain application        hardware modality laboratories       theory / complexity
         |                          |                                  |
         +------ common benchmark: accuracy + cost + energy + evidence +
                             |
             scientifically reviewed publication/capstone
\`\`\`

A curriculum should declare *scientific objective, prior knowledge, equivalences, core/optional modules, learning outcomes, runnable environment, CPU/GPU/QPU route, validation, literature, formative assessment, capstone, uncertainty and evidence level*. **Modules** are reusable objects; an **academy** composes them into a substantial track. A course never silently rewrites its pinned source, execution image or assessment rubric.

## 2. Shared core: substantial foundational academies, not four introductory lessons

The reusable shared trunk should contain independent notebook families:

| Prefix | Core academy | Indicative notebooks / exercises (proposed) |
| --- | --- | --- |
| FND | Scientific computing, reproducible research | Python/NumPy, environments/Git, scientific data/uncertainty, plotting, units, tests, provenance, open science |
| MTH | Mathematical methods | linear algebra/eigensystems/tensors; calculus, Fourier/Laplace; probability/statistics; optimisation; complex analysis; functional analysis; stochastic processes; introductory PDEs |
| NUM | Numerical methods | floating-point/error, quadrature, root-finding, ODE/SDE, FDM/FVM/FEM, sparse Krylov/preconditioning, spectral, Monte Carlo, inverse problems and UQ |
| PHY | Classical and quantum physics | waves/EM/optics, thermodynamics/stat mech, classical Hamiltonian dynamics; QM Hilbert spaces, density matrices, open quantum systems, many-body physics, second quantisation |
| HPC | Classical and accelerated computation | serial → OpenMP → MPI → Slurm → HPL/HPCC → GPU profiling/memory → multi-GPU → performance/energy modelling; strong/weak scaling and reproducibility |
| ALG | Classical algorithms / computational complexity | graph algorithms, sampling/Markov chains, deterministic/stochastic search, P/NP/BPP/BQP/QMA; oracle models, algorithmic cost lower bounds |
| QIN | Quantum information foundations | qubits, qudits, modes, circuits, measurement, Bell/CHSH, entanglement entropy, channels, POVMs, tomography, quantum communication |
| RES | Research engineering | literature/DOI/ORCID/RO-Crate, replication, datasets, scientific software design, manuscript/figures, ethical/approved AI-assisted research |

Do **not** force domain experts to repeat their existing mathematics. Use competency equivalences and short optional refreshers.

## 3. Complete general-purpose quantum-computing core

| Prefix | Dedicated track | Curriculum coverage |
| --- | --- | --- |
| CIR | Quantum circuit design and synthesis | gate matrices, universality, reversible arithmetic, multi-control, circuit identity proofs, routing/connectivity, commutation, Trotter, circuit cutting, mid-circuit feed-forward, dynamic circuits, depth/fidelity tradeoffs |
| QAL | Quantum algorithms | Deutsch–Jozsa/Bernstein–Vazirani, Grover/amplitude amplification, QFT/QPE, Shor/order finding (toy), VQE/ADAPT-VQE, QAOA, quantum walks, amplitude estimation, HHL, quantum linear algebra, QSP/QSVT, Hamiltonian simulation, Gibbs sampling, search/sampling, block encoding, oracle and I/O costs |
| CMP | Compilers, transpilation and ISA/IR | OpenQASM, QIR, quantum control flow, circuit graphs, optimisations, device-native lowering, pulses, QDMI/QRMI boundaries, logical ISA, QEC-aware scheduling, capability negotiation, unsupported-op rejection |
| SIM | Quantum simulation methods | dense/sparse exact diagonalisation, statevector/density matrix, stabilizer, tensor networks/MPS/DMRG/TEBD, quantum trajectories, GPU simulation, analog Hamiltonians, digital Trotter vs LCU/qubitization, finite-size/entanglement scaling |
| QML | Quantum ML and hybrid AI | classical ML baselines, feature encoding costs, kernels, trainability/barren plateaus, VQCs/QNNs, quantum generative models, data re-uploading, graph learning, reservoir methods, quantum-inspired tensor methods, dequantisation, experimental design, statistical evaluation |
| QEC | Noise, suppression, correction and fault tolerance | CPTP/Lindblad/channel noise, dynamical decoupling and mitigation, stabilizer/CSS/Steane, surface/color, erasure/leakage, hypergraph product/QLDPC/bicycle codes, bosonic cat/GKP/dual-rail, qudits, decoders, circuit-level syndrome extraction, biased noise, magic states/T/CCZ, logical gates/factories/code switching |
| QRE | Quantum resource estimation / energetic advantage | shots, oracles, state prep, gate/T/CCZ/depth, logical/physical ratios, decoder throughput, architecture routing, wall time, calibration/repetition, cryo/optical/electric energy, classical GPU costs, uncertainty; fixed scientific accuracy and independent baselines |
| QNT | Communication, crypto and networks | QKD BB84/E91/decoy-state, teleportation, entanglement swapping, repeaters, quantum memories and spectral matching, network orchestration, entanglement rates, security assumptions |
| QTH | Quantum theory frontier | complexity and hardness, information scrambling/thermalisation, quantum thermodynamics, open Markovian/non-Markovian dynamics, Gibbs/mixing, Hamiltonian learning and validation, fault tolerance thresholds, quantum gravity/holography as clearly labelled advanced research |
| AIS | AI co-scientist, verified algorithm discovery | tensor/attention basics, structured circuit graph representations, ML/LLM circuit proposals, formally checked equivalence and independent classical evaluators, literature-grounded tool use, reproducibility, no unsupported "AI discovered an advantage" claims |

Each of these is a **first-class academy/track** with multiple notebooks, not one example buried in foundations.

## 4. Hardware-modality academies — each with theory, engineering, native SDK, noise/QEC and resource model

Each modality should cover seven common *pedagogical axes*: (1) device physics; (2) state/interaction representation; (3) state prep/control/readout; (4) analogue/digital/native program; (5) realistic simulation and calibration/noise; (6) error suppression/QEC + logical operations if supported; (7) resource estimation, HPC/QPU execution and independent comparison. **Do not require equivalent instructions where no physical correspondence exists.**

| Track | Physics, engineering and experiments | Representative SDKs / tools (compatibility to verify) |
| --- | --- | --- |
| MOD-SC Superconducting Josephson/transmon | circuits/Josephson/SQUIDs, circuit QED, microwave gates, native CZ/iSWAP/echo/CR, resonators, readout, cross-talk, leakage, cryogenics, surface/QLDPC and bosonic overlays | scqubits, QuTiP, Qiskit, Cirq, pulse simulators |
| MOD-SI Semiconductor spin/donor | quantum dots, exchange/spin-orbit/hyperfine, silicon donor vs dot, spin readout, coherent shuttling, CMOS/cryo-CMOS, multi-dot Hubbard, transport-aware compilation | QuTiP, custom exchange/Hubbard, Qiskit-compatible gate models |
| MOD-ION Trapped ion | Paul/Penning traps, spin–phonon normal modes, Mølmer–Sørensen/XX gates, motional heating, QCCD shuttling, long-range analogue Ising, digital gates, qudits, networking and syndrome schedules | QuTiP, QuSpin, PennyLane/Qiskit, provider SDKs for exposed capabilities |
| MOD-NA Neutral atoms | laser cooling/tweezers, Rydberg blockade, geometric arrays, analogue Hamiltonians, digital entangling gates, atom rearrangement, atom loss/erasures, reconfigurable QEC | Pulser, Bloqade Analog/Digital, Braket AHS |
| MOD-PDV Photonic discrete-variable | optical bench, sources, heralding, beam splitters, indistinguishability/HOM, dual-rail/path/time bins, photon number, fusion/LOQC, detectors, optical loss and multiplexing | Perceval, QuTiP, circuit/photonic models |
| MOD-PCV Photonic continuous-variable | phase-space/quadratures, Gaussian states, squeezing, homodyne, non-Gaussian gates, cluster states, Fock cutoffs, finite-squeezing GKP, optical loss | Strawberry Fields, QuTiP, Gaussian and Fock simulators |
| MOD-BOS Microwave bosonic cavity | oscillator/circuit QED, cat/GKP/dual-rail, stabilisation, parity, erasure vs leakage, outer codes, repeated readout | QuTiP, oscillator/QEC models |
| MOD-ANN Annealing/adiabatic | Ising/QUBO encoding, minor embedding, chains, anneal schedules, open systems, reverse annealing, sampling and time-to-target | D-Wave Ocean, dimod/minorminer, classical annealers |
| MOD-DEF Defect centres/networked spins | NV/colour-centre spins, optical readout, spin–photon interface, memory lifetimes, heralded entanglement, interconnects | QuTiP, network and optics simulators |
| MOD-TOP Topological and other emerging architectures | anyons/braiding and Majorana proposals, hardware evidence versus hypothetical logical resources, alternate qudit/mode platforms | mathematical/research simulators, evidence-level labels |

**Quantum optics is also its own full classical→nonlinear→quantum curriculum**, not merely an appendix to photonic QPU hardware (see staged \`labs/04\`).

## 5. First-class domain academy: Financial Engineering (FIN)

The finance learning sequence must be **self-contained for a physicist with no assumed finance background**. Suggested modules (each breaks into several notebooks, readings and assessments):

| Stage | Content and example workbooks | Scientific deliverable |
| --- | --- | --- |
| FIN-00 Financial literacy and markets | interest, discounting/time value, bonds/equities/options/futures, balance sheets/cash flow, trading/market microstructure, order books and volatility | annotated synthetic market data and payoff diagrams |
| FIN-01 Financial maths and probability | return distributions, conditional probability, Brownian motion, Itô calculus, martingales, risk-neutral valuation, no-arbitrage/replication | stochastic-process notebooks with tests |
| FIN-02 Classical derivatives and SDEs | binomial trees, Black–Scholes–Merton derivation, Greeks and sensitivities, exotic options, put–call parity, hedging | analytic vs numeric consistency |
| FIN-03 Numerical quant finance | Black–Scholes PDE, FDM, Monte Carlo, variance reduction, Fourier methods, calibration, stochastic/local volatility, jumps | pricing/error benchmark |
| FIN-04 Risk, portfolio and optimisation | Markowitz efficient frontier, factor/covariance models, rebalancing, constraints, VaR/CVaR, stress testing, yield curves, counterparty/credit/XVA as advanced options | reference convex/MIP optimisers and uncertainty |
| FIN-05 Time series, economics and ML | econometrics/ARIMA/GARCH, simulation, time-series cross-validation, gradient boosted trees and deep models, regime changes, fraud, transaction-cost aware evaluation | robust out-of-sample classical baseline |
| FIN-06 HPC/GPU financial engine | vectorised pricing, MPI scenario partitioning, CPU/OpenMP, GPU Monte Carlo and Greeks, throughput/memory/strong-weak scaling, Slurm provenance | CPU→GPU/MPI scaling report |
| FIN-07 Quantum finance methods | QAE for pricing/risk (including state prep/oracle costs); QUBO/QAOA/annealing for constrained portfolios; HHL/QSVT for selected discretised PDE/linear subproblems; quantum kernels/generative models with ML comparisons | quantum vs classical with end-to-end costs |
| FIN-08 Research studies | GameStop/options/short-squeeze as *data-backed historical reference study* (market microstructure, liquidity, volatility, derivatives), African energy/commodity FX exposures, reproducible published benchmarks and negative findings | capstone paper, dataset rights and reproducibility |

Do not equate “HHL solves Black–Scholes” with a turnkey quantum pricing advantage; the PDE discretisation, state loading, conditioning, output extraction and nonlinearity must all be priced. Never imply a trading strategy or financial profit without out-of-sample evidence.

**Flagship FIN capstone:** one pricing/risk/portfolio problem from derivation -> CPU reference -> MPI/GPU -> robust ML baseline -> permitted quantum encoding/algorithm -> error/uncertainty/QRE/energy and statistically valid comparison.

## 6. First-class domain academy: Nuclear and High-Energy Physics (NHEP)

| Stage | Example research notebook families |
| --- | --- |
| NHEP-00 Classical physics refresher | mechanics, scattering, nuclear structure, relativistic kinematics, angular momentum, group representations, particle interactions, nuclear/HEP experimental measurements |
| NHEP-01 Computational physics | Monte Carlo integration and variance reduction; detector/transport paradigms; Geant4 and ALICE O2 **as classical applications**, not direct QPU replacements |
| NHEP-02 Quantum many-body | spin chains, fermions, second quantisation, Jordan–Wigner/Bravyi–Kitaev, Hubbard, nuclear shell models, configuration interaction, tensor networks/DMRG |
| NHEP-03 Lattice field/gauge theory | lattice discretisation, gauge constraints/Gauss law, Z2 and U(1) (1+1D to tractable 2+1D), Wilson loops, string breaking, electric/magnetic observables, truncations, Abelian vs non-Abelian resource obstacles |
| NHEP-04 Real-time dynamics/scattering | Hamiltonian evolution, product formulas, digital/analogue emulation, open-system and thermal approaches, scattering toy models, neutrinos, coherent transport |
| NHEP-05 HPC/GPU | sparse exact diagonalisation, contraction/tensor networks, lattice updates, Monte Carlo/Markov-chain and GPU benchmark, finite-volume errors |
| NHEP-06 QPU mapping and QEC | VQE/QPE/Hamiltonian simulation, fermionic encodings, qubit/qudit gauge links, analogue vs digital trapped-ion/neutral-atom mapping, logical error/QRE estimates |
| NHEP-07 Nuclear applications | fusion plasma links, nuclear medicine/radiation transport and imaging, nuclear fuel/reactor physics as *separately scoped* domain extensions, event-classification QML with strong classical baseline |
| NHEP-08 Research frontier | QCD beyond toy theories, sign problem, non-Abelian gauge theory, nuclear/HEP data pipelines, physics validation/collaborative reproductions |

Do not claim a simulated lattice Z2 string-breaking experiment reproduces full four-dimensional QCD or a nuclear collision detector supplies a usable quantum state by default.

**Flagship:** strong classical sparse/tensor benchmark -> ion and Rydberg emulators for same model/observables -> digital circuit -> QEC/resource estimates -> paper-quality provenance and uncertainty.

## 7. First-class domain academy: CFD, PDEs and Scientific Linear Systems (CFD)

| Stage | Example research notebook families |
| --- | --- |
| CFD-00 Continuum mechanics | conservation laws, dimensional analysis, Euler/Navier–Stokes, boundary/initial conditions, fluid regimes |
| CFD-01 Discretisation | FDM/FVM/FEM/spectral, CFL/stability, mesh quality, sparse operators, advection-diffusion, Burgers, Poisson, incompressible-flow projection |
| CFD-02 Linear/nonlinear solvers | sparse Krylov, preconditioning/multigrid, nonlinear Newton/Picard, operator splitting, optimisation/inverse problems |
| CFD-03 HPC | OpenMP/MPI, Slurm, domain decomposition, GPU stencil/linear algebra, benchmark CPU/GPU/MPI scaling, energy/UQ |
| CFD-04 ML surrogates | physics-informed networks, Fourier neural operators, DeepONet, generalisation, physical conservation and failure modes |
| CFD-05 Quantum linear algebra | honest HHL small examples; block encodings/QSVT/quantum linear-system solvers; condition number, data loading, output/observable extraction, subroutine cost |
| CFD-06 Quantum PDE approaches | linearised PDE systems, variational linear solvers, quantum lattice Boltzmann / quantum-walk candidates, amplitude encoding, quantum-inspired tensor alternatives, nonlinear coupling via classical outer iteration |
| CFD-07 Coupled applications | turbulence/plasma/fusion, radiometry, compressible flow and financial Black–Scholes PDE transfer studies; validate against trusted classical solvers |
| CFD-08 Research benchmark | fixed residual/physical observable target, wall-time/energy including I/O and postprocessing; negative results retained |

**Flagship:** 2D Poisson -> diffusion/advection -> Burgers or small incompressible flow reference -> HPC/GPU solver -> block-encoded/variational small linear subproblem -> fully accounted end-to-end error and runtime. **HHL is not a drop-in solver for nonlinear Navier–Stokes.**

## 8. Other first-class applied research academies

- **CHEM Materials and Quantum Chemistry:** molecular electronic structure, Hartree–Fock/DFT/coupled cluster, PySCF/ffsim, integrals/active spaces, quantum chemistry mappings, VQE/ADAPT, SQD/SKQD, QPE, catalysis, energy and quantum advantage benchmarks. Link existing N2 SQD workflow.
- **OPT Laser, Structured Light and Quantum Photonics:** Maxwell/Gaussian beams/ray ABCD, nonlinear crystal processes, Fourier and diffractive optics, polarisation/Jones/Mueller, waveplates/birefringence, SLM/OAM, propagation, detectors/tomography, SPDC, DV/CV optical information, QKD/teleportation/memories; reusable object-oriented optical bench (staged 34 notebooks).
- **MED Nuclear Medicine, Radiation, Medical Physics:** radiation-matter interaction, imaging/inverse problems, Geant4/GATE or equivalent domain references, Monte Carlo dose and detector modelling, tomographic reconstruction, GPU acceleration/ML, quantum sensing/imaging/limited quantum algorithm candidates; patient privacy and clinical validity.
- **QML Applied Quantum AI / NLP:** standard ML and optimisation first; embeddings, supervised/unsupervised, transformers/attention, classical GPU; kernels/feature maps, trainability, QNN/generative/reservoir learning, text/graph problems, dequantisation and controls. A stand-alone curriculum, not "one QML exercise".
- **OPTZ Optimisation, Logistics and Operations Research:** LP/convex/MIP, scheduling/routing, graph/energy models, heuristics, integer formulations/QUBO/Ising, QAOA, annealing, quantum walks, baselines and solution-quality/latency evaluation.
- **CRYP Quantum Communications, Cryptography and Networks:** classical and quantum information, QKD (BB84/E91/decoy), entanglement/teleportation, network repeaters, quantum memories, device-independent assumptions, attack models and realistic key rates; distinguish quantum cryptography from post-quantum classical cryptography.
- **GRAV Quantum Gravity and Topological Field Theory (advanced research elective):** relativity/differential geometry, black-hole thermodynamics, entanglement/holography, quantum information, topological charge and field solitons, toy gauge/gravity analogues; label conjectures, analogy and experiments separately.
- **QEI Full-Stack Quantum Energetics and Sustainability:** quantum thermodynamics, autonomous optical Bloch equations, metric-noise-resource framework, QEC energy costs, photonic/ion/superconducting control overhead, facility-grade CPU/GPU/QPU energy and joules per validated scientific result.

Applied programmes can cross-reference modules from other disciplines (finance PDE from CFD, nuclear imaging from MED, optical qudits from OPT, Gibbs learning from QTH) without copying notebook source.

## 9. Cross-track sample pathway plans

### New learner: Quantum error correction

Optional FND/MTH/QIN refresh -> noise and measurement -> 3-bit repetition -> stabiliser/CSS -> syndrome/decoder -> surface and QLDPC -> choose hardware noise model -> logical gates/resource estimation -> reproducible advanced paper. The currently staged QEC 29-notebook collection is a seed, not a complete published doctorate.

### Researcher: Semiconductor quantum computers

QM/statistics -> Hubbard/spin qubits -> dots/donors/circuit control -> silicon gates/readout -> noise/leakage/transport -> QEC → native compiled gates -> full-stack QRE -> paper validation. They **need not take neutral-atom analogue tutorials** except as comparative electives.

### Researcher: Quantum financial engineering

FIN-00 through FIN-06 as the *main curriculum* -> classical measured baseline -> QAL/CIR/QML as needed -> FIN-07 quantum candidates -> full QRE/dequantisation -> FIN-08 capstone. This remains a standard independent pathway even if the user has no prior quantum programming.

### Researcher: Nuclear/Hamiltonian simulation

NHEP-00/01/02 -> SIM/HPC -> NHEP-03/04 -> choose trapped-ion or neutral-atom analogue branch *or* gate-based superconducting/digital branch -> QEC as needed -> measured accuracy/resource/uncertainty comparison -> reproduction.

### Researcher: Quantum CFD

NUM/PDE -> CFD-00–04 -> introductory QAL HHL -> CFD-05–06 -> QRE and I/O checks -> independent benchmark.

### Researcher: Photonic computing

Classical laser/optical bench -> field propagation and nonlinear optics -> photon sources/detectors -> DV **or** CV branch -> QKD/teleportation/fusion/GKP -> loss/time/energy/QRE -> hardware-specific experiment.

## 10. Cross-cutting science and evidence rules

1. Specify the **same problem and scientific observables**, units, initial conditions and tolerances before cross-modality comparisons.
2. Always publish strongest feasible relevant **classical CPU, MPI/GPU, numerical, ML and quantum-inspired baselines**; record if quantum has no advantage.
3. Separate ideal algorithmic queries, compiled native operations, circuit-level noise, logical resource projections, wall-time/queue, wall-plug energy, hardware billing and scientific error.
4. Separate **classically simulated**, **hardware-calibrated**, **experimentally run**, and **hypothetical future FT** results.
5. Reproducible runner code and QA belong to \`quantum-workflows\`; Jupyter login/enrolment to \`quantum-platform\`; durable agent plan to ACP; infrastructure scheduling to Slurm/GitOps.
6. Keep teaching assessments instructor-reviewable; do not claim student completion without evidence. Citation/library records must be correctable and human verified.
7. Vendor-neutral scientific intent with vendor-native implementation; do not manufacture common hardware functionality that doesn't exist.
8. Software environments are separately versioned/pinned where needed. Preserve immutable notebook revision and result provenance; do not silently rewrite approved courses.
9. Support low-bandwidth and non-QPU access for African learners; broaden to EOSC/AOSP/GOSC-aligned FAIR metadata and data federation only with validated agreements.
10. Make advanced tracks deep enough for MSc/PhD work, while preserving small quickstart examples for outreach.

## 11. Implementation order that does not block the platform MVP

| Gate | Actual intended change | Acceptance |
| --- | --- | --- |
| P0 / M4a | Separate ACP destructive PostgreSQL cross-client continuity | Recorded observed evidence, automatic conformance and second-user denial; never mark done from proposal |
| P0 / R1 | Quantum Platform -> JupyterHub -> one existing Bell notebook -> NFS resume | User executes/edits/saves, workbench replaced, same content and access controls survive |
| P1 | Review/import only the small \`labs/02\` foundation subset *needed* for R1–R3; keep others independently staged | Pin environment; isolated kernel; semantic numerical tests; scientific review |
| P1 | Adopt this master curriculum as the canonical **future academy catalogue** and add course/pathway schema, ability/goal entrypoints | Every named first-class subject has a track ID, prerequisites, progress/evidence contract, source status |
| P2 | Build dedicated financial engineering Stage 00–03 and quantum algorithms/CIR/QML core in small focused PRs; initiate HPC/PDE and NHEP references | one complete classical→HPC→quantum pilot and teacher review |
| P3 | Expand all modality-specific hands-on tracks, 29 QEC and 34 photonics validation, cross-track capstones and QRE | reproducible modality-specific experiments |
| P4 | PI studio and federated publication of verified curricula; QPU and scientific-workflow orchestration | signed-off research cohort and resource/provenance reports |

Prefer introducing one vertically complete well-tested **learning pathway** over importing dozens of notebooks as disconnected demos. Do not broaden the ACP M4a closeout criterion.

## 12. Cross-repository crosswalk and long-term research ambition

- **\`quantum-workflows\`**: this comprehensive catalogue, executable science, curricula, portable runners, benchmark/provenance.
- **\`quantum-platform\`**: research learner/cohort/PI experiences, catalogue view, assessments and identity.
- **\`agent-control-plane\`**: durable guided research conversations, projects and evidence-based curriculum proposals/reviews; model/harness replaceable.
- **\`infra-hpc-qc-k8s\`**: policy-aware deployment/operating environment for Jupyter, Slurm, GPU/QPU access and observability.

The long-term goal is a continental African research pipeline (and possible EOSC/AOSP/GOSC interoperability) that brings novices to research-ready competence and allows experienced PIs to curate and review specialisms, rather than a vendor-catalogue portal or a one-size-fits-all course.

**Do not confuse this proposed scope with the necessarily narrow, testable PhD claim.** The PhD's central contribution should remain resource-aware, verifiable, modality-aware quantum-centric supercomputing with focused scientific application case studies. Broader courses and domains form a national research/teaching programme, with individually reviewed published milestones.
