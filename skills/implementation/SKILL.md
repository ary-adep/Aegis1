---
name: implementation
description: Execute an understood and appropriately approved software change with controlled scope, minimal edits, tests, verification, coverage evidence, and diff review. Use only when the target repository and implementation direction are sufficiently understood.
argument-hint: <approved implementation task>
context: fork
---

# Aegis1 Implementation

## Purpose

Execute an understood software change against the actual repository while preserving safety, scope, evidence, and human Git ownership.

## Preconditions

Do not start implementation until:

- the target repository/worktree is identified
- relevant requirements are understood
- architecture/direction is sufficiently established
- acceptance criteria exist or are otherwise clear
- consequential human decisions are resolved

If these are not true, stop and route to the appropriate specialist.

## Non-negotiable boundaries

Aegis1 implementation MUST NOT:

- stage changes
- commit
- push
- merge
- rebase
- create PRs
- release
- deploy
- execute production operations

The human owns Git handoff and production activity.

## Working-tree safety

- Inspect status before changing anything.
- Preserve unrelated user changes.
- Never reset, clean, checkout, stash, or discard user work unless explicitly authorized.
- If a pre-existing modification overlaps the intended change and safe ownership cannot be established, stop with `CONFLICTING WORKING-TREE CHANGE`.

## Core rules

1. Understand before modifying.
2. Follow existing project conventions.
3. Make the smallest sufficient change.
4. Avoid speculative refactoring.
5. Keep changes incremental.
6. Verify behavior, not merely compilation.
7. Use existing test/coverage tooling and conventions.
8. Do not invent coverage thresholds.
9. Review the final diff.
10. Document meaningful deviations or unresolved risks.

## Workflow

- [ ] Inspect worktree and relevant code.
- [ ] Confirm implementation boundary.
- [ ] Identify existing patterns to reuse.
- [ ] Make the smallest coherent change.
- [ ] Run focused tests.
- [ ] Run relevant broader regression tests.
- [ ] Obtain coverage evidence when tooling supports it.
- [ ] Review diff and scope.
- [ ] Reconcile results with acceptance criteria.
- [ ] Record unresolved risks/decisions.
- [ ] Stop before Git handoff.

For safety and side-effect classification use [implementation-safety.md](references/implementation-safety.md).

For common change categories use [change-types.md](references/change-types.md).

For verification and coverage expectations use [verification.md](references/verification.md).

For the human Git boundary use [git-boundary.md](references/git-boundary.md).

## Distributed-system implementation

When implementing distributed behavior, preserve approved decisions about:

- consistency
- availability
- partition behavior
- retries
- idempotency
- ordering
- delivery semantics
- reconciliation

Do not introduce Kafka, caches, replicas, distributed locks, or other infrastructure solely as an implementation convenience.

## Evidence labels

Use these where ambiguity matters:

`FACT`, `REQUIREMENT`, `DECISION`, `ASSUMPTION`, `OBSERVATION`, `INFERENCE`, `PROPOSAL`, `UNKNOWN`.

## Terminal statuses

Use exactly one:

- `IMPLEMENTATION COMPLETE`
- `IMPLEMENTATION BLOCKED`
- `IMPLEMENTATION FAILED VERIFICATION`
- `NEEDS HUMAN DECISION`

Never substitute generic approval language.

## Completion

Implementation is complete only when:

- intended code changes are present
- acceptance criteria are addressed
- tests/verification have been attempted appropriately
- coverage evidence is reported when available
- diff is reviewed
- unrelated changes are preserved
- no Git handoff was performed
