# Computational Photonics — N01 to N03

These are original, **development-stage** introductory Jupyter lessons authored and versioned in Quantum Workflows. They use the **existing** object-oriented PhotonicsLab optical models.

| Lab | Topic | Outcome |
| --- | --- | --- |
| [N01](N01_fields_sampling.ipynb) | Gaussian field, units and sampling | Absolute power, inferred waist, clipping diagnostic |
| [N02](N02_diffraction_convergence.ipynb) | Diffraction and convergence | Rayleigh law, self-derived Fresnel FFT, boundary failure |
| [N03](N03_polarization_stokes.ipynb) | Jones/retarders/Stokes | Malus law, signed Stokes, component composition |

### Standalone developer setup (Python 3.14)

```bash
python -m venv .venv-photonics
source .venv-photonics/bin/activate
python -m pip install 'numpy>=2,<3' 'matplotlib>=3.9,<4' 'nbclient>=0.10,<1' 'ipykernel>=6,<8'
python -m pip install 'photonicslab @ git+https://github.com/nyameko/photonicslab.git@141258d308b11569b37628c003ace15e385fba3d'
python scripts/validate_photonics_lessons.py
```

Work from a disposable environment or a vetted cohort image. The commit is deliberate: `photonicslab` is **not** an implicit unpinned dependency. Learners can run any notebook directly in JupyterLab with the same kernel. Notebook execution does not require `quantum-workflows` full Qiskit SDK dependencies.

For the longer curriculum and ownership boundaries, see [Computational Photonics](../../docs/courses/COMPUTATIONAL-PHOTONICS.md). Actual Quantum Platform entitlements, durable `RunArtifacts`, remote Slurm A100/H200 and image-pinning are future integration work; **do not represent this local CPU course as deployed on the platform yet**.
