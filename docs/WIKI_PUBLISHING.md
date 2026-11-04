# Quantum Workflows Wiki publishing and editorial contract

These reviewed `docs/wiki/` Markdown sources are copied to GitHub's independent native `.wiki.git` repository only after a merged documentation PR. Initialise the native wiki if necessary, then `bash scripts/publish-github-wiki.sh --dry-run` to review and `bash scripts/publish-github-wiki.sh` to commit/push using normal secure Git authentication. The script preserves unrelated pages.

ArchWiki-inspired style: task-oriented names and concise context, prerequisites, commands that actually match the source branch, known-failure sections, source links, warnings beside expensive/sensitive actions, clear implemented versus planned status. Scientific claims additionally require units, independent baselines, numerical convergence, uncertainty and provider/hardware disclosures.

Guide/agent indexing must retain experiment identifier, framework/versions, backend applicability, source commit, status, prerequisite level and scientific validity caveats. A proposed curriculum item is not a runnable notebook; a tutorial is not a hardware entitlement; a job completion is not scientific proof.

## Automatic publishing from `dev`

After review and merge of `.github/workflows/publish-github-wiki.yml` to `dev`, changing `docs/wiki/` on `dev` validates the versioned Guide index and publishes managed Markdown pages to this repository's separate native GitHub Wiki. The job uses the built-in short-lived GitHub Actions `GITHUB_TOKEN` with `contents: write` and `gh auth setup-git`, a dry-run, and GitHub's native Wiki Git remote. No vendor LLM API token or personal GitHub PAT is normally required.

**Initialize once:** in GitHub repository Settings → General → Features, enable Wikis; open Wiki → Create the first page → save a `Home` page. Otherwise the `.wiki.git` remote does not yet exist and the job fails. Run only after reviewed changes reach `dev`, and verify the workflow result plus actual Wiki Home/sidebar. This publishes **development documentation**, not independently verified production status.

You may also publish manually: authenticate with `gh auth login` / `gh auth setup-git`, check out `dev`, then run `bash scripts/publish-github-wiki.sh --dry-run` followed by `bash scripts/publish-github-wiki.sh`. `workflow_dispatch` is declared but GitHub's Actions UI may not expose manual runs until the workflow is also present on the default branch. Changes to unrelated native Wiki pages are preserved by this script; roll back via reviewed `dev` documentation or the native Wiki Git history. Repositories can restrict Actions token permissions, in which case review the job failure before changing credential strategy.
