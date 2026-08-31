---
name: ddd-lite
description: Model business behavior when invariants, lifecycle, consistency boundaries, domain language, or context translation need a decision; choose the smallest useful DDD pattern. Do not activate for simple CRUD or primarily technical boundaries, DI, or active failure diagnosis.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "domain-modeling"
---

# DDD Lite

## Use this skill when

Use this Skill when a feature has a business invariant, lifecycle, state transition, domain language, consistency boundary, domain event, or model translation problem. First decide whether the business pressure is real; DDD is an optional modeling response, not a default architecture template.

Do not use it for simple CRUD, a technical dependency boundary, DI, or an active failure that needs evidence first. A repository, service, or stateful record does not by itself justify DDD.

## Governing rule

Model the business pressure before naming a pattern. Choose the smallest domain structure that protects the invariant or consistency boundary, and record why a simpler structure is insufficient.

## Decision sequence

1. State the business capability in the user's language.
2. Identify the invariant, decision, lifecycle, or transition that must remain true.
3. Identify the owner and what must be consistent together.
4. Reconcile the requested behavior with existing requirements, implemented behavior, and release baselines.
5. Choose the smallest useful Entity, Value Object, Aggregate, Domain Service, Event, or Context boundary.
6. Keep application orchestration and infrastructure translation outside the domain model.
7. Define behavior tests and, where relevant, a release baseline for the invariant.
8. Re-check whether the model is simpler than the problem it solves.

## MUST

- State the invariant before introducing a DDD pattern.
- Keep business rules close to the model that owns them when that improves correctness.
- Make consistency boundaries explicit when they matter.
- Preserve domain language in names and behavior.
- Reconcile an intentional behavior change with the released baseline before implementation.
- Test important invariants through observable behavior.
- Keep infrastructure concerns outside the domain model.

## SHOULD

- Use a Value Object when value semantics and validation are important.
- Use an Entity when identity and lifecycle matter.
- Keep Aggregates small enough to protect one consistency boundary.
- Use Domain Services only for behavior that does not naturally belong to one domain object.
- Use Domain Events for meaningful facts that other parts of the system must react to.
- Use Bounded Contexts when models, ownership, or language genuinely diverge.

## CONDITIONAL patterns

- **Aggregate** — introduce it when multiple state changes must remain atomically consistent.
- **Domain Event** — introduce it when the fact of a completed business action matters beyond the local transaction.
- **Anti-Corruption Layer** — introduce it when an external model would otherwise distort the internal model.
- **CQRS** — introduce it when read and write models have materially different needs.
- **Event Sourcing** — introduce it only when event history and replay are core requirements.

## Reject cargo-cult modeling

Do not introduce an Aggregate for every database table, a Domain Event for every method call, or a Value Object for every scalar without a behavior or invariant to protect. Do not turn an anemic data bag into an anemic model with more classes. Simple CRUD may remain simple.

Read [tactical-modeling.md](references/tactical-modeling.md) for pattern conditions, [bounded-contexts.md](references/bounded-contexts.md) for context boundaries, and [anti-patterns.md](references/anti-patterns.md) before approving a complex model.

## Routing

Route unclear business behavior to `requirement-engineering`. Route an approved but complex domain change to `change-planning`. Route dependency direction, ports, adapters, or infrastructure isolation to `architecture-boundaries`. Route implementation behavior to `test-driven-development`; route a failing invariant to `systematic-debugging`.

## Verification

An acceptable design can name:

- the business invariant;
- the owner of that invariant;
- the consistency boundary;
- the reconciliation classification and any user decision;
- the reason for each introduced pattern;
- the behavior and release-baseline tests that protect it;
- the simpler alternative that was rejected and why.
