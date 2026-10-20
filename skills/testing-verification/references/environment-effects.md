# Environment Effects

## Contents

- Disposable local artifacts
- Classification principle
- Read-only examples
- Consequential examples
- Container/runtime operations
- Test infrastructure
- Approval
- Recovery

## Classification principle

Classify the actual operation by its effect, not by the tool or command family.

The same tool may perform a safe inspection or a consequential mutation.

## Read-only examples

Usually read-only:

- `git status`
- `git diff`
- `podman ps`
- `podman inspect`
- `podman logs`
- `podman port`
- `podman network inspect`
- reading configuration
- inspecting test reports

Still verify context when the environment is unusual or the command has flags with side effects.

## Potentially consequential examples

Treat as potentially environment-changing:

- `podman run`
- `podman start`
- `podman restart`
- `podman rm`
- `podman network create`
- starting/stopping services
- changing local infrastructure configuration
- creating databases/queues/topics
- destructive test setup
- modifying shared test resources

## Container/runtime operations

Do not assume a container command is safe because it is "for testing."

For `podman exec` or similar commands, classify the command executed inside the container.

Read-only inspection may be allowed; database writes, package installation, service changes, file deletion, or configuration changes may be consequential.

## Test infrastructure

Integration tests may mutate:

- databases
- queues
- topics
- containers
- files
- caches
- external test services

Determine the effect before execution when the environment is shared or consequential.

## Existing-resource preference

Prefer an already-running suitable resource when it can safely satisfy the test.

Obtain approval before necessary consequential creation, start, stop, restart, or modification. Reuse does not authorize writes to shared data; inspect the test target and setup first.

## Approval

Obtain human approval before consequential environment changes.

Explain:

- operation
- expected effect
- scope
- reversibility
- why it is needed

## Recovery

If an operation partially changes environment state:

- stop
- record evidence
- do not silently clean up consequential state
- identify recovery
- escalate when necessary

## Disposable local artifacts

Routine temporary output within an inspected local test scope is not automatically consequential. Preserve source and user files. Before execution, inspect setup hooks and resource targets; approval follows actual effects, including shared or persistent writes. Production operations remain outside Aegis1 authority.
