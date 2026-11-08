# Candidate builder for the first batch-first GPU runner; test on the actual facility.
# Build/publish by a reviewed workflow; promote by immutable OCI digest, then
# convert to a SIF on the execution site. Never use :latest for scientific runs.
FROM python:3.14-slim-bookworm
ARG VCS_REF=unknown
LABEL org.opencontainers.image.title="quantum-workflows Aer GPU batch runner" \
      org.opencontainers.image.source="https://github.com/nyameko/quantum-workflows" \
      org.opencontainers.image.revision="${VCS_REF}"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN python -m pip install --no-cache-dir \
    'qiskit>=2.5,<3' 'qiskit-aer-gpu==0.18.2'
RUN useradd --create-home --uid 1000 runner
COPY runners/qiskit-aer-gpu/aer_gpu_run.py /opt/quantum-workflows/aer_gpu_run.py
USER runner
WORKDIR /work
ENTRYPOINT ["python", "/opt/quantum-workflows/aer_gpu_run.py"]
