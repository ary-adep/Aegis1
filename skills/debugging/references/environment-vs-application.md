# Environment vs Application Failure

## Contents

- Application indicators
- Environment indicators
- Dependency indicators
- Data/setup indicators
- Mixed failures
- Decision rules

## Application indicators

Examples:

- deterministic failure in a stable environment
- failing assertion caused by changed logic
- reproducible exception in application code
- incorrect state transition

## Environment indicators

Examples:

- service unavailable before application code executes
- container runtime/network failure
- missing infrastructure
- OS/tooling incompatibility
- resource exhaustion outside application control

## Dependency indicators

Examples:

- external API unavailable
- incompatible dependency version
- broker/database unavailable
- third-party service error

## Data/setup indicators

Examples:

- missing fixture
- corrupted test data
- invalid environment configuration
- migration/setup mismatch

## Mixed failures

A product defect may trigger an environment symptom.

Do not stop at the first visible error. Establish causal order.

## Decision rules

If a failure occurs before the relevant application path can execute, investigate environment/dependency causes first.

If the application path executes and produces incorrect behavior under stable conditions, application defect becomes more likely.

When uncertain, report the uncertainty.
