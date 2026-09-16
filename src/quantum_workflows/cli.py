"""Command-line entry point for reference workflows."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from . import __version__


def _output_path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qw",
        description="Run reproducible hybrid quantum-classical reference workflows.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    hello = commands.add_parser("hello", help="Run the IBM-compatible Bell handshake")
    hello.add_argument("--executor", choices=("aer", "ibm", "qrmi"), default="aer")
    hello.add_argument("--backend", help="Pin an IBM backend; default selects least busy")
    hello.add_argument("--shots", type=int, default=1024)
    hello.add_argument("--minimum-correlation", type=float, default=0.70)
    hello.add_argument("--seed", type=int, default=42)
    hello.add_argument("--output", type=_output_path, default=_output_path("results"))

    trotter = commands.add_parser("trotter", help="Run transverse-field Ising dynamics")
    trotter.add_argument("--executor", choices=("aer", "ibm", "qrmi"), default="aer")
    trotter.add_argument("--backend", help="Pin an IBM backend; default selects least busy")
    trotter.add_argument("--qubits", type=int, default=4)
    trotter.add_argument("--coupling", type=float, default=1.0)
    trotter.add_argument("--field", type=float, default=0.7)
    trotter.add_argument("--final-time", type=float, default=2.0)
    trotter.add_argument("--time-points", type=int, default=9)
    trotter.add_argument("--trotter-steps", type=int, default=4)
    trotter.add_argument("--shots", type=int, default=4096)
    trotter.add_argument("--seed", type=int, default=42)
    trotter.add_argument("--output", type=_output_path, default=_output_path("results"))

    sqd = commands.add_parser("sqd", help="Run N2 sample-based quantum diagonalization")
    sqd.add_argument("--executor", choices=("statevector", "ibm", "qrmi"), default="statevector")
    sqd.add_argument("--backend", help="Pin an IBM backend; default selects least busy")
    sqd.add_argument("--connectivity", choices=("auto", "heavy-hex", "square"), default="auto")
    sqd.add_argument("--shots", type=int, default=20_000)
    sqd.add_argument("--samples-per-batch", type=int, default=1_000)
    sqd.add_argument("--num-batches", type=int, default=3)
    sqd.add_argument("--max-iterations", type=int, default=5)
    sqd.add_argument("--max-dim", type=int, default=50)
    sqd.add_argument("--seed", type=int, default=42)
    sqd.add_argument("--output", type=_output_path, default=_output_path("results"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "hello":
        from .hello import run_hello

        summary, directory = run_hello(
            executor=args.executor,
            shots=args.shots,
            output=args.output,
            backend=args.backend,
            seed=args.seed,
            minimum_correlation=args.minimum_correlation,
        )
    elif args.command == "trotter":
        from .trotter import run_trotter

        summary, directory = run_trotter(
            executor=args.executor,
            qubits=args.qubits,
            coupling=args.coupling,
            field=args.field,
            final_time=args.final_time,
            time_points=args.time_points,
            trotter_steps=args.trotter_steps,
            shots=args.shots,
            output=args.output,
            backend=args.backend,
            seed=args.seed,
        )
    else:
        from .sqd import run_sqd

        summary, directory = run_sqd(
            executor=args.executor,
            shots=args.shots,
            samples_per_batch=args.samples_per_batch,
            num_batches=args.num_batches,
            max_iterations=args.max_iterations,
            max_dim=args.max_dim,
            output=args.output,
            backend=args.backend,
            connectivity=args.connectivity,
            seed=args.seed,
        )
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    print(f"\nResults: {directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
