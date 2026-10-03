---
name: system-discovery
description: Discover and map a software workspace, including multiple repositories, services, libraries, adapters, dependencies, communication paths, data relationships, and external integrations. Use when system-level understanding is required.
---

# System Discovery

## Purpose

System Discovery provides an evidence-based understanding of a software system before architecture analysis, implementation, debugging, review, or verification.

It answers:

> What exists, and how is it connected?

It does not answer:

> What should we change?

System Discovery is read-only by default.

Do not modify application source code, configuration, build files, databases, documentation, or repository state during discovery.

---

# 1. Discovery Principles

## Inspect before concluding

Do not assume architecture from:

- repository names;
- directory names;
- service names;
- README descriptions;
- conventional Spring Boot patterns;
- package names;
- Docker service names;
- module names.

Use repository evidence.

Prefer:

- source code;
- build files;
- configuration;
- API contracts;
- database schemas;
- deployment definitions;
- messaging configuration;
- integration configuration;
- scripts;
- tests;
- documentation as supporting evidence.

---

# 2. Evidence Classification

Every important finding must be classified as one of:

### CONFIRMED

Directly supported by source code, configuration, build files, schema, deployment configuration, or other strong workspace evidence.

### INFERRED

Not directly confirmed, but strongly supported by available evidence.

Explain the evidence and why the relationship is inferred.

### UNKNOWN

The workspace does not contain enough evidence to establish the relationship.

Do not convert UNKNOWN into an assumption.

Never present an inferred relationship as confirmed.

---

# 3. Workspace Discovery

First determine the workspace boundary.

Inspect:

- workspace folders;
- top-level directories;
- Git repositories;
- nested Git repositories;
- build roots;
- multi-module structures;
- deployment/infrastructure directories.

Determine whether the workspace contains:

- one repository;
- multiple repositories;
- a monorepo;
- multiple independent applications;
- shared libraries;
- infrastructure repositories;
- configuration repositories;
- contracts repositories.

Do not assume every repository located near the workspace belongs to the system.

For a multi-root workspace, analyze only repositories that are actually part of the workspace unless the user explicitly requests otherwise.

---

# 4. Multi-Repository Discovery

When multiple Git repositories are present:

1. Identify every repository in the workspace.
2. Analyze each repository independently.
3. Preserve repository boundaries.
4. Identify the role of each repository.
5. Identify cross-repository dependencies only after individual repository analysis.
6. Correlate repositories using evidence.

Distinguish:

- Git repository boundary;
- Maven/Gradle module boundary;
- application boundary;
- service boundary;
- deployable boundary;
- library boundary.

Do not assume:

```text
1 repository = 1 service