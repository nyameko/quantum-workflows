"""M4d resource references are inert; they cannot execute SDKs or claim job permissions."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "catalog" / "agent-skills"


def test_review_candidates_point_to_existing_sources_without_execution_entrypoints() -> None:
    files = sorted(SKILLS.glob("*.json"))
    assert {p.name for p in files} == {"research-bell-aer.json", "research-cpu-smoke.json"}
    expected = {
        "learning.quantum-foundations": "jupyter_notebook",
        "reference.cpu-smoke-provenance": "python_source",
    }
    seen = set()
    for filename in files:
        item = json.loads(filename.read_text(encoding="utf-8"))
        assert item["id"] not in seen
        seen.add(item["id"])
        assert item["id"] in expected
        assert item["version"] == "0.2.0"
        assert item["status"] == "proposed"
        assert item["resource"]["type"] == expected[item["id"]]
        assert (ROOT / item["resource"]["path"]).is_file()
        assert item["required_capabilities"] == ["resource:read"]
        assert item["requires_external_credentials"] is False
        assert "entrypoint" not in item
        assert "fixed_arguments" not in item
        assert item["execution_policy"] == {
            "automatic_code_execution": False,
            "remote_execution_enabled": False,
            "human_review_required_to_enable": True,
        }
        if item["resource"]["type"] == "jupyter_notebook":
            notebook = json.loads((ROOT / item["resource"]["path"]).read_text())
            assert notebook["cells"]
            assert any(cell["cell_type"] == "markdown" for cell in notebook["cells"])
            assert any(cell["cell_type"] == "code" for cell in notebook["cells"])
            assert (
                ROOT / item["resource"]["environment_requirements"]
            ).is_file()
            assert item["resource"]["upstream_sdks"] == ["qiskit", "qiskit-aer"]
    assert seen == set(expected)
