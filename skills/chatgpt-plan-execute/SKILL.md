---
name: chatgpt-plan-execute
description: Orchestrate an explicit Codex workflow that inspects a local repository, packages a minimal auditable context bundle, delegates architecture reasoning and implementation planning or review to ChatGPT Web using the Codex built-in browser by default or the Codex Chrome Extension when an existing Chrome session is required, validates the returned plan against repository facts, then executes and verifies it locally. Use only when the user explicitly asks Codex to hand off repository context to ChatGPT Web; never upload secrets or infer consent from an ordinary coding request.
license: AGPL-3.0-only
metadata:
  version: "0.4.0"
  category: "workflow"
---

# ChatGPT Plan Execute

## Purpose

Use this Skill when the user explicitly wants Codex to use the local repository as evidence, ask ChatGPT Web to reason about architecture, planning, or review, then continue implementation in Codex.

This is an orchestration Skill, not an engineering methodology. It does not replace `requirement-engineering`, `change-planning`, `architecture-boundaries`, `incremental-implementation`, `test-driven-development`, or `code-review-and-quality`. Those Skills still own the engineering decisions. This Skill owns the handoff boundary between Codex and ChatGPT Web.

## Invocation and consent

This Skill is explicit-only because it can transmit selected local files to ChatGPT Web.

Explicit invocation means the user authorizes Codex to prepare and send the minimal manifest-reviewed context needed for the requested handoff. Do not infer upload consent from an ordinary coding, planning, debugging, or review request. If the manifest reports any blocked or potentially sensitive content, a repository policy forbids external sharing, or the selected scope is unexpectedly broad, stop before upload and ask the user to resolve the blocker.

A user may request `dry run`, `prepare only`, or `do not upload`; in that mode produce the handoff package and manifest but do not open or submit to ChatGPT Web.

## Role contract

```text
Codex
  = repository explorer
  = repository source-of-truth keeper
  = context compiler
  = browser-transport selector
  = implementation executor
  = local verifier

ChatGPT Web
  = architecture/planning consultant
  = optional post-implementation reviewer
```

ChatGPT may reason from the supplied evidence, but it is never the authority on repository facts. A returned plan is a proposal that Codex must reconcile with the current workspace before editing.

## Workflow

### 1. Reconnaissance before solution design

Read the repository before asking ChatGPT to plan. Inspect the smallest useful evidence surface, including applicable `AGENTS.md`, project Skills or rules, README/design docs, entry points, existing capability owners, relevant call paths, tests, configuration boundaries, and composition/wiring code.

During this phase, distinguish:

- `Repository Fact`: directly supported by current local evidence;
- `User Constraint`: explicitly requested by the user;
- `Engineering Constraint`: applicable rule from project/global Skills;
- `Unknown`: material information not established yet.

Do not invent a new architecture merely to make the handoff look complete. The output of reconnaissance is a concise `repository-facts.md` plus an exact `selected-files.txt`.

Read [context-selection.md](references/context-selection.md) before selecting files.

### 2. Compile a minimal auditable handoff

Resolve this Skill's local directory and run:

```bash
python3 <skill-dir>/scripts/prepare_handoff.py create \
  --workspace "$PWD" \
  --task-file /path/to/task.md \
  --facts-file /path/to/repository-facts.md \
  --file-list /path/to/selected-files.txt
```

The packager uses exact workspace-relative file selection only. There is no implicit whole-workspace upload mode. It rejects path traversal, symlinks, common secret paths, private-key/certificate material, binary files, oversized files, and common credential patterns. Any blocked selected file makes packaging fail closed and no context ZIP is produced.

Inspect `.chatgpt_handoffs/<id>/manifest.json` before browser submission. The manifest is the auditable statement of what will leave the local workspace.

Read [handoff-contract.md](references/handoff-contract.md) for state, safety, browser-transport, and response-marker rules.

### 3. Choose a browser transport and submit

Prefer the **Codex built-in browser** for the normal handoff. It keeps the browser interaction inside the Codex desktop workflow and is the first transport to try when the handoff needs to attach the locally generated `context-*.zip`.

Use the **Codex Chrome Extension** when the user explicitly wants the existing Chrome profile/session, an already-open ChatGPT conversation in Chrome, or another Chrome-specific capability. The extension is a supported transport, not the protocol itself.

Do not use an independent Playwright/Puppeteer profile, shell browser automation, cookie/session export, undocumented ChatGPT APIs, AppleScript, Computer Use, or another browser path to bypass the selected transport's security or upload controls.

Open or reuse `chatgpt.com` in the selected transport. If the user requested a specific model or reasoning mode, select and verify the visible requested option. Otherwise keep the current visible ChatGPT selection and record what was actually used; do not silently substitute a different requested model/mode.

Attach the generated `context-*.zip`, paste `prompt.md`, and submit only when the manifest is `ready` and the invocation/consent conditions above are satisfied. If the selected transport cannot access the local attachment, the file picker requires user confirmation, or login/CAPTCHA/OAuth/model selection/browser control becomes ambiguous, stop for user takeover. Do not compensate by pasting unreviewed source, exporting credentials, or using an undocumented upload path.

A transport switch is allowed only between the two supported Codex transports and only when it preserves the user's consent and can satisfy the same manifest-reviewed upload boundary. Do not assume the Chrome Extension can upload local files merely because it can control an authenticated Chrome tab.

After submission, record the conversation URL and transport:

```bash
python3 <skill-dir>/scripts/prepare_handoff.py record-session \
  --handoff-dir .chatgpt_handoffs/<id> \
  --chat-url "https://chatgpt.com/c/..." \
  --actual-mode "<visible model/mode>" \
  --browser-transport codex-in-app
```

Use `--browser-transport codex-chrome-extension` when that transport was actually used.

### 4. Import the planning response

Request exactly one marker pair:

```text
BEGIN_CHATGPT_PLAN_RESPONSE
...
END_CHATGPT_PLAN_RESPONSE
```

Capture only the latest assistant response for the current handoff turn. Save it to a local text file, then run:

```bash
python3 <skill-dir>/scripts/prepare_handoff.py import-response \
  --handoff-dir .chatgpt_handoffs/<id> \
  --response-file /path/to/raw-response.md \
  --kind plan
```

The importer fails if the marker pair is missing, duplicated, or reversed.

### 5. Reconcile plan against repository facts

Before editing, validate every material ChatGPT assumption against the current repository. Classify plan items as:

- `Confirmed`: supported and executable as written;
- `Adapted`: goal/decision is useful but implementation detail conflicts with repository facts;
- `Rejected`: contradicts the repository, project rules, user constraints, or acceptance criteria;
- `Needs Decision`: requires user-visible product semantics not established by evidence.

Repository facts override ChatGPT assumptions. Preserve the approved goal and valid architecture decision while adapting implementation details to existing owners and boundaries. Do not create a second abstraction when an existing one already owns the required behavior.

Read [planning-contract.md](references/planning-contract.md) for the expected plan and reconciliation contract.

### 6. Execute and verify locally

Route each material decision to the focused engineering Skill that owns it. Implement in small runnable slices, run focused tests first, then the applicable broader verification. Record any intentional deviation from the ChatGPT plan and the repository evidence that justified it.

ChatGPT does not declare implementation complete. Local executable evidence does.

### 7. Optional review loop

When useful, reopen the saved ChatGPT conversation URL using the browser transport recorded in `session.json` and send a follow-up containing the implemented diff summary, test/build evidence, and any plan deviations. Do not reupload unchanged original context. If relevant source files have changed materially and the review depends on their current contents, refresh only those files into a new context bundle or explicitly tell ChatGPT which earlier context is stale.

If the recorded transport is unavailable, a switch to the other supported Codex transport requires the same upload/consent checks as the initial handoff. Import review responses with `--kind review`, then validate findings locally before applying them.

Read [review-loop.md](references/review-loop.md) for context-freshness and stop rules.

## Stop conditions

Stop and report rather than silently degrading when:

- neither supported Codex browser transport can safely perform the required ChatGPT interaction;
- local file attachment is unavailable or ambiguous and requires user takeover;
- ChatGPT login/CAPTCHA/OAuth requires user action;
- a requested model or mode cannot be selected or verified;
- manifest status is `blocked`;
- secret scanning finds suspicious selected content;
- repository policy disallows external sharing;
- the returned response markers are invalid;
- ChatGPT requires a product decision that the repository cannot establish;
- local verification disproves a material part of the returned plan.

## Verification

A successful run leaves auditable local evidence:

```text
.chatgpt_handoffs/<id>/
  task.md
  repository-facts.md
  selected-files.txt
  manifest.json
  prompt.md
  context-<id>.zip
  session.json
  raw_response.md
  response.md
```

`session.json` records the ChatGPT conversation URL, visible model/mode, and the browser transport used for the submitted handoff.

The workflow is complete only when the implementation has been verified locally, not merely when ChatGPT returns a plan.
