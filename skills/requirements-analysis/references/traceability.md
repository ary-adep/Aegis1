# Requirement Traceability

## Contents

- Traceability chain
- Identifiers
- Coverage
- Gaps
- Human decisions

## Traceability chain

Prefer:

`Requirement → acceptance criterion → verification evidence`

For larger work:

`Requirement → design decision → implementation change → test → verification evidence`

## Identifiers

Use stable identifiers such as:

- REQ-001
- NFR-001
- BR-001
- AC-001

Do not create identifiers merely for cosmetic completeness.

## Coverage

For each important requirement determine:

- acceptance criterion exists
- verification method exists
- implementation/design mapping exists when applicable

## Gaps

Report:

- requirement without acceptance criterion
- acceptance criterion without requirement
- implementation without requirement justification
- test without clear requirement relevance
- unresolved decision affecting correctness

## Human decisions

A requirement should become a human decision when the missing information is business-owned or materially changes:

- user-visible behavior
- compliance
- security posture
- compatibility
- data semantics
- availability/consistency expectations
- irreversible behavior

Trace the decision back to the affected requirement.
