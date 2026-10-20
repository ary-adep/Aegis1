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

A recorded read event establishes that a read occurred, not the truth of a claim about unseen contents. Confirmation requires the relevant contents or result to be available in the current evidence. A claim copied from an earlier report without that support must be attributed as `REPORTED — not independently verified in this revision`; its underlying truth remains `UNKNOWN`. This provenance label does not replace the evidence classifications.

Keep claims at the evidence's level: source declares behavior; a runtime observation demonstrates behavior only for the observed environment and conditions. A local config import does not establish remote values, successful retrieval, or effective settings after profile/environment overrides. Quantifiers such as "all applications" require evidence for every member, including provider or infrastructure modules.

For a supplied-evidence-only task, distinguish literal observations from technical interpretation. Confirm that an excerpt contains a key/value or omits a key within the stated complete scope; this does not by itself confirm successful parsing, binding, framework defaults, network reachability, startup behavior, or effective runtime settings. Background framework or standards knowledge is not evidence supplied by the user. If useful and within scope, label it as a conditional interpretation with its assumptions, rather than as a confirmed excerpt finding; otherwise omit it.

If the named file format and supplied syntax appear inconsistent, report the literal text and the interpretation uncertainty together. Do not first present it as an effective setting and later retract that certainty. Missing settings in a complete file establish absence there, not absence from other configuration sources or a runtime default.

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

## Coverage and negative findings

Record which files, sections, search outputs, and repository boundaries were actually inspected. A file inventory is not a content read; search hits are not full-file inspection. A count-only glob cannot establish which names matched or that a deployment technology is absent. Negative findings require a successful appropriately scoped search with visible results and known exclusions; otherwise say "not established in the inspected evidence."

Report denied or approval-pending checks as not executed, with their exact available error and effect on completeness. Do not invent an error when only a summary is supplied. A later partial substitute does not prove the original check succeeded.

Distinguish "no write action appears in the supplied trace" from "files were preserved." Independent preservation evidence requires a comparable baseline and final snapshot/diff, with coverage stated. A tracked-file diff alone does not establish preservation of untracked or ignored files.

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
