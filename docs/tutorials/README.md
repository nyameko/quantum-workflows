# Tutorials

The first learning path follows the same progression used by the executable workflows:

1. [IBM QPU handshake](01-IBM-QPU-HANDSHAKE.md) — establish the local → direct QPU → QRMI path.
2. [Trotterized dynamics](02-TROTTERIZED-DYNAMICS.md) — separate product-formula and shot error.
3. [Sample-based quantum diagonalization](03-SAMPLE-BASED-QUANTUM-DIAGONALIZATION.md) — execute a
   real CPU → quantum sampler → classical eigensolver QCSC workflow.

Each tutorial explains what runs locally, what consumes remote QPU time, where credentials enter,
which files constitute the result, and how the same work maps onto Slurm/Apptainer.
