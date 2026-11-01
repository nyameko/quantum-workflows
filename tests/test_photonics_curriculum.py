"""Static, dependency-free contract checks for the Computational Photonics lessons."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "labs" / "04-zero-to-hero-photonics"
SHA = "141258d308b11569b37628c003ace15e385fba3d"
LABS = {
    "N01_fields_sampling": "photonics.n01",
    "N02_diffraction_convergence": "photonics.n02",
    "N03_polarization_stokes": "photonics.n03",
}


def test_photonics_notebook_contracts():
    for stem, expected_id in LABS.items():
        metadata = json.loads((LESSONS / f"{stem}.json").read_text())
        notebook = json.loads((LESSONS / f"{stem}.ipynb").read_text())
        assert metadata["id"] == expected_id
        assert metadata["status"] == "development"
        assert metadata["environment"]["science_dependency"]["commit"] == SHA
        assert metadata["resources"]["gpu_required"] is False
        assert metadata["resources"]["credentials_required"] is False
        assert notebook["nbformat"] == 4
        assert notebook["metadata"]["photonics_course"]["id"] == expected_id
        assert notebook["metadata"]["photonics_course"]["science_revision"] == SHA
        code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
        assert len(code_cells) >= 3
        assert all(c["execution_count"] is None and not c["outputs"] for c in code_cells)
        for cell in code_cells:
            compile("".join(cell["source"]), str(LESSONS / f"{stem}.ipynb"), "exec")
