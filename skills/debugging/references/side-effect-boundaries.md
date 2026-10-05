# Debugging Side-Effect Boundaries

## Contents

- Principle
- Read-only inspection
- Potential mutation
- Existing resources
- Human approval
- Recovery

## Principle

Classify the actual operation by effect, not by the tool.

## Read-only inspection

Usually safe:

- status
- logs
- inspect
- configuration reads
- process listing
- network inspection
- test report inspection

## Potential mutation

Examples:

- starting services
- restarting containers
- creating networks
- creating databases
- deleting resources
- changing configuration
- writing test data
- installing packages

## Existing resources

Prefer inspection and reuse of suitable existing resources.

Do not create duplicate infrastructure solely for convenience.

## Human approval

Obtain approval when the operation changes shared, persistent, infrastructure, production, or otherwise consequential state.

State the exact operation and expected effect.

## Recovery

If diagnosis causes an approved consequential change:

- record it
- verify resulting state
- do not conceal it
- restore only when authorized and safe
