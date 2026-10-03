---
name: architecture-analysis
description: Analyze an existing or proposed software architecture using evidence, identify architectural boundaries, dependencies, trade-offs, risks, constraints, and options. Use after system understanding is sufficient and before consequential architectural decisions.
---

# Architecture Analysis

## Purpose

Architecture Analysis evaluates how a software system is structured and how its important architectural decisions affect behavior, maintainability, reliability, security, performance, scalability, operability, and changeability.

It answers:

> How is the system architected, what are the important trade-offs and risks, and what options exist?

It does not automatically decide or implement architectural changes.

Architecture Analysis should normally follow sufficient System Discovery.

---

# 1. Core Principles

## Evidence before judgment

Base architectural observations on:

- source code;
- configuration;
- build files;
- API contracts;
- database schemas;
- deployment configuration;
- infrastructure;
- tests;
- runtime topology;
- documented requirements;
- System Discovery findings.

Do not infer architecture solely from:

- repository names;
- package names;
- framework conventions;
- README claims;
- common industry patterns.

Clearly distinguish:

- FACT;
- REQUIREMENT;
- OBSERVATION;
- INFERENCE;
- RISK;
- OPTION;
- DECISION;
- UNKNOWN.

---

# 2. Use System Discovery First

When architecture depends on multiple repositories, services, libraries, adapters, databases, or external integrations, perform System Discovery first.

Do not duplicate discovery unnecessarily.

Use existing System Discovery findings when they are current and sufficient.

If important architectural evidence is missing:

1. identify the missing evidence;
2. perform targeted read-only discovery;
3. update the architectural understanding;
4. do not invent the missing information.

For a multi-repository system, preserve repository boundaries during analysis.

---

# 3. Architecture Scope

Determine the scope from the task.

Possible scopes include:

- application;
- service;
- repository;
- multi-repository system;
- API platform;
- data architecture;
- integration architecture;
- deployment architecture;
- security architecture;
- observability architecture;
- complete system architecture.

Do not analyze unrelated parts of the system unless they materially affect the requested architecture.

---

# 4. Architectural Boundaries

Identify important boundaries.

Examples:

- repository boundaries;
- service boundaries;
- module boundaries;
- API boundaries;
- database ownership boundaries;
- transaction boundaries;
- deployment boundaries;
- trust boundaries;
- configuration boundaries;
- external system boundaries.

For each important boundary determine:

- what is inside;
- what is outside;
- how communication crosses the boundary;
- what dependency exists;
- whether the boundary is enforced technically.

Distinguish logical boundaries from physically enforced boundaries.

---

# 5. Architecture Style

Identify the architecture style actually present.

Possible styles include:

- monolith;
- modular monolith;
- layered architecture;
- hexagonal architecture;
- clean architecture;
- microservices;
- service-oriented architecture;
- event-driven architecture;
- serverless;
- batch;
- hybrid.

Do not label an architecture based only on repository/module naming.

Explain the evidence supporting the classification.

A system may contain multiple architectural styles.

---

# 6. Dependency Analysis

Map important dependencies.

Analyze:

- service-to-service dependencies;
- library dependencies;
- database dependencies;
- configuration dependencies;
- infrastructure dependencies;
- external API dependencies;
- runtime dependencies;
- compile-time dependencies.

Identify:

- direct dependencies;
- indirect dependencies;
- dependency concentration;
- circular dependencies;
- shared infrastructure;
- tightly coupled components.

Do not call a dependency problematic merely because it exists.

Explain the architectural consequence.

---

# 7. Communication Architecture

Analyze how components communicate.

Consider:

- synchronous HTTP;
- REST;
- WebClient;
- RestClient;
- Feign;
- messaging;
- Kafka;
- RabbitMQ;
- JMS;
- gRPC;
- database integration;
- file integration;
- external APIs.

Evaluate relevant characteristics:

- coupling;
- latency;
- failure propagation;
- retry behavior;
- timeout behavior;
- circuit breaking;
- idempotency;
- ordering;
- consistency;
- observability.

Do not recommend asynchronous messaging simply because a system uses microservices.

---

# 8. API Architecture

Analyze important API boundaries.

Consider:

- API ownership;
- gateway behavior;
- endpoint design;
- versioning;
- request/response models;
- DTO ownership;
- backward compatibility;
- error handling;
- authentication;
- authorization;
- rate limiting;
- contract management.

Identify whether APIs have:

- formal contracts;
- generated clients;
- contract tests;
- duplicated DTOs;
- implicit contracts.

Separate factual observations from recommendations.

---

# 9. Data Architecture

Analyze:

- database ownership;
- schemas;
- shared databases;
- database-per-service boundaries;
- foreign keys;
- transactions;
- consistency;
- ID-based relationships;
- caching;
- data duplication;
- migrations;
- initialization scripts.

Pay particular attention to:

- cross-service database relationships;
- shared schemas;
- cross-boundary foreign keys;
- distributed transactions;
- stale data risks.

Do not assume database-per-service merely because services have separate codebases.

---

# 10. Transaction and Consistency Analysis

Determine where transactions exist.

Analyze:

- transaction boundaries;
- local transactions;
- cross-service operations;
- distributed transactions;
- eventual consistency;
- retries;
- duplicate requests;
- idempotency;
- failure recovery.

Identify where a business operation crosses multiple architectural boundaries.

Describe the consistency model supported by the evidence.

---

# 11. Configuration Architecture

Analyze configuration ownership and flow.

Consider:

- local configuration;
- external configuration;
- config servers;
- environment variables;
- profiles;
- secrets;
- runtime overrides;
- configuration repositories.

Identify:

- configuration dependencies;
- startup dependencies;
- configuration failure modes;
- environment-specific behavior.

Never expose secret values.

---

# 12. Security Architecture

Analyze visible architectural security controls.

Consider:

- authentication;
- authorization;
- identity propagation;
- service-to-service authentication;
- TLS;
- secrets management;
- credential storage;
- API exposure;
- trust boundaries;
- sensitive data flows;
- auditability.

Report missing evidence as UNKNOWN.

Do not claim a system is secure or insecure solely from absence of a visible mechanism.

---

# 13. Reliability Architecture

Analyze:

- timeouts;
- retries;
- circuit breakers;
- bulkheads;
- fallback behavior;
- health checks;
- service discovery;
- graceful shutdown;
- failure isolation;
- dependency failures.

Identify possible failure propagation paths.

Describe evidence-backed failure modes.

Do not exaggerate hypothetical failures.

---

# 14. Scalability and Performance Architecture

Analyze only where relevant to the task.

Consider:

- statelessness;
- horizontal scaling;
- connection pools;
- caching;
- synchronous call chains;
- database bottlenecks;
- shared resources;
- fan-out;
- payload size;
- expensive external calls;
- concurrency.

Do not make performance claims without evidence.

If performance data is unavailable, identify it as UNKNOWN.

---

# 15. Observability Architecture

Analyze:

- logging;
- metrics;
- tracing;
- health endpoints;
- correlation IDs;
- dashboards;
- alerting;
- monitoring coverage.

Determine whether observability crosses service boundaries.

Identify important blind spots as observations, not automatic recommendations.

---

# 16. Deployment Architecture

Analyze:

- Docker;
- Kubernetes;
- VM deployment;
- cloud deployment;
- service discovery;
- networking;
- configuration injection;
- startup dependencies;
- scaling boundaries;
- infrastructure dependencies.

Distinguish:

- local development;
- test;
- staging;
- production.

Do not assume local configuration represents production.

---

# 17. Architectural Risks

Identify evidence-backed architectural risks.

For each risk provide:

```text
Risk
Evidence
Impact
Likelihood if evidence permits
Affected boundary
Confidence
```

Examples:

- shared database creates coupling between services;
- synchronous dependency chain increases failure propagation;
- duplicated DTOs create contract drift risk;
- external configuration creates startup dependency;
- missing formal API contracts increase integration ambiguity.

Do not assign numerical risk scores unless explicitly requested.

Do not rank architectural risks into best/worst categories.

---

# 18. Architectural Trade-offs

For important architectural characteristics, explain trade-offs.

Example:

```text
Decision/Pattern:
Synchronous HTTP communication

Benefits:
- simple request/response model
- immediate response
- straightforward debugging

Costs:
- runtime coupling
- failure propagation
- latency across dependencies

Evidence:
...
```

Do not turn trade-off analysis into a recommendation automatically.

---

# 19. Architectural Options

When the user asks what should change, identify viable options.

For each option describe:

- approach;
- affected components;
- benefits;
- costs;
- risks;
- migration complexity;
- operational implications;
- compatibility implications;
- prerequisites.

Example:

```text
Option A
Keep current synchronous integration.

Option B
Introduce asynchronous messaging for selected workflows.

Option C
Introduce an integration/outbox boundary.
```

Do not declare an option the winner.

Do not provide overall rankings or scores.

The purpose is to support the human architectural decision.

---

# 20. Simplicity and YAGNI

Prefer the simplest architecture that satisfies the documented requirements.

Do not introduce:

- microservices;
- Kafka;
- Redis;
- event buses;
- API gateways;
- service meshes;
- distributed transactions;
- additional databases;
- complex patterns

merely because they are common architectural technologies.

Every proposed architectural component must have a demonstrated requirement or problem it addresses.

---

# 21. Brownfield Architecture

For an existing system:

- preserve working behavior unless change is required;
- understand existing conventions;
- identify why current boundaries exist where evidence is available;
- avoid unnecessary rewrites;
- prefer incremental migration where appropriate;
- identify compatibility constraints.

Do not redesign the system merely because a different architecture is theoretically cleaner.

---

# 22. Greenfield Architecture

For a new system:

Start with:

1. requirements;
2. quality attributes;
3. business capabilities;
4. domain boundaries;
5. data ownership;
6. API boundaries;
7. integration needs;
8. security requirements;
9. operational requirements;
10. deployment constraints.

Then evaluate architectural options.

Do not start with a technology stack and force the requirements around it.

---

# 23. Architecture Decision Boundary

Architecture Analysis may identify options.

It must not silently make consequential architectural decisions.

For consequential decisions use:

```text
Evidence
   ↓
Analysis
   ↓
Options
   ↓
Trade-offs
   ↓
Human Decision
   ↓
Approved Architecture
```

Human approval is required before implementing consequential changes involving, for example:

- service boundary changes;
- database boundary changes;
- breaking API changes;
- major technology changes;
- security exceptions;
- distributed transaction design;
- production infrastructure changes;
- irreversible migrations.

---

# 24. Implementation Boundary

Architecture Analysis does not automatically implement its recommendations.

If implementation is requested:

1. identify the approved architectural decision;
2. verify required human approval;
3. determine affected components;
4. create implementation design;
5. implement through the appropriate workflow;
6. verify against requirements and architecture.

Do not modify source code during pure Architecture Analysis.

---

# 25. Architecture Analysis Report

Use this structure:

## 1. Scope

State what system/components were analyzed.

## 2. Architecture Summary

Describe the architecture actually present.

## 3. Architectural Boundaries

Describe important boundaries.

## 4. Component / Service Map

Describe important components and responsibilities.

## 5. Dependency Architecture

Describe important dependencies.

## 6. Communication Architecture

Describe synchronous, asynchronous, and external communication.

## 7. API Architecture

Describe important API boundaries and contracts.

## 8. Data Architecture

Describe ownership, schemas, relationships, and consistency.

## 9. Security Architecture

Describe visible security boundaries and controls.

## 10. Reliability Architecture

Describe failure handling and dependency behavior.

## 11. Observability Architecture

Describe logs, metrics, tracing, health, and monitoring.

## 12. Deployment Architecture

Describe deployment/runtime relationships.

## 13. Architectural Observations

Facts and evidence-backed observations.

## 14. Architectural Risks

Evidence-backed risks and affected boundaries.

## 15. Trade-offs

Important architectural trade-offs.

## 16. Architectural Options

Options only when a change or decision is requested.

## 17. Unknowns / Missing Evidence

Identify important missing information.

## 18. Decisions Requiring Human Approval

List consequential decisions that require a human decision.

## 19. Analysis Status

Architecture Analysis should conclude with:

```text
ARCHITECTURE ANALYSIS COMPLETE
```

Do not ask the user to approve the analysis itself.

Do not use:

```text
READY FOR APPROVAL
```

The report should state:

```text
Scope:
Evidence:
Files Modified: None
Tests Run: None, unless explicitly required
Human Decisions Required:
Known Limitations:
```

If consequential architectural decisions are identified, list them under:

```text
Human Decisions Required:
```

A decision requiring human approval must identify the specific decision, affected boundaries, available options, and relevant trade-offs.

Do not imply that the human has approved a decision unless the user explicitly approves that decision.

Architecture Analysis is complete when the analysis is complete; approval applies only to consequential architectural decisions that may follow from the analysis.

---

# 26. Completion Criteria

Architecture Analysis is complete when:

- the architecture scope is clear;
- relevant System Discovery evidence has been considered;
- important boundaries are identified;
- component responsibilities are understood;
- important dependencies are mapped;
- communication architecture is understood;
- API architecture is understood;
- data architecture is understood;
- relevant security architecture is considered;
- reliability characteristics are considered;
- deployment/operational architecture is considered where relevant;
- architectural risks are evidence-backed;
- trade-offs are documented;
- unknowns are identified;
- options are documented when requested;
- consequential decisions are clearly separated from analysis;
- no unapproved architectural decision is presented as fact;
- no source/configuration changes are made during pure analysis.

---

# 27. Boundary With Other Aegis1 Capabilities

System Discovery answers:

> What exists, and how is it connected?

Architecture Analysis answers:

> How is it architected, what are the trade-offs and risks, and what options exist?

Requirements Analysis answers:

> What does the system need to do?

API Design answers:

> What should the API contract be?

Database Design answers:

> What should the data model and persistence design be?

Implementation answers:

> How should an approved change be built?

Verification answers:

> Does the implementation satisfy the requirements and approved design?

Keep these responsibilities separate.

---

# 28. Final Principle

Architecture Analysis should improve human architectural decisions, not replace them.

Use evidence.

Expose uncertainty.

Explain trade-offs.

Prefer simplicity.

Make consequential decisions explicit.

Require human authority for consequential architectural choices.

Do not require approval merely to acknowledge or accept an analysis report.
