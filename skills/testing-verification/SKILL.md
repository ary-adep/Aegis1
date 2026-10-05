---
name: testing-verification
description: Independently verify software changes and requirements through test discovery, execution, coverage evidence, regression analysis, and acceptance-criteria verification. Use when Aegis1 must determine whether a change works or whether a failure is environmental versus application-related. Read-only to product and repository state; environment-changing operations require approval.
---

# Testing & Verification

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
- [ ] Run focused tests.
- [ ] Run relevant regression tests.
- [ ] Collect coverage evidence where available.
- [ ] Verify acceptance criteria.
- [ ] Classify failures.
- [ ] Assess environment-side effects before further commands.
- [ ] Record limitations and unresolved evidence gaps.
- [ ] Report the verification result.

Use [verification-strategy.md](references/verification-strategy.md) for detailed strategy.

Use [coverage.md](references/coverage.md) for coverage rules.

Use [environment-effects.md](references/environment-effects.md) before environment-changing operations.

Use [acceptance-verification.md](references/acceptance-verification.md) for requirement-level verification.

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

## Feedback loop

If a verification step fails:

1. classify the failure
2. inspect evidence
3. correct only if the requested workflow authorizes correction
4. rerun the relevant verification
5. stop if the required correction is outside scope or needs human approval

## Terminal statuses

Use exactly one, as the final status line of the report:

- `VERIFICATION COMPLETE` — all required/in-scope verification was completed successfully and no required verification remains unverified.
- `VERIFICATION FAILED` — verification executed and product/test verification failed.
- `VERIFICATION BLOCKED` — environment, tooling, access, or another external constraint prevented required verification from being completed.
- `NEEDS HUMAN DECISION` — human approval, unresolved ambiguity, or a consequential decision is required before verification can continue.

`VERIFICATION COMPLETE` means the required verification evidence was actually obtained, not merely that findings were reported.

Partially verified or unverified acceptance criteria must not be reported as `VERIFICATION COMPLETE`.

## Completion standard

Verification is complete only when the evidence supports a clear statement of what passed, what failed, what remains unverified, and why.
