"""Sampling executors with a common, deliberately small result contract."""

from __future__ import annotations

import os
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SampleBatch:
    counts: list[dict[str, int]]
    backend: str
    job_id: str | None
    transpiled_circuits: Sequence[Any]


def sample_circuits(
    circuits: Sequence[Any],
    *,
    executor: str,
    shots: int,
    backend_name: str | None = None,
    seed: int = 42,
) -> SampleBatch:
    """Sample circuits on Aer, IBM Quantum Compute Service, or QRMI."""
    if executor == "aer":
        return _sample_aer(circuits, shots=shots, seed=seed)
    if executor == "ibm":
        return _sample_ibm(circuits, shots=shots, backend_name=backend_name)
    if executor == "qrmi":
        return _sample_qrmi(circuits, shots=shots)
    raise ValueError(f"unsupported sampling executor: {executor}")


def _sample_aer(circuits: Sequence[Any], *, shots: int, seed: int) -> SampleBatch:
    from qiskit import transpile
    from qiskit_aer import AerSimulator

    backend = AerSimulator(seed_simulator=seed)
    isa = transpile(list(circuits), backend=backend, optimization_level=1, seed_transpiler=seed)
    job = backend.run(isa, shots=shots)
    result = job.result()
    counts = [_normalize_counts(result.get_counts(i)) for i in range(len(isa))]
    return SampleBatch(counts, backend.name, job.job_id(), isa)


def _sample_ibm(circuits: Sequence[Any], *, shots: int, backend_name: str | None) -> SampleBatch:
    try:
        from qiskit.transpiler import generate_preset_pass_manager
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError("Install the IBM executor with: pip install -e '.[ibm]'") from exc

    token = os.environ.get("IBM_QUANTUM_API_KEY")
    instance = os.environ.get("IBM_QUANTUM_INSTANCE")
    kwargs = {key: value for key, value in {"token": token, "instance": instance}.items() if value}
    service = QiskitRuntimeService(**kwargs)
    backend = (
        service.backend(backend_name)
        if backend_name
        else service.least_busy(
            operational=True, simulator=False, min_num_qubits=max(c.num_qubits for c in circuits)
        )
    )
    manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa = manager.run(list(circuits))
    sampler = SamplerV2(mode=backend)
    job = sampler.run(isa, shots=shots)
    result = job.result()
    counts = [_normalize_counts(pub.data.meas.get_counts()) for pub in result]
    return SampleBatch(counts, backend.name, job.job_id(), isa)


def _sample_qrmi(circuits: Sequence[Any], *, shots: int) -> SampleBatch:
    try:
        from qiskit.transpiler import generate_preset_pass_manager
        from qrmi.primitives import QRMIService
        from qrmi.primitives.ibm import SamplerV2, get_target
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError("Install the QRMI executor with: pip install -e '.[qrmi-ibm]'") from exc

    if not os.environ.get("QRMI_JOB_QPU_RESOURCES"):
        raise RuntimeError("QRMI_JOB_QPU_RESOURCES was not injected by Slurm/SPANK")
    resources = QRMIService().resources()
    if not resources:
        raise RuntimeError("QRMI did not discover an allocated QPU resource")
    resource = resources[0]
    target = get_target(resource)
    manager = generate_preset_pass_manager(target=target, optimization_level=1)
    isa = manager.run(list(circuits))
    sampler = SamplerV2(resource, options={"default_shots": shots})
    job = sampler.run([(circuit,) for circuit in isa])
    result = job.result()
    counts = [_normalize_counts(pub.data.meas.get_counts()) for pub in result]
    return SampleBatch(counts, resource.resource_id(), job.job_id(), isa)


def _normalize_counts(counts: Any) -> dict[str, int]:
    return dict(Counter({str(key).replace(" ", ""): int(value) for key, value in counts.items()}))
