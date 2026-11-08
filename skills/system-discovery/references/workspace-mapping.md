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

Use the folder the user opened or named as the workspace root. Read
`WORKSPACE.md` at that root if present. Treat its service names, relative
checkout paths, contract paths, and owners as navigation hints. Check those
claims against the repositories. Without a map, use explicitly named repos
or discover relevant checkouts within the authorized workspace. Leave
missing checkouts and paths resolving outside that scope as evidence gaps.

Treat each repository as an independent change and ownership boundary.
Confirm each repository root separately. For every repository that
contributes evidence, record the workspace-relative root, branch (or
detached HEAD), commit ID, and whether the working tree differs. Use
read-only Git inspection such as `git --no-optional-locks -C ROOT status
--short --branch` and `git -C ROOT rev-parse --show-toplevel HEAD` when
commands are allowed. If Git state cannot be determined, label it unknown.
Cite the working files actually inspected and identify local edits affecting
the findings. Do not fetch, switch branches, or change repository state
during discovery.

For a cross-repo contract change, trace the producer, contract declaration,
and each relevant consumer. Cite findings as `repo/path:line`. Distinguish
the observed checked-out behavior from inferred impact. Identify missing
repositories, requested branches that are not checked out, external
configuration, and other evidence gaps. A producer or schema alone cannot
establish what a missing consumer accepts. A discovered dependency does
not authorize edits in that repository.

When the user explicitly asks to save a cross-repo finding, use the
workspace root as the memory scope. Cite the relevant files using paths
relative to that root, including all source files the finding depends on.

## Mapping principle

The map is a representation of the existing system. It is not an architecture proposal.
