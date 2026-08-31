# ChatGPT Plan Execute Cases

## CPE-001 Explicit handoff request

The user opens a local repository in Codex and explicitly invokes `$chatgpt-plan-execute` to have ChatGPT Web analyze selected repository context, create an implementation plan, and then have Codex implement and verify it locally.

## CPE-002 Ordinary coding request

The user asks Codex to add an endpoint but does not ask to send repository context to ChatGPT Web and does not invoke `$chatgpt-plan-execute`.

## CPE-003 Sensitive selected file

The relevant directory contains `.env.production`, private-key material, or a source file containing an actual credential value. A naive whole-directory bundle would include it.

## CPE-004 Broad repository with narrow change

A monorepo contains many unrelated services. The requested change touches one handler, one service, one adapter, wiring, and their tests.

## CPE-005 Planner conflicts with repository facts

ChatGPT proposes a new `RuleEventBus` interface, but Codex finds an existing consumer-owned `EventPublisher` port already used by the current runtime.

## CPE-006 Persistent review

After implementation the user asks ChatGPT to review the diff and test results in the same conversation.

## CPE-007 Built-in browser cannot attach local bundle

The Codex built-in browser reaches ChatGPT Web, but local file attachment is unavailable or the file picker requires user confirmation. The Chrome Extension is also known not to have permission to upload the local archive automatically.

## CPE-008 Stale context after implementation

ChatGPT's original uploaded context contains an older version of `runtime.go`; Codex materially changes that file before requesting follow-up review.

## CPE-009 Existing Chrome session explicitly required

The user explicitly asks to continue an already-authenticated ChatGPT conversation that is open in their normal Chrome profile and wants the Chrome session reused.

## CPE-010 Default browser transport

The user explicitly invokes `$chatgpt-plan-execute`, does not request an existing Chrome profile/session, and the handoff requires attaching the locally generated context archive.
