# Quantum Workflows Wiki publishing and editorial contract

These reviewed `docs/wiki/` Markdown sources are copied to GitHub's independent native `.wiki.git` repository only after a merged documentation PR. Initialise the native wiki if necessary, then `bash scripts/publish-github-wiki.sh --dry-run` to review and `bash scripts/publish-github-wiki.sh` to commit/push using normal secure Git authentication. The script preserves unrelated pages.

ArchWiki-inspired style: task-oriented names and concise context, prerequisites, commands that actually match the source branch, known-failure sections, source links, warnings beside expensive/sensitive actions, clear implemented versus planned status. Scientific claims additionally require units, independent baselines, numerical convergence, uncertainty and provider/hardware disclosures.

Guide/agent indexing must retain experiment identifier, framework/versions, backend applicability, source commit, status, prerequisite level and scientific validity caveats. A proposed curriculum item is not a runnable notebook; a tutorial is not a hardware entitlement; a job completion is not scientific proof.