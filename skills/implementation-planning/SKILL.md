---
name: implementation-planning
description: Create evidence-based implementation plans from approved requirements and known architecture, identifying affected components, files, changes, sequencing, tests, risks, and verification before code changes.
---

# Implementation Planning

## Purpose

Implementation Planning converts understood requirements and architectural decisions into a concrete, reviewable plan for implementation.

It answers:

> What needs to change, where does it change, in what order, and how will the result be verified?

Implementation Planning does not implement the change.

## Core Principles

### 1. Plan from evidence

Inspect the actual repository before naming files, classes, modules, APIs, schemas, or configuration.

Do not invent file paths or component names.

### 2. Requirements traceability

Every meaningful implementation change should trace back to:

```text
Requirement
    ↓
Architecture / Design Decision
    ↓
Implementation Change
    ↓
Verification
```

If a planned change has no requirement or established technical reason, identify it as optional or remove it.

### 3. Brownfield first

For an existing system:

- inspect established conventions;
- identify the actual affected components;
- understand current behavior;
- preserve compatibility unless a change is required;
- avoid unrelated refactoring.

### 4. Smallest sufficient change

Prefer:

- existing abstractions;
- existing libraries;
- existing patterns;
- localized changes;
- reversible changes.

Do not introduce speculative frameworks, abstractions, or infrastructure.

## Inputs

Use available evidence such as:

- approved requirements;
- acceptance criteria;
- architecture analysis;
- system discovery;
- source code;
- tests;
- API contracts;
- database schema and migrations;
- configuration;
- build files;
- deployment configuration.

If required information is missing, record it as unknown.

## Scope

Identify:

- in-scope implementation work;
- out-of-scope work;
- affected modules;
- affected services;
- affected APIs;
- affected data;
- affected configuration;
- affected integrations;
- affected tests.

## Affected Components

For each component, identify:

| Component | Evidence | Change | Reason |
| --- | --- | --- | --- |
| Module/service | Actual repository evidence | Required modification | Requirement/design link |
| API | Existing contract/code | Contract or implementation change | Requirement link |
| Database | Schema/migration evidence | Data/schema change | Requirement link |
| Configuration | Existing config | Required setting | Operational requirement |
| Integration | Existing adapter/client | Required integration change | Dependency |

Never claim a component is affected without evidence.

## File-Level Planning

When repository evidence permits, identify:

- file path;
- class/module;
- method/function;
- intended change;
- related requirement;
- related test.

Example:

```text
src/.../CustomerController.java
    Change: add validation for requested field
    Requirement: FR-4
    Test: CustomerControllerTest
```

If the exact file is unknown, state that instead of guessing.

## API Changes

For API-related changes identify:

- endpoint;
- HTTP method;
- request changes;
- response changes;
- validation;
- error behavior;
- authentication/authorization;
- compatibility impact;
- idempotency;
- affected consumers.

Do not invent endpoint names or schemas.

## Database Changes

Identify:

- affected tables/entities;
- columns;
- indexes;
- constraints;
- migrations;
- data backfill;
- rollback implications.

Distinguish confirmed schema changes from proposed changes.

For destructive or irreversible database operations, explicitly flag the risk and human decision requirement.

## Configuration

Identify:

- application configuration;
- environment variables;
- secrets;
- feature flags;
- timeout/retry settings;
- external endpoints;
- deployment configuration.

Never include actual secret values in a plan.

## Integration Changes

For external or internal integrations identify:

- caller;
- target;
- protocol;
- contract;
- timeout;
- retry;
- error handling;
- idempotency;
- observability;
- compatibility.

Use existing system evidence where available.

## Test Planning

Map implementation changes to verification.

Include, where applicable:

- unit tests;
- integration tests;
- API tests;
- contract tests;
- database tests;
- end-to-end tests;
- regression tests;
- security tests;
- failure-path tests.

Each important acceptance criterion should have a verification path.

## Implementation Sequence

Define a logical order such as:

```text
1. Contract / requirement preparation
2. Data or migration changes
3. Domain/application changes
4. API/integration changes
5. Tests
6. Configuration
7. Verification
```

Do not force this sequence when the repository's conventions require another order.

Identify dependencies between steps.

## Compatibility

Evaluate:

- API compatibility;
- database compatibility;
- configuration compatibility;
- event/message compatibility;
- existing consumer behavior;
- deployment ordering.

Flag breaking changes explicitly.

## Rollout and Rollback

When relevant, identify:

- feature flag needs;
- migration ordering;
- backward-compatible deployment sequence;
- rollback constraints;
- data rollback limitations.

Do not claim rollback is safe when data changes are irreversible.

## Risks

For each significant risk capture:

```text
Risk:
Evidence:
Impact:
Likelihood / confidence:
Mitigation:
Human decision required:
```

Do not invent numerical risk scores unless the project already uses them.

## Human Decisions

Escalate consequential decisions such as:

- breaking API changes;
- destructive database operations;
- security exceptions;
- major architecture deviations;
- irreversible migrations;
- unclear business behavior;
- compatibility trade-offs;
- production rollout decisions.

Record the decision required without making it on behalf of the human.

## Assumptions and Unknowns

Keep separate:

- confirmed facts;
- requirements;
- architecture decisions;
- assumptions;
- unknowns.

A plan must not silently convert an assumption into an implementation requirement.

## Definition of Done

The implementation plan should define completion in terms of:

- requirements satisfied;
- acceptance criteria covered;
- implementation changes completed;
- tests added or updated;
- relevant verification executed;
- compatibility checked;
- security implications reviewed;
- database/configuration changes verified;
- documentation updated where required;
- unresolved risks recorded.

## Read/Write Boundary

Pure Implementation Planning is read-only.

Do not:

- modify source code;
- modify tests;
- modify configuration;
- create migrations;
- change API contracts;
- install dependencies;
- commit changes.

If implementation is explicitly requested after planning, the implementation workflow may continue separately.

## Relationship to Other Aegis1 Capabilities

Requirements Analysis answers:

> What must the system do?

System Discovery answers:

> What exists and how is it connected?

Architecture Analysis answers:

> How is the system structured and what trade-offs exist?

Implementation Planning answers:

> What concrete changes are required to implement the approved direction?

Implementation answers:

> How is the approved plan executed in code?

Testing answers:

> Does the implementation satisfy the requirements?

Do not collapse these responsibilities.

## Workflow

```text
Understand approved requirements
        ↓
Inspect repository and evidence
        ↓
Identify affected components
        ↓
Map requirements to changes
        ↓
Identify API/data/config/integration impact
        ↓
Define implementation sequence
        ↓
Define tests and verification
        ↓
Assess compatibility and risks
        ↓
Identify human decisions
        ↓
Report plan
```

Use only the stages necessary for the task.

## Reporting

Use this structure for pure Implementation Planning:

```markdown
# Implementation Plan

## Objective

## Requirements / Acceptance Criteria

## Scope

## Affected Components

## File-Level Changes

## API Changes

## Database Changes

## Configuration Changes

## Integration Changes

## Implementation Sequence

## Test Plan

## Compatibility

## Rollout / Rollback

## Risks

## Assumptions

## Unknowns

## Human Decisions Required

## Out of Scope

## Traceability

## Plan Status
```

Keep evidence and proposed changes distinct.

## Completion Criteria

Implementation Planning is complete when:

- the relevant requirements are understood;
- the repository has been inspected sufficiently;
- affected components are identified;
- planned changes are traceable to requirements or established decisions;
- implementation sequence is defined;
- tests and verification are identified;
- compatibility and risks are considered;
- assumptions and unknowns are explicit;
- human decisions are identified;
- no implementation changes were made during pure planning.

## Plan Status

Pure Implementation Planning should conclude with exactly:

```text
IMPLEMENTATION PLAN COMPLETE
```

Do not replace this with:

- READY FOR APPROVAL
- NEEDS HUMAN DECISION
- BLOCKED
- FAILED VERIFICATION

A consequential decision may still be listed under `Human Decisions Required`. That does not prevent the implementation plan itself from being complete.

## Final Principle

An implementation plan should be specific enough for an engineer to execute without guessing, while remaining faithful to the approved requirements, architecture, repository evidence, and human decisions.
