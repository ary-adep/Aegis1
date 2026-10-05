# Discovery Evidence Model

## Contents

- Evidence classifications
- Confidence rules
- Source precedence
- Handling uncertainty
- Reporting examples

## Evidence classifications

### CONFIRMED

Use when the claim is directly supported by authoritative evidence such as source code, build configuration, tests, schema, migration, API contract, deployment configuration, or an observed runtime result.

### INFERRED

Use when multiple pieces of evidence support a conclusion that is not directly declared.

State the evidence that produced the inference.

### UNKNOWN

Use when available evidence is insufficient.

Do not convert an unknown into an assumption merely to make the report complete.

## Source precedence

Prefer evidence in roughly this order:

1. Executable source and tests.
2. Database schema and migrations.
3. API contracts and generated contracts.
4. Build/dependency configuration.
5. Runtime/deployment configuration.
6. Operational evidence and logs.
7. Project documentation.
8. Naming conventions or indirect clues.

The order is contextual. A runtime fact can supersede a stale source comment when the question is current runtime behavior.

## Confidence rules

A finding can be:

- directly observed
- directly declared
- strongly inferred
- weakly inferred
- unresolved

Avoid numerical confidence scores unless the task requires them.

## Handling uncertainty

When evidence conflicts:

1. Identify the conflicting sources.
2. State which source is more authoritative for the question.
3. Preserve the conflict if it cannot be resolved.
4. Do not silently choose a convenient interpretation.

## Reporting examples

Good:

`CONFIRMED: OrderService calls InventoryClient through the Feign interface in OrderServiceClient.java.`

Good:

`INFERRED: The inventory service appears to be the owner of stock quantity because its schema writes quantity and the order service only reads it.`

Good:

`UNKNOWN: The production retry policy could not be established from repository evidence.`

Avoid:

`The system probably retries three times.`

That is an unsupported assumption.
