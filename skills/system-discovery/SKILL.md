---
name: system-discovery
description: Discover and map a software workspace, including multiple repositories, services, libraries, adapters, dependencies, communication paths, data relationships, and external integrations. Use when system-level understanding is required.
---

# Aegis1 System Discovery

## Purpose

Build an evidence-based understanding of the software system before architecture, implementation, debugging, review, or verification work that requires cross-project context.

This capability is primarily for workspaces containing:

- multiple Git repositories;
- multiple services;
- shared libraries;
- adapters;
- integration projects;
- infrastructure projects;
- monorepos containing multiple applications.

The objective is to understand what exists and how it relates.

System Discovery must not redesign the system.

System Discovery must not modify application source code.

---

# 1. Discovery Principles

Inspect before concluding.

Use actual repository evidence.

Do not assume repository names describe their actual responsibility.

Do not assume:

- every repository is a service;
- every Spring Boot application is independently deployable;
- `common` means utility library;
- `adapter` means external integration;
- communication is REST;
- dependencies imply runtime communication;
- configuration values are unused;
- documentation accurately describes current behavior;
- similarly named services have the same responsibility.

Use evidence from the workspace.

Distinguish every important finding as:

- CONFIRMED — directly supported by evidence;
- INFERRED — strongly suggested by evidence but not fully proven;
- UNKNOWN — insufficient evidence.

Never present an inference as confirmed architecture.

---

# 2. Workspace Discovery

First identify the workspace boundary.

Determine:

- current working directory;
- Git repositories;
- nested repositories;
- repository roots;
- monorepo structure;
- build systems;
- project manifests;
- top-level documentation;
- architecture documentation;
- configuration files.

For a parent directory containing multiple repositories:

1. identify each repository independently;
2. inspect each repository independently;
3. preserve repository boundaries;
4. correlate repositories only after individual discovery.

Do not assume sibling directories are related until evidence supports the relationship.

---

# 3. Multi-Repository Discovery

When multiple independent Git repositories exist under one parent workspace:

- identify each Git repository;
- record its repository root;
- identify its branch/status where relevant;
- identify its build system;
- identify its project type;
- identify its dependencies;
- identify its service/application role;
- identify relationships crossing repository boundaries.

Distinguish:

```text
Repository relationship