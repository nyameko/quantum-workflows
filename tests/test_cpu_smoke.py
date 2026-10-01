import json

import pytest

from quantum_workflows.cpu_smoke import run_cpu_smoke


def test_cpu_smoke_writes_completed_manifest(tmp_path) -> None:
    summary, directory = run_cpu_smoke(iterations=1000, output=tmp_path)

    manifest = json.loads((directory / "manifest.json").read_text())
    persisted = json.loads((directory / "summary.json").read_text())

    assert summary["passed"] is True
    assert persisted["checksum"] == summary["checksum"]
    assert manifest["workflow"] == "cpu-smoke"
    assert manifest["status"] == "completed"
    assert manifest["runtime"]["executor"] == "cpu"


def test_cpu_smoke_rejects_non_positive_iterations(tmp_path) -> None:
    with pytest.raises(ValueError, match="positive"):
        run_cpu_smoke(iterations=0, output=tmp_path)
