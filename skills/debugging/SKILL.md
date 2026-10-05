---
name: debugging
description: Investigate software failures using evidence-based reproduction, tracing, hypothesis testing, root-cause analysis, and verification. Use when behavior fails, tests fail, errors occur, or application versus environment/tooling responsibility must be established. Diagnosis is read-only unless an approved implementation workflow is requested.
---

# Debugging / Root Cause Analysis

## Purpose

Determine the most likely root cause of a software failure using evidence rather than guesswork.

## Operating rules

1. Capture the exact failure.
2. Reproduce when practical and safe.
3. Separate symptom, hypothesis, contributing factor, and root cause.
4. Test hypotheses with evidence.
5. Distinguish application defects from environment, tooling, dependency, data, and infrastructure failures.
6. Preserve the working tree.
7. Do not silently fix the defect during diagnosis.
8. Classify environment operations by actual effect.
9. Obtain human approval before consequential environment mutation.
10. Do not stage, commit, push, merge, rebase, create PRs, release, or deploy.

## Workflow

- [ ] Capture expected vs actual behavior.
- [ ] Capture exact error/log/stack trace.
- [ ] Reproduce safely when practical.
- [ ] Localize the failing path.
- [ ] Inspect recent relevant changes.
- [ ] Form explicit hypotheses.
- [ ] Test hypotheses.
- [ ] Separate application from environment/tooling/dependency/data causes.
- [ ] Identify root cause or establish why it cannot be confirmed.
- [ ] Identify contributing factors.
- [ ] Define verification for a future fix when needed.
- [ ] Report evidence and limitations.

For diagnosis methodology use [diagnosis-method.md](references/diagnosis-method.md).

For application-vs-environment classification use [environment-vs-application.md](references/environment-vs-application.md).

For side-effect boundaries use [side-effect-boundaries.md](references/side-effect-boundaries.md).

## Distributed failures

When the failure crosses service/process boundaries, inspect:

- timeouts
- retries
- duplicate requests/messages
- ordering
- dependency health
- network partitions
- stale/replicated state
- correlation IDs
- recovery/reconciliation

Do not assume a distributed symptom proves an application defect.

## Evidence labels

Use:

`FACT`, `EXPECTED`, `OBSERVATION`, `HYPOTHESIS`, `EVIDENCE`, `ROOT CAUSE`, `CONTRIBUTING FACTOR`, `SYMPTOM`, `UNKNOWN`, `RECOMMENDATION`.

## Root-cause standard

A root cause must explain the observed failure and survive reasonable alternative-hypothesis testing.

If evidence is insufficient, say so.

## Terminal statuses

Use exactly one:

- `ROOT CAUSE IDENTIFIED`
- `ROOT CAUSE NOT CONFIRMED`
- `DEBUGGING BLOCKED`
