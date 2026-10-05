---
name: requirements-analysis
description: Analyze software requirements, clarify scope and behavior, identify ambiguity, define acceptance criteria, and establish requirement traceability before design or implementation. Use when business or technical intent is incomplete, inconsistent, or needs to become testable.
---

# Requirements Analysis

## Purpose

Establish an evidence-based understanding of what the software must do, what constraints apply, and how correctness can be demonstrated.

This is read-only by default. It does not select architecture or implement the solution.

## When to use

Use when requirements need to be:

- extracted from prose, tickets, existing behavior, or contracts
- clarified
- bounded
- made testable
- traced to acceptance criteria
- checked for ambiguity or contradiction

## Operating rules

1. Separate stated requirements from interpretation.
2. Do not invent missing business rules.
3. Identify contradictions explicitly.
4. Identify assumptions and unknowns.
5. Treat existing behavior as evidence, not automatically as desired behavior.
6. Do not turn requirements into architecture without an explicit architecture task.
7. Define observable acceptance criteria.
8. Escalate business decisions that materially affect behavior.
9. Preserve out-of-scope boundaries.

## Workflow

- [ ] Establish objective and scope.
- [ ] Identify actors, systems, and relevant states.
- [ ] Extract functional requirements.
- [ ] Extract non-functional requirements.
- [ ] Identify business rules and constraints.
- [ ] Map important workflows/state transitions.
- [ ] Identify dependencies and external constraints.
- [ ] Identify assumptions, unknowns, contradictions, and decisions.
- [ ] Write testable acceptance criteria.
- [ ] Build requirement-to-acceptance traceability.
- [ ] Separate in-scope from out-of-scope behavior.

## Requirements detail

Use [requirements-model.md](references/requirements-model.md).

For acceptance criteria use [acceptance-criteria.md](references/acceptance-criteria.md).

For traceability use [traceability.md](references/traceability.md).

## Distributed-system requirements

When the product depends on distributed state, explicitly capture requirements for:

- consistency
- availability
- durability
- ordering
- idempotency
- retry behavior
- failure behavior
- stale data tolerance

Do not choose a CAP position as a requirement unless the evidence or decision actually supports it.

## Output

Report:

1. Objective.
2. Scope/in-scope/out-of-scope.
3. Actors and system boundaries.
4. Functional requirements.
5. Non-functional requirements.
6. Business rules.
7. Workflows/state.
8. Dependencies and constraints.
9. Acceptance criteria.
10. Traceability.
11. Assumptions.
12. Unknowns.
13. Human decisions required.

## Terminal status

End with exactly:

`REQUIREMENTS ANALYSIS COMPLETE`
