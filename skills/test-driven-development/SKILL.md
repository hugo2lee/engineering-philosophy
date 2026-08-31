---
name: test-driven-development
description: Develop or change observable behavior through focused Red-Green-Refactor loops, vertical slices, regression tests, and release behavior baselines. Use when acceptance behavior is clear; not as the primary Skill for unclear requirements, active diagnosis, or code review.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "implementation"
---

# Test-Driven Development

## Use this Skill when

Use this Skill for a new behavior, a change with clear acceptance criteria, a bug fix that needs a regression test, or an incremental refactor that must preserve behavior.

Use a lighter form for trivial configuration or documentation changes. Route unclear requirements to `requirement-engineering` before writing tests.

## Governing loop

1. Choose one observable behavior from the approved requirement or bug report.
2. Write the smallest test that expresses the behavior and confirm it fails for the expected reason.
3. Implement only enough to make that test pass.
4. Run the focused test and relevant existing suite.
5. Refactor the design while keeping the tests green.
6. Repeat for the next business slice or boundary behavior.

The loop is Red → Green → Refactor. A test that never failed has not demonstrated that it protects the intended behavior.

## TDD versus Release Behavior Baseline

TDD is the implementation feedback method: it helps discover and shape one behavior during development.

A Release Behavior Baseline is the accepted promise that must remain executable after release. It is organized by stable boundary rather than by every internal function:

- Service Behavior Baseline;
- Persistence Integration Baseline, when persistence semantics matter;
- Outbound Contract Baseline, when an external protocol/provider matters;
- Inbound Mapping Baseline, when transport mapping matters.

Do not confuse a green focused unit test with complete release evidence. Establish the applicable baseline before the Gate 3 change review; a baseline may be refined during implementation, but it must exist before the review decision and may change only through an authorized behavior decision.

## MUST

- Test behavior through a stable public interface or meaningful boundary.
- Keep one focused behavior per iteration.
- Confirm the failure is caused by the missing behavior, not by a broken test.
- Keep the implementation minimal until the next behavior requires more.
- Preserve a regression test for every confirmed bug.
- Establish or update the appropriate release baseline only with an authorized behavior decision.
- Establish the applicable release baseline before Gate 3 review, not after review has already approved the change.
- Never weaken a failing baseline merely to make new implementation pass.
- If a baseline must change, record the requirement and user/product decision first.

## SHOULD

- Prefer a vertical slice over a large layer-first implementation.
- Use domain and application behavior as the test vocabulary.
- Use fakes or contract tests when a real boundary is expensive or unstable.
- Keep tests deterministic and easy to diagnose.
- Let test friction reveal a boundary or dependency problem.
- Refactor duplication after behavior is protected.

## Avoid

- writing all production code first and adding tests afterward;
- testing private implementation details when public behavior is available;
- adding interfaces only to satisfy a mocking library;
- asserting every incidental call or internal data structure;
- increasing coverage with tests that do not protect a decision;
- changing a failing baseline and implementation together without an explicit behavior decision.

Read [red-green-refactor.md](references/red-green-refactor.md) for the loop, [test-design.md](references/test-design.md) for behavior and boundary choices, [vertical-slices.md](references/vertical-slices.md) for larger changes, and [release-behavior-baseline.md](references/release-behavior-baseline.md) for the four baseline boundaries.

## Routing

Route unclear scope or acceptance criteria to `requirement-engineering`. Route an approved multi-boundary change to `change-planning` and `incremental-implementation`. Route a failing test or unexpected result to `systematic-debugging`.

## Verification

Before declaring a TDD step complete, record:

- the behavior under test;
- the observed failing reason;
- the minimal implementation;
- the focused test result;
- the broader verification result;
- the baseline impact, if any;
- the refactoring performed while green.
