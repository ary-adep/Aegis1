---
name: requirements-analysis
description: Analyze software requirements, clarify scope and behavior, identify ambiguity, define acceptance criteria, and establish requirement traceability before design or implementation.
---

# Requirements Analysis

## Purpose

Requirements Analysis establishes an evidence-based understanding of what the software must do, what constraints apply, and how correctness can be demonstrated.

It answers:

> What exactly needs to be built or changed, and how will we know it is correct?

Requirements Analysis does not design the solution and does not implement code.

## Core Principles

### 1. Requirements before solutions

Understand the desired behavior before proposing technical implementation.

Do not turn a technical preference into a business requirement.

### 2. Evidence over invention

Classify important statements as:

- FACT — established by available evidence.
- REQUIREMENT — explicitly requested or established by authoritative project material.
- ASSUMPTION — temporarily necessary but not confirmed.
- CONSTRAINT — a limitation that must be respected.
- DEPENDENCY — an external condition, system, team, or capability required for the requirement.
- UNKNOWN — insufficient evidence.

Never silently convert an assumption into a requirement.

### 3. Separate what from how

Requirements describe desired behavior and constraints.

Architecture and implementation describe how the behavior will be achieved.

Do not introduce classes, APIs, databases, frameworks, or infrastructure unless they are actually required by the requirement or are explicitly requested.

### 4. Brownfield first

For an existing system:

- inspect existing behavior and contracts;
- identify current requirements represented by code and tests;
- preserve established behavior unless a change is requested;
- identify compatibility constraints;
- distinguish current behavior from desired behavior.

For greenfield work:

- establish the business outcome first;
- define actors, goals, scope, behavior, and constraints;
- avoid premature technical design.

## Scope

Establish:

- objective;
- actors and users;
- business outcome;
- functional requirements;
- non-functional requirements;
- inputs;
- outputs;
- business rules;
- states and transitions;
- dependencies;
- constraints;
- assumptions;
- out-of-scope behavior.

## Requirement Extraction

Convert the user's request into explicit, testable requirements.

For each requirement capture, where possible:

| Field | Meaning |
| --- | --- |
| ID | Stable requirement identifier |
| Requirement | What the system must do |
| Source | User, specification, existing behavior, contract, etc. |
| Type | Functional, non-functional, constraint, dependency |
| Priority | Only when explicitly provided or objectively required |
| Acceptance Criteria | Observable conditions proving the requirement |
| Dependencies | Required external behavior or capability |
| Open Questions | Information still required |

Do not invent priorities.

## Functional Requirements

Identify observable system behavior such as:

- commands or user actions;
- inputs and validation;
- successful outcomes;
- rejected inputs;
- state transitions;
- error behavior;
- retries;
- duplicate handling;
- authorization requirements;
- integration behavior;
- persistence requirements;
- notifications or side effects.

A functional requirement should be specific enough to derive a test.

## Non-Functional Requirements

Identify requirements concerning:

- security;
- privacy;
- performance;
- availability;
- reliability;
- scalability;
- observability;
- accessibility;
- compatibility;
- auditability;
- data retention;
- recovery;
- operational constraints.

Do not invent numerical targets. If a target is missing, record it as an unknown or decision.

## Business Rules

Extract rules separately from technical behavior.

Examples:

- eligibility conditions;
- validation rules;
- state transition rules;
- uniqueness rules;
- limits;
- time windows;
- authorization rules;
- calculation rules;
- approval requirements.

When a business rule is ambiguous, surface the ambiguity rather than selecting a rule silently.

## Actors and Goals

Identify:

- primary actors;
- supporting actors;
- external systems;
- administrators or operators;
- automated processes.

For each important actor, identify the goal relevant to the requested change.

Do not infer sensitive business roles without evidence.

## Workflow and State

For workflows, identify:

```text
Initial State
    ↓
Action / Event
    ↓
Validation
    ↓
State Transition
    ↓
Outcome
```

Capture:

- valid transitions;
- invalid transitions;
- retry behavior;
- expiration;
- cancellation;
- duplicate events;
- terminal states.

If the state model cannot be established from evidence, record it as incomplete.

## Inputs and Outputs

For each interaction identify:

- required inputs;
- optional inputs;
- format;
- validation;
- output;
- error output;
- side effects;
- idempotency expectations where relevant.

Do not design an API merely because the requirement describes an interaction.

## Ambiguity Analysis

Actively look for:

- contradictory statements;
- undefined terms;
- missing actors;
- missing error behavior;
- missing edge cases;
- unclear ownership;
- unclear timing;
- unclear authorization;
- unspecified data requirements;
- unspecified external dependencies;
- conflicting existing behavior.

Classify each issue:

- Blocking — cannot safely define the requirement without an answer.
- Non-blocking — reasonable interpretation exists but should be recorded.
- Informational — useful clarification with no immediate impact.

Do not resolve blocking business ambiguity by guessing.

## Acceptance Criteria

Acceptance criteria must be observable and testable.

Prefer:

```text
Given ...
When ...
Then ...
```

or equivalent explicit conditions.

Cover, when applicable:

- happy path;
- validation failures;
- authorization failures;
- boundary conditions;
- duplicate requests;
- retries;
- dependency failures;
- persistence failures;
- state transitions;
- security-sensitive cases.

Do not create acceptance criteria for behavior that was never required or reasonably implied.

## Negative and Edge Cases

Consider:

- missing input;
- malformed input;
- invalid state;
- duplicate request;
- repeated operation;
- concurrent operation;
- timeout;
- dependency unavailable;
- partial failure;
- stale data;
- unauthorized access;
- unexpected external response.

Only include cases relevant to the requirement.

## Dependencies

Identify dependencies such as:

- external services;
- databases;
- identity providers;
- configuration;
- message brokers;
- files;
- third-party APIs;
- upstream or downstream teams;
- existing application behavior.

Distinguish confirmed dependencies from assumptions.

## Constraints

Capture constraints explicitly stated or established by authoritative evidence.

Examples:

- backward compatibility;
- regulatory requirements;
- supported runtime;
- existing API contract;
- deployment restrictions;
- technology constraints;
- performance targets.

Do not manufacture constraints.

## Scope Boundary

Explicitly identify:

### In Scope

Behavior required to satisfy the request.

### Out of Scope

Behavior that is intentionally not part of the request or cannot be established as required.

### Deferred

Relevant work that may be required later but is not part of the current task.

## Existing System Requirements

In brownfield systems, inspect:

- source code;
- tests;
- API contracts;
- database schema;
- migrations;
- configuration;
- documentation;
- integration contracts.

Existing behavior is evidence, not automatically the desired future behavior.

If requested behavior conflicts with an existing contract, identify the conflict and its compatibility implications.

## Requirement Traceability

Where meaningful, maintain:

```text
Requirement
    ↓
Acceptance Criterion
    ↓
Design Decision
    ↓
Implementation Change
    ↓
Test
```

Requirements Analysis itself normally stops at the requirements and acceptance-criteria level.

Design, implementation, and testing are handled by their respective workflows.

## Human Decisions

Human decisions are required when requirements contain consequential unresolved choices, including:

- conflicting business rules;
- ambiguous ownership;
- security policy;
- data retention;
- externally visible behavior;
- compatibility trade-offs;
- irreversible business behavior;
- missing business authority.

Record:

```text
Decision:
Why it matters:
Options / interpretations:
Evidence:
What is needed from the human:
```

Do not make the business decision on behalf of the human.

## Read/Write Boundary

Pure Requirements Analysis is read-only.

Do not:

- modify source code;
- modify configuration;
- modify schemas;
- create migrations;
- change API contracts;
- add tests;
- create implementation files;
- modify project documentation;
- commit changes.

If implementation is requested, Requirements Analysis may establish the requirements and then the appropriate implementation workflow may continue.

## Relationship to Other Aegis1 Capabilities

Requirements Analysis answers:

> What must the system do?

System Discovery answers:

> What exists and how is it connected?

Architecture Analysis answers:

> How is the system structured, and what architectural trade-offs exist?

Implementation answers:

> How should the approved change be built?

Testing answers:

> Does the implementation satisfy the requirements?

Do not collapse these responsibilities.

## Recommended Workflow

```text
Understand request
      ↓
Extract requirements
      ↓
Inspect relevant evidence
      ↓
Classify facts / requirements / assumptions
      ↓
Identify scope and dependencies
      ↓
Analyze ambiguity and conflicts
      ↓
Define acceptance criteria
      ↓
Identify human decisions
      ↓
Establish traceability
      ↓
Report
```

Use only the stages necessary for the task.

## Reporting

Use this structure for pure Requirements Analysis:

```markdown
# Requirements Analysis

## Objective

## Scope

## Actors

## Functional Requirements

## Non-Functional Requirements

## Business Rules

## Workflow / State

## Acceptance Criteria

## Dependencies

## Constraints

## Assumptions

## Unknowns / Ambiguities

## Human Decisions Required

## Out of Scope

## Traceability

## Analysis Status
```

Keep evidence and interpretation distinct.

Do not present assumptions as facts.

## Completion Criteria

Requirements Analysis is complete when:

- the objective is understood;
- scope is explicit;
- requirements are identified;
- relevant business rules are captured;
- acceptance criteria are testable;
- dependencies and constraints are identified;
- important ambiguities are surfaced;
- assumptions and unknowns are explicit;
- consequential human decisions are identified;
- no implementation was performed during pure analysis.

## Analysis Status

Pure Requirements Analysis should conclude with exactly:

```text
REQUIREMENTS ANALYSIS COMPLETE
```

Do not replace this with:

- READY FOR APPROVAL
- NEEDS HUMAN DECISION
- BLOCKED
- FAILED VERIFICATION

A consequential decision may still be listed under `Human Decisions Required`. That does not prevent the requirements analysis itself from being complete.

## Final Principle

Requirements Analysis should make the requested behavior precise enough that architecture, implementation, and testing can proceed without inventing business intent.

It should reduce ambiguity, not hide it.
