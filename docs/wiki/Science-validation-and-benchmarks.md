# Scientific quality, comparison benchmarks and uncertainty

## Execution success is not scientific correctness

A Slurm exit code `0:0`, non-empty result file or successful GPU kernel is insufficient evidence of correct physics, convergence or research advantage. Maintain an independent mathematical oracle where available and a reproducible classical baseline. For quantum simulation, statevector/tensor-network/exact-diagonalization references are useful at small system sizes; for chemistry, compare against published, properly configured reference energies and clearly identify basis-set and approximation errors.

## Verification layers

| Layer | What it establishes | What it does not establish |
|---|---|---|
| Unit test | implementation matches a known local behavior | physical truth outside tested regime |
| Analytical limit | expected special-case behavior | convergence for hard large cases |
| Mesh/time/shot sweep | numerical sensitivity/convergence | correctness of omitted physics |
| Independent implementation | reduces correlated code defects | complete physical validation |
| Real hardware experiment | observed provider outcome | transferable quantum advantage |
| Performance benchmark | timing/resource result for specified hardware | superiority for all workloads |

## Experimental design

Write a problem statement, input units, Hamiltonian/equations, boundary conditions, classical solver, quantum encoding, observable, error budget and stopping criterion **before** running. Separate shot noise from algorithmic approximation, hardware noise, optimizer variation and finite precision. Pin seeds, library versions, image digest, job resources, simulator method, calibration snapshot and raw results. Report negative findings as well as successful plots.

For HPC scaling, measure wall time, parallel efficiency, memory, communication and energy if trustworthy; never compare an H200 GPU result to a single-core CPU as if both consumed equivalent resources. For QPU benchmarks report compile depth, two-qubit gate count, transpilation, mitigation overhead, queue time and shots.

## Research provenance

An `artifact.manifest` should link input parameters and hashes to outputs, backend and run IDs. Platform job ID, ACP agent task UUID, provider QPU run ID and Quantum Workflows result ID are correlated but not interchangeable.

Sources: [artifacts code](https://github.com/nyameko/quantum-workflows/blob/main/src/quantum_workflows/artifacts.py), [Trotter reference](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/02-TROTTERIZED-DYNAMICS.md), [SQD science reference](https://github.com/nyameko/quantum-workflows/blob/main/docs/tutorials/03-SAMPLE-BASED-QUANTUM-DIAGONALIZATION.md).