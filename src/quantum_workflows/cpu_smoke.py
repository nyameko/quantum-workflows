"""Credential-free CPU smoke workflow for platform-to-Slurm validation."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from .artifacts import RunArtifacts


def run_cpu_smoke(*, iterations: int, output: Path) -> tuple[dict[str, Any], Path]:
    if iterations < 1:
        raise ValueError("iterations must be positive")

    parameters = {"iterations": iterations}
    artifacts = RunArtifacts("cpu-smoke", output, parameters, "cpu")

    try:
        started = time.perf_counter()
        checksum = sum((index * index) % 104729 for index in range(iterations))
        elapsed = time.perf_counter() - started

        summary = {
            "workflow": "cpu-smoke",
            "executor": "cpu",
            "iterations": iterations,
            "checksum": checksum,
            "elapsed_seconds": round(elapsed, 6),
            "passed": checksum >= 0,
        }
        artifacts.finish(summary)
        return summary, artifacts.directory
    except Exception as exc:
        artifacts.fail(exc)
        raise
