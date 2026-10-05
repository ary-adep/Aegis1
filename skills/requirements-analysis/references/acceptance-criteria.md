# Acceptance Criteria

## Contents

- Characteristics
- Positive behavior
- Negative behavior
- Boundary conditions
- Failure behavior
- Distributed behavior
- Examples

## Characteristics

Good acceptance criteria are:

- observable
- testable
- unambiguous
- scoped
- traceable to a requirement

Avoid implementation-specific criteria unless implementation is itself part of the requirement.

## Positive behavior

State what should happen for valid inputs and normal flows.

## Negative behavior

Capture important:

- invalid input
- unauthorized access
- unavailable dependency
- duplicate request
- conflicting state
- unsupported transition

## Boundary conditions

Capture meaningful boundaries such as:

- empty
- maximum
- minimum
- repeated
- concurrent
- expired
- missing
- already completed

Only include boundaries supported by requirements or evidence.

## Failure behavior

Define expected behavior when a dependency or operation fails:

- response/outcome
- state preservation
- retry behavior
- user-visible behavior
- recovery expectation

## Distributed behavior

When applicable, acceptance criteria may include:

- stale reads
- duplicate delivery
- ordering
- idempotency
- partition behavior
- reconciliation
- recovery

Do not invent a consistency guarantee.

## Example

Requirement:

`A duplicate request must not create two customer records.`

Acceptance criterion:

`Given the same idempotency key is submitted twice for the same operation, the system produces one customer creation outcome and does not create a second customer record.`

The exact implementation remains an architecture/implementation decision.
