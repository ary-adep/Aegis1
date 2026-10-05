# Acceptance Verification

## Contents

- Requirement mapping
- Evidence
- Negative cases
- Distributed behavior
- Gaps
- Final judgment

## Requirement mapping

For each important acceptance criterion identify the evidence that demonstrates it.

Use:

`AC-001 → test/report/observation`

## Evidence

Prefer:

- automated test result
- contract verification
- observed runtime result
- measured metric
- database assertion
- static verification where appropriate

Avoid relying solely on code inspection when behavior can be executed safely.

## Negative cases

Verify important invalid/failure paths when they are part of the requirement.

## Distributed behavior

When applicable, acceptance evidence may include:

- duplicate request handling
- idempotency
- ordering
- stale data tolerance
- dependency failure
- partition behavior
- recovery/reconciliation

## Gaps

Report criteria that are:

- verified
- partially verified
- unverified
- blocked

## Final judgment

Do not say "all requirements pass" when some criteria are unverified.

The final status should reflect evidence, not optimism.
