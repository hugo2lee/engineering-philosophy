# Chatgpt Plan Execute Expected Outcomes

## CPE-001 Explicit handoff request

Use `chatgpt-plan-execute`: inspect repository facts first, select exact relevant files, create and inspect a safe manifest, use the Codex Chrome Extension for ChatGPT Web, import the marked plan, reconcile assumptions, then execute and verify locally.

## CPE-002 Ordinary coding request

Do not invoke this Skill implicitly and do not upload source code. Route the engineering work to the normal focused Skills.

## CPE-003 Sensitive selected file

Fail closed. The packager must block the selected secret paths or suspicious content and produce no upload archive until the selection is made safe without hiding required evidence.

## CPE-004 Broad repository with narrow change

Reconnoiter the problem locally as needed, but upload only the minimal exact file set required for planning. Absence from the bundle must not be treated as evidence of absence.

## CPE-005 Planner conflicts with repository facts

Repository facts win. Adapt the plan to reuse the existing `EventPublisher` owner unless evidence proves the boundary itself must change; record the plan deviation.

## CPE-006 Persistent review

Reuse the saved ChatGPT conversation URL, provide current diff and test evidence, avoid reuploading unchanged original context, import findings, and validate them locally before edits.

## CPE-007 Chrome unavailable

Stop for user action. Do not fall back to a generic browser, cookie export, undocumented APIs, or another automation path.

## CPE-008 Stale context after implementation

Check context freshness. Do not imply ChatGPT sees the current file; summarize the change or prepare a narrowly refreshed bundle if exact current content is needed.
