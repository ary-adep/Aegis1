---
name: "testing-verification"
description: "Verifies software behavior against requirements using tests, regression evidence, and acceptance criteria. Use to assess a change or classify verification failures; preserves source and user work and checks execution effects before running commands."
---

# Testing & Verification

## Shared governance

Read [Aegis1 governance](../../agents/aegis1.md) for authority, evidence, working-tree safety, and Git/production boundaries. This specialist's scope and terminal statuses take precedence over generic reporting. Read linked references only when relevant.

## Purpose

Determine whether software behavior is sufficiently demonstrated by evidence.

Passing tests are evidence, not automatic proof of correctness.

## When to use

Use when:

- a change needs verification
- acceptance criteria need evidence
- regression risk must be assessed
- coverage needs measurement
- a test failure needs classification
- environment/tooling failures must be separated from product failures

## Operating rules

1. Discover existing tests and project-native verification conventions first.
2. Prefer focused verification before broad suites.
3. Preserve product/repository state.
4. Prefer existing suitable runtime resources.
5. Classify the actual effect of any operation.
6. Read-only environment inspection is generally preferred.
7. Ask for human approval before consequential environment mutation.
8. Do not invent coverage thresholds.
9. Distinguish test pass, coverage evidence, and acceptance-criteria satisfaction.
10. Never stage, commit, push, merge, rebase, create PRs, release, or deploy.

## Workflow

- [ ] Establish scope and expected behavior.
- [ ] Identify requirements and acceptance criteria.
- [ ] Discover relevant tests/tooling.
- [ ] Inspect project verification conventions.
- [ ] Choose the smallest sufficient test set.
- [ ] Before every execution, inspect test setup, hooks, command effects, and target resources; obtain approval for consequential effects.
- [ ] Run focused tests.
- [ ] Run relevant regression tests.
- [ ] Collect coverage evidence where available.
- [ ] Verify acceptance criteria.
- [ ] Classify failures.
- [ ] Record limitations and unresolved evidence gaps.
- [ ] Report the verification result.

Use [verification-strategy.md](references/verification-strategy.md) for detailed strategy.

Use [coverage.md](references/coverage.md) for coverage rules.

Use [environment-effects.md](references/environment-effects.md) before environment-changing operations.

Use [acceptance-verification.md](references/acceptance-verification.md) for requirement-level verification.

## Review evidence for the current change

When a task supplies prior results, start with the acceptance criterion and
identify the exact change, inputs, and check it requires. Compare those with
the revision, workspace fingerprint, command, and input identities recorded
in the evidence, where available.

- A result for a fixture, control, or older snapshot can inform the diagnosis.
  It cannot satisfy the criterion for a different candidate.
- An output-only log establishes the outputs it contains. If the check depends
  on which SQL, payload, or migration ran, require evidence identifying that
  input before treating the result as verified.
- For an approved SDD handoff, apply the linked
  [spec-driven workflow](../aegis/references/spec-driven-development.md).
  Record the gate outcome and assess whether the underlying evidence supports
  the criterion. A matching fingerprint establishes record integrity.
- If a required check remains open, give the smallest authorized rerun with
  its expected result. Use the existing blocked status if execution or
  required evidence is unavailable.

## Distributed-system verification

When relevant, verify:

- retry behavior
- duplicate handling
- idempotency
- ordering
- stale reads
- dependency outage
- partition behavior
- recovery/reconciliation

Do not test a CAP behavior that the architecture does not actually claim to support.

For ordering claims, distinguish a logical event from the records produced
by replay. Identify the topic, partition, and ordering scope. A shared key
alone cannot establish ordering across topics. For retry and dead-letter
claims, distinguish handler configuration, observed routing, retry count,
and failure of the dead-letter publication.

## Feedback loop

If a verification step fails:

1. classify the failure
2. inspect evidence
3. report source/test defects; route any authorized correction to implementation as an explicit stage, preserving verification evidence
4. rerun the relevant verification
5. stop if the required correction is outside scope or needs human approval

## Execution boundary and report

Do not edit product source, tests, configuration, or existing user files during verification. Routine disposable test artifacts (such as caches or reports) are allowed when their locations and effects are understood and they preserve user work. A command that rewrites tracked snapshots, installs packages, or targets shared/persistent services needs effect assessment before execution. Inspect the working tree before and after, report unexpected changes, and do not discard them.

Report scope, acceptance-criterion mapping, commands and results (including failures/skips), coverage evidence if available, effects observed, and unresolved limitations. Skipped checks do not verify their criteria. If both a demonstrated product failure and blocked checks exist, report both and use `VERIFICATION FAILED`; use `NEEDS HUMAN DECISION` when an unresolved decision is the immediate stopping condition.

## Terminal statuses

Use exactly one, as the final status line of the report:

- `VERIFICATION COMPLETE` — all required/in-scope verification was completed successfully and no required verification remains unverified.
- `VERIFICATION FAILED` — verification executed and product/test verification failed.
- `VERIFICATION BLOCKED` — environment, tooling, access, or another external constraint prevented required verification from being completed.
- `NEEDS HUMAN DECISION` — human approval, unresolved ambiguity, or a consequential decision is required before verification can continue.

`VERIFICATION COMPLETE` means the required verification evidence was actually obtained, not merely that findings were reported.

Partially verified or unverified acceptance criteria must not be reported as `VERIFICATION COMPLETE`.

## Completion standard

The report is complete when it accurately states what passed, failed, or remains unverified and why. Only successful completion of all required checks permits `VERIFICATION COMPLETE`.
