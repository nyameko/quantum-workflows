"""M4d science skill seeds are inert, pinned-candidate references to existing qw commands."""

from __future__ import annotations

import json
from pathlib import Path

from quantum_workflows.cli import build_parser

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "catalog" / "agent-skills"


def test_seeded_skill_records_are_bounded_and_parseable() -> None:
    files = sorted(SKILLS.glob("*.json"))
    assert {p.name for p in files} == {"research-bell-aer.json", "research-cpu-smoke.json"}
    expected = {"research.bell-aer": "hello", "research.cpu-smoke": "cpu-smoke"}
    seen = set()
    for filename in files:
        item = json.loads(filename.read_text(encoding="utf-8"))
        assert item["id"] not in seen
        seen.add(item["id"])
        assert item["id"] in expected
        assert item["version"] == "0.1.0"
        assert item["status"] == "proposed"
        assert item["kind"] == "scientific_workflow_reference"
        assert item["source_path"].startswith("src/quantum_workflows/")
        assert (ROOT / item["source_path"]).is_file()
        if item["tutorial_path"] is not None:
            assert (ROOT / item["tutorial_path"]).is_file()
        assert item["required_capabilities"] == ["workflow:simulate:cpu"]
        assert item["requires_external_credentials"] is False
        assert item["execution_policy"] == {
            "remote_execution_enabled": False,
            "requires_approved_platform_submission": True,
            "human_review_required_to_enable": True,
        }
        assert item["entrypoint"]["cli"] == "qw"
        assert item["entrypoint"]["subcommand"] == expected[item["id"]]
        argv = [item["entrypoint"]["subcommand"], *item["entrypoint"]["fixed_arguments"]]
        assert all(isinstance(x, str) and x and "\\x00" not in x for x in argv)
        assert not any(x in {"ibm", "qrmi"} for x in argv)
        parsed = build_parser().parse_args(argv)
        assert parsed.command == expected[item["id"]]
        assert parsed.command == "cpu-smoke" or parsed.executor == "aer"
    assert seen == set(expected)
