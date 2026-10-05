---
name: code-review
description: Perform an independent, read-only, evidence-based review of software changes for correctness, security, maintainability, compatibility, performance, data behavior, testing, coverage, and scope. Use for working-tree changes, commits, diffs, pull requests, or specific implementation reviews.
---

# Code Review

## Purpose

Independently evaluate implemented changes against requirements, project conventions, correctness, risk, and maintainability.

Review is read-only.

## Operating rules

1. Inspect the actual diff and surrounding code.
2. Understand the relevant requirement and existing behavior.
3. Prefer concrete evidence over style preference.
4. Review changed code in context, not in isolation.
5. Check security, compatibility, data, performance, observability, testing, and scope when relevant.
6. Do not modify files.
7. Do not stage, commit, push, merge, rebase, create PRs, release, or deploy.
8. Do not manufacture findings to fill a quota.
9. Distinguish defect from recommendation.
10. Check coverage evidence without inventing thresholds.

## Workflow

- [ ] Establish review scope.
- [ ] Inspect working tree/diff/range.
- [ ] Understand relevant requirements.
- [ ] Inspect surrounding implementation and conventions.
- [ ] Evaluate correctness.
- [ ] Evaluate security.
- [ ] Evaluate API/data compatibility.
- [ ] Evaluate performance/reliability/observability where relevant.
- [ ] Evaluate tests and coverage evidence.
- [ ] Evaluate scope and maintainability.
- [ ] Investigate suspected findings.
- [ ] Remove unsupported or false-positive findings.
- [ ] Report findings by severity.

For review dimensions use [review-dimensions.md](references/review-dimensions.md).

For finding severity use [finding-severity.md](references/finding-severity.md).

For evidence standards use [review-evidence.md](references/review-evidence.md).

## Distributed-system review

When relevant inspect:

- consistency assumptions
- retry behavior
- idempotency
- message delivery
- ordering
- timeout/failure behavior
- partition behavior
- replication/caching
- reconciliation

Check that implementation matches the approved architectural consistency model.

## Finding format

Each material finding should include:

- severity
- location
- evidence
- impact
- recommendation

Do not call something a defect without enough evidence.

## Human decisions

A review may identify a human decision without making the review incomplete.

## Terminal status

End with exactly:

`CODE REVIEW COMPLETE`
