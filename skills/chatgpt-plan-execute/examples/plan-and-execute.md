# Example: Plan then execute

User:

```text
$chatgpt-plan-execute
Wire the real scene completion callback into the rule engine. Let ChatGPT Web analyze the repository context and make the implementation plan, then implement it here.
```

Codex behavior:

1. inspect the current scene completion path, rule runtime, wiring, project rules, and tests;
2. write repository facts without inventing a solution;
3. select only the relevant source/tests/docs;
4. create and inspect the handoff manifest;
5. prefer the Codex built-in browser, attach the audited local bundle, and submit to ChatGPT Web;
6. use the Codex Chrome Extension instead only when the user explicitly needs the existing Chrome session and that transport can satisfy the same upload boundary;
7. record the actual browser transport and ChatGPT conversation URL;
8. import the marked plan;
9. reconcile each assumption with the current repository;
10. implement the confirmed/adapted plan in runnable slices;
11. run focused and broader verification;
12. report any plan deviation with repository evidence.

The key behavior is that ChatGPT designs from a curated repository snapshot while Codex remains responsible for current facts and executable completion evidence.
