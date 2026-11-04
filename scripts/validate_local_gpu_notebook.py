#!/usr/bin/env python3
"""Opt-in live GPU acceptance of the Bell Jupyter notebook on a local workstation.

Never runs on automated CI: requires an explicit GPU-capable Jupyter kernel,
NVIDIA drivers, and a compatible Aer GPU or PennyLane Lightning GPU environment.
No QPU access or vendor API credentials are used.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import nbformat
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
BELL = ROOT / "labs/01-intro-quantum-computing/02-bell-cpu-gpu-qpu.ipynb"
DEFAULT = 'EXECUTOR = "aer"'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executor", required=True, choices=("aer-gpu", "lightning-gpu"))
    parser.add_argument("--kernel", required=True, help="Jupyter kernel registered from this GPU venv")
    args = parser.parse_args()

    try:
        details = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv"],
            check=True, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("NVIDIA GPU/driver check failed; no CPU fallback") from exc
    print(details.stdout.strip(), flush=True)

    spec = KernelSpecManager().get_kernel_spec(args.kernel)
    kernel_python = Path(spec.argv[0]).expanduser().resolve()
    current_python = Path(sys.executable).resolve()
    if kernel_python != current_python:
        raise RuntimeError(
            f"Kernel {args.kernel!r} is registered to {kernel_python}, "
            f"but the script is running with {current_python}; use the GPU venv for both."
        )

    if args.executor == "aer-gpu":
        from qiskit_aer import AerSimulator

        devices = AerSimulator().available_devices()
        print("Qiskit Aer devices:", devices, flush=True)
        if "GPU" not in devices:
            raise RuntimeError("Aer has no compatible CUDA GPU; refusing CPU fallback")

    notebook = nbformat.read(BELL, as_version=4)
    nbformat.validate(notebook)
    parameter_cells = [
        c for c in notebook.cells
        if c.cell_type == "code"
        and DEFAULT in c.source
        and "CONFIRM_REMOTE_QPU_EXECUTION = False" in c.source
    ]
    if len(parameter_cells) != 1:
        raise RuntimeError("Notebook defaults changed: inspect before GPU acceptance")
    parameter_cells[0].source = parameter_cells[0].source.replace(
        DEFAULT, f'EXECUTOR = "{args.executor}"', 1
    )
    os.environ.setdefault("MPLBACKEND", "Agg")

    # Change only an in-memory notebook; keep the versioned source untouched.
    with tempfile.TemporaryDirectory(prefix="qw-gpu-notebook-") as tmp:
        NotebookClient(
            notebook,
            kernel_name=args.kernel,
            timeout=240,
            resources={"metadata": {"path": tmp}},
        ).execute()
        results = list(Path(tmp).glob("results/hello-ibm/*/summary.json"))
        if len(results) != 1:
            raise RuntimeError(f"Expected one recorded Bell result; found {len(results)}")
        summary = json.loads(results[0].read_text())
        if not summary.get("passed") or summary.get("executor") != args.executor:
            raise RuntimeError(f"GPU Bell acceptance failed: {summary}")
        print(
            f"PASS {args.executor}: {summary['shots_observed']} shots, "
            f"Bell correlation {summary['bell_correlation']:.5f}",
            flush=True,
        )
    print("This verifies a tiny Bell workload, not GPU speedup or memory scaling.")


if __name__ == "__main__":
    main()
