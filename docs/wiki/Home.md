# Quantum Workflows wiki

**Quantum Workflows** is the scientific notebook, runner, curriculum and provenance layer of the hybrid quantum-centric supercomputing environment. It is not the user identity provider, Kubernetes/Slurm scheduler or Agent Control Plane.

**Audience:** first-time students, domain researchers, scientific software engineers, curriculum authors and advanced HPC/QPU users. **Source basis:** 4 November 2026, `main`. Distinguish committed runnable content from staged educational material and the multi-year proposed curriculum.

## Start here

| Goal | Guide |
|---|---|
| Install and run a first credential-free experiment | [Getting started](Getting-started.md) |
| Find an education or specialization track | [Academy and learning paths](Academy-and-learning-paths.md) |
| Run Bell, Ising, SQD and CPU smoke | [Reference experiments](Reference-experiments.md) |
| Use notebooks, Slurm, GPU or an authorised QPU | [Execution environments](Execution-environments.md) |
| Interpret results and reproduce them | [Scientific provenance](Scientific-provenance.md) |
| Inspect the code and develop new runners | [Developer guide](Developer-guide.md) |
| Integrate with portal/ACP and PhotonicsLab | [Ecosystem integration](Ecosystem-integration.md) |
| Resolve import/runtime/physics errors | [Troubleshooting](Troubleshooting.md) |
| Understand sensitive data and remote costs | [Security and responsible science](Security-and-responsible-science.md) |
| Contribute a validated notebook or benchmark | [Contributing](Contributing.md) |

## Current scope

The repository contains `qw` reference runners for `cpu-smoke`, `hello` (Bell), `trotter` (four-qubit default transverse-field Ising) and `sqd` (N₂ sample-based diagonalization). It also contains an introductory quantum computing lab and three committed computational photonics notebooks (N01–N03). The extensive planned academy is **not** equivalent to a full implemented collection of notebooks.

See [README](https://github.com/nyameko/quantum-workflows/blob/main/README.md), [scientific architecture](https://github.com/nyameko/quantum-workflows/blob/main/docs/ARCHITECTURE.md), [quick start](https://github.com/nyameko/quantum-workflows/blob/main/docs/QUICK_START.md) and [academy roadmap](https://github.com/nyameko/quantum-workflows/blob/main/docs/MASTER-ACADEMY-AND-RESEARCH-TRACKS.md).

## Guide discovery and support

[Guide integration, issue routing and safe agent retrieval](Guide-assistance.md) · [machine-readable page index](guide-index.json). Neither documentation nor its index grants resource permissions.


## Detailed scientific engineering

- [Slurm runner contract](Slurm-runner-contract.md)
- [Quantum SDK and executor matrix](Quantum-SDK-and-executor-matrix.md)
- [Research curriculum design](Research-curriculum-design.md)
- [Science validation and benchmarks](Science-validation-and-benchmarks.md)
- [Notebook environments and reproducibility](Notebook-environments-and-reproducibility.md)
