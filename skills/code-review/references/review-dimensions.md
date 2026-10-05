# Review Dimensions

## Contents

- Correctness
- Requirements
- Security
- API compatibility
- Data
- Performance
- Reliability
- Observability
- Testing
- Coverage
- Maintainability
- Scope
- Distributed systems

## Correctness

Check logic, state transitions, error handling, concurrency, edge cases, and invariants.

## Requirements

Determine whether changed behavior matches the stated requirement and acceptance criteria.

## Security

Check:

- authentication
- authorization
- validation
- sensitive data
- secret handling
- injection
- trust boundaries
- logging

## API compatibility

Check request/response/event contracts, consumers, versioning, error behavior, and breaking changes.

## Data

Check schema, migrations, transactions, ownership, consistency, and data preservation.

## Performance

Look for material:

- unnecessary I/O
- N+1 queries
- unbounded work
- contention
- memory growth
- latency amplification

Do not speculate without a plausible mechanism.

## Reliability

Check:

- timeouts
- retries
- duplicate effects
- fallback
- failure propagation
- recovery

## Observability

Check whether important new failure paths are diagnosable.

## Testing

Check whether changed behavior and important risks have adequate tests.

## Coverage

Check actual coverage evidence when available. Do not impose arbitrary thresholds.

## Maintainability

Check clarity, coupling, duplication, complexity, and consistency with existing patterns.

## Scope

Identify unrelated changes, unnecessary refactoring, and accidental behavior changes.

## Distributed systems

When relevant review consistency, partition behavior, message semantics, idempotency, replication, caching, and reconciliation.
