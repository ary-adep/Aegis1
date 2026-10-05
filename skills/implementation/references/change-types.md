# Implementation Change Types

## Contents

- Application code
- Tests
- APIs
- Database
- Configuration
- Messaging
- Security
- Observability

## Application code

Reuse existing patterns and keep changes localized.

Avoid unrelated refactoring.

## Tests

Add or update tests that demonstrate changed behavior.

Prefer focused tests first, then relevant regression coverage.

## APIs

Consider:

- validation
- compatibility
- error behavior
- authentication/authorization
- idempotency
- versioning

Do not introduce breaking changes without an explicit decision.

## Database

Treat schema and data changes as high-impact.

Check:

- migration ordering
- backward compatibility
- indexes
- transaction behavior
- rollback/recovery
- data preservation

## Configuration

Reuse established configuration mechanisms.

Never hard-code secrets.

Do not invent environment names when project conventions already exist.

## Messaging

Check:

- delivery semantics
- duplicates
- ordering
- retries
- idempotency
- consumer compatibility

## Security

Check:

- trust boundaries
- authorization
- sensitive data
- secret handling
- logging
- dependency risk

## Observability

Add only observability needed to understand or operate the changed behavior.

Avoid noisy or duplicated telemetry.
