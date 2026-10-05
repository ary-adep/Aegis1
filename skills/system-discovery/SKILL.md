---
name: system-discovery
description: Discover and map an existing software workspace, including repositories, services, modules, libraries, dependencies, communication paths, data relationships, configuration, runtime boundaries, and external integrations. Use when reliable system understanding is required before requirements, architecture, planning, implementation, review, or debugging.
---

# System Discovery

## Purpose

Establish an evidence-based model of what exists and how its parts connect. Discovery is read-only and does not redesign or implement the system.

## When to use

Use when the task requires understanding:

- repository and module boundaries
- services, libraries, adapters, and deployables
- dependencies and communication paths
- APIs, messaging, databases, caches, files, and external systems
- configuration and runtime/deployment structure
- ownership or responsibility boundaries
- data movement and important state transitions

Do not use discovery to choose a new architecture or implement a change.

## Operating rules

1. Inspect before concluding.
2. Prefer authoritative evidence over documentation claims.
3. Distinguish `CONFIRMED`, `INFERRED`, and `UNKNOWN`.
4. Treat each Git repository independently; do not invent a single repository boundary across multiple repositories.
5. Preserve module/service/deployable/library boundaries.
6. Trace important communication and data paths end-to-end.
7. Record uncertainty instead of filling gaps with assumptions.
8. Do not modify product or repository state.
9. Do not persist project knowledge during pure discovery unless the user explicitly asks for it.

## Workflow

- [ ] Establish workspace and repository boundaries.
- [ ] Identify applications, services, modules, libraries, and deployables.
- [ ] Inspect build files and dependency relationships.
- [ ] Trace relevant HTTP, messaging, database, file, cache, and SDK communication.
- [ ] Inspect configuration and environment-sensitive behavior.
- [ ] Map important data stores, ownership, and flows.
- [ ] Identify external integrations and runtime/deployment boundaries.
- [ ] Cross-check important findings against source evidence.
- [ ] Separate confirmed facts from inference and unknowns.
- [ ] Report the discovered model without redesigning it.

## Evidence

Use the evidence model in [evidence-model.md](references/evidence-model.md).

## Discovery dimensions

For detailed discovery methods, use [discovery-methods.md](references/discovery-methods.md).

For workspace/repository mapping, use [workspace-mapping.md](references/workspace-mapping.md).

## Output

Report:

1. Scope inspected.
2. Repository/module/service boundaries.
3. Major components and responsibilities.
4. Dependency and communication map.
5. Data and integration relationships.
6. Configuration/runtime findings.
7. Confirmed facts.
8. Inferences.
9. Unknowns and evidence gaps.
10. Important discovery limitations.

Do not include architecture recommendations unless a separate architecture-analysis task is explicitly requested.

## Terminal status

End with exactly:

`DISCOVERY COMPLETE`
