import json

from quantum_workflows.artifacts import RunArtifacts


def test_manifest_uses_an_environment_allowlist(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DO_NOT_LEAK_THIS_TOKEN", "secret-value")
    artifacts = RunArtifacts("test", tmp_path, {"safe": True}, "unit")
    artifacts.finish({"ok": True})
    raw = (artifacts.directory / "manifest.json").read_text()
    manifest = json.loads(raw)
    assert "secret-value" not in raw
    assert manifest["status"] == "completed"
