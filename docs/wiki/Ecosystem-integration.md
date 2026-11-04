# Integration with the five-repository platform

```text
Quantum Platform (identity, programmes, entitlements, UI)
  -> Infra (Kubernetes/JupyterHub, Slurm, GPU nodes, storage, GitOps)
  -> Quantum Workflows (native SDK notebooks, reviewed runners, artifacts)
  -> result catalog / platform ExecutionRecord
ACP (durable project, chat, skills, task references) points to the same work
PhotonicsLab (optical source/bench and detectors) exports validated experiments
  -> Quantum Workflows adapter/runner -> provenance + results
```

Do not replicate user identity, group membership, resource quotas or provider credentials inside `quantum-workflows`. Do not copy science equations and datasets into ACP's task manager. Agents can recommend approved notebook references but execution requires an independent Platform entitlement and runner.

## Science skill references

Current `catalog/agent-skills/` items are **inert reviewed resource candidates**, not automatically executable code or a new SDK. A notebook link can open learning material; an approved job submission is a separate action with its own audit and policy.

## PhotonicsLab

The PhotonicsLab adapter example currently emits artifacts using the actual `RunArtifacts` API when both packages are installed; it is not a registered `qw photonicslab` subcommand or deployed portal offering. A planned coupling must preserve optical physics assumptions and independent validation.

References: [ACP integration](https://github.com/nyameko/quantum-workflows/blob/main/docs/agent-control-plane-integration.md), [M4 reviewed skills](https://github.com/nyameko/quantum-workflows/blob/main/docs/M4-REVIEWED-SCIENCE-SKILLS.md), [PhotonicsLab adapter](https://github.com/nyameko/photonicslab/blob/main/examples/quantum_workflows_polarization.py).