# Changelog

## Unreleased

### Changed

- Removed the hard-coded 12-Skill publication count from repository validation. Published Skill cardinality is now derived from `skills/registry.yaml`, with a regression test proving that a matching 13-Skill discovered/active set is valid.

## v0.4.0 - Continuous Knowledge Compilation

### Added

- Added the `knowledge-compilation` Skill as the twelfth top-level Skill for repository evidence discovery, artifact classification, knowledge reconciliation, provenance, candidate/active lifecycle, registration, and retirement.
- Added the generic Knowledge Compilation Lifecycle and the Source, Reference, Evidence, Decision, Generated Artifact, and Skill taxonomy.
- Added candidate promotion, generated Skill sidecar records, canonical-source precedence, redaction, project/global promotion, and registry contracts.
- Added machine-validatable knowledge registry and generated Skill record sidecar schemas with executable Draft 2020-12 validation.
- Added 12 knowledge-compilation specialist eval cases and 31 knowledge lifecycle eval cases covering owner reuse, Skill explosion, provenance, source conflicts, redaction, write scope, candidate isolation, frontmatter compatibility, and project/global leakage.

### Changed

- Bumped all 12 Skill metadata versions to `0.4.0`.
- Added `skills/registry.yaml` as the intended published Skill surface and made validation, deployment, and smoke tests share the registry-driven discovered/active/published Skill-set contract.
- Extended engineering-philosophy routing for repository knowledge evolution while keeping ordinary feature work on its focused Skills.
- Added candidate-path isolation rules so lifecycle candidates cannot be silently installed by runtimes that discover every `SKILL.md`.
- Added registry owner, verification, generation, and promotion contracts plus valid/invalid schema fixtures.

### Design intent

v0.4.0 defines a project-neutral protocol for continuously turning repository evidence into governed, discoverable Agent knowledge. It does not implement a universal crawler, bot, RAG platform, automatic global promotion, or any project-specific executor.

## v0.3.0 - Evidence-Driven Feature Lifecycle

### Added

- Added a six-principle evidence-driven feature lifecycle covering Requirement Contract, Requirement Reconciliation, Repository Analysis, evolutionary architecture, vertical slices, and executable release baselines.
- Added proportional Gate 1 Requirement Approved, Gate 2 Ready for Implementation, Gate 3 Ready for Review, and Gate 4 Ready for Release decisions.
- Added Feature Change Record guidance and a project-local `docs/changes/<feature-name>.md` template with service, persistence, outbound, and inbound release baselines.
- Added requirement reconciliation references for New, Overlap, Duplicate, Compatible Extension, Conflict, and Replacement classifications.
- Added repository impact analysis, change-plan, dependencies/risk, and architecture pressure/enabler references.
- Added release behavior baseline guidance distinguishing service behavior, persistence integration, outbound contract, and inbound mapping evidence.
- Added 30 machine-readable lifecycle eval cases covering clarification, reconciliation, repository analysis, architecture pressure, slices, baselines, debugging, review, and release gates.
- Added a root `VERSION` file and version consistency checks for all 11 Skills, README, CHANGELOG, and optional tag context.
- Added the v0.3.0 migration note for the two Skill renames and the public repository identity.

### Renamed

- Renamed `spec-driven-development` to `requirement-engineering`.
- Renamed `planning-and-task-breakdown` to `change-planning`.
- Updated repository-facing installation documentation to the public `engineering-philosophy` repository identity.

### Changed

- Kept exactly 11 top-level Skills and did not create a C++ Skill or additional security, observability, or ADR Skill.
- Updated `engineering-philosophy` to route the full lifecycle without copying specialist Skill details.
- Updated architecture guidance to require demonstrated change pressure and a smallest useful architectural enabler.
- Updated DDD guidance to reconcile domain behavior with existing releases and remain conditional rather than becoming a default architecture template.
- Updated incremental implementation to combine Business Value, Just-enough Architecture, and Verification in runnable slices.
- Updated TDD and debugging guidance to protect released behavior baselines and forbid unauthorized baseline weakening.
- Updated review guidance to compare requirement, plan, diff, baselines, and evidence, while allowing recorded plan evolution.
- Updated Git and CI/CD guidance to preserve release traceability, artifact identity, failure evidence, and stop conditions.
- Updated validation, deployment, smoke-test, routing, README, release checklist, and CHANGELOG for the v0.3 contract.
- Generalized public documentation, attribution, and review language so the Skill Suite is presented as an industry-wide engineering reference rather than an author's personal methodology.

### Design intent

This release makes feature delivery evidence-driven without turning every small change into a documentation project. The system should clarify behavior, reconcile it with what users already have, inspect the repository before planning, introduce architecture only under demonstrated pressure, and freeze important released behavior as executable evidence.

## v0.2.1 - CI-Gated Automated Releases

### Added

- Added a CI-gated GitHub Release workflow for future stable tags.
- Added release-job checks for the exact tag and source commit.

## v0.2.0 - Reliable Routing & Distribution

### Added

- Added an explicit-only `engineering-philosophy` governance and routing entrypoint.
- Added discriminating discovery descriptions for all 11 Skills, with primary decision ownership and exclusions.
- Added `skills/engineering-philosophy/references/routing-matrix.md` with primary, secondary, forbidden, and escalation guidance.
- Added 30 machine-readable routing eval cases with 12 Chinese, 12 English, and 6 mixed-language prompts, including negative routing cases.
- Added the C++ boundary realization reference under `architecture-boundaries` without creating a C++ top-level Skill.
- Added a GitHub Actions validation workflow and an isolated `npx skills` discovery/installation smoke test.
- Added a maintainer release checklist covering validation, versioning, tags, GitHub Releases, and post-release installation verification.

### Changed

- Bumped all Skill metadata versions to `0.2.0`.
- Made `skills-ref` the standards-level validator and retained repository-specific validation plus the bundled skill-creator check as supplemental coverage.
- Made `~/.agents/skills` the default shared Codex/Cline destination in `deploy.sh`; explicit root flags remain available for legacy or isolated layouts.
- Reframed `deploy.sh` as a maintainer local-development helper while making `npx skills@latest` the ordinary user installation path.
- Reworked the README around quick start, routing, verification, updates, contributor workflow, and releases.

### Design intent

This release improves selection and distribution reliability without increasing the 11-Skill surface area. The routing matrix is guidance rather than a mandatory full workflow, and negative cases protect against activating DDD, architecture, planning, or delivery ceremony from incidental keywords alone.

## v0.1.0 - Initial Skill Suite

### Added

- Added engineering-philosophy as the governance and routing entrypoint.
- Added architecture-boundaries with pragmatic Ports and Adapters, dependency inversion, explicit dependency injection, test seams, and Go references.
- Added ddd-lite with invariant-first modeling and conditional DDD decisions.
- Added test-driven-development with a behavior-first Red-Green-Refactor loop.
- Added systematic-debugging with reproduction, evidence, hypotheses, minimal fixes, and regression verification.
- Added spec-driven-development, planning-and-task-breakdown, and incremental-implementation for the front half of the delivery workflow.
- Added code-review-and-quality, git-workflow-and-versioning, and ci-cd-and-automation for the delivery and verification stages.
- Added independent eval cases for every Skill.
- Added static validation and safe copy-based deployment scripts for Cline, Codex, and OpenClaw.

### Design intent

This release establishes a portable personal engineering baseline. It favors meaningful boundaries over mechanical abstractions, conditional use of heavyweight patterns, explicit verification, and small reversible changes.

The suite intentionally does not include C++, security-hardening, observability, documentation-and-ADRs, or an Agent-specific automatic eval runner.
