from quantum_workflows.cli import build_parser


def test_default_hello_is_local() -> None:
    args = build_parser().parse_args(["hello"])
    assert args.executor == "aer"
    assert args.shots == 1024


def test_default_sqd_is_credential_free() -> None:
    args = build_parser().parse_args(["sqd"])
    assert args.executor == "statevector"
    assert args.backend is None
