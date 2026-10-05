# Workspace Mapping

## Contents

- Repository map
- Module map
- Service map
- Communication map
- Data map
- Integration map
- Runtime map
- Multi-repository rules

## Repository map

Use a compact structure:

`Repository → modules → deployables/libraries → important tests/configuration`

## Module map

For each important module capture:

- purpose
- source location
- public boundary
- dependencies
- tests
- persistence or integration responsibility

## Service map

For each service capture:

- responsibility
- inbound interfaces
- outbound dependencies
- data ownership indicators
- messaging
- configuration
- runtime/deployment boundary

## Communication map

Use:

`Caller → protocol → target → synchronous/asynchronous → purpose → evidence`

## Data map

Use:

`Component → store → read/write behavior → ownership evidence → important consistency implications`

## Integration map

Use:

`Internal component → adapter/client → external system → protocol → failure dependency`

## Runtime map

Capture only evidence relevant to the requested scope:

- process/container
- port
- deployment unit
- configuration source
- dependency on infrastructure
- observed health/readiness

## Multi-repository rules

Treat each repository as an independent change and ownership boundary.

Cross-repository relationships may be described, but do not imply that a change in one repository automatically authorizes modification of another.

When a task spans repositories, explicitly identify:

- repositories inspected
- contracts crossing repository boundaries
- evidence available in each repository
- unresolved cross-repository assumptions

## Mapping principle

The map is a representation of the existing system. It is not an architecture proposal.
