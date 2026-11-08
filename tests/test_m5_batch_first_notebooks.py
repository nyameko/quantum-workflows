"""Validate batch-first notebook source without installing vendor SDKs or using GPUs."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
LABS = HERE / "labs/01-intro-quantum-computing/batch-first"


def test_eight_notebooks_are_valid_and_python_compiles():
    books = sorted(LABS.glob("[0-9][0-9]-*.ipynb"))
    assert [p.name[:2] for p in books] == [f"{n:02d}" for n in range(8)]
    for path in books:
        doc = json.loads(path.read_text())
        assert doc["nbformat"] == 4
        assert len({cell["id"] for cell in doc["cells"]}) == len(doc["cells"])
        assert doc["cells"][0]["cell_type"] == "markdown"
        for cell in doc["cells"]:
            if cell["cell_type"] == "code":
                assert cell["outputs"] == []
                compile("".join(cell["source"]), path.name, "exec")


def test_researcher_ssh_submission_is_identity_bound():
    source = (LABS / "01-first-gpu-slurm-batch.ipynb").read_text()
    assert "SLURM_LOGIN_HOST" in source
    assert "SLURM_RESEARCHER_SSH_KEY" in source
    assert "StrictHostKeyChecking=yes" in source
    assert "IdentitiesOnly=yes" in source
    assert "RESEARCH_USER" in source
    assert "shlex.join(args)" in source
    assert "f\\"{RESEARCH_USER}@{SLURM_LOGIN_HOST}\\"" in source
    assert "subprocess.run(" in source


def test_batch_template_uses_native_slurm_and_no_privileged_impersonation():
    content = (HERE / "slurm/aer-gpu.sbatch").read_text()
    assert "--gres=gpu:1" in content
    assert "srun apptainer exec --nv" in content
    for unsafe in ("runuser", "sudo ", "su - ", "jupyterhub-slurm-helper"):
        assert unsafe not in content
