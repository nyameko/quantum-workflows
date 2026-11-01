# Computational Photonics: table-top experiments to reproducible research

**Status: development / not a published or certified course.**
**Canonical teaching home:** Quantum Workflows. **Physics dependency:** PhotonicsLab `0.6.0a1` at `141258d308b11569b37628c003ace15e385fba3d` (pinned for N01–N03). **Runtime:** Python 3.14 Jupyter kernel, NumPy CPU. **GPU:** not required for foundational lessons.

## Learning contract

An eight-week course (~4 contact hours and 4–6 self-study hours per week), with an optional Python/complex-numbers bridge. Each notebook asks for (1) apparatus/observable, (2) physical state and units, (3) prediction before calculation, (4) readable first-principles algorithm where educational, (5) independent analytical/library comparison, (6) deliberate failure case, (7) real-lab apparatus, calibration and safety translation, and (8) parameter/provenance record and assessment. All students have a CPU completion path. A100/H200 jobs require authorised Quantum Platform allocation and are used only for genuinely large validated computations.

| ID | Wk | Work | Status |
| --- | --- | --- | --- |
| N01 | 1 | Fields, Gaussian waist, units, camera, FFT grid and clipping | **Implementation proposed here** |
| N02 | 1 | Fresnel and angular-spectrum diffraction; sampling, mesh and window checks | **Implementation proposed here** |
| N03 | 2 | Jones polarization, HWP/QWP, analyser and Stokes observables | **Implementation proposed here** |
| N04 | 2 | Mach–Zehnder/Michelson, optical-path carrier phase, splitters and coherence | Future |
| N05 | 3 | Gaussian q, lenses, ABCD and complex mode overlap | Future |
| N06 | 3 | *Guided:* 4f Fourier planes, SLM and diffraction orders | Future |
| N07 | 4 | Fabry–Perot spectra, linewidth, finesse and ringdown | Future |
| N08 | 4 | Stable resonators, Gouy phase and transverse mode families | Future |
| N09 | 5 | *Guided:* Fox–Li spatial eigenmodes and aperture loss | Future |
| N10 | 5 | *Guided:* pumping, four-level laser threshold and thermal lenses | Future |
| N11 | 6 | Photon counting, coherence and detector artefacts | Future |
| N12 | 6 | Bosonic modes, linear optical unitaries and HOM interference | Future |
| N13 | 7 | *Guided:* SPDC complex JSA, quadrature weights and heralded purity | Future |
| N14 | 7 | CPU→A100/H200 FFT scaling at equal physical accuracy | Future |
| N15 | 7 | Quantum Workflows provenance, Slurm retries and durable artifact execution | Future |
| N16 | 8 | Design capstone, independent reproduction and oral defense | Future |

Week 5 is a cavity-design studio using validated N07/N08, not a claim that detailed pumping is ready. N01–N03 do not submit Slurm jobs, invoke hardware drivers, or write production `RunArtifacts`; workflow registration will be a separate reviewed PR.

## Repository boundaries

- **PhotonicsLab:** validated sources, fields, physical optical components and numerical methods. Small reference algorithms are intentionally readable.
- **Quantum Workflows:** course notebooks, scientific runner/orchestration contracts, assessments and provenance.
- **Quantum Platform:** identity, access/quotas, Jupyter workbench and CPU/A100/H200 scheduling and results.
- **Agent Control Plane:** persistent guided-learning context; never authoritative for measurements or grading.
- **infra-hpc-qc-k8s:** scheduled compute, pinned images, network/storage and operational safeguards.

Never reimplement an entire maintained engine: compare or integrate HCIPy/LightPipes/Diffractio for wave propagation, Finesse 3 for interferometers/cavities, QuTiP for open quantum states, Perceval for discrete-variable photonic circuits, SPDCalc for SPDC, and specialist GPU backends after *measured* equivalence. Adapters are not yet implemented; labels such as `GPU enabled`, `nonlinear solver` or `SPDC supported` must never be used for N01–N03.

## Scientific non-negotiables

- `Field` is a classical power-normalised two-component coherent Jones envelope in √W/m, not a physical V/m electric field or a quantum Fock state.
- `FreeSpace` removes homogeneous carrier phase: branching interferometers and cavities **must** restore relative optical path phase before recombining fields; a naive sum of independently propagated envelopes is wrong.
- Power equality alone never certifies sampling or boundary accuracy. Verify aperture clipping, grid spacing, edge power and independent convergence.
- SPDC heralded purity requires the *complex* weighted joint spectral amplitude, including phase and quadrature weights; a plot of joint spectral intensity is insufficient.
- An ideal four-level gain model is not a predictive Yb:YAG model by substituting its coefficients. Distinguish model regime and material data.
- No notebook starts hardware control or GPU allocation without explicit student/user action and platform authorisation.

## Reading spine

**Goodman** — *Introduction to Fourier Optics*; **Saleh & Teich** — *Fundamentals of Photonics*; **Siegman** — *Lasers*; **Mandel & Wolf** — *Optical Coherence and Quantum Optics*; **Boyd** — *Nonlinear Optics*; **Gerry & Knight** — *Introductory Quantum Optics*.

Relevant primary anchors: Kogelnik & Li (1966) https://doi.org/10.1364/AO.5.001550; Fox & Li (1961) https://doi.org/10.1002/j.1538-7305.1961.tb01625.x; Matsushima & Shimobaba (2009) https://doi.org/10.1364/OE.17.019662; Glauber (1963) https://doi.org/10.1103/PhysRev.130.2529; HOM (1987) https://doi.org/10.1103/PhysRevLett.59.2044; Law et al. (2000) https://doi.org/10.1103/PhysRevLett.84.5304; Mosley et al. (2008) https://doi.org/10.1103/PhysRevLett.100.133601.

Use original code/plots and cite textbooks; do not redistribute copyrighted figures.

## Reviewer acceptance and next gate

Run three notebooks from a fresh Python 3.14 kernel with the **pinned exact source revision** above. Confirm all analytical assertions pass, no remote credentials or GPU calls, no stored notebook outputs and matching course metadata. Then pilot with learners. No guarantee of published readiness follows automatically from CI.

After N01–N03: add a phase-aware port/splitter primitive and independent N04 Mach–Zehnder energy/phase acceptance tests in PhotonicsLab before an interferometry notebook is accepted. Keep N05–N13 as independent scientific reviewable increments, not a single enormous implementation.
