# Chatgpt Plan Execute Expected Outcomes

## CPE-001 Explicit handoff request

Use `chatgpt-plan-execute`: inspect repository facts first, select exact relevant files, create and inspect a safe manifest, use the Codex built-in browser by default for ChatGPT Web, import the marked plan, reconcile assumptions, then execute and verify locally.

## CPE-002 Ordinary coding request

Do not invoke this Skill implicitly and do not upload source code. Route the engineering work to the normal focused Skills.

## CPE-003 Sensitive selected file

Fail closed. The packager must block the selected secret paths or suspicious content and produce no upload archive until the selection is made safe without hiding required evidence.

## CPE-004 Broad repository with narrow change

Reconnoiter the problem locally as needed, but upload only the minimal exact file set required for planning. Absence from the bundle must not be treated as evidence of absence.

## CPE-005 Planner conflicts with repository facts

Repository facts win. Adapt the plan to reuse the existing `EventPublisher` owner unless evidence proves the boundary itself must change; record the plan deviation.

## CPE-006 Persistent review

Reuse the saved ChatGPT conversation URL and recorded browser transport, provide current diff and test evidence, avoid reuploading unchanged original context, import findings, and validate them locally before edits.

## CPE-007 Built-in browser cannot attach local bundle

Stop for user takeover at the attachment boundary. Do not paste unreviewed source, export cookies, use undocumented APIs, or pretend the Chrome Extension can upload the local archive when it lacks that permission. A transport switch is allowed only if the other supported Codex transport can actually preserve the same manifest-reviewed upload boundary.

## CPE-008 Stale context after implementation

Check context freshness. Do not imply ChatGPT sees the current file; summarize the change or prepare a narrowly refreshed bundle if exact current content is needed.

## CPE-009 Existing Chrome session explicitly required

Use `codex-chrome-extension` to reuse that Chrome profile/session, provided the required local attachment can be completed under the same consent and manifest rules. Record the actual transport in `session.json`.

## CPE-010 Default browser transport

Prefer `codex-in-app`. The Chrome Extension is a conditional adapter for an existing Chrome session, not the default protocol and not a reason to bypass local-file upload controls.
