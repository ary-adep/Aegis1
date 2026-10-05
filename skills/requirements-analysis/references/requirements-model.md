# Requirements Model

## Contents

- Requirement types
- Business rules
- Constraints
- State and workflow
- Non-functional requirements
- Assumptions and unknowns
- Distributed-system requirements

## Requirement types

### Functional

What the system must do.

### Non-functional

How the system must behave, including performance, availability, security, reliability, observability, usability, and compliance.

### Business rule

A rule that determines allowed behavior or outcome.

### Constraint

A limitation imposed by business, technology, regulation, compatibility, infrastructure, or external systems.

## State and workflow

For meaningful workflows identify:

- starting state
- trigger
- validation
- state transition
- side effects
- success outcome
- failure outcome
- retry/re-entry behavior
- terminal state

Do not invent states merely because they are common in similar systems.

## Non-functional requirements

Capture measurable or observable expectations where available.

Avoid invented numbers. If a target is missing, record it as unknown or a decision.

## Assumptions

An assumption is an interpretation used temporarily to proceed.

Label it and explain its impact.

## Unknowns

An unknown is information required for correctness but not established by available evidence.

Do not silently convert an unknown into a requirement.

## Distributed-system requirements

When multiple nodes/services/stores can diverge, ask:

- What must never be stale?
- What may be eventually consistent?
- What happens during communication loss?
- Can requests be retried?
- Can messages duplicate or reorder?
- Which operation is authoritative?
- What is the acceptable recovery behavior?

These questions feed architecture analysis; they do not themselves choose the architecture.
