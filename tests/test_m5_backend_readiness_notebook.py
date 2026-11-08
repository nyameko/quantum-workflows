"""Contract for the credential-safe, CPU-default M5 readiness notebook."""

from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parents[1] / "labs/06-facility-acceptance/00-backend-readiness.ipynb"


def _notebook_cells():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    return notebook["cells"]


def test_readiness_notebook_defaults_are_non_consuming() -> None:
    cells = _notebook_cells()
    source = "\n".join("".join(cell["source"]) for cell in cells if cell["cell_type"] == "code")
    assert "ENABLE_GPU_SMOKES = False" in source
    assert "ENABLE_IBM_DISCOVERY = False" in source
    assert "WRITE_REPORT = False" in source
    assert "QiskitRuntimeService(token=token, instance=crn)" in source
    assert "service.run(" not in source
    assert "service.backend(" not in source


def test_readiness_notebook_cpu_executes_without_provider_credentials() -> None:
    scope: dict[str, object] = {}
    for index, cell in enumerate(_notebook_cells()):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        exec(compile(source, f"{NOTEBOOK.name}:cell_{index}", "exec"), scope)
    checks = scope["checks"]
    assert checks["Aer CPU Bell"]["status"] == "PASS"
    assert checks["Aer GPU Bell"]["status"] == "TODO"
    assert checks["Lightning GPU Bell"]["status"] == "TODO"
    assert checks["IBM classroom access"]["status"] == "TODO"
