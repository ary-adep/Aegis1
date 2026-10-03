---
name: system-discovery
description: Discover and map a software workspace, including multiple repositories, services, libraries, adapters, dependencies, communication paths, data relationships, and external integrations. Use when system-level understanding is required.
---

# System Discovery

## Purpose

System Discovery establishes an evidence-based understanding of what exists in a software workspace and how its parts are connected.

It answers:

> What exists, and how is it connected?

System Discovery is read-only by default.

It does not redesign the system, recommend improvements, implement changes, or make architectural decisions.

---

# 1. Discovery Principles

## Inspect before concluding

Use evidence from:

- repository structure;
- Git metadata;
- build files;
- source code;
- configuration;
- API contracts;
- database schemas;
- migrations;
- messaging configuration;
- deployment definitions;
- documentation.

Do not assume architecture from:

- repository names;
- directory names;
- framework conventions;
- README claims alone;
- common industry patterns.

For every important finding classify it as:

- CONFIRMED;
- INFERRED;
- UNKNOWN.

## Evidence hierarchy

Prefer:

1. source code;
2. tests;
3. schemas/migrations;
4. API contracts;
5. configuration;
6. build/dependency definitions;
7. deployment definitions;
8. documentation.

Documentation can explain intent, but implementation evidence determines what actually exists.

---

# 2. Workspace Discovery

First determine the workspace boundary.

Identify:

- current working directory;
- workspace roots;
- Git repositories;
- nested repositories;
- multi-root workspace folders;
- monorepos;
- sibling repositories explicitly included in the workspace.

Do not assume every repository near the workspace belongs to the system.

For a multi-root workspace, analyze repositories that are actually part of the workspace unless the user explicitly requests broader discovery.

Record the workspace boundary in the report.

---

# 3. Repository Inventory

For every repository in scope identify:

- repository path;
- Git status;
- branch;
- commit when useful;
- remote when useful;
- repository role;
- build system;
- primary technology;
- application/module count.

Possible repository roles include:

- SERVICE;
- SHARED_LIBRARY;
- ADAPTER;
- API_GATEWAY;
- FRONTEND;
- BATCH_APPLICATION;
- CLI;
- INFRASTRUCTURE;
- TEST;
- CONTRACT;
- DOCUMENTATION;
- CONFIGURATION;
- UNKNOWN.

Do not assume one repository equals one service.

---

# 4. Multi-Repository Discovery

When multiple Git repositories are present:

1. identify every repository in the workspace;
2. analyze each repository independently;
3. preserve repository boundaries;
4. identify the role of each repository;
5. identify cross-repository dependencies only after individual analysis;
6. correlate repositories using evidence.

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
```

or:

```text
1 module = 1 deployable
```

or:

```text
1 service = 1 database
```

---

# 5. Module Discovery

Within each repository identify:

- Maven modules;
- Gradle modules;
- packages;
- deployable applications;
- libraries;
- generated code;
- test modules;
- infrastructure modules.

For each important module determine:

- purpose;
- role;
- dependencies;
- deployability;
- ownership evidence where available.

---

# 6. Build and Dependency Discovery

Inspect:

- pom.xml;
- build.gradle;
- settings.gradle;
- dependency management;
- plugins;
- profiles;
- generated sources;
- shared parent builds.

Identify:

- direct dependencies;
- important transitive relationships when evidence is available;
- shared libraries;
- framework dependencies;
- generated-code dependencies;
- build-time versus runtime dependencies.

Do not interpret a dependency as an architectural relationship unless evidence supports that conclusion.

---

# 7. Application and Service Discovery

Identify independently deployable applications.

For each application record:

- name;
- responsibility;
- framework;
- entry point;
- runtime profile;
- configuration source;
- deployment definition;
- exposed interfaces;
- persistence;
- external dependencies.

Classify each application as appropriate.

Do not infer business responsibility solely from class names.

---

# 8. Shared Library Discovery

Identify libraries used by multiple applications.

Determine:

- repository containing the library;
- consumers;
- compile-time relationships;
- runtime relationships;
- versioning;
- generated/shared models.

Distinguish:

- genuinely shared code;
- duplicated code;
- copied DTOs;
- shared parent/build configuration.

---

# 9. Adapter Discovery

Identify adapters between:

- application and external API;
- application and database;
- application and messaging platform;
- application and cloud SDK;
- application and file/SFTP system;
- application and identity provider;
- application and legacy system.

For each adapter record:

- caller;
- target;
- mechanism;
- configuration;
- contract;
- failure handling evidence.

---

# 10. Communication Discovery

Identify all important communication paths.

Consider:

- HTTP/REST;
- WebClient;
- RestClient;
- RestTemplate;
- Feign;
- gRPC;
- Kafka;
- RabbitMQ;
- JMS;
- other messaging;
- database access;
- file exchange;
- SFTP;
- caches;
- SDK calls;
- scheduled jobs.

For every important relationship classify:

- CONFIRMED;
- INFERRED;
- UNKNOWN.

Provide evidence.

---

# 11. REST and HTTP Discovery

For HTTP relationships identify where evidence permits:

- caller;
- target;
- HTTP client;
- endpoint;
- method;
- route;
- load balancing;
- authentication;
- timeout;
- retry;
- circuit breaker;
- fallback.

Do not claim runtime behavior that was only inferred from configuration.

---

# 12. Messaging Discovery

Search for:

- Kafka producers/consumers;
- RabbitMQ producers/consumers;
- JMS listeners;
- event publishers;
- event handlers;
- topics;
- queues;
- exchanges;
- bindings.

Identify:

- producer;
- consumer;
- message type;
- topic/queue;
- serialization;
- configuration;
- retry/dead-letter evidence.

If no messaging exists, state that based on the inspected evidence.

---

# 13. Configuration-Driven Relationships

Identify relationships created by configuration rather than direct source references.

Examples:

- service discovery names;
- URLs;
- config-server relationships;
- environment variables;
- profiles;
- feature flags;
- external config repositories;
- datasource URLs;
- message broker configuration;
- deployment variables.

Never expose secret values.

Describe the relationship without reproducing credentials, tokens, private keys, or sensitive values.

---

# 14. API and Contract Discovery

Identify important contracts:

- REST endpoints;
- OpenAPI;
- AsyncAPI;
- generated interfaces;
- DTOs;
- schemas;
- event schemas;
- external API definitions.

For each important API identify:

- provider;
- consumer;
- endpoint/operation;
- request/response contract;
- versioning evidence;
- contract-test evidence.

Do not call an undocumented interface "internal" merely because its URL looks internal.

---

# 15. Database Discovery

Identify:

- databases;
- schemas;
- tables;
- ownership;
- repositories;
- migrations;
- initialization scripts;
- foreign keys;
- cross-service references;
- shared schemas.

Distinguish:

- logical ownership;
- physical database location;
- runtime connection;
- compile-time dependency.

Pay particular attention to cross-service database relationships.

Do not assume database-per-service architecture.

---

# 16. Data Relationships

Identify relationships such as:

- shared IDs;
- foreign keys;
- copied data;
- replicated data;
- snapshots;
- caches;
- materialized views;
- external master data.

Classify whether each relationship is:

- confirmed;
- inferred;
- unknown.

Do not infer synchronization behavior without evidence.

---

# 17. Runtime Relationships

Identify runtime relationships between:

- services;
- databases;
- config servers;
- discovery systems;
- message brokers;
- caches;
- observability systems;
- external APIs.

Distinguish runtime relationships from compile-time relationships.

A dependency in a build file does not automatically mean a runtime communication path.

---

# 18. Deployment and Infrastructure Discovery

Inspect:

- Dockerfiles;
- docker-compose;
- Kubernetes manifests;
- Helm charts;
- Terraform;
- cloud deployment files;
- scripts;
- CI/CD definitions.

Identify:

- deployable units;
- container relationships;
- ports;
- networks;
- startup dependencies;
- infrastructure dependencies;
- environment-specific configuration.

Do not assume local deployment equals production deployment.

---

# 19. External Integration Discovery

Identify external systems such as:

- payment systems;
- identity providers;
- notification services;
- cloud APIs;
- AI/LLM APIs;
- CRM/LOS systems;
- SFTP;
- databases;
- observability platforms.

For each integration identify:

- consumer;
- target;
- mechanism;
- configuration;
- contract evidence;
- authentication evidence without exposing secrets.

---

# 20. System Relationship Map

Build a system-level map.

Use a concise representation such as:

```text
Browser
  |
  v
API Gateway
  |
  +--> Customer Service
  |
  +--> Visit Service
  |
  +--> External API

Customer Service
  |
  +--> Customer DB
```

For each relationship indicate confidence when useful.

Do not introduce relationships merely to make the diagram complete.

---

# 21. Confirmed Relationships

List important relationships directly supported by evidence.

For each:

```text
Relationship
Evidence
Confidence: CONFIRMED
```

Use source paths, configuration files, class/method names, or other useful references.

---

# 22. Inferred Relationships

List relationships that are strongly suggested but not directly proven.

For each:

```text
Relationship
Evidence
Inference
Confidence
```

Never present an inferred relationship as confirmed.

---

# 23. Unknowns

Record important unknowns explicitly.

Examples:

- external configuration not available;
- production topology unknown;
- runtime behavior not executed;
- external consumer unknown;
- authentication mechanism outside repository scope;
- database runtime not verified.

Do not fill unknowns with conventional assumptions.

---

# 24. Architecture Observations

System Discovery may record neutral observations about the discovered structure.

Examples:

- one repository contains multiple deployable services;
- several services share a database;
- configuration is externalized;
- a gateway composes responses.

Do not turn observations into recommendations.

Architecture recommendations belong to Architecture Analysis or an explicitly requested design workflow.

---

# 25. Risks and Follow-up Questions

Record evidence-backed discovery risks or questions when they affect understanding.

Examples:

- external repository required to confirm runtime configuration;
- production deployment definition unavailable;
- service-to-service authentication cannot be confirmed;
- runtime behavior not executed.

Do not rank risks or recommend fixes during pure discovery.

---

# 26. Knowledge Persistence

System Discovery is read-only by default.

Do not automatically:

- create `.ai/` files;
- update `.ai/`;
- create architecture documents;
- create maps;
- update CLAUDE.md;
- modify source;
- modify configuration;
- modify build files;
- commit changes.

If persistence is explicitly requested or approved as part of another workflow, create only the requested knowledge and preserve evidence/confidence labels.

---

# 27. File Modification Boundary

During pure System Discovery:

DO NOT:

- modify source code;
- modify configuration;
- modify build files;
- modify database schemas;
- create migrations;
- create documentation;
- create `.ai/` files;
- create architecture files;
- commit changes;
- delete files;
- install dependencies;
- change IDE settings.

Read-only inspection is permitted.

---

# 28. Efficiency

Use high-value evidence first.

Prefer:

1. workspace/repository inventory;
2. build files;
3. application entry points;
4. configuration;
5. API contracts;
6. communication clients;
7. database schemas;
8. deployment definitions;
9. targeted source inspection.

Do not blindly read every file.

Do not truncate evidence when correctness requires more context.

Use targeted searches and progressively expand investigation.

---

# 29. Discovery Report

Use this structure:

## 1. Workspace

## 2. Repository Inventory

## 3. Repository Relationships

## 4. Module / Application Inventory

## 5. Dependency Map

## 6. Communication Map

## 7. External Integrations

## 8. Data Relationships

## 9. Configuration Relationships

## 10. Deployment / Runtime Relationships

## 11. System Architecture Map

## 12. Confirmed Relationships

## 13. Inferred Relationships

## 14. Unknowns

## 15. Observations

## 16. Risks / Follow-up Questions

## 17. Files Modified

For pure discovery:

```text
Files Modified: None
```

Do not add a recommendation section unless the user explicitly asks for recommendations.

---

# 30. Completion Criteria

System Discovery is complete when:

- workspace boundaries are identified;
- repositories are identified;
- repository roles are identified;
- modules/applications are identified;
- important dependencies are mapped;
- service relationships are mapped;
- REST/HTTP relationships are investigated;
- messaging relationships are investigated;
- configuration-driven relationships are investigated;
- external integrations are identified;
- database relationships are investigated;
- important API contracts are identified;
- deployment/runtime relationships are investigated where relevant;
- important relationships have confidence classifications;
- evidence supports important findings;
- unknowns are explicitly recorded;
- no source/configuration/application files were modified;
- no architectural recommendation was silently introduced.

End with exactly:

```text
DISCOVERY COMPLETE
```

Do not ask the user to approve the discovery report.

If a separate human decision is required, identify the specific decision only when it is actually part of a requested downstream workflow.

---

# 31. Final Principle

System Discovery answers:

> What exists, and how is it connected?

It does not answer:

> What should we change?

Use evidence.

Preserve uncertainty.

Do not guess.

Keep discovery read-only.

Keep architectural decisions separate from discovery.
