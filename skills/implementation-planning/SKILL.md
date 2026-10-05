---
name: implementation-planning
description: Create evidence-based implementation plans from approved requirements and known architecture, identifying affected components, files, interfaces, data changes, sequencing, tests, risks, and verification before code changes.
---

# Implementation Planning

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

## Terminal status

End with exactly:

`IMPLEMENTATION PLAN COMPLETE`
