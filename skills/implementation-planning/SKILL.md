---
name: "implementation-planning"
description: "Creates evidence-based implementation plans from understood requirements and established architectural direction. Use to map changes, dependencies, risks, and verification before editing code."
---

# Implementation Planning

## Shared governance

Read [Aegis1 governance](../../agents/aegis1.md) for authority, evidence, working-tree safety, and Git/production boundaries. This specialist's scope and terminal statuses take precedence over generic reporting. Read linked references only when relevant.

## Purpose

Convert understood requirements and approved architectural direction into a concrete, reviewable implementation plan.

Planning is read-only and does not implement changes.

## Preconditions

Before planning, establish enough evidence about:

- requirements
- acceptance criteria
- architecture
- repository/module structure
- existing conventions

If a critical prerequisite is missing, identify the gap rather than inventing details.

## Operating rules

1. Trace planned changes to requirements.
2. Prefer existing patterns over introducing new ones.
3. Identify concrete affected components when evidence permits.
4. Mark proposed paths/components when the target does not yet exist.
5. Do not pretend a proposed design is an existing code structure.
6. Include tests and verification in the plan.
7. Include compatibility, migration, rollout, and rollback implications when relevant.
8. Identify risks and human decisions.
9. Do not modify the repository.

## Workflow

- [ ] Confirm requirements and acceptance criteria.
- [ ] Confirm architecture decisions.
- [ ] Identify affected repositories/modules/services.
- [ ] Identify concrete files/classes/packages/configuration where known.
- [ ] Identify API and contract changes.
- [ ] Identify database/schema/migration changes.
- [ ] Identify integration/messaging changes.
- [ ] Identify tests and coverage evidence.
- [ ] Sequence implementation steps.
- [ ] Check compatibility and rollout/rollback.
- [ ] Identify risks, unknowns, and human decisions.
- [ ] Validate requirement traceability.

For detailed planning guidance use [planning-model.md](references/planning-model.md).

For impact analysis use [change-impact.md](references/change-impact.md).

## Distributed-system planning

When architecture involves distributed state, carry forward explicit decisions for:

- consistency
- partition behavior
- retries
- idempotency
- ordering
- messaging delivery
- reconciliation
- observability

Do not introduce distributed infrastructure merely because it is available.

## Output

Produce:

1. Preconditions/evidence.
2. Requirement traceability.
3. Affected components/files.
4. API/contracts.
5. Data/schema/migrations.
6. Configuration/integrations.
7. Test/verification plan.
8. Ordered implementation sequence.
9. Compatibility/rollout/rollback.
10. Risks and human decisions.
11. Definition of done.

## Terminal statuses

End the report with exactly one status line:

- `IMPLEMENTATION PLAN COMPLETE` — each material requirement has an implementation and verification mapping and no unresolved prerequisite prevents execution.
- `IMPLEMENTATION PLAN BLOCKED` — missing access, artifacts, tooling, or evidence prevents the requested analysis from being completed.
- `NEEDS HUMAN DECISION` — unresolved scope, approval, or a consequential choice prevents further work.

An analysis may finish by identifying unknowns or decisions when that was the requested output. Completion does not imply approval of those decisions, a defect-free product, or authorization to implement. If a missing input prevents the requested output, use the blocked or decision status instead.
