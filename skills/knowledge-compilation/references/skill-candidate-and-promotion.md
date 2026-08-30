# Skill Candidate and Promotion

## Candidate gate

A proposed Skill should have:

- a clear task signal and explicit exclusion boundary;
- at least one canonical source and a provenance path;
- a responsibility not already owned by an active Skill;
- repeated work or a sufficiently high-cost/high-risk failure mode;
- an independent verification method;
- at least five discriminating eval cases, unless a documented high-risk gate
  justifies a smaller initial set for quarantine;
- no secrets, private customer data, device identifiers, or production-only
  configuration in its instructions or generated references.

One transient incident, one new document, one bounded context, or a future
possibility is not enough by itself.

## Candidate isolation

A candidate is a lifecycle state, not necessarily a deployable Skill directory.
If a runtime automatically discovers every `SKILL.md` under a configured
active path, a candidate must remain outside the active path until activation;
the registry status alone is insufficient to protect discovery. Candidate
material may be recorded under an isolated candidate location such as a
generator-owned output area, but the concrete path is project-specific and
must not be assumed by this generic protocol.

The three sets must remain distinguishable:

```text
Discovered Skill Set       = filesystem facts under the runtime discovery path
Published Active Skill Set = registry entries whose status is active
Installed Skill Set        = the result emitted by an installer
```

Validation must fail when a non-active directory appears under an automatically
discovered active path instead of silently treating it as published. Deployment
and smoke tests must use the same published registry-driven set. Membership and
cardinality must be derived from that set; validators and installers must not
hard-code the number of Skills in the current release.

## Lifecycle

```text
candidate → active → deprecated → archived
```

### candidate

The material is generated or proposed for evaluation. It is not a stable
project rule and must not be a default route or ordinary installation target.

### active

The source, provenance, links, evals, redaction, route distinction, and
verification gates pass. It may participate in normal Agent discovery.

### deprecated

An active replacement exists, but consumers may still need the old material.
Record `replaced_by` and keep a migration path.

### archived

The material is historical only and must not participate in default discovery.

## Promotion

Activation is a governed decision, not a side effect of generation. Project
automation may produce candidates and run objective gates; it must not promote
project knowledge to organization or global engineering-philosophy scope.
Promotion requires independent evidence, redaction, eval, and review records.
