"""M5a numerical checks: independent QUBO reference before H200 execution."""

from __future__ import annotations

import json
from dataclasses import replace
from itertools import product

import numpy as np
import pytest

from quantum_workflows.portfolio_ising import (
    exact_reference,
    ising_coefficients,
    ising_energy,
    objective,
    reference_problem,
    run_lightning_cpu,
)


def test_every_basis_energy_agrees_with_independent_binary_objective():
    problem = reference_problem()
    for bits in product((0, 1), repeat=3):
        assert np.isclose(
            objective(problem, bits), ising_energy(problem, bits),
            atol=1e-12, rtol=0,
        )


def test_exact_small_portfolio_reference_is_reproducible():
    reference = exact_reference(reference_problem())
    assert reference["optimal_bits"] == [0, 1, 0]
    assert reference["minimum_energy"] == pytest.approx(-0.09)
    assert len(reference["spectrum"]) == 8
    assert len({tuple(row["bits"]) for row in reference["spectrum"]}) == 8


def test_ising_coefficients_preserve_constant_offset_and_pair_terms():
    offset, local_z, pair = ising_coefficients(reference_problem())
    assert isinstance(offset, float)
    assert local_z.shape == (3,)
    assert pair.shape == (3, 3)
    assert np.allclose(np.tril(pair), 0)
    assert np.isfinite(local_z).all()
    assert np.isfinite(pair).all()


@pytest.mark.parametrize(
    ("changed", "message"),
    [
        ({"budget": -1}, "Budget"),
        ({"budget": 5}, "Budget"),
        ({"budget": True}, "Budget"),
        ({"risk_weight": -1}, "Risk weight"),
        ({"budget_penalty": 0}, "budget penalty"),
        ({"expected_returns": (0.1, float("nan"), 0.2)}, "finite"),
        ({"covariance": ((1.0,),)}, "Covariance"),
    ],
)
def test_reject_invalid_physical_inputs(changed, message):
    with pytest.raises(ValueError, match=message):
        exact_reference(replace(reference_problem(), **changed))


def test_reject_nonbinary_holding():
    with pytest.raises(ValueError, match="binary"):
        objective(reference_problem(), (0, 2, 1))


@pytest.mark.integration
def test_actual_pennylane_lightning_cpu_analytic_reference(tmp_path):
    pytest.importorskip("pennylane")
    summary, directory = run_lightning_cpu(
        problem=reference_problem(), output=tmp_path, seed=7,
        restarts=4, maxiter=180,
    )
    assert summary["backend"] == "lightning.qubit"
    assert summary["shots"] is None
    assert summary["analytic_expectation"] is True
    assert summary["qpu_executed"] is False
    assert summary["gpu_allocated"] is False
    assert summary["exact_reference_bits"] == [0, 1, 0]
    assert summary["optimality_gap"] >= -1e-6

    manifest = json.loads((directory / "manifest.json").read_text())
    persisted = json.loads((directory / "summary.json").read_text())
    spectrum = json.loads((directory / "data/reference_spectrum.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["runtime"]["executor"] == "lightning-cpu"
    assert manifest["quantum"]["provider"] == "local"
    assert manifest["quantum"]["backend"] == "lightning.qubit"
    assert persisted["optimized_energy"] == pytest.approx(summary["optimized_energy"])
    assert len(spectrum["spectrum"]) == 8
    assert any(a["path"] == "data/reference_spectrum.json" for a in manifest["artifacts"])


def test_parameter_limits_fail_before_importing_pennylane(tmp_path):
    with pytest.raises(ValueError, match="Seed"):
        run_lightning_cpu(problem=reference_problem(), output=tmp_path, seed=-1)
    with pytest.raises(ValueError, match="bounded CPU"):
        run_lightning_cpu(problem=reference_problem(), output=tmp_path, restarts=33)
