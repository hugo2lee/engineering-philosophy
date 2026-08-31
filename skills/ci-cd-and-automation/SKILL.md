---
name: ci-cd-and-automation
description: Design or verify proportional build, test, baseline, artifact, release, deployment, and post-deployment gates with failure evidence and stop conditions. Do not use it for branch, commit, or tag history.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "delivery"
---

# CI/CD and Automation

## Use this skill when

Use this Skill when adding or changing automated checks, build pipelines, release workflows, deployment verification, or failure handling. It protects delivery evidence; a green pipeline does not by itself prove every business decision is correct.

Do not invent provider-specific configuration without repository evidence. Keep project-specific commands in project rules or pipeline files.

## Gate sequence

1. **Behavior and baseline gate** — run focused behavior tests and establish or verify the applicable service, persistence, outbound, and inbound baselines.
2. **Change Review / Gate 3 handoff** — consume the review result only after the implementation is runnable, relevant tests are green, applicable baselines exist, and requirement/plan deviations are recorded.
3. **Quality gate** — run formatting, static analysis, unit/integration tests, validation, and build checks appropriate to the repository.
4. **Artifact gate** — verify the exact package, image, source revision, version, and metadata that will be deployed or published.
5. **Deployment gate** — verify the target environment, health checks, compatibility, and rollout evidence.
6. **CI / Artifact / Release Verification / Gate 4** — publish only when the prior gates pass, the verified artifact identity is recorded, and stop or rollback conditions are defined.

## MUST

- Keep required checks deterministic enough to diagnose.
- Fail when a required gate fails and retain actionable logs or artifacts.
- Verify the artifact produced by the pipeline, not only the source checkout.
- Ensure release behavior baselines are present, passing, or intentionally updated with authorization.
- Do not treat Gate 3 as complete when a required baseline is scheduled for after review.
- Define what happens after a failed deployment or health check.
- Stop release when the artifact identity, version, baseline, or required evidence does not match.
- Keep secrets and environment-specific policy out of general Skill instructions.

## SHOULD

- Run fast checks before slower integration or deployment checks.
- Separate build, test, package, deploy, and post-deploy verification responsibilities.
- Make flaky checks visible and track their removal.
- Prefer a reversible rollout when failure cost is high.
- Preserve the evidence needed for `systematic-debugging` when a job fails.

## Do not

- treat a green pipeline as proof of all business correctness;
- delete or weaken a baseline to make the pipeline green;
- hide failures through retries without measuring the underlying cause;
- deploy an artifact different from the one verified;
- encode a project-specific provider assumption as a global rule;
- define product semantics in CI configuration.

Read [quality-gates.md](references/quality-gates.md) for check design and [release-verification.md](references/release-verification.md) for artifact and deployment verification.

## Routing

Use `code-review-and-quality` to inspect pipeline changes, `git-workflow-and-versioning` for release history and tag mechanics, and `systematic-debugging` for failed jobs or deployments. Use `test-driven-development` references when a missing baseline is a behavior gap.

## Verification

Gate 4 is ready when required checks, release baselines, failure evidence, artifact identity, deployment verification, and rollback or stop conditions are demonstrably defined. The handoff must distinguish verified facts from residual operational uncertainty.
