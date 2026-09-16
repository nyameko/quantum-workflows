# 3. Sample-based quantum diagonalization

## Why SQD is the first flagship QCSC workflow

Sample-based quantum diagonalization (SQD) is genuinely heterogeneous. A QPU or simulator samples
configurations with useful support; classical computing performs symmetry recovery, Hamiltonian
projection and eigensolving in selected subspaces. The quantum stage is not presented as an
isolated replacement for the entire chemistry calculation.

```text
CPU chemistry preparation
  PySCF integrals + CCSD amplitudes
              │
              ▼
quantum circuit preparation
  ffsim LUCJ ansatz
              │
              ▼
sampler
  local statevector / IBM / QRMI
              │
              ▼
CPU postprocessing
  configuration recovery + selected CI
              │
              ▼
energy, error, occupancies, provenance
```

## Local N₂ baseline

Install the scientific extras:

```bash
.venv/bin/python -m pip install -e '.[sqd]'
```

Run the default N₂/STO-6G workflow:

```bash
.venv/bin/qw sqd \
  --executor statevector \
  --shots 20000 \
  --samples-per-batch 1000 \
  --num-batches 3 \
  --max-iterations 5 \
  --max-dim 50
```

The active space freezes two core orbitals, leaving 8 spatial orbitals / 16 qubits and 10 active
electrons. The workflow calculates an exact CASCI reference locally, allowing the reported SQD
energy error to be interpreted directly.

The output includes:

- `summary.json` — SCF, CCSD, CASCI and SQD energies; validity fraction; final error;
- `data/samples.json` — raw sampled bitstrings for reproducible postprocessing research;
- `data/iterations.csv` — energy and subspace dimension per recovery iteration/batch;
- `data/orbital-occupancies.csv` — alpha, beta and total occupancy;
- `manifest.json` — versions, circuits, target, inputs and artifact hashes.

## What configuration recovery does

The molecular Hamiltonian conserves particle number and spin projection. In an ideal run, each
sample therefore has the expected alpha and beta Hamming weights. Noise can violate those
symmetries. Throwing every invalid sample away loses signal; recovery probabilistically repairs
configurations using evolving orbital-occupancy estimates, samples subspaces, diagonalizes the
projected Hamiltonian, and iterates.

Compare:

```text
valid_configuration_fraction
uniform_random_valid_fraction
```

The comparison helps establish that the ansatz/hardware samples meaningful support even when the
absolute valid fraction is modest.

## Direct hardware

Install both optional groups and run:

```bash
.venv/bin/python -m pip install -e '.[ibm,sqd]'
.venv/bin/qw sqd --executor ibm --shots 20000
```

The workflow inspects the IBM processor family to select the ffsim LUCJ connectivity convention:
heavy-hex for Heron and square for Nighthawk. If a new family is not known, execution stops and asks
for an explicit `--connectivity`; silently guessing a layout would invalidate comparisons.

This workload consumes materially more QPU time than the Bell handshake. Validate locally first,
inspect the transpiled circuit, and begin with the small teaching active space.

## QRMI/Slurm execution

```bash
sbatch --gres=qpu:1 --qpu=ibm_resource_name slurm/sqd.sbatch
```

The initial script executes all phases in one allocation for integration simplicity. The production
QCSC form will split preparation, QPU sampling and postprocessing into dependent jobs:

```text
prepare job ─afterok─► quantum job ─afterok─► postprocess job
```

That split is required before assigning H200 or large MPI resources: remote provider queue time must
not hold scarce classical accelerators idle.

## Scaling beyond the teaching example

The next reference is N₂/cc-pVDZ (26 spatial orbitals / 52 qubits), aligned with current IBM QRMI
educational material. Classical postprocessing then becomes a serious HPC stage. The target stack is:

```text
QPU samples
    │
    ▼
qiskit-addon-sqd-hpc
    │
MPI + OpenMP + SBD eigensolver
    │
    ▼
distributed subspace diagonalization
```

We will integrate and parameterize the maintained upstream implementation rather than reimplementing
the eigensolver. Follow-on SKQD will construct time-evolved Krylov states using the Trotter workflow,
sample them, then diagonalize in the resulting subspace.

## Interpretation and limits

- A low energy error for a small noiseless case validates implementation, not quantum advantage.
- SQD accuracy depends on ansatz support, noise, samples, subspace size, recovery settings and the
  classical solver.
- The variational energy should be interpreted alongside the exact/reference method and active-space
  definition.
- Result comparisons are meaningful only with source/image digests, dependency versions, circuit
  fingerprints, target calibration context and sampling parameters.

## Exercises

1. Sweep `samples-per-batch` and plot energy error against subspace dimension and CPU time.
2. Inject bit-flip noise locally and quantify recovery improvement over strict postselection.
3. Compare one and four LUCJ repetitions at fixed shots.
4. Separate sample generation from postprocessing and reuse one sample set across solver settings.
5. Repeat through direct IBM and QRMI paths and confirm that algorithm results match while resource
   lifecycle/provenance differs.
