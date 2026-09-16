import json

import pytest

from quantum_workflows.hello import bell_circuit, run_hello


def test_bell_circuit_shape() -> None:
    circuit = bell_circuit()
    assert circuit.num_qubits == 2
    assert circuit.count_ops()["h"] == 1
    assert circuit.count_ops()["cx"] == 1


def test_local_handshake_writes_a_completed_manifest(tmp_path) -> None:
    summary, directory = run_hello(executor="aer", shots=512, output=tmp_path, seed=7)
    manifest = json.loads((directory / "manifest.json").read_text())
    assert summary["passed"]
    assert summary["bell_correlation"] > 0.95
    assert manifest["status"] == "completed"
    assert manifest["quantum"]["shots"] == 512
    assert len(manifest["circuits"]) == 2


def test_failed_acceptance_is_recorded_as_failed(tmp_path) -> None:
    with pytest.raises(RuntimeError, match="below threshold"):
        run_hello(
            executor="aer",
            shots=64,
            output=tmp_path,
            seed=7,
            minimum_correlation=1.1,
        )
    directory = next((tmp_path / "hello-ibm").iterdir())
    manifest = json.loads((directory / "manifest.json").read_text())
    assert manifest["status"] == "failed"
    assert (directory / "summary.json").exists()
