---
name: code-review-and-quality
description: Review a feature against its requirement contract, change plan, actual diff, release baselines, regressions, and verification evidence before merge or handoff. Do not use it as the primary Skill for live failure diagnosis or new implementation planning.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "quality"
---

# Code Review and Quality

## Use this skill when

Use this Skill before merging, handing off, or declaring a meaningful change complete. It reviews the evidence chain from approved behavior to implementation and release readiness; it is not a substitute for requirement clarification, planning, or live failure diagnosis.

## Review contract

Compare these artifacts rather than reviewing the diff in isolation:

1. Requirement Contract and reconciliation decision;
2. Implementation Plan and Feature Change Record;
3. actual diff and surrounding code;
4. behavior tests and the applicable release baselines;
5. build, CI, artifact, and deployment evidence.

## Review order

1. Confirm the requested behavior, compatibility decision, and non-goals.
2. Check whether the implementation matches the requirement and whether the plan evolved with evidence.
3. Check correctness, state transitions, errors, and important edge cases.
4. Check dependency direction and meaningful boundaries.
5. Check whether the smallest useful architecture was used or unnecessary abstractions were added.
6. Check service, persistence, outbound, and inbound baselines where applicable.
7. Check regression risk, scope creep, unapproved behavior changes, and missing release evidence.
8. Report findings by severity with location, impact, recommendation, and evidence.

## MUST

- Review the actual diff and relevant surrounding code.
- Identify a mismatch between requirement, plan, diff, and baseline as a review finding.
- Treat silent plan drift, unrecorded architecture changes, and unapproved behavior changes as blocking until reconciled.
- Distinguish blocking defects from suggestions.
- Verify claims with tests, reproduction, or direct evidence.
- Check that the change stays within scope.
- Complete Gate 3 only when the implementation is runnable, relevant behavior tests are green, applicable Release Behavior Baselines are established, requirement/plan deviations are recorded, the Feature Change Record is updated when applicable, and remaining uncertainty is visible.

## SHOULD

- Review high-risk behavior and boundaries before stylistic details.
- Look for missing regression tests and weakened baselines.
- Prefer an evidence-backed, actionable finding over a speculative redesign.
- Allow a plan to evolve when the Feature Change Record explains the evidence and the affected gate is rechecked.
- State what was checked and what was not.

## Do not

- approve because tests are green without checking behavior;
- reject a change only because it differs from subjective taste;
- request an interface or pattern without concrete change pressure;
- mix unrelated cleanup into a required fix;
- delete a failing baseline to make CI green;
- claim security, performance, or compatibility properties that were not evaluated.

Read [review-rubric.md](references/review-rubric.md) for finding quality and [verification.md](references/verification.md) for evidence.

## Routing

Route requirement mismatch to `requirement-engineering`, planning or repository-analysis gaps to `change-planning`, architecture findings to `architecture-boundaries` or `ddd-lite`, missing behavior tests to `test-driven-development`, and an observed defect to `systematic-debugging`. Route merge and release concerns to `git-workflow-and-versioning` and `ci-cd-and-automation`.

## Verification

Gate 3 is ready only after the baseline is established and each finding has severity, location, impact, recommendation, and evidence; the summary states contract/plan/diff/baseline alignment, residual risk, checks performed, and any explicit follow-up.
