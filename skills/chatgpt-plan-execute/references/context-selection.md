# Context Selection

## Principle

Send the smallest repository slice that lets ChatGPT reason about the user's actual problem without fabricating missing structure.

Context selection is a Codex responsibility because Codex can inspect the real local repository before the handoff. The packager intentionally does not infer relevance from the task prompt.

## Reconnaissance sequence

1. Read applicable repository instructions and project knowledge.
2. Locate the observable behavior or failing/changed entry point.
3. Follow references and call paths to the current capability owner.
4. Locate interfaces/ports only when they participate in that path.
5. Locate composition/wiring where the path is assembled.
6. Locate focused tests and relevant integration/release baselines.
7. Add design/ADR/docs only when they are canonical for a material decision.

Produce `repository-facts.md` before asking ChatGPT to design the solution.

## selected-files.txt

Use exact workspace-relative paths, one per line. Blank lines and `#` comments are allowed.

Prefer:

- current implementation owners;
- direct callers/callees needed to understand the path;
- current tests around the behavior;
- composition root or route/wiring code when relevant;
- canonical architecture or requirement documents.

Avoid:

- the entire repository just because it is available;
- generated build output;
- vendored dependencies unless the task is specifically about them;
- unrelated sibling modules;
- caches and IDE state;
- credentials, environment files, certificates, keys, production dumps, or customer data.

## Absence semantics

Directed context is incomplete by design. The planning prompt must state that absence from the archive is not evidence that a file, requirement, capability, configuration, or implementation does not exist.

If ChatGPT needs a missing fact, it should name the missing evidence. Codex then decides whether to inspect it locally, add a narrowly refreshed context, or resolve the question without another upload.
