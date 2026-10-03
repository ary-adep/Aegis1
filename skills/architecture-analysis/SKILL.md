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