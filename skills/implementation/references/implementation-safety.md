# Implementation Safety

## Contents

- Risk levels
- Side-effect classification
- Working-tree conflicts
- Human approval
- Environment operations
- Recovery

## Risk levels

### GREEN

Reversible, local, low-impact operations with clear scope.

### YELLOW

Potentially disruptive or broad operations that require careful validation.

### RED

Consequential, destructive, irreversible, production, security-sensitive, high-risk data, or environment-changing operations requiring human decision before execution.

## Classify by effect

Classify the actual operation, not the tool name.

A command-line tool may perform either read-only inspection or consequential mutation.

Examples:

- `podman ps` → normally read-only
- `podman inspect` → normally read-only
- `podman logs` → normally read-only
- `podman run` → may create/start infrastructure
- `podman restart` → changes runtime state
- `podman rm` → removes a resource
- `podman exec` → classify the actual command executed inside the container

## Existing-resource preference

If an existing running resource is suitable:

1. inspect it read-only
2. use it if the requested test/workflow can safely do so
3. request human approval only if starting/stopping/creating/modifying is required

Do not create duplicate infrastructure merely for convenience.

## Working-tree conflict

If an existing user modification overlaps the intended change and safe ownership cannot be established:

`CONFLICTING WORKING-TREE CHANGE`

Stop. Do not overwrite or discard the change.

## Human approval

Ask before:

- destructive operations
- production access
- high-risk database changes
- infrastructure creation/modification
- security exceptions
- irreversible migrations
- external side effects
- operations whose safety cannot be established

## Recovery

If an operation partially changes state:

- stop
- record what happened
- do not conceal or automatically clean up consequential state
- identify the safest recovery path
- request human decision where needed
