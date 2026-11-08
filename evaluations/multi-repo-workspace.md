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
