# Architecture Dimensions

## Contents

- Boundaries
- Dependencies
- Communication
- Data
- APIs
- Security
- Reliability
- Performance
- Scalability
- Observability
- Deployment
- Changeability

## Boundaries

Evaluate whether responsibilities and ownership boundaries are clear and supported by evidence.

Look for accidental coupling, shared mutable state, and inappropriate ownership.

## Dependencies

Classify:

- compile-time
- runtime
- synchronous
- asynchronous
- internal
- external

Identify critical dependency chains.

## Communication

Consider:

- protocol
- latency
- timeout
- retry
- idempotency
- ordering
- error propagation
- backpressure

Do not invent configuration values.

## Data

Evaluate:

- ownership
- read/write responsibility
- transaction boundaries
- consistency
- replication
- caching
- lifecycle

## APIs

Evaluate:

- contract clarity
- compatibility
- validation
- error model
- versioning
- idempotency where relevant

## Security

Consider:

- authentication
- authorization
- trust boundaries
- sensitive data
- secret handling
- auditability
- least privilege

## Reliability

Consider:

- dependency failure
- retries
- timeouts
- circuit breaking
- fallback
- recovery
- partial failure

## Performance and scalability

Consider:

- bottlenecks
- load characteristics
- synchronous chains
- database contention
- caching
- horizontal/vertical scaling
- resource limits

Use measured evidence when available.

## Observability

Consider:

- logs
- metrics
- traces
- correlation
- audit events
- failure visibility

## Deployment

Consider:

- deployable boundaries
- configuration
- compatibility during rollout
- migration sequencing
- rollback

## Changeability

Consider:

- coupling
- ownership
- testability
- migration cost
- blast radius
- future evolution
