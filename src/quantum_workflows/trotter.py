"""Trotterized transverse-field Ising dynamics reference workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.synthesis import SuzukiTrotter
from scipy.linalg import expm

from .artifacts import RunArtifacts
from .executors import sample_circuits


def ising_hamiltonian(qubits: int, coupling: float, field: float) -> SparsePauliOp:
    if qubits < 2:
        raise ValueError("the Ising chain requires at least two qubits")
    terms: list[tuple[str, list[int], float]] = []
    terms.extend(("ZZ", [i, i + 1], -coupling) for i in range(qubits - 1))
    terms.extend(("X", [i], -field) for i in range(qubits))
    return SparsePauliOp.from_sparse_list(terms, num_qubits=qubits)


def initial_neel_circuit(qubits: int) -> QuantumCircuit:
    circuit = QuantumCircuit(qubits, name="neel-state")
    for qubit in range(0, qubits, 2):
        circuit.x(qubit)
    return circuit


def trotter_circuit(
    hamiltonian: SparsePauliOp, time_value: float, trotter_steps: int
) -> QuantumCircuit:
    if trotter_steps < 1:
        raise ValueError("trotter_steps must be positive")
    circuit = initial_neel_circuit(hamiltonian.num_qubits)
    if time_value:
        synthesis = SuzukiTrotter(order=2, reps=trotter_steps, preserve_order=False)
        circuit.append(
            PauliEvolutionGate(hamiltonian, time=time_value, synthesis=synthesis), circuit.qubits
        )
    return circuit.decompose(reps=2)


def magnetization_operator(qubits: int) -> SparsePauliOp:
    return SparsePauliOp.from_sparse_list(
        [("Z", [qubit], 1.0 / qubits) for qubit in range(qubits)], num_qubits=qubits
    )


def magnetization_from_counts(counts: dict[str, int], qubits: int) -> float:
    shots = sum(counts.values())
    if not shots:
        raise ValueError("counts contain no shots")
    total = 0.0
    for bitstring, occurrences in counts.items():
        bits = bitstring.replace(" ", "").zfill(qubits)
        value = sum(1 if bit == "0" else -1 for bit in bits[-qubits:]) / qubits
        total += occurrences * value
    return total / shots


def run_trotter(
    *,
    executor: str,
    qubits: int,
    coupling: float,
    field: float,
    final_time: float,
    time_points: int,
    trotter_steps: int,
    shots: int,
    output: Path,
    backend: str | None = None,
    seed: int = 42,
) -> tuple[dict[str, Any], Path]:
    if qubits > 12:
        raise ValueError(
            "the exact-reference path is limited to 12 qubits; use the future scalable runner "
            "for larger simulations"
        )
    if time_points < 2:
        raise ValueError("time_points must be at least two")
    if final_time <= 0:
        raise ValueError("final_time must be positive")
    parameters = {
        "qubits": qubits,
        "coupling": coupling,
        "field": field,
        "final_time": final_time,
        "time_points": time_points,
        "trotter_steps": trotter_steps,
        "shots": shots,
        "backend_requested": backend,
        "seed": seed,
    }
    artifacts = RunArtifacts("trotterized-dynamics", output, parameters, executor)
    try:
        hamiltonian = ising_hamiltonian(qubits, coupling, field)
        observable = magnetization_operator(qubits)
        initial = Statevector.from_instruction(initial_neel_circuit(qubits))
        times = np.linspace(0.0, final_time, time_points)
        circuits = [trotter_circuit(hamiltonian, float(t), trotter_steps) for t in times]
        measured = []
        for circuit in circuits:
            measured_circuit = circuit.copy()
            measured_circuit.measure_all()
            measured.append(measured_circuit)

        sampled = sample_circuits(
            measured, executor=executor, shots=shots, backend_name=backend, seed=seed
        )
        hamiltonian_matrix = hamiltonian.to_matrix()
        rows = []
        for index, (time_value, circuit, counts) in enumerate(
            zip(times, circuits, sampled.counts, strict=True)
        ):
            trotter_state = Statevector.from_instruction(circuit)
            exact_state = Statevector(
                expm(-1j * float(time_value) * hamiltonian_matrix) @ initial.data
            )
            exact_m = float(np.real(exact_state.expectation_value(observable)))
            trotter_m = float(np.real(trotter_state.expectation_value(observable)))
            sampled_m = magnetization_from_counts(counts, qubits)
            rows.append(
                {
                    "index": index,
                    "time": float(time_value),
                    "exact_magnetization": exact_m,
                    "trotter_magnetization": trotter_m,
                    "sampled_magnetization": sampled_m,
                    "trotter_abs_error": abs(trotter_m - exact_m),
                    "sampling_abs_error": abs(sampled_m - trotter_m),
                }
            )

        for circuit in circuits:
            artifacts.add_circuit(circuit, stage="logical-trotter")
        for circuit in sampled.transpiled_circuits:
            artifacts.add_circuit(circuit, stage="transpiled-sampling")
        artifacts.write_csv("dynamics.csv", rows)
        artifacts.write_json("counts.json", sampled.counts, data=True)
        max_trotter_error = max(row["trotter_abs_error"] for row in rows)
        rms_trotter_error = float(np.sqrt(np.mean([row["trotter_abs_error"] ** 2 for row in rows])))
        summary = {
            "workflow": "trotterized-dynamics",
            "model": "open-boundary transverse-field Ising chain",
            "executor": executor,
            "backend": sampled.backend,
            "provider_job_id": sampled.job_id,
            "maximum_trotter_magnetization_error": max_trotter_error,
            "rms_trotter_magnetization_error": rms_trotter_error,
            "final": rows[-1],
        }
        artifacts.set_quantum_metadata(
            provider="local" if executor == "aer" else "ibm",
            backend=sampled.backend,
            job_id=sampled.job_id,
            shots_per_circuit=shots,
            circuits=len(circuits),
        )
        artifacts.finish(summary)
        return summary, artifacts.directory
    except Exception as exc:
        artifacts.fail(exc)
        raise
