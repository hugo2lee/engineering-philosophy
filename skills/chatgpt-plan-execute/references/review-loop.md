# Review Loop

## Reuse the same conversation

After the initial plan, keep the saved ChatGPT conversation URL when the user wants architecture or implementation review. Reopen that conversation through the Codex Chrome Extension so ChatGPT can use the earlier planning context.

Do not automatically reupload the original archive on every turn.

## Context freshness

Before review, compare the current files relevant to the review with the hashes in the original manifest.

- unchanged relevant file: rely on the original uploaded context;
- materially changed relevant file: summarize the change and, if exact current content is necessary, prepare a narrowly refreshed bundle;
- newly relevant file absent from the original bundle: add only that evidence when necessary;
- unrelated changed file: do not refresh merely because the repository changed somewhere.

Never imply that ChatGPT sees the current working tree unless the relevant current state was actually supplied.

## Review payload

A follow-up should normally include:

- implementation summary;
- plan deviations and why repository evidence required them;
- focused and broad verification results;
- unresolved risks;
- a diff or narrowly selected changed files when needed.

Ask for findings, not unconditional approval.

## Findings are proposals

Validate every finding against the current repository before changing code. If the review contradicts executable tests, repository contracts, or current code facts, investigate the contradiction instead of obeying the review mechanically.

Stop the loop when local verification is green and the remaining review comments are either resolved, explicitly accepted as risk, or outside the approved scope. Do not create an endless planner-reviewer cycle.
