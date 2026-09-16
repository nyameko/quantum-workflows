import csv
import json

import pytest
from qiskit.quantum_info import Statevector

from quantum_workflows.trotter import (
    initial_neel_circuit,
    ising_hamiltonian,
    magnetization_from_counts,
    run_trotter,
    trotter_circuit,
)


def test_ising_hamiltonian_term_count() -> None:
    hamiltonian = ising_hamiltonian(4, coupling=1.0, field=0.7)
    assert len(hamiltonian) == 7


def test_zero_time_is_the_initial_state() -> None:
    hamiltonian = ising_hamiltonian(4, 1.0, 0.7)
    evolved = trotter_circuit(hamiltonian, 0.0, 4)
    assert Statevector.from_instruction(evolved).equiv(
        Statevector.from_instruction(initial_neel_circuit(4))
    )


def test_magnetization_from_counts() -> None:
    assert magnetization_from_counts({"0000": 10}, 4) == 1.0
    assert magnetization_from_counts({"1111": 10}, 4) == -1.0
    assert magnetization_from_counts({"0101": 10}, 4) == 0.0


def test_small_trotter_run(tmp_path) -> None:
    summary, directory = run_trotter(
        executor="aer",
        qubits=2,
        coupling=1.0,
        field=0.7,
        final_time=0.5,
        time_points=3,
        trotter_steps=2,
        shots=512,
        output=tmp_path,
        seed=5,
    )
    rows = list(csv.DictReader((directory / "data" / "dynamics.csv").open()))
    manifest = json.loads((directory / "manifest.json").read_text())
    assert len(rows) == 3
    assert summary["maximum_trotter_magnetization_error"] >= 0
    assert manifest["status"] == "completed"
    assert manifest["quantum"]["circuits"] == 3


def test_invalid_chain_size() -> None:
    with pytest.raises(ValueError, match="at least two"):
        ising_hamiltonian(1, 1.0, 0.7)


def test_exact_reference_has_a_safe_size_limit(tmp_path) -> None:
    with pytest.raises(ValueError, match="limited to 12 qubits"):
        run_trotter(
            executor="aer",
            qubits=13,
            coupling=1.0,
            field=0.7,
            final_time=1.0,
            time_points=2,
            trotter_steps=1,
            shots=16,
            output=tmp_path,
        )
