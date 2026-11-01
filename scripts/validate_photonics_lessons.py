"""Execute the three beginner PhotonicsLab notebooks in clean kernels.

Requirements: nbformat, nbclient, ipykernel, matplotlib, numpy and pinned photonicslab.
This script intentionally never contacts a QPU, GPU service or a lab instrument.
"""

from __future__ import annotations

import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "labs" / "04-zero-to-hero-photonics"
STEMS = (
    "N01_fields_sampling",
    "N02_diffraction_convergence",
    "N03_polarization_stokes",
)
PHOTONICSLAB_SHA = "141258d308b11569b37628c003ace15e385fba3d"


def main() -> None:
    import photonicslab

    assert photonicslab.__version__ == "0.6.0a1", photonicslab.__version__
    for stem in STEMS:
        path = LESSONS / f"{stem}.ipynb"
        record = json.loads((LESSONS / f"{stem}.json").read_text())
        assert record["environment"]["science_dependency"]["commit"] == PHOTONICSLAB_SHA
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        assert notebook.metadata.photonics_course.science_revision == PHOTONICSLAB_SHA
        assert all(cell.get("execution_count") is None for cell in notebook.cells if cell.cell_type == "code")
        assert all(not cell.get("outputs") for cell in notebook.cells if cell.cell_type == "code")
        print(f"EXECUTE {record['id']} ({path})", flush=True)
        NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(LESSONS)}},
        ).execute()
        print(f"PASS {record['id']}", flush=True)


if __name__ == "__main__":
    main()
