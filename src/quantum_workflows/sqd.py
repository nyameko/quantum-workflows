"""N₂ sample-based quantum diagonalization reference workflow."""

from __future__ import annotations

import math
import os
from functools import partial
from pathlib import Path
from typing import Any

import numpy as np

from .artifacts import RunArtifacts


def is_valid_configuration(bitstring: str, norb: int, nelec: tuple[int, int]) -> bool:
    n_alpha, n_beta = nelec
    bits = bitstring.replace(" ", "")
    return (
        len(bits) == 2 * norb
        and bits[norb:].count("1") == n_alpha
        and bits[:norb].count("1") == n_beta
    )


def _connectivity_for_backend(backend: Any, requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        family = backend.configuration().processor_type["family"]
    except AttributeError, KeyError, TypeError:
        return "heavy-hex"
    mapping = {"Heron": "heavy-hex", "Nighthawk": "square"}
    if family not in mapping:
        raise RuntimeError(
            f"Unknown IBM processor family {family!r}; pass --connectivity heavy-hex or square"
        )
    return mapping[family]


def _backend_and_sampler(
    executor: str, backend_name: str | None, seed: int
) -> tuple[Any, Any, str]:
    if executor == "statevector":
        from qiskit.primitives import StatevectorSampler
        from qiskit.providers.fake_provider import GenericBackendV2
        from qiskit.transpiler import CouplingMap

        coupling_map = CouplingMap.from_grid(8, 2)
        backend = GenericBackendV2(
            coupling_map.size(),
            coupling_map=coupling_map,
            basis_gates=["cp", "xx_plus_yy", "p", "x", "swap"],
        )
        return backend, StatevectorSampler(seed=seed), "generic-square-statevector"
    if executor == "ibm":
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "Install the IBM executor with: pip install -e '.[ibm,sqd]'"
            ) from exc
        token = os.environ.get("IBM_QUANTUM_API_KEY")
        instance = os.environ.get("IBM_QUANTUM_INSTANCE")
        kwargs = {
            key: value for key, value in {"token": token, "instance": instance}.items() if value
        }
        service = QiskitRuntimeService(**kwargs)
        backend = (
            service.backend(backend_name)
            if backend_name
            else service.least_busy(operational=True, simulator=False, min_num_qubits=16)
        )
        return backend, SamplerV2(mode=backend), backend.name
    if executor == "qrmi":
        try:
            from qrmi.primitives import QRMIService
            from qrmi.primitives.ibm import SamplerV2, get_backend
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "Install the QRMI executor with: pip install -e '.[qrmi-ibm,sqd]'"
            ) from exc
        if not os.environ.get("QRMI_JOB_QPU_RESOURCES"):
            raise RuntimeError("QRMI_JOB_QPU_RESOURCES was not injected by Slurm/SPANK")
        resources = QRMIService().resources()
        if not resources:
            raise RuntimeError("QRMI did not discover an allocated QPU resource")
        resource = resources[0]
        return get_backend(resource), SamplerV2(resource), resource.resource_id()
    raise ValueError(f"unsupported SQD executor: {executor}")


def run_sqd(
    *,
    executor: str,
    shots: int,
    samples_per_batch: int,
    num_batches: int,
    max_iterations: int,
    max_dim: int,
    output: Path,
    backend: str | None = None,
    connectivity: str = "auto",
    seed: int = 42,
) -> tuple[dict[str, Any], Path]:
    """Run the complete small N₂ SQD workflow locally or on an IBM-compatible QPU."""
    parameters = {
        "molecule": "N2",
        "bond_length_angstrom": 1.0,
        "basis": "sto-6g",
        "frozen_orbitals": 2,
        "shots": shots,
        "samples_per_batch": samples_per_batch,
        "num_batches": num_batches,
        "max_iterations": max_iterations,
        "max_dim": max_dim,
        "backend_requested": backend,
        "connectivity": connectivity,
        "seed": seed,
    }
    artifacts = RunArtifacts("sqd-n2", output, parameters, executor)
    try:
        try:
            import ffsim
            import ffsim.qiskit
            import pyscf.ao2mo
            import pyscf.cc
            import pyscf.gto
            import pyscf.mcscf
            import pyscf.scf
            from qiskit import QuantumCircuit, QuantumRegister
            from qiskit_addon_sqd.fermion import (
                SCIResult,
                diagonalize_fermionic_hamiltonian,
                solve_sci_batch,
            )
        except ImportError as exc:
            raise RuntimeError("Install the SQD workflow with: pip install -e '.[sqd]'") from exc

        mol = pyscf.gto.Mole()
        mol.build(
            atom=[["N", (0, 0, -0.5)], ["N", (0, 0, 0.5)]],
            basis="sto-6g",
            symmetry="Dooh",
            verbose=0,
        )
        n_frozen = 2
        active_space = range(n_frozen, mol.nao_nr())
        scf = pyscf.scf.RHF(mol).run()
        norb = len(active_space)
        n_electrons = int(sum(scf.mo_occ[active_space]))
        n_alpha = (n_electrons + mol.spin) // 2
        n_beta = (n_electrons - mol.spin) // 2
        nelec = (n_alpha, n_beta)
        cas = pyscf.mcscf.CASCI(scf, norb, nelec)
        mo = cas.sort_mo(active_space, base=0)
        hcore, nuclear_repulsion_energy = cas.get_h1cas(mo)
        eri = pyscf.ao2mo.restore(1, cas.get_h2cas(mo), norb)
        reference_energy = float(cas.run().e_tot)

        frozen = [index for index in range(mol.nao_nr()) if index not in active_space]
        ccsd = pyscf.cc.CCSD(scf, frozen=frozen).run()
        backend_object, sampler, resolved_backend = _backend_and_sampler(executor, backend, seed)
        resolved_connectivity = (
            "square"
            if executor == "statevector"
            else _connectivity_for_backend(backend_object, connectivity)
        )

        pairs_aa = [(orbital, orbital + 1) for orbital in range(norb - 1)]
        pass_manager, pairs_ab = ffsim.qiskit.generate_lucj_pass_manager(
            backend=backend_object,
            norb=norb,
            connectivity=resolved_connectivity,
            interaction_pairs=(pairs_aa, None),
            optimization_level=3,
        )
        ucj_op = ffsim.UCJOpSpinBalanced.from_t_amplitudes(
            t2=ccsd.t2,
            t1=ccsd.t1,
            n_reps=1 if executor != "statevector" else 4,
            interaction_pairs=(pairs_aa, pairs_ab),
            optimize=True,
        )
        qubits = QuantumRegister(2 * norb, name="q")
        circuit = QuantumCircuit(qubits)
        circuit.append(ffsim.qiskit.PrepareHartreeFockJW(norb, nelec), qubits)
        circuit.append(ffsim.qiskit.UCJOpSpinBalancedJW(ucj_op), qubits)
        circuit.measure_all()
        isa_circuit = pass_manager.run(circuit)
        artifacts.add_circuit(circuit, stage="logical-lucj")
        artifacts.add_circuit(isa_circuit, stage="transpiled-lucj")

        if executor == "qrmi":
            job = sampler.run([(isa_circuit,)], shots=shots)
        else:
            job = sampler.run([isa_circuit], shots=shots)
        primitive_result = job.result()
        bit_array = primitive_result[0].data.meas
        bitstrings = bit_array.get_bitstrings()
        valid_count = sum(is_valid_configuration(bits, norb, nelec) for bits in bitstrings)
        valid_fraction = valid_count / bit_array.num_shots
        expected_random = math.comb(norb, n_alpha) * math.comb(norb, n_beta) / 2 ** (2 * norb)

        initial_occupancies = (
            np.array([1] * n_alpha + [0] * (norb - n_alpha)),
            np.array([1] * n_beta + [0] * (norb - n_beta)),
        )
        result_history: list[list[SCIResult]] = []

        def callback(results: list[SCIResult]) -> None:
            result_history.append(results)

        rng = np.random.default_rng(seed)
        sqd_result = diagonalize_fermionic_hamiltonian(
            hcore,
            eri,
            bit_array,
            samples_per_batch=samples_per_batch,
            norb=norb,
            nelec=nelec,
            num_batches=num_batches,
            energy_tol=1e-3,
            occupancies_tol=1e-3,
            max_iterations=max_iterations,
            sci_solver=partial(solve_sci_batch, spin_sq=0.0, max_cycle=200),
            symmetrize_spin=True,
            max_dim=max_dim,
            initial_occupancies=initial_occupancies,
            carryover_threshold=1e-4,
            callback=callback,
            seed=rng,
        )
        final_energy = float(sqd_result.energy + nuclear_repulsion_energy)
        energy_error = final_energy - reference_energy
        history_rows = []
        for iteration, batch_results in enumerate(result_history, start=1):
            for batch, result in enumerate(batch_results):
                history_rows.append(
                    {
                        "iteration": iteration,
                        "batch": batch,
                        "energy_hartree": float(result.energy + nuclear_repulsion_energy),
                        "subspace_dimension": int(np.prod(result.sci_state.amplitudes.shape)),
                    }
                )
        occupancy_rows = [
            {
                "orbital": orbital,
                "alpha": float(sqd_result.orbital_occupancies[0][orbital]),
                "beta": float(sqd_result.orbital_occupancies[1][orbital]),
                "total": float(
                    sqd_result.orbital_occupancies[0][orbital]
                    + sqd_result.orbital_occupancies[1][orbital]
                ),
            }
            for orbital in range(norb)
        ]
        artifacts.write_csv("iterations.csv", history_rows)
        artifacts.write_csv("orbital-occupancies.csv", occupancy_rows)
        artifacts.write_json(
            "samples.json",
            {"bitstrings": bitstrings, "shots": bit_array.num_shots},
            data=True,
        )
        job_id = job.job_id() if hasattr(job, "job_id") else None
        summary = {
            "workflow": "sqd-n2",
            "executor": executor,
            "backend": resolved_backend,
            "provider_job_id": job_id,
            "orbitals": norb,
            "qubits": 2 * norb,
            "electrons": nelec,
            "connectivity": resolved_connectivity,
            "scf_energy_hartree": float(scf.e_tot),
            "ccsd_energy_hartree": float(ccsd.e_tot),
            "reference_casci_energy_hartree": reference_energy,
            "sqd_energy_hartree": final_energy,
            "energy_error_hartree": energy_error,
            "absolute_error_kcal_per_mol": abs(energy_error) * 627.509474,
            "valid_configuration_fraction": valid_fraction,
            "uniform_random_valid_fraction": expected_random,
            "iterations_completed": len(result_history),
        }
        artifacts.set_quantum_metadata(
            provider="local" if executor == "statevector" else "ibm",
            backend=resolved_backend,
            job_id=job_id,
            shots=bit_array.num_shots,
        )
        artifacts.finish(summary)
        return summary, artifacts.directory
    except Exception as exc:
        artifacts.fail(exc)
        raise
