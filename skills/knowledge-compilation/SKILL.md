---
name: knowledge-compilation
description: Evolve repository evidence into governed, discoverable project knowledge by classifying artifacts, reconciling canonical sources, deciding when to update an existing owner or create a Skill candidate, preserving provenance, validating redaction, and controlling candidate/active/retired states. Use when repository changes should update Agent knowledge; do not use for ordinary feature implementation, debugging, review, or release work alone.
license: AGPL-3.0-only
metadata:
  version: "0.5.0"
  category: "knowledge-governance"
---

# Knowledge Compilation

## Use this Skill when

Use this Skill when a repository change may alter the knowledge that an Agent
uses to work in the project, for example:

- new or changed project documentation, architecture references, runbooks, or evidence;
- source, test, build, deployment, or generated-artifact changes that affect project guidance;
- deciding whether to update an existing reference/Skill or create a project Skill candidate;
- reconciling generated knowledge with its canonical source;
- validating provenance, redaction, lifecycle status, or project/global scope.

Do not use it merely because a repository contains documentation. Ordinary
requirements, architecture decisions, implementation, debugging, review, and
release work stay with their focused Skills; route to this Skill only when the
repository's Agent knowledge itself is the thing being evolved.

## Governing rules

1. **Compile knowledge from evidence, not filenames.** Inspect the changed artifact, its source, behavior, and task signal before deciding what knowledge product it represents.
2. **Prefer an existing owner.** Update an existing reference, registry entry, or Skill when it already owns the task; repeated files do not by themselves justify a new Skill.
3. **Generation does not imply activation.** A candidate may be synthesized for evaluation without becoming an active default route; candidates must remain outside automatically discovered active paths.
4. **Preserve provenance.** Generated Skill `SKILL.md` files keep standard-compatible frontmatter; structured provenance, generation, lifecycle, ownership, and promotion data live in a linked validated sidecar record.
5. **Canonical sources outrank generated summaries.** A conflict is surfaced for reconciliation; it is never silently merged in favor of generated text.
6. **Keep scope project-local by default.** A project observation or generated Skill cannot automatically become a global engineering-philosophy rule.
7. **Protect the write boundary.** Automation may update registered knowledge artifacts, references, evals, and compiler metadata; it must not modify unrelated product source, production data, secrets, or submodule contents.
8. **Redact before registration.** Block or redact credentials, private keys, tokens, device identifiers, customer data, and unredacted production configuration without inventing replacement facts.
9. **Keep the registry executable.** Owner, verification, generation, and promotion records must satisfy the knowledge registry schema before synchronization.

## Lifecycle

Use the smallest proportional form of this lifecycle:

```text
Repository Change
    -> Discover Changed Evidence
    -> Classify Artifact
    -> Resolve Canonical Source and Provenance
    -> Reconcile Existing Knowledge and Conflicts
    -> Decide Reference / Evidence / Decision / Generated Artifact / Skill
    -> Synthesize or Update
    -> Validate Provenance, Redaction, Links, and Evals
    -> Register
    -> Candidate / Active Decision
    -> Agent Discovery
    -> Staleness, Deprecation, or Retirement
```

Not every change needs every step. The depth of the process should match the
knowledge risk and the stability of the task boundary.

Read the relevant reference before making the decision:

- [knowledge-compilation-lifecycle.md](references/knowledge-compilation-lifecycle.md) for the end-to-end flow;
- [artifact-classification.md](references/artifact-classification.md) for Source, Reference, Evidence, Decision, Generated Artifact, and Skill;
- [knowledge-reconciliation.md](references/knowledge-reconciliation.md) for owner selection and conflict handling;
- [skill-candidate-and-promotion.md](references/skill-candidate-and-promotion.md) for candidate gates and lifecycle status;
- [generated-knowledge-contract.md](references/generated-knowledge-contract.md) for generated metadata;
- [source-of-truth-and-provenance.md](references/source-of-truth-and-provenance.md) for canonical-source precedence;
- [validation-and-redaction.md](references/validation-and-redaction.md) for safety and validation gates;
- [project-vs-global-promotion.md](references/project-vs-global-promotion.md) for scope and promotion;
- [knowledge-registry.md](references/knowledge-registry.md) for the machine-readable registry contract.

## Routing

- Repository change that should update Agent knowledge -> `knowledge-compilation`.
- Architecture pressure discovered while classifying evidence -> secondary `architecture-boundaries`.
- Domain invariant or bounded-context evidence discovered -> secondary `ddd-lite`.
- Generated Skill review -> secondary `code-review-and-quality`.
- Project-to-global promotion -> primary `engineering-philosophy`, with `knowledge-compilation` as secondary.
- Knowledge compiler CI or artifact gate -> primary `ci-cd-and-automation`, with `knowledge-compilation` as secondary.

Do not activate this Skill as a mandatory prelude to ordinary feature work. It
should be selected when the knowledge surface, its lifecycle, or its automatic
registration is the current decision.

## Stop conditions

Stop synthesis or activation and surface the issue when:

- the canonical source is missing or conflicts with a released baseline;
- the proposed Skill duplicates an existing owner or has no stable task signal;
- fewer than enough discriminating evals can be defined for the intended scope;
- provenance cannot be established;
- sensitive material cannot be safely redacted;
- the change would cross project scope into organization/global scope without an explicit promotion review;
- automation would need to write product source, production configuration, secrets, data, or submodule code.

The goal is continuously maintainable project knowledge, not an unbounded
self-modifying Skill collection.
