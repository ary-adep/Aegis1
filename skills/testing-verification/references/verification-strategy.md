# Verification Strategy

## Contents

- Scope
- Test discovery
- Test selection
- Execution
- Regression
- Failure classification
- Environment preference
- Completion

## Scope

Start from the changed behavior and its acceptance criteria.

Do not run every available test by default.

## Test discovery

Inspect:

- build files
- test source
- test naming conventions
- test profiles
- integration-test configuration
- coverage configuration
- CI commands when relevant

Prefer project-native commands.

## Test selection

Use a risk-based sequence:

1. changed behavior
2. directly affected components
3. relevant integration/contract behavior
4. regression suite
5. broader suite when justified

## Execution

Record:

- command
- scope
- result
- duration when useful
- environment assumptions
- failures/errors/skips

## Regression

A regression test set should cover behavior likely affected by the change, not merely tests with similar names.

## Failure classification

Classify evidence as:

- application defect
- test defect
- environment/tooling failure
- dependency failure
- data/setup failure
- unknown

Do not claim an application defect when the evidence only establishes an environmental failure.

## Environment preference

If an existing suitable resource is available:

- inspect it
- reuse it if safe
- avoid creating duplicate infrastructure

If mutation is required, classify its effect and obtain approval when consequential.

## Completion

State:

- verified
- not verified
- blocked
- failed
- limitations
