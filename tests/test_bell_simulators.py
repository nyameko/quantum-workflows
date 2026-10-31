"""Credential-free coverage of the Bell simulator integrations."""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace

import pytest

from quantum_workflows import executors
from quantum_workflows.hello import run_hello
from quantum_workflows.lightning import sample_bell


@pytest.mark.parametrize(
    ("executor", "backend"),
    [
        ("lightning-cpu", "lightning.qubit"),
        ("lightning-gpu", "lightning.gpu"),
    ],
)
def test_lightning_native_bell_counts(monkeypatch, executor, backend):
    selected = []

    def device(name, *, wires, shots, seed):
        selected.append((name, wires, shots, seed))
        return object()

    fake_qml = SimpleNamespace(
        device=device,
        qnode=lambda _device: lambda fn: fn,
        Hadamard=lambda **kwargs: None,
        CNOT=lambda **kwargs: None,
        counts=lambda *, wires: {"00": 16, "11": 16},
    )
    monkeypatch.setitem(sys.modules, "pennylane", fake_qml)
    counts, actual = sample_bell(executor=executor, shots=32, seed=7)
    assert counts == {"00": 16, "11": 16}
    assert actual == backend
    assert selected == [(backend, 2, 32, 7)]


def test_lightning_hello_emits_the_same_scientific_contract(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "quantum_workflows.lightning.sample_bell",
        lambda *, executor, shots, seed: ({"00": shots // 2, "11": shots // 2}, "lightning.qubit"),
    )
    summary, directory = run_hello(executor="lightning-cpu", shots=64, output=tmp_path, seed=11)
    manifest = json.loads((directory / "manifest.json").read_text())
    assert summary["passed"]
    assert summary["provider_job_id"] is None
    assert summary["bell_correlation"] == 1.0
    assert summary["backend"] == "lightning.qubit"
    assert manifest["status"] == "completed"
    assert manifest["quantum"]["provider"] == "local"
    assert manifest["runtime"]["executor"] == "lightning-cpu"
    assert len(manifest["circuits"]) == 1
    assert (directory / "data" / "counts.json").exists()


def test_lightning_rejects_remote_backend_override(tmp_path):
    with pytest.raises(ValueError, match="only supported"):
        run_hello(executor="lightning-cpu", shots=64, output=tmp_path, backend="ibm_example")


def test_aer_gpu_is_opt_in(monkeypatch):
    selected = []

    def fake_aer(circuits, *, shots, seed, gpu=False):
        selected.append((shots, seed, gpu))
        return executors.SampleBatch([], "aer-gpu", None, [])

    monkeypatch.setattr(executors, "_sample_aer", fake_aer)
    sample = executors.sample_circuits([], executor="aer-gpu", shots=100, seed=5)
    assert selected == [(100, 5, True)]
    assert sample.backend == "aer-gpu"


def test_aer_gpu_fails_if_not_supported(monkeypatch):
    class CpuOnlyBackend:
        def __init__(self, **kwargs):
            self.options = kwargs

        def available_devices(self):
            return ["CPU"]

    monkeypatch.setitem(sys.modules, "qiskit_aer", SimpleNamespace(AerSimulator=CpuOnlyBackend))
    with pytest.raises(RuntimeError, match="GPU is unavailable"):
        executors.sample_circuits([], executor="aer-gpu", shots=100, seed=5)
