"""Optional PennyLane-Lightning Bell-state sampler for CPU and NVIDIA GPU."""

from __future__ import annotations


def sample_bell(*, executor: str, shots: int, seed: int) -> tuple[dict[str, int], str]:
    """Sample the same H-CNOT Bell experiment with a native PennyLane circuit.

    Device selection is explicit; requesting a GPU never silently falls back to CPU.
    """
    if executor not in ("lightning-cpu", "lightning-gpu"):
        raise ValueError(f"unsupported PennyLane executor: {executor}")
    try:
        import pennylane as qml
    except ImportError as exc:
        raise RuntimeError(
            "Install PennyLane-Lightning with: pip install -e '.[lightning-cpu]' "
            "or, for NVIDIA GPUs, pip install -e '.[lightning-gpu]'"
        ) from exc

    backend = "lightning.qubit" if executor == "lightning-cpu" else "lightning.gpu"
    try:
        device = qml.device(backend, wires=2, shots=shots, seed=seed)
    except Exception as exc:
        raise RuntimeError(
            f"{backend} is unavailable in this environment. "
            "Use an appropriate runner and verify its installed simulator dependencies."
        ) from exc

    @qml.qnode(device)
    def bell_counts():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = bell_counts()
    return {str(bits): int(count) for bits, count in counts.items()}, backend
