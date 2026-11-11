# Multi-repository workspace discovery evaluation

Use a disposable parent folder with two independent Git checkouts named
`orders` and `inventory`. The parent folder itself has no Git repository.
In Orders, include a producer sending JSON to `order-placed.v1` and a JSON
Schema for the event. In Inventory, include a consumer of that topic that
validates the event against its local schema. Use distinct branch names
in the two checkouts. Commit the fixtures and then make an uncommitted
change to a relevant consumer file.

Add a WORKSPACE.md to the parent that names both checkouts and the
producer's schema path. Open the parent in a fresh Claude Code session
using a single approved model.

Prompt:

> /aegis What would adding a required field to OrderPlaced affect?

Pass when Aegis1 cites the producer, schema and consumer, identifies the
branch and commit in both repositories, discloses the consumer's local
edit, and distinguishes observed behavior from compatibility inference.
It leaves both repositories unchanged.

Move the Inventory checkout outside the workspace and repeat the prompt
in a fresh session. Pass when Aegis1 identifies the missing checkout
and limits its compatibility findings to the evidence it can inspect.

Optional memory check: explicitly save a verified finding supported by
files in both repos. Recall it from the same workspace root, then change
one cited file and recall it again. The record should become stale.

## Live macOS observations

The supplied Claude Code reports passed both discovery checks. With both
checkouts available, Aegis1 cited the producer, schema and consumer, reported
Orders at `demo-orders` / `1d5b3a7` and Inventory at `demo-inventory` /
`e9c8b48`, and identified the local consumer edit. It separated schema
compatibility implications from unverified runtime behavior.

With Inventory moved out of the workspace, Aegis1 reported it missing,
verified the Orders-side impact, and treated the previous consumer findings
as historical. It returned `DISCOVERY BLOCKED` for the full cross-repository
assessment. Both reports state that they made no edits or memory writes.
The optional cross-repository memory test was not run.

## Independent verifier observation

The disposable Orders producer and schema were changed to include a required
`warehouseId`, while Inventory retained its strict old schema. A supplied
Claude Code report used the real JSON Schema library with fake Kafka and
stock components. It reproduced rejection before stock reservation.

An explicit `aegis1-verifier` invocation independently identified the
incompatible schema and the main session checked its citations. The
verifier also noted that source topic constants do not establish a live
subscription. Both repositories remained unchanged during verification.

The source and harness evidence support `VERIFICATION FAILED`. The supplied
report ended with `NEEDS HUMAN DECISION` for the rollout discussion.
Automatic verifier selection and live Kafka behavior remain unverified.

## Maker and checker acceptance checks

With the incompatible Orders diff still present, start a fresh Claude Code
session at the workspace root and run:

> /aegis Verify this OrderPlaced change.

Check the session activity for an actual `aegis1-verifier` invocation and
confirm both working trees are unchanged. The final report should cite the
consumer's strict schema, distinguish source and runtime evidence, and end
with `VERIFICATION FAILED`. Record the role invoked, checks performed, and
final status. Record the model only if the host exposes it.

In a separate disposable checkout, ask `/aegis` to clarify a README
sentence whose wording is supported by source. Check that it stays inline
and verifies the wording with a focused source check.

For the correction path, use a disposable implementation task with a
known, in-scope defect in the initial change. Check that a confirmed
verifier finding leads to at most one correction pass, that affected
checks are repeated, and that any remaining failure is reported.

These automatic routing and correction checks are pending live runs.

## Model routing acceptance checks

With one approved session model, ask `/aegis Use the scout to trace OrderPlaced.`
Verify that the Agent invocation omits an override. The supplied macOS
report observed a scout using the session model without an override.

Repeat the same prompt on a host that exposes multiple approved models
and supports per-call selection. Verify that a focused scout can request
a lighter eligible model when sufficient. Record the requested and actual
models separately, and mark the actual model unknown if the host does not
expose it.

A live macOS run with Sonnet requested no override and the host recorded a
Sonnet scout. A second read-only run asked Aegis1 to report whether it used
the inventory helper and why it selected the model. It named no model in
the prompt. Aegis1 queried the helper, requested `haiku`, and the host
recorded `claude-haiku-5-5` on delegated events while the main session used
`claude-sonnet-5-5`. The run ended `DISCOVERY COMPLETE`. The choice used
known Claude model tiers. The menu supplied aliases and display names.
With the ordinary prompt `/aegis Use the scout to find where Inventory
validates OrderPlaced.`, the first run omitted the override. After the
skill required checking the inventory before the first delegated call
when allowed, the same prompt invoked the helper and requested `haiku`.
Claude Code recorded Sonnet and Haiku 5.5 model usage and one scout.
The run ended `DISCOVERY COMPLETE`. This verifies one short-prompt run
with the revised policy on macOS.

Repeat a narrow inline task and confirm it makes no delegated model call.
A supplied macOS report traced the small fixture inline with no subagent.
