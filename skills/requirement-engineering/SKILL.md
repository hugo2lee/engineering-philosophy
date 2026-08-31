---
name: requirement-engineering
description: Turn a feature request into a proportional Requirement Contract, reconcile it with existing requirements, capabilities, baselines, and released behavior, and stop for user decisions when product behavior conflicts. Do not force full ceremony on obvious safe edits.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "planning"
---

# Requirement Engineering

## Use this Skill when

Use this Skill when a request introduces or changes behavior, has ambiguous acceptance, crosses existing capabilities, may conflict with released behavior, or carries a material product decision.

Use a lightweight clarification for a small, explicit, low-risk change. Do not manufacture a long contract when the desired behavior, scope, and verification are already clear.

## Requirement Contract

Clarify the smallest contract that makes behavior testable:

- Goal
- Inputs
- Outputs
- Observable Behavior
- Error Behavior
- Scope
- Acceptance Criteria
- Non-goals

Separate repository facts, user-provided requirements, assumptions, and unresolved decisions. A requirement is not approved merely because an implementation idea exists.

## Requirement Reconciliation

Before approving a meaningful change, compare the request with:

- related existing requirements;
- existing implemented behavior;
- existing service capabilities and contracts;
- existing baseline tests;
- behavior already released to users.

Classify each relationship as **New**, **Overlap**, **Duplicate**, **Compatible Extension**, **Conflict**, or **Replacement**. Record compatibility impact, migration impact, and which artifact proves the accepted behavior.

The newer request does not automatically override released behavior. The agent may discover and explain a conflict, but it must not silently choose product semantics.

## User Decision Gate

If materially different behaviors are possible, stop planning and present:

```text
Existing behavior
New requirement
Conflict
Compatibility impact

Option A
Trade-offs

Option B
Trade-offs

Option C, when useful
Trade-offs

Decision required from user
```

Do not route to implementation until the user decision is recorded or the conflict is explicitly removed from scope.

## Gate 1 — Requirement Approved

The requirement is ready for planning only when the applicable checks are true:

```text
[ ] Goal, inputs, outputs, observable behavior, and errors are clear
[ ] Scope, acceptance criteria, and non-goals are clear
[ ] Existing requirements, behavior, capability, and baselines were checked
[ ] Overlap, duplication, conflict, and replacement relationships are classified
[ ] Compatibility impact is understood
[ ] Material user decisions are resolved
```

If a major product decision remains open, report `NOT READY FOR PLANNING` and ask only the smallest question needed to proceed.

Read [requirement-contract.md](references/requirement-contract.md) for contract shape, [requirement-reconciliation.md](references/requirement-reconciliation.md) for comparison rules, and [user-decision-gates.md](references/user-decision-gates.md) for decision output.

## Proportionality

For a typo, obvious configuration edit, or safe documentation change, state the lightweight acceptance check and proceed. The full reconciliation record is for meaningful behavior, compatibility, migration, or release changes.

## Routing

Route an approved requirement to `change-planning`. Route repository and change-pressure questions to `change-planning` and `architecture-boundaries` as appropriate. Route business invariants to `ddd-lite`, implementation behavior to `test-driven-development`, and actual failures to `systematic-debugging`.

## Verification

A requirement is approved when another engineer can identify the intended behavior, compatibility decision, non-goals, and acceptance evidence without guessing product intent.
