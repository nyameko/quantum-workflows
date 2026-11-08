#!/usr/bin/env python3
"""Scheduler-backed one-GPU reference, never executed by the web notebook kernel."""
import argparse
import importlib.metadata
import json
import os
import time
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qubits", type=int, default=22)
    parser.add_argument("--shots", type=int, default=2048)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.qubits < 2 or args.qubits > 34 or args.shots < 1:
        parser.error("qubits must be 2..34 and shots must be positive")

    simulator = AerSimulator(method="statevector", device="GPU")
    devices = simulator.available_devices()
    if "GPU" not in devices:
        raise RuntimeError("Aer GPU unavailable: verify approved CUDA image and Slurm GPU assignment")
    circuit = QuantumCircuit(args.qubits, args.qubits)
    circuit.h(0)
    for i in range(1, args.qubits):
        circuit.cx(i - 1, i)
    circuit.measure(range(args.qubits), range(args.qubits))
    started = time.perf_counter()
    result = simulator.run(
        transpile(circuit, simulator), shots=args.shots, seed_simulator=42
    ).result()
    elapsed = time.perf_counter() - started
    counts = result.get_counts()
    valid = (
        result.success and sum(counts.values()) == args.shots
        and set(counts) <= {"0" * args.qubits, "1" * args.qubits}
    )
    payload = {
        "experiment": "ideal-ghz-gpu",
        "qubits": args.qubits,
        "shots": args.shots,
        "counts": counts,
        "scientific_check_passed": bool(valid),
        "duration_seconds": round(elapsed, 5),
        "device_requested": "GPU",
        "available_devices": list(devices),
        "aer_metadata": result.results[0].metadata,
        "slurm_job_id": os.getenv("SLURM_JOB_ID"),
        "slurm_job_name": os.getenv("SLURM_JOB_NAME"),
        "cuda_visible_devices": os.getenv("CUDA_VISIBLE_DEVICES"),
        "container_image_path": os.getenv("QISKIT_AER_GPU_IMAGE"),
        "qiskit_version": importlib.metadata.version("qiskit"),
        "qiskit_aer_version": importlib.metadata.version("qiskit-aer"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    if not valid:
        raise SystemExit("Scientific GHZ validation failed")
    print(f"Validated Aer GPU result written to {args.output}", flush=True)


if __name__ == "__main__":
    main()
