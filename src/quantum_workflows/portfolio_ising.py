"""M5a: independently validated portfolio Ising / PennyLane Lightning CPU reference.

This is a scientific experiment, not a new workflow SDK, scheduler or CLI.
The exact classical enumeration is the benchmark for an analytic VQE-style
product-state ansatz. No GPU, QPU or remote provider is invoked.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from .artifacts import RunArtifacts


@dataclass(frozen=True)
class PortfolioProblem:
    expected_returns: tuple[float, ...]
    covariance: tuple[tuple[float, ...], ...]
    budget: int
    risk_weight: float
    budget_penalty: float


def reference_problem() -> PortfolioProblem:
    """Small, deterministic, synthetic three-asset teaching problem."""
    return PortfolioProblem(
        expected_returns=(0.08, 0.11, 0.07),
        covariance=((0.06, 0.01, 0.0), (0.01, 0.04, 0.01), (0.0, 0.01, 0.03)),
        budget=1,
        risk_weight=0.5,
        budget_penalty=1.0,
    )


def _validated(problem: PortfolioProblem) -> tuple[np.ndarray, np.ndarray]:
    returns = np.asarray(problem.expected_returns, dtype=float)
    covariance = np.asarray(problem.covariance, dtype=float)
    n = returns.size
    if returns.ndim != 1 or not 2 <= n <= 8:
        raise ValueError("Portfolio must contain between 2 and 8 assets")
    if covariance.shape != (n, n):
        raise ValueError("Covariance must be a square matrix matching the assets")
    if not np.isfinite(returns).all() or not np.isfinite(covariance).all():
        raise ValueError("Portfolio parameters must be finite")
    if not np.allclose(covariance, covariance.T, atol=1e-12, rtol=0):
        raise ValueError("Covariance must be symmetric")
    if np.min(np.linalg.eigvalsh(covariance)) < -1e-10:
        raise ValueError("Covariance must be positive semidefinite")
    if type(problem.budget) is not int or not 0 <= problem.budget <= n:
        raise ValueError("Budget must be an integer between zero and asset count")
    if (
        not np.isfinite(problem.risk_weight)
        or problem.risk_weight < 0
        or not np.isfinite(problem.budget_penalty)
        or problem.budget_penalty <= 0
    ):
        raise ValueError("Risk weight must be nonnegative and budget penalty positive")
    return returns, covariance


def objective(problem: PortfolioProblem, bits: tuple[int, ...]) -> float:
    """Independent classical portfolio objective, with binary holdings."""
    returns, covariance = _validated(problem)
    if len(bits) != returns.size or any(bit not in (0, 1) for bit in bits):
        raise ValueError("Holdings must be a binary vector matching the asset count")
    x = np.asarray(bits, dtype=float)
    return float(
        -returns @ x
        + problem.risk_weight * (x @ covariance @ x)
        + problem.budget_penalty * (sum(bits) - problem.budget) ** 2
    )


def ising_coefficients(
    problem: PortfolioProblem,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Return c, h, J for c + sum(h_i Z_i) + sum_(i<j)(J_ij Z_i Z_j).

    With x_i=(1-Z_i)/2, x_i^2=x_i and a binary budget penalty,
    the diagonal covariance contributes to the linear QUBO terms.
    """
    returns, covariance = _validated(problem)
    linear = (
        -returns
        + problem.risk_weight * np.diag(covariance)
        + problem.budget_penalty * (1 - 2 * problem.budget)
    )
    quadratic = 2 * problem.risk_weight * covariance + 2 * problem.budget_penalty
    np.fill_diagonal(quadratic, 0)
    offset = float(
        problem.budget_penalty * problem.budget**2
        + np.sum(linear) / 2
        + np.sum(np.triu(quadratic, 1)) / 4
    )
    local_z = -linear / 2 - np.sum(quadratic, axis=1) / 4
    coupling = np.triu(quadratic, 1) / 4
    return offset, local_z, coupling


def ising_energy(problem: PortfolioProblem, bits: tuple[int, ...]) -> float:
    """Evaluate the Pauli-Z encoding on a computational basis bitstring."""
    offset, local_z, coupling = ising_coefficients(problem)
    if len(bits) != local_z.size or any(bit not in (0, 1) for bit in bits):
        raise ValueError("Expected binary basis bitstring")
    z = 1 - 2 * np.asarray(bits, dtype=float)
    return float(offset + local_z @ z + np.sum(coupling * np.outer(z, z)))


def exact_reference(problem: PortfolioProblem) -> dict[str, Any]:
    """Enumerate the exact classical minimum; never derive it from VQE."""
    returns, _ = _validated(problem)
    spectrum = [
        {"bits": list(bits), "energy": objective(problem, bits)}
        for bits in product((0, 1), repeat=returns.size)
    ]
    optimum = min(spectrum, key=lambda row: row["energy"])
    return {
        "minimum_energy": optimum["energy"],
        "optimal_bits": optimum["bits"],
        "spectrum": spectrum,
    }


def run_lightning_cpu(
    *,
    problem: PortfolioProblem,
    output: Path,
    seed: int = 7,
    restarts: int = 4,
    maxiter: int = 180,
) -> tuple[dict[str, Any], Path]:
    """Optimize a local analytic VQE ansatz and retain reference/manifest.

    A computational-basis product state can represent the classical Ising
    minimum, but the optimizer is not assumed to find the global optimum.
    The observed gap to exact enumeration is always reported.
    """
    returns, _ = _validated(problem)
    if type(seed) is not int or seed < 0:
        raise ValueError("Seed must be a nonnegative integer")
    if not 1 <= restarts <= 32 or not 1 <= maxiter <= 2000:
        raise ValueError("Restarts/maxiter exceed bounded CPU experiment limits")
    try:
        import pennylane as qml
    except ImportError as exc:
        raise RuntimeError("Install CPU PennyLane: pip install -e '.[lightning-cpu]'") from exc

    try:
        device = qml.device("lightning.qubit", wires=returns.size, shots=None)
    except Exception as exc:
        raise RuntimeError("lightning.qubit unavailable: install the CPU plugin") from exc

    offset, local_z, coupling = ising_coefficients(problem)
    coefficients = [offset]
    operators = [qml.Identity(wires=0)]
    for i, coefficient in enumerate(local_z):
        coefficients.append(float(coefficient))
        operators.append(qml.PauliZ(wires=i))
    for i in range(returns.size):
        for j in range(i + 1, returns.size):
            if coupling[i, j] != 0:
                coefficients.append(float(coupling[i, j]))
                operators.append(qml.PauliZ(wires=i) @ qml.PauliZ(wires=j))
    hamiltonian = qml.dot(coefficients, operators)

    @qml.qnode(device)
    def energy(angles):
        for wire, angle in enumerate(angles):
            qml.RY(angle, wires=wire)
        return qml.expval(hamiltonian)

    reference = exact_reference(problem)
    parameters = {
        "expected_returns": list(problem.expected_returns),
        "covariance": [list(row) for row in problem.covariance],
        "budget": problem.budget,
        "risk_weight": problem.risk_weight,
        "budget_penalty": problem.budget_penalty,
        "seed": seed,
        "restarts": restarts,
        "maxiter": maxiter,
        "shots": None,
    }
    artifacts = RunArtifacts("portfolio-ising-cpu", Path(output), parameters, "lightning-cpu")
    try:
        rng = np.random.default_rng(seed)
        results = []
        for attempt in range(restarts):
            initial = (
                np.full(returns.size, np.pi / 2)
                if attempt == 0
                else rng.uniform(0, np.pi, size=returns.size)
            )
            fit = minimize(
                lambda theta: float(energy(theta)),
                initial,
                method="L-BFGS-B",
                bounds=[(0, np.pi)] * returns.size,
                options={"maxiter": maxiter, "ftol": 1e-11},
            )
            results.append(fit)

        best = min(results, key=lambda result: float(result.fun))
        observed = float(energy(best.x))
        gap = observed - float(reference["minimum_energy"])
        if gap < -1e-6:
            raise ArithmeticError("Quantum expectation fell below exact classical minimum")
        summary = {
            "workflow": "portfolio-ising-cpu",
            "backend": "lightning.qubit",
            "shots": None,
            "analytic_expectation": True,
            "assets": int(returns.size),
            "seed": seed,
            "restarts": restarts,
            "best_angles_rad": [float(angle) for angle in best.x],
            "optimized_energy": observed,
            "exact_reference_energy": reference["minimum_energy"],
            "exact_reference_bits": reference["optimal_bits"],
            "optimality_gap": gap,
            "within_reference_tolerance": bool(-1e-6 <= gap <= 1e-3),
            "optimizer_success": bool(best.success),
            "gpu_allocated": False,
            "qpu_executed": False,
        }
        artifacts.set_quantum_metadata(
            provider="local",
            backend="lightning.qubit",
            qubits=int(returns.size),
            shots=None,
            analytic=True,
        )
        artifacts.write_json("reference_spectrum.json", reference, data=True)
        artifacts.finish(summary)
        return summary, artifacts.directory
    except Exception as exc:
        artifacts.fail(exc)
        raise
