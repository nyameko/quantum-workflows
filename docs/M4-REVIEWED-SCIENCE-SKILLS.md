# M4d reviewed resource candidates (inert)

These proposed records are **links to existing scientific resources**, not
executable agent skills, another quantum SDK, or an allocation engine.

- `learning.quantum-foundations` points to the Qiskit/Aer introductory
  Jupyter notebook and its Python requirements. Researchers use upstream
  SDKs directly, with theory, figures and exercises.
- `reference.cpu-smoke-provenance` points to the existing operational
  CPU runner source for administrators studying the current provenance path.
  It is **not** a learning notebook and must not be exposed as a quantum lesson.

The JSON record does not confer access to a workspace, a cluster, model keys
or QPU provider credentials. `automatic_code_execution=false`, and no
command `entrypoint` or shell argument vectors are part of either record.
ACP's eventual reviewed skill binding may reference an immutable Git commit
and manifest digest; actual user authorization remains in Quantum Platform.

Opening the resource may display a reviewed notebook, an environment
prerequisite or a source file. **Execution is always a separate, explicitly
authorized action** in Jupyter or a later Slurm/provider integration. Notebook
content itself must remain portable and runnable without ACP or `qw` commands.

M4 does not require GPU/QPU hardware or a home-built science execution API.
A correct Bell/CHSH educational notebook belongs to the scientific curriculum,
not to ACP runtime code. A reference does not constitute scientific evidence.
