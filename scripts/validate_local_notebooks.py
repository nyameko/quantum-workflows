#!/usr/bin/env python3
"""Execute committed intro Qiskit notebooks in isolated, credential-free CPU kernels.

Requires Python 3.14, the quantum-workflows notebook extra, nbformat and nbclient.
This script is intentionally not an acceptance test for NVIDIA GPU or QPU access.
"""
from __future__ import annotations

import ast
import os
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb",
    "labs/01-intro-quantum-computing/02-bell-cpu-gpu-qpu.ipynb",
)


def validate_cpu_only(notebook: nbformat.NotebookNode, name: str) -> None:
    """Refuse to execute the Bell lesson if its defaults changed to remote/GPU."""
    if name != "02-bell-cpu-gpu-qpu.ipynb":
        return
    values: dict[str, object] = {}
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        try:
            tree = ast.parse(cell.source)
        except SyntaxError as exc:
            raise AssertionError(f"Invalid notebook code: {exc}") from exc
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in {
                        "EXECUTOR", "CONFIRM_REMOTE_QPU_EXECUTION"
                    }:
                        values[target.id] = node.value.value
    assert values == {
        "EXECUTOR": "aer",
        "CONFIRM_REMOTE_QPU_EXECUTION": False,
    }, f"Unsafe Bell notebook defaults for CI: {values}"


def main() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    with tempfile.TemporaryDirectory(prefix="qw-local-notebooks-") as path:
        workdir = Path(path)
        for name in NOTEBOOKS:
            source = ROOT / name
            notebook = nbformat.read(source, as_version=4)
            nbformat.validate(notebook)
            validate_cpu_only(notebook, source.name)
            assert not any(
                cell.get("outputs") or cell.get("execution_count") is not None
                for cell in notebook.cells if cell.cell_type == "code"
            ), f"Clear stored outputs before committing: {source}"
            print(f"EXECUTE CPU: {source.relative_to(ROOT)}", flush=True)
            NotebookClient(
                notebook,
                kernel_name="python3",
                timeout=180,
                resources={"metadata": {"path": str(workdir)}},
            ).execute()
            print(f"PASS CPU: {source.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
