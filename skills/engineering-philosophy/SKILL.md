---
name: engineering-philosophy
description: Govern evidence-driven feature changes, reconcile requirements with released behavior, route decisions to the smallest focused Skill, and keep global principles separate from project rules. Use as an explicit governance entrypoint, not as a mandatory prelude for every task.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "engineering-governance"
---

# Engineering Philosophy

## Use this Skill when

Use this Skill as an explicit governance and routing entrypoint when:

- a request spans requirements, repository understanding, architecture, implementation, verification, and release;
- it is unclear which specialist Skill owns the main decision;
- a new requirement may conflict with existing capability or released behavior;
- a project rule may be mistaken for a global engineering principle; or
- repository evidence should be reconciled into maintained Agent knowledge or a project/global promotion decision; or
- the process should be lighter or heavier based on risk.

Ordinary architecture, domain, testing, debugging, review, Git, and CI requests should go directly to their specialist. Do not turn the lifecycle into mandatory paperwork for a typo, an obvious safe edit, or a small configuration change.

## Core principle

> Prefer the simplest architecture that preserves meaningful boundaries.

The six principles below govern meaningful feature changes:

1. **Clarify business behavior before designing implementation.** Establish the goal, inputs, outputs, observable behavior, error behavior, scope, acceptance criteria, and non-goals before proposing services, repositories, interfaces, or patterns.
2. **Reconcile new requirements with released behavior.** A newer request does not automatically override an existing contract, baseline, or released behavior. Discover conflicts and let the user decide materially different product behavior.
3. **Read before design.** Inspect the existing entry points, capabilities, domain behavior, persistence, outbound dependencies, tests, baselines, architecture, constraints, and related requirements before planning a meaningful change.
4. **Derive architecture from demonstrated business and change pressure.** Move from business requirement to change pressure to architecture requirement to decision. Architecture is conditional and cannot invent missing business semantics.
5. **Evolve business behavior and architectural enablers together.** A vertical slice may contain business value, the minimum architectural enabler needed to support it, and verification. Architecture grows with verified business pressure.
6. **Freeze accepted release behavior as executable baselines.** A released feature preserves its accepted behavior at stable boundaries through tests that future changes can run and review.

## Rule levels

Use these levels consistently:

- **MUST**: a stable engineering constraint. Violating it requires an explicit, high-quality reason.
- **SHOULD**: the default practice. A project may deviate when the reason, cost, and alternative are stated.
- **CONDITIONAL**: apply only when its trigger conditions are present. Never introduce a pattern by name alone.

For every important rule, explain:

1. Rule
2. Why
3. Do
4. Do not
5. Verification

## Feature Change Lifecycle

For a meaningful new feature, behavior change, migration, cross-boundary change, architecture-affecting change, or release-worthy behavior, use the smallest proportional form of this lifecycle:

```text
User Request
    ↓
Requirement Clarification
    ↓
Requirement Reconciliation
    ↓
User Decision Gate, when product behavior conflicts
    ↓
Approved Requirement Contract
    ↓
Repository Analysis
    ↓
Business Change / Impact Analysis
    ↓
Architecture Pressure Analysis
    ↓
Conditional architecture-boundaries / ddd-lite routing
    ↓
Implementation Plan
    ↓
Incremental Implementation
    ↓
TDD / Focused Verification
    ↓
Release Behavior Baseline
    ↓
Change Review / Gate 3
    ↓
CI / Artifact / Release Verification / Gate 4
    ↓
Version / Tag / Release
```

This is not a waterfall model. Documents and plans may evolve when new evidence appears, but implementation must not silently diverge from the Feature Change Record. Record the evidence, decision, and impact when the plan changes.

The four gates protect decisions, not paperwork:

- **Gate 1 — Requirement Approved**: behavior, scope, acceptance, existing behavior, baselines, conflicts, and material user decisions are resolved.
- **Gate 2 — Ready for Implementation**: repository analysis, impact analysis, architecture pressure, required decisions, implementation plan, and verification approach exist.
- **Gate 3 — Ready for Review**: the implementation is runnable, relevant behavior tests are green, applicable Release Behavior Baselines have been established, requirement/plan deviations are recorded, and the Feature Change Record is updated when applicable. Only then is the change reviewed against the approved contract.
- **Gate 4 — Ready for Release**: review, applicable baselines, integration checks, CI, Feature Change Record, and traceability are complete.

Read [feature-change-lifecycle.md](references/feature-change-lifecycle.md) for the detailed lifecycle and gates. Use [feature-change-record.md](references/feature-change-record.md) for the project-level record when the change justifies one. Route repository knowledge evolution to [knowledge-compilation](../knowledge-compilation/SKILL.md), which owns artifact classification, provenance, reconciliation, candidate activation, and retirement.

## Requirement decisions

The agent may discover and explain product conflicts, but it must not silently decide them. Classify the relationship between a request and existing behavior as **New**, **Overlap**, **Duplicate**, **Compatible Extension**, **Conflict**, or **Replacement**. If the difference changes user-visible behavior, compatibility, data meaning, or release promises, stop at a User Decision Gate and present options with trade-offs.

Do not weaken a release baseline merely to make an implementation pass. If behavior is intentionally changing, update the requirement decision, Feature Change Record, baseline, implementation, and release traceability together.

## Global versus project rules

Keep cross-project principles here. Keep project-specific facts in the project:

- language or framework versions;
- database, message broker, or cloud provider choices;
- repository layout and team naming conventions;
- hosting workflow and pipeline commands;
- domain-specific aggregates and terminology;
- mandatory test libraries and CI commands.

When a project rule conflicts with a global SHOULD, follow the explicit project rule and record the trade-off. Do not silently promote a local convention into universal doctrine.

## Routing behavior

Select the smallest set of Skills needed for the current decision:

- requirement ambiguity, reconciliation, or a material product decision → `requirement-engineering`;
- approved requirements plus repository and change planning → `change-planning`;
- demonstrated architecture pressure or dependency boundaries → `architecture-boundaries`;
- business invariants, lifecycle, or consistency boundaries → `ddd-lite`;
- large cross-boundary implementation → `incremental-implementation`;
- focused behavior implementation → `test-driven-development`;
- actual failure → `systematic-debugging`;
- requirement/plan/diff/baseline consistency → `code-review-and-quality`;
- history and release traceability → `git-workflow-and-versioning`;
- quality gates and release verification → `ci-cd-and-automation`.
- repository evidence that should update Agent knowledge → `knowledge-compilation`;
- project-to-global rule promotion → keep `engineering-philosophy` primary and use `knowledge-compilation` for provenance and eval evidence.

Use [routing-matrix.md](references/routing-matrix.md) for primary ownership, secondary collaboration, forbidden routing, and escalation conditions. The matrix is a decision aid, not a mandatory full workflow.

## Rule promotion

Do not promote an isolated workaround or project-generated Skill into global doctrine. Follow:

```text
Observation → Repeated Pattern → Candidate Rule → Eval Case → Real-project Validation → Global Rule
```

A rule may be promoted when the same pattern appears in two independent projects, a high-cost incident yields a general safeguard, or repeated reviews identify the same failure mode. Otherwise keep it as a project rule, ADR, or observation note.

Knowledge compilation uses the same boundary: generation defaults to project
scope, activation is gated, and project-to-global promotion is never an
automatic side effect.

Read [rule-lifecycle.md](references/rule-lifecycle.md) when changing the philosophy or promoting a rule. Read [global-vs-project.md](references/global-vs-project.md) when deciding where a rule belongs.

## Verification

Before declaring a meaningful change complete, identify evidence for the requirement, repository analysis, implementation behavior, release baseline, review, CI, and traceability claims. Never claim that a design is correct merely because it compiles, follows a familiar pattern name, or resembles a diagram.
