---
name: architecture-analysis
description: Analyze an existing or proposed software architecture using evidence, identify boundaries, dependencies, data and communication behavior, consistency and availability trade-offs, risks, constraints, and viable options. Use after system or requirements understanding is sufficient and before consequential architectural decisions.
---

# Architecture Analysis

## Purpose

Evaluate how a system is structured and how architectural choices affect correctness, maintainability, reliability, security, performance, scalability, operability, and changeability.

This is read-only. Do not implement or redesign the system during pure analysis.

## When to use

Use for:

- existing architecture assessment
- proposed architecture assessment
- service/module boundary analysis
- integration and data-flow analysis
- reliability/scalability analysis
- distributed consistency analysis
- architecture trade-offs and risks

## Operating rules

1. Start from evidence and requirements.
2. Separate current architecture from proposed options.
3. Do not assume a pattern is beneficial merely because it is common.
4. Identify trade-offs rather than declaring a universal winner.
5. Do not rank options unless the task explicitly asks for ranking.
6. Do not implement changes.
7. Make assumptions and unknowns explicit.
8. Escalate consequential architectural decisions to the human.
9. Analyze CAP only when distributed state, replication, or partition behavior can affect correctness or availability.

## Workflow

- [ ] Establish architectural scope.
- [ ] Confirm relevant requirements and constraints.
- [ ] Map boundaries and responsibilities.
- [ ] Analyze dependencies and communication.
- [ ] Analyze data ownership and consistency.
- [ ] Analyze APIs/contracts and compatibility.
- [ ] Analyze security.
- [ ] Analyze reliability and failure behavior.
- [ ] Analyze performance/scalability.
- [ ] Analyze observability and operations.
- [ ] Analyze deployment/runtime implications.
- [ ] Evaluate distributed consistency/availability when applicable.
- [ ] Identify risks, trade-offs, and viable options.
- [ ] Record human decisions required.
- [ ] Cross-check conclusions against evidence.

## Architecture dimensions

Use [architecture-dimensions.md](references/architecture-dimensions.md).

For distributed consistency and CAP analysis use [distributed-consistency.md](references/distributed-consistency.md).

For decision/trade-off analysis use [decision-analysis.md](references/decision-analysis.md).

## CAP rule

CAP is a conditional analysis lens, not a mandatory architecture section.

When relevant, describe:

- partition scenario
- consistency guarantee
- availability expectation
- affected data/operation
- failure behavior
- recovery/reconciliation
- evidence or decision supporting the trade-off

Do not reduce the architecture to a simplistic "choose two of three" statement.

## Output

Report:

1. Scope and evidence.
2. Current/proposed architecture.
3. Important boundaries.
4. Dependencies and communication.
5. Data ownership and consistency.
6. API/contract implications.
7. Security.
8. Reliability/failure behavior.
9. Performance/scalability.
10. Observability/operations.
11. Distributed-system trade-offs when applicable.
12. Risks and constraints.
13. Viable options/trade-offs.
14. Human decisions required.
15. Unknowns/evidence gaps.

## Terminal status

End with exactly:

`ARCHITECTURE ANALYSIS COMPLETE`
