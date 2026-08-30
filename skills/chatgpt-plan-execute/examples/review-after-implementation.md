# Example: Review after implementation

After Codex implements the reconciled plan, the user asks:

```text
Continue the same ChatGPT conversation and have it review the implementation and test evidence.
```

Codex should reopen the saved `chatgpt.com` conversation through the Codex Chrome Extension, compare current relevant files with the original manifest hashes, and send only the current diff, verification evidence, plan deviations, and narrowly refreshed source context that the review actually needs.

ChatGPT returns marker-bounded findings. Codex imports them, validates each finding against the current repository, applies only confirmed fixes, and reruns local verification.

The earlier uploaded snapshot must never be described as current when relevant files have changed.
