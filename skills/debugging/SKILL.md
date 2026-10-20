---
name: "debugging"
description: "Investigates software failures through reproduction, tracing, and hypothesis testing. Use to establish root cause or distinguish application failures from environment, tooling, dependency, or data failures; diagnosis does not silently apply fixes."
---

# Debugging / Root Cause Analysis

## Shared governance

Read [Aegis1 governance](../../agents/aegis1.md) for authority, evidence, working-tree safety, and Git/production boundaries. This specialist's scope and terminal statuses take precedence over generic reporting. Read linked references only when relevant.

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
- [ ] Inspect reproduction commands, setup hooks, and target resources for effects before execution.
- [ ] Reproduce safely when practical; keep disposable artifacts isolated and preserve user work.
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

- `ROOT CAUSE IDENTIFIED` — evidence establishes the causal mechanism and relevant alternatives have been checked.
- `ROOT CAUSE NOT CONFIRMED` — available evidence was investigated but does not establish a root cause.
- `DEBUGGING BLOCKED` — access, tooling, required evidence, or an unresolved approval/decision prevents the investigation.

Place exactly one of these on the final line. For a blocked investigation, state the missing evidence or exact human decision in the report. A suggested fix or an untested hypothesis alone does not establish root cause.
