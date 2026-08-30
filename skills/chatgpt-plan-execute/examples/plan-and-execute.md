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
5. submit through the Codex Chrome Extension;
6. import the marked plan;
7. reconcile each assumption with the current repository;
8. implement the confirmed/adapted plan in runnable slices;
9. run focused and broader verification;
10. report any plan deviation with repository evidence.

The key behavior is that ChatGPT designs from a curated repository snapshot while Codex remains responsible for current facts and executable completion evidence.
