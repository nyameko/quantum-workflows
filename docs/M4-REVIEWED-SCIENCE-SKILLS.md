# M4d seed catalogue — reviewed scientific skill references, not executable agent grants

This **proposed** data-only catalogue provides two narrow, reviewed-source references
to existing `quantum-workflows` runners. No ACP runtime ingestion, model/tool
capability, scheduler submission or production activation is included.

## Ownership and use

- `quantum-workflows` owns the science implementations, input semantics, teaching
  notebooks and result provenance. `qw hello` and `qw cpu-smoke` already exist.
- The immutable source Git commit and manifest hash are required in any downstream
  ACP M4d registry binding; a mutable branch name alone is insufficient.
- ACP owns **authorization** of any enabled skill, user/project binding and
  tool capabilities. A JSON record here is **not** an authorization grant.
- Quantum Platform owns approved user and programme permissions, execution
  entitlements and the researcher UI. Slurm/provider owns the physical job.
- `fixed_arguments` are argv tokens, not a shell command or prompt; do not
  evaluate or interpolate them. Validation uses the already shipped `qw`
  argument parser. Path references may never be used to read arbitrary files.
- Downstream adapters must pin the runner OCI digest, enforce allowlisted
  parameters/quotas, run without provider tokens for these samples and record
  Platform execution ID, ACP task/run UUID, Slurm job ID (if used) and workflow
  experiment ID **as distinct references**.
- `status: proposed` and `remote_execution_enabled: false` mean these
  records are visible for review only. No agent may enable or invoke them
  on cluster resources until approved integration PRs and policy tests pass.

## First end-to-end product demonstration

A researcher asks Quantum Guide to explain Bell-state correlations; Guide
identifies `research.bell-aer`, links the existing intro notebook, and offers
a local/reviewed runner. When an approved scientific execution adapter is
available, the user may request a typed run, see its genuine progress, and
inspect source commit, seeds, circuit, measured counts, correlation and result
checksums. A refusal or missing adapter must be shown plainly.

Do not claim a notebook run completed just because this catalogue entry exists.
Do not equate a valid manifest with a scientifically correct result.
