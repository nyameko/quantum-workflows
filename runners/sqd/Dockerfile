FROM python:3.14-slim-bookworm

ARG VCS_REF=unknown
LABEL org.opencontainers.image.title="quantum-workflows SQD runner" \
      org.opencontainers.image.source="https://github.com/nyameko/quantum-workflows" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=1

RUN apt-get update && \
    apt-get install --yes --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd --gid 1000 runner && \
    useradd --uid 1000 --gid runner --create-home runner

WORKDIR /opt/quantum-workflows
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --upgrade pip && \
    python -m pip install '.[sqd,ibm,qrmi-ibm]'

USER runner
WORKDIR /work
ENTRYPOINT ["qw"]
CMD ["sqd", "--help"]
