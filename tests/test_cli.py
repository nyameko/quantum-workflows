from quantum_workflows.cli import build_parser


def test_default_hello_is_local() -> None:
    args = build_parser().parse_args(["hello"])
    assert args.executor == "aer"
    assert args.shots == 1024


def test_hello_supports_explicit_simulator_backends() -> None:
    for executor in ("aer-gpu", "lightning-cpu", "lightning-gpu"):
        args = build_parser().parse_args(["hello", "--executor", executor])
        assert args.executor == executor


def test_default_sqd_is_credential_free() -> None:
    args = build_parser().parse_args(["sqd"])
    assert args.executor == "statevector"
    assert args.backend is None


def test_default_cpu_smoke_is_credential_free() -> None:
    args = build_parser().parse_args(["cpu-smoke"])
    assert args.iterations == 100_000
