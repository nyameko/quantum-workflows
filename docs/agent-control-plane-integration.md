# Agent Control Plane integration boundary

Phase 1 introduces administrative infrastructure diagnostics. It does not execute
quantum workflows or grant an administrative profile access to provider tokens.
This documentation extension preserves the current scientific runners and their
result manifests while defining their later integration seam.

A future platform job submission will authorize a user/programme and a versioned
workflow/configuration. The control plane may help prepare the request; a typed
execution adapter will submit through Kubernetes/Slurm/provider integration under
that authority. The workflow remains usable from its CLI without an agent service.

Keep four identifiers distinct: platform scientific job ID, ACP task/run UUIDs,
scheduler/provider job IDs, and the workflow's experiment ID. Store their mapping
in the platform/adapter ledger. A chat summary is not scientific provenance.
Existing RunArtifacts manifests provide a place to reference source versions,
parameters, executor, circuit metadata and output checksums; any correlation field
added later must be optional and must not be treated as authorization.

Before enabling submission, define allowlisted workflow names and parameter
schemas, pinned runner images, resource quotas, cancellation, idempotency,
provider-secret injection and output redaction. Validate the manifest's source
commit against the actual checked-out workflow repository, and test whether error
messages or environment-derived metadata can disclose secrets. The current writer
updates a manifest during execution; publish a finalized immutable artifact only
once the experiment completes, retaining failed-run evidence too.

Keep workflow, agent and infrastructure evaluations separate. An agent-generated
circuit still needs scientific validation, reference results, seeds/precision and
hardware/provider metadata. A successful agent run does not prove a scientifically
correct result. QPU credentials and entitlement checks remain with the platform
and provider adapters, not gptel buffers or shared Hermes memory.

See [the integration review](https://github.com/nyameko/agent-control-plane/blob/main/docs/14-integration-review.md)
for the staged roadmap, and [Phase 1](https://github.com/nyameko/agent-control-plane/blob/main/docs/12-phase1.md)
for the currently executable scope.
