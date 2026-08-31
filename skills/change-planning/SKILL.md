---
name: change-planning
description: Plan an approved software change from repository evidence, existing capabilities, business changes, architecture pressure, dependencies, risks, vertical slices, and verification. Do not invent services or boundaries before inspecting the system.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "planning"
---

# Change Planning

## Use this Skill when

Use this Skill after a requirement is clear enough to plan and the change has multiple tasks, dependencies, repository impact, migration risk, or cross-boundary coordination.

Do not use it to bypass unresolved product decisions. Route those to `requirement-engineering` first. Use a short checklist for a trivial, explicit, safe edit.

## Read before plan

Inspect the existing system before choosing tasks or new abstractions:

- existing entry points;
- existing services and capability owners;
- existing domain behavior and invariants;
- persistence and migrations;
- outbound dependencies and adapters;
- existing tests and release baselines;
- current architecture and dependency direction;
- compatibility constraints and related requirements.

Do not invent a new Service, Port, Repository, Aggregate, or Adapter before checking whether an existing capability already owns the behavior. Reuse or extend the existing owner unless evidence shows that the boundary itself must change.

## Change analysis

Translate evidence into:

```text
Business Change
    ↓
Change Pressure
    ↓
Architecture Requirement
    ↓
Architecture Decision or minimum Enabler
```

Distinguish explicit architecture requirements from derived requirements. Architecture may protect a demonstrated change pressure; it may not supply missing business semantics.

## Implementation Plan

Organize work by behavior and boundary, not by a mechanical file list. Each step names:

- the behavior or capability it changes;
- the current owner and affected boundary;
- dependencies and compatibility state;
- the smallest vertical slice;
- focused and broader verification;
- completion evidence and remaining risk.

Prefer a business slice plus the minimum architectural enabler required to support it. Keep every stage runnable when practical, and record deviations when new evidence changes the plan.

## Gate 2 — Ready for Implementation

Planning is ready when the applicable items exist:

```text
[ ] Approved Requirement Contract
[ ] Repository and impact analysis
[ ] Business changes and architecture pressure
[ ] Required architecture or domain decisions
[ ] Ordered behavior-oriented implementation plan
[ ] Dependencies, risks, checkpoints, and completion criteria
[ ] Focused and broader verification approach
```

If the plan discovers a new product decision, return to `requirement-engineering` instead of hiding it in a task.

Read [repository-impact-analysis.md](references/repository-impact-analysis.md) for the evidence inventory, [change-plan.md](references/change-plan.md) for plan shape, and [dependencies-and-risks.md](references/dependencies-and-risks.md) for risk and checkpoint rules.

## Routing

Use `incremental-implementation` to execute large plans, `architecture-boundaries` when a real technical boundary is demonstrated, `ddd-lite` when business invariants require modeling, and `test-driven-development` for each behavior slice. Use `systematic-debugging` when a planned step fails.

## Verification

A plan is ready when implementation can proceed without inventing product semantics, repository structure, ownership, interfaces, or acceptance checks.
