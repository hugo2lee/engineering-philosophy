# Planning Contract

## What ChatGPT should produce

Ask ChatGPT to reason from the supplied task, repository facts, engineering constraints, and selected context. It should not produce a speculative rewrite or assume absent files do not exist.

A useful plan covers, as applicable:

1. current-state interpretation grounded in supplied evidence;
2. assumptions and unknowns;
3. architecture/design decision and alternatives only where needed;
4. existing owner/boundary to reuse or change;
5. ordered implementation slices;
6. likely files/areas affected without pretending the list is complete;
7. focused tests and broader verification;
8. compatibility, migration, concurrency, error, or rollback risks;
9. acceptance criteria.

Do not ask ChatGPT to fabricate code for the whole repository when the goal is planning. Small illustrative pseudocode is acceptable only when it clarifies a decision.

## Repository-facts priority

After import, Codex validates the plan item by item:

| Result | Meaning | Action |
| --- | --- | --- |
| Confirmed | Repository supports the assumption and step | Execute when otherwise approved |
| Adapted | Goal/decision is useful but implementation detail is stale or wrong | Reuse current owner/boundary and record deviation |
| Rejected | Conflicts with current facts/rules/requirements | Do not implement |
| Needs Decision | Requires user-visible semantics not established | Return to user/requirement gate |

Repository facts override ChatGPT assumptions. A plan never authorizes weakening tests, release baselines, safety rules, or user-approved behavior merely to make implementation easier.

## Engineering Skill routing

This workflow does not own design semantics. Route material decisions to the smallest focused Skill:

- unclear behavior -> `requirement-engineering`;
- repository impact/ordering -> `change-planning`;
- dependency direction/ports/DI -> `architecture-boundaries`;
- business invariants -> `ddd-lite`;
- large migration -> `incremental-implementation`;
- implementation behavior/tests -> `test-driven-development`;
- observed failure -> `systematic-debugging`;
- final diff/readiness -> `code-review-and-quality`.
