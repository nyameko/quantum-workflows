# 1. IBM QPU handshake

## Objective

Prove the complete execution and artifact path with the smallest scientifically meaningful circuit:
a Bell pair. This is an integration acceptance test, not a performance benchmark.

The circuit prepares

$$|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt{2}.$$

An ideal sampler returns only `00` and `11`. Hardware noise can produce `01` and `10`, so the
workflow checks the observed correlated fraction against a configurable threshold.

## Local acceptance test

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/qw hello --executor aer --shots 1024
```

Expected properties:

- `passed` is `true`;
- `bell_correlation` is close to 1;
- `manifest.json` contains logical and transpiled circuit fingerprints;
- `data/counts.json` contains approximately equal `00` and `11` populations.

The random seed makes the local acceptance run reproducible, not mathematically identical across
every future simulator implementation.

## Direct IBM Quantum Compute Service

Install the optional client:

```bash
.venv/bin/python -m pip install -e '.[ibm]'
```

Save the API key using Qiskit's account store as documented by IBM. Do this only on a trusted
machine, never in the repository or container image. Then run:

```bash
.venv/bin/qw hello --executor ibm --shots 1024
```

The executor selects the least-busy operational non-simulator with at least two qubits. To make a
controlled comparison, pass `--backend NAME`.

The direct path follows the Qiskit pattern:

1. construct the circuit;
2. obtain the backend;
3. transpile to the backend's instruction-set architecture;
4. submit with `SamplerV2` in job mode;
5. retrieve counts and validate correlations.

Job mode is deliberate: Open Plan accounts do not support sessions, and one Bell circuit does not
benefit from a reserved session.

## Slurm + QRMI/SPANK

After the infrastructure track installs and configures QRMI/SPANK:

```bash
sbatch --gres=qpu:1 --qpu=ibm_resource_name slurm/hello-ibm.sbatch
```

The plugin owns allocation/session lifecycle and injects:

```text
QRMI_JOB_QPU_RESOURCES
QRMI_JOB_QPU_TYPES
```

The `qrmi` executor discovers that resource, gets its compilation target, transpiles, and submits
with QRMI's Qiskit-compatible `SamplerV2`. It must not call `release()` on a session owned by the
SPANK plugin.

## Acceptance criteria

The facility milestone is accepted when:

- a Slurm job requests a logical QPU with `--gres=qpu:1 --qpu=...`;
- the job discovers the allocation without a hardcoded physical backend;
- a real provider job ID is present in the result manifest;
- the Bell correlation passes the selected hardware threshold;
- no token appears in Git, `scontrol show job`, stdout/stderr, or result artifacts;
- the resource/session is released when the Slurm job ends, including failure paths.

Do not lower the correlation threshold merely to make a failing device run green. Retain the raw
counts and investigate calibration, layout, transpilation and readout mitigation separately.
