---
name: system-discovery
description: Discover and map a software workspace, including multiple repositories, services, libraries, adapters, dependencies, communication paths, and external integrations. Use when system-level understanding is required.
---

# Aegis1 System Discovery

## Purpose

Build an evidence-based understanding of the software system before architecture, implementation, debugging, review, or verification work that requires cross-project context.

This skill is primarily for workspaces containing:

- multiple repositories;
- multiple services;
- shared libraries;
- adapters;
- integration projects;
- infrastructure projects;
- monorepos containing multiple applications.

Do not modify application source code during discovery.

---

# 1. Discovery Principles

Inspect before concluding.

Do not assume repository names describe their actual responsibility.

Do not assume:

- every repository is a service;
- every Spring Boot application is independently deployable;
- `common` means utility library;
- `adapter` means external integration;
- communication is REST;
- dependencies imply runtime communication;
- configuration values are unused;
- documentation accurately describes current behavior.

Use repository evidence.

Distinguish:

- CONFIRMED — directly supported by evidence;
- INFERRED — strongly suggested by evidence;
- UNKNOWN — insufficient evidence.

Never present an inference as confirmed architecture.

---

# 2. Workspace Discovery

First identify the workspace boundary.

Determine:

- current working directory;
- Git repositories;
- nested repositories;
- monorepo structure;
- repository roots;
- build systems;
- project manifests;
- top-level documentation;
- architecture documentation;
- configuration files.

For a parent directory containing multiple repositories, inspect each repository independently before correlating them.

Do not assume sibling directories are related until evidence supports the relationship.

---

# 3. Repository Classification

Classify each discovered repository based on evidence.

Possible classifications:

- SERVICE
- SHARED_LIBRARY
- ADAPTER
- API_GATEWAY
- FRONTEND
- BATCH_APPLICATION
- CLI
- INFRASTRUCTURE
- TEST
- CONTRACT
- DOCUMENTATION
- UNKNOWN

For each repository determine:

- name;
- path;
- Git status;
- language;
- framework;
- build system;
- entry points;
- deployable artifacts;
- major modules;
- relevant dependencies.

If classification is uncertain, report the uncertainty.

---

# 4. Build and Dependency Discovery

Inspect build definitions such as:

- `pom.xml`;
- `build.gradle`;
- package manifests;
- module definitions;
- dependency management;
- version catalogs;
- internal artifact references.

Identify relationships such as:

```text
Repository A
    depends on
Repository B