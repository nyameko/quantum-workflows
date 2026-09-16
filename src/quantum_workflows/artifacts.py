"""Structured, redacted result artifacts shared by every workflow."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _git_value(*args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return None


def _package_versions() -> dict[str, str]:
    names = (
        "quantum-workflows",
        "qiskit",
        "qiskit-aer",
        "qiskit-ibm-runtime",
        "qrmi",
        "ffsim",
        "pyscf",
        "qiskit-addon-sqd",
        "numpy",
        "scipy",
    )
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            continue
    return versions


def circuit_fingerprint(circuit: Any) -> str:
    """Return a stable-enough SHA-256 for comparing circuit artifacts within a run."""
    try:
        from qiskit import qasm3

        payload = qasm3.dumps(circuit).encode()
    except Exception:  # pragma: no cover - fallback for unsupported instructions
        payload = repr(circuit).encode()
    return hashlib.sha256(payload).hexdigest()


@dataclass
class RunArtifacts:
    """Own one workflow result directory and its provenance manifest."""

    workflow: str
    root: Path
    parameters: Mapping[str, Any]
    executor: str
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    started_at: str = field(default_factory=_utc_now)
    _started_monotonic: float = field(default_factory=time.monotonic, repr=False)
    manifest: dict[str, Any] = field(init=False)

    def __post_init__(self) -> None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        self.directory = self.root / self.workflow / f"{stamp}-{self.run_id}"
        self.data_directory = self.directory / "data"
        self.data_directory.mkdir(parents=True, exist_ok=False)
        self.manifest = {
            "schema_version": "1.0",
            "experiment_id": self.run_id,
            "workflow": self.workflow,
            "status": "running",
            "started_at": self.started_at,
            "source": {
                "repository": "https://github.com/nyameko/quantum-workflows",
                "commit": _git_value("rev-parse", "HEAD"),
                "dirty": bool(_git_value("status", "--porcelain")),
            },
            "software": {
                "python": sys.version.split()[0],
                "packages": _package_versions(),
            },
            "runtime": {
                "executor": self.executor,
                "hostname": socket.gethostname(),
                "platform": platform.platform(),
                "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
                "slurm_cluster": os.environ.get("SLURM_CLUSTER_NAME"),
                "slurm_partition": os.environ.get("SLURM_JOB_PARTITION"),
                "qrmi_resources": os.environ.get("QRMI_JOB_QPU_RESOURCES"),
                "qrmi_types": os.environ.get("QRMI_JOB_QPU_TYPES"),
            },
            "parameters": dict(self.parameters),
            "quantum": {},
            "circuits": [],
            "timings_seconds": {},
            "artifacts": [],
        }
        self.write_manifest()

    def add_circuit(self, circuit: Any, *, stage: str) -> None:
        self.manifest["circuits"].append(
            {
                "stage": stage,
                "hash": circuit_fingerprint(circuit),
                "qubits": circuit.num_qubits,
                "depth": circuit.depth(),
                "operations": dict(circuit.count_ops()),
            }
        )

    def set_quantum_metadata(self, **values: Any) -> None:
        self.manifest["quantum"].update(values)
        self.write_manifest()

    def write_json(self, name: str, value: Any, *, data: bool = False) -> Path:
        path = (self.data_directory if data else self.directory) / name
        path.write_text(json.dumps(value, indent=2, sort_keys=True, default=_json_default) + "\n")
        self._record_artifact(path)
        return path

    def write_csv(self, name: str, rows: Iterable[Mapping[str, Any]]) -> Path:
        rows = list(rows)
        if not rows:
            raise ValueError("cannot write an empty CSV")
        path = self.data_directory / name
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        self._record_artifact(path)
        return path

    def finish(self, summary: Mapping[str, Any]) -> None:
        self.write_json("summary.json", summary)
        self.manifest["status"] = "completed"
        self.manifest["finished_at"] = _utc_now()
        self.manifest["timings_seconds"]["total"] = round(
            time.monotonic() - self._started_monotonic, 6
        )
        self.write_manifest()

    def fail(self, error: BaseException) -> None:
        self.manifest["status"] = "failed"
        self.manifest["finished_at"] = _utc_now()
        self.manifest["error"] = {"type": type(error).__name__, "message": str(error)}
        self.manifest["timings_seconds"]["total"] = round(
            time.monotonic() - self._started_monotonic, 6
        )
        self.write_manifest()

    def write_manifest(self) -> None:
        path = self.directory / "manifest.json"
        path.write_text(
            json.dumps(self.manifest, indent=2, sort_keys=True, default=_json_default) + "\n"
        )

    def _record_artifact(self, path: Path) -> None:
        relative = path.relative_to(self.directory)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        item = {"path": str(relative), "sha256": digest, "bytes": path.stat().st_size}
        artifacts = self.manifest["artifacts"]
        artifacts[:] = [entry for entry in artifacts if entry["path"] != str(relative)]
        artifacts.append(item)
        self.write_manifest()


def _json_default(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "tolist"):
        return value.tolist()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value).__name__}")
