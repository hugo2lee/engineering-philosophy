---
name: git-workflow-and-versioning
description: Manage scoped branches, traceable commits, versions, tags, changelogs, and release history for evidence-driven feature delivery. Do not use it for CI pipeline design or code correctness review.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "delivery"
---

# Git Workflow and Versioning

## Use this skill when

Use this Skill when creating commits, preparing a branch, describing a release, updating a changelog, or deciding how to preserve a clean and reviewable history. It connects the release artifact to the Feature Change Record and verification evidence; it does not replace review or CI design.

## Traceability chain

A meaningful feature release should be traceable through:

```text
Requirement Contract
    -> Feature Change Record
    -> source diff and behavior baselines
    -> CI and artifact evidence
    -> commit
    -> version/tag/release notes
```

If an item is not applicable, record why. Do not manufacture a tag or release merely to complete a checklist.

## Operating rules

1. Confirm the current branch, remote, and working tree.
2. Keep branch scope aligned with the approved change.
3. Group related changes into atomic, reviewable commits.
4. Write commit messages that explain behavior and intent.
5. Review the diff and verification evidence before committing.
6. Keep version, Skill metadata, README, CHANGELOG, and release identity consistent.
7. Record why a meaningful engineering rule, baseline, or workflow changed.
8. Preserve old released tags; never move or rewrite immutable release history.

## MUST

- Do not discard user changes or use destructive Git commands without explicit authorization.
- Keep unrelated formatting and cleanup out of the task branch.
- Make commits internally coherent and traceable to the change record.
- Ensure the changelog describes user-visible behavior and design intent.
- Do not create a tag or GitHub Release before the intended release commit and required CI evidence exist.
- Verify that the tag, artifact, and release notes refer to the same source commit.

## SHOULD

- Prefer one behavior or migration step per commit.
- Mention verification in the commit or handoff summary.
- Use patch, minor, and major version changes consistently with compatibility impact.
- Keep release checklists explicit about pending manual actions.
- Use annotated tags for stable releases.

## Versioning

- **PATCH** — wording, examples, ambiguity removal, or non-decision-changing corrections.
- **MINOR** — new rules, references, eval cases, or capabilities that preserve the philosophy.
- **MAJOR** — a change to a core engineering principle or a breaking public workflow.

Read [branches-and-commits.md](references/branches-and-commits.md) for history shape and [history-hygiene.md](references/history-hygiene.md) for safe cleanup and release notes.

## Routing

Use `code-review-and-quality` before committing a meaningful change. Use `ci-cd-and-automation` for quality gates, artifact verification, and release automation. Use `systematic-debugging` for failed checks. Use `engineering-philosophy` when deciding whether a local observation should become a global rule.

## Verification

Before handoff, show the branch, diff summary, requirement/record traceability, tests and baselines, commit scope, version impact, changelog update, and whether tag/release actions are pending or complete.
