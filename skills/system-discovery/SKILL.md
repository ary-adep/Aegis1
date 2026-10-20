---
name: "system-discovery"
description: "Maps existing repositories, components, dependencies, communication, data, and runtime boundaries from evidence. Use when system understanding is needed; does not redesign or implement changes."
---

# System Discovery

## Shared governance

Read [Aegis1 governance](../../agents/aegis1.md) for authority, evidence, working-tree safety, and Git/production boundaries. This specialist's scope and terminal statuses take precedence over generic reporting. Read linked references only when relevant.

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

## Revision and coverage boundaries

For a report-only revision, use the supplied report and evidence under the user's tool constraints; do not restart the discovery checklist. If raw source content is absent, attribute retained claims to the earlier report and leave their truth unverified. Do not redefine `CONFIRMED` to mean that a file-read event was recorded.

Report full reads, partial excerpts, searches, and inventories at their actual scope. Include approval-blocked checks and the questions they leave unresolved. Do not retry them without authorization. Separate local configuration declarations, uninspected external configuration, and inferred effective runtime behavior. Claim file preservation was independently verified only to the extent supported by a before/after comparison; absence of visible writes alone is narrower evidence.

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

## Terminal statuses

End the report with exactly one status line:

- `DISCOVERY COMPLETE` — the requested discovery output is supported by the inspected evidence and its scope and limitations are explicit. A constrained report revision may complete by correcting or removing unsupported claims; it does not certify new inspection. Loading instructions alone is not discovery. Do not silently shrink requested scope to accessible scope when a blocker prevents a required finding.
- `DISCOVERY BLOCKED` — missing access, artifacts, tooling, or evidence prevents the requested analysis from being completed.
- `NEEDS HUMAN DECISION` — unresolved scope, approval, or a consequential choice prevents further work.

When the requested deliverable is a bounded account of what supplied evidence confirms and leaves unknown, produce that account and use `DISCOVERY COMPLETE` once the requested distinctions are made. Uninspected runtime behavior, historical approval-blocked checks, or absent before/after snapshots are reportable limitations, not automatically blockers to this deliverable. Do not require approval, new reads, or resolution of every unknown merely to finish it. Reserve blocked/decision statuses for a missing prerequisite or choice that actually prevents the requested output; missing required instructions still follow the governance precedence rule.

An analysis may finish by identifying unknowns or decisions when that was the requested output. Completion does not imply approval of those decisions, a defect-free product, or authorization to implement. If a missing input prevents the requested output, use the blocked or decision status instead.
