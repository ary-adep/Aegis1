# Implementation Planning Model

## Contents

- Change inventory
- File-level planning
- API planning
- Data planning
- Integration planning
- Test planning
- Sequencing
- Definition of done

## Change inventory

For each change capture:

- requirement
- component
- change type
- reason
- dependency
- verification

## File-level planning

Use actual paths when established by repository evidence.

If a new path is proposed, label it `PROPOSED`.

Never invent an existing class or module merely because its name is conventional.

## API planning

Capture:

- endpoint/message
- request
- response/event
- validation
- errors
- authentication/authorization
- compatibility
- idempotency
- versioning

## Data planning

Capture:

- table/collection
- owner
- schema change
- migration
- indexes
- backfill
- compatibility
- rollback

## Integration planning

Capture:

- caller
- target
- protocol
- contract
- timeout/retry
- failure behavior
- observability

## Test planning

Map tests to acceptance criteria and important risks.

Include:

- unit
- integration
- contract
- end-to-end
- regression
- failure-path
- security
- performance

Only include categories relevant to the change.

## Sequencing

Prefer:

`preparation → implementation → migration/compatibility → tests → verification`

Make ordering explicit where one step depends on another.

## Definition of done

A plan is complete when every material requirement has:

- implementation mapping
- verification mapping
- identified risk/decision where applicable
