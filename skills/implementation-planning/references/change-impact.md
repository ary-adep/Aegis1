# Change Impact Analysis

## Contents

- Scope
- Dependency impact
- Data impact
- Contract impact
- Operational impact
- Distributed impact
- Risk

## Scope

Identify:

- repositories
- modules
- services
- files
- tests
- configuration

## Dependency impact

Determine what callers and dependencies may be affected.

## Data impact

Check:

- schema
- migrations
- existing records
- indexes
- data ownership
- transaction boundaries

## Contract impact

Check:

- API consumers
- message consumers
- generated clients
- compatibility
- versioning

## Operational impact

Check:

- configuration
- observability
- deployment order
- feature flags
- rollback

## Distributed impact

When applicable check:

- partition behavior
- stale reads
- replication lag
- duplicate messages
- retry amplification
- idempotency
- reconciliation

## Risk

Record material risk with:

`risk → affected area → impact → mitigation/decision`

Avoid speculative risks unsupported by the change.
