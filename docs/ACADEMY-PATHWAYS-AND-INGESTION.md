# Zero-to-Hero Academy: pathway design and notebook ingestion (RFC)

Status: **proposed / not yet published**. Keep existing `labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb` as the canonical working starting point until any new notebooks pass repository review.

## Purpose

One scientific intent, many possible execution targets. A student asks “I want to learn quantum error correction”, not “show me all notebooks”. The system selects or proposes a flexible **prerequisite graph** of lectures, readable references, exercises, executable notebooks, assessments and research opportunities. The scientific content remains independently usable without a running agent.

## Staged teaching corpus (source archives prepared separately)

A staged external **87-notebook** academy was prepared for review, but **those notebooks are not yet committed by this RFC**:

| Proposed namespace | Count | Scope |
| --- | ---: | --- |
| `labs/02-zero-to-hero/` | 24 | Foundations, Bell, Grover, VQE, HHL, Ising/Trotter, modality introductions, comparisons |
| `labs/03-zero-to-hero-qec/` | 29 | Noise, stabilisers, Steane/surface/CSS/QLDPC, bicycle codes, erasures, bosonic codes, magic states, logical ISA |
| `labs/04-zero-to-hero-photonics/` | 34 | Classical optics, lasers, SLMs, propagation, nonlinear optics, detectors, DV/CV photons, QKD, teleportation |

Do not count them as deployed or scientifically approved. Keep repository-local import and rigorous review in a **separate implementation PR** to avoid hiding a large code change behind this architecture RFC. Check scientific assumptions, dependencies, licensing and copyright, lab solutions, code style, kernel versions and reproducibility. Maintain backward compatibility with `labs/01`.

### Proposed modules after those three sets

- Advanced theory / fault tolerance: complexity, Gibbs sampling, Hamiltonian learning and validation, Stim/PyMatching/BP+OSD, QLDPC logical operations, tricycle/CCZ proposals, bosonic error correction, magic-state resource estimation.
- Cross-modality QRE: superconducting, trapped-ion analogue/digital, neutral-atom analogue/digital, semiconductor spins, discrete- and continuous-variable photonics, annealing, cavities, networked qubits; count sources, gates, pulses, photons/modes, loss, decoder costs, time, wall-plug energy.
- Logical/physical ISA: typed capability contracts, unsupported-operation rejection, provenance and estimators, QIR/OpenQASM/QRMI/QDMI integration where appropriate, no false promise that every analogue/CV/annealing device supplies an error-corrected qubit.
- Research reproduction track: published numerical figure, independent classical reference, uncertainty and limitations, GPU/QPU resources when approved.

## Suggested pathway graph

```text
QEC interest
 -> [optional: quantum linear algebra] -> Bell measurement
 -> noise channels -> repetition code -> stabilisers
 -> CSS/Steane -> surface-code syndrome -> decoder
            \-> QLDPC + bicycle -> hardware-aware QEC
            \-> bosonic / erasure-aware -> photonics or cavities
 -> resource estimation -> logical ISA -> literature reproduction
```

Prerequisites are **recommendations** unless required for safety, authentic learning assessment or expensive-resource authorisation. A PI can fork/reorder/publish after review. Personalised pathways are revisions/references, not AI rewrites of immutable released notebooks.

## Versioned curriculum objects

An approved course pins `repo + commit_sha + module_path + environment/image digest + assessment version + literature identifiers`. Stable IDs survive file renames by an explicit migration map. Evaluation results are immutable, scoped to the learner and linked to an experiment manifest. Distinguish: draft, under-review, scientifically-approved, published and deprecated.

An agent may recommend/reorder. It cannot silently edit a published course, invent a citation, grade its own unreviewed exercise or fabricate notebook completion.

## Minimal R1 path (today's priority)

The existing `labs/01-intro-quantum-computing/Intro_QC_Demo.ipynb` is sufficient for initial proof:

1. Approved research user opens it in a regular Kubernetes/Jupyter workbench using a known dependency environment.
2. Run a small Bell-state experiment locally without secrets/QPU.
3. Save user-owned notebook copy and results in persistent research home with checksum, environment and source SHA.
4. Terminate that user's workbench only through approved infrastructure workflow; resume to the identical files.
5. Repeat execution and record verified provenance; verify other users cannot read private files.

This acceptance belongs across Quantum Platform and infrastructure. `quantum-workflows` provides the runnable scientific content and its manifest, not portal identity or Kubernetes deployment.

## Notebook contribution/validation contract

Every new lesson must include stable ID, audience, outcomes, prerequisites, theory/equations, native SDK details where relevant, credential-free local path, tests, seed, limits, assessment, real references, expected runtime/memory, result shape, environment spec and rights/licence. QPU/GPU usage is opt-in and must be separately authorised. An educational simulation cannot claim experimental hardware validation.

Validation gates before an 87-notebook merge: notebook syntax, isolated-kernel execution on pinned environment, deterministic numeric assertions, cross-platform CI budget, dependency audit, licensing, dataset/PII scan, course-manifest reference resolution and an instructor science review. Store large outputs and private datasets outside Git. Split coherent imports into modest PRs.

## Research/FAIR export

Future output objects should support persistent IDs, software/author attribution, ORCID/DOI, metadata, reproducibility manifests, citations and explicit licence/embargo policy (consider RO-Crate, CodeMeta, W3C PROV after review). AOSP/EOSC/GOSC alignment is a design goal, not a claim of technical federation or endorsement. Skills and agent context belong to ACP; enrolment and public course publication belong to Platform.

See the proposed example `catalog/paths/qec-foundations.yaml` for a safe draft that references the only currently-committed introductory notebook.
