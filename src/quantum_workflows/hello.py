"""IBM-compatible Bell-state handshake."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from qiskit import QuantumCircuit

from .artifacts import RunArtifacts
from .executors import sample_circuits


def bell_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2, name="bell-handshake")
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    return circuit


def run_hello(
    *,
    executor: str,
    shots: int,
    output: Path,
    backend: str | None = None,
    seed: int = 42,
    minimum_correlation: float = 0.70,
) -> tuple[dict[str, Any], Path]:
    parameters = {
        "shots": shots,
        "backend_requested": backend,
        "seed": seed,
        "minimum_correlation": minimum_correlation,
    }
    artifacts = RunArtifacts("hello-ibm", output, parameters, executor)
    try:
        circuit = bell_circuit()
        artifacts.add_circuit(circuit, stage="logical")
        sampled = sample_circuits(
            [circuit], executor=executor, shots=shots, backend_name=backend, seed=seed
        )
        artifacts.add_circuit(sampled.transpiled_circuits[0], stage="transpiled")
        counts = sampled.counts[0]
        observed = sum(counts.values())
        correlated = counts.get("00", 0) + counts.get("11", 0)
        correlation = correlated / observed if observed else 0.0
        passed = correlation >= minimum_correlation
        summary = {
            "workflow": "hello-ibm",
            "executor": executor,
            "backend": sampled.backend,
            "provider_job_id": sampled.job_id,
            "counts": counts,
            "shots_observed": observed,
            "bell_correlation": correlation,
            "minimum_correlation": minimum_correlation,
            "passed": passed,
        }
        artifacts.set_quantum_metadata(
            provider="local" if executor == "aer" else "ibm",
            backend=sampled.backend,
            job_id=sampled.job_id,
            shots=observed,
        )
        artifacts.write_json("counts.json", counts, data=True)
        if not passed:
            artifacts.write_json("summary.json", summary)
            raise RuntimeError(
                f"Bell correlation {correlation:.3f} is below threshold {minimum_correlation:.3f}"
            )
        artifacts.finish(summary)
        return summary, artifacts.directory
    except Exception as exc:
        artifacts.fail(exc)
        raise
