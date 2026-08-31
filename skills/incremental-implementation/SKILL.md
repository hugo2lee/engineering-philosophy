---
name: incremental-implementation
description: Deliver an approved change through small vertical slices that combine user-visible business value, the minimum architectural enabler, compatibility steps, and frequent verification. Use for migrations and cross-boundary features; not for unclear requirements or active failure diagnosis.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "implementation"
---

# Incremental Implementation

## Use this Skill when

Use this Skill for refactors, migrations, new features spanning layers, dependency replacement, or any change whose full implementation would be difficult to verify in one step.

Do not use it to postpone requirement decisions, or to build an entire platform before one business path demonstrates the need.

## Vertical Slice

A slice is not merely a layer or file group. It is:

```text
Vertical Slice = Business Value + Just-enough Architecture + Verification
```

Each slice should exercise a real path. It may contain a user-visible behavior and the minimum Architectural Enabler required to support it, such as a small Rule model, Trigger matcher, or Action executor. The enabler must be justified by demonstrated change pressure.

Example:

```text
Business: Temperature Trigger → Open Valve
Enabler: minimal Rule model + Trigger abstraction + Action abstraction
Verification: behavior test at the service boundary
```

## Operating model

1. Confirm the approved requirement and release behavior safety net.
2. Choose one real business path and name its boundary, dependency, and completion evidence.
3. Add the smallest compatible change and required enabler.
4. Run focused verification and relevant broader checks.
5. Keep old and new paths explicit while both exist.
6. Record new evidence and update the Feature Change Record and plan when the design changes.
7. Migrate the next slice only after the current slice is runnable and understandable.
8. Remove temporary compatibility code only after usage and verification prove it is safe.

## MUST

- Keep each slice independently understandable and verifiable.
- Preserve a working state between slices when practical.
- Make compatibility, fallback, and removal conditions explicit.
- Do not combine unrelated feature work with a migration.
- Verify behavior before deleting the old path.
- Do not silently drift from the approved requirement or plan.
- Do not keep adding conditionals after evidence shows a purposeful boundary is needed.

## SHOULD

- Prefer vertical slices over layer-by-layer speculative scaffolding.
- Add seams before replacing implementations.
- Use adapters, feature flags, dual reads, or staged writes only when their trade-offs are understood.
- Keep commits small enough to review and revert.
- Track temporary code and its removal condition in the Feature Change Record.

## Do not

- rewrite an entire subsystem before proving one path;
- leave two sources of truth without an explicit reconciliation plan;
- call a partial migration complete because it compiles;
- use a compatibility layer as a permanent architecture;
- create a complete Rule Engine, DDD model, or integration platform before its business pressure is demonstrated.

Read [vertical-slices.md](references/vertical-slices.md) for slice selection and [safe-change-sequencing.md](references/safe-change-sequencing.md) for migrations. Use the Feature Change Record from `engineering-philosophy` when discovery changes the plan.

## Routing

Use `change-planning` to define slices. Use `test-driven-development` inside each slice. Use `architecture-boundaries` or `ddd-lite` only when the slice reveals the corresponding pressure. Use `systematic-debugging` when a slice fails and `code-review-and-quality` before merging.

## Verification

For each slice record the behavior covered, architectural enabler, checks run, compatibility state, remaining risk, and condition for moving forward.
