# Aegis1 order reservation benchmark

Use the sibling order-reservation project in a fresh Claude Code session. Record
the host, selected model, starting code, actions, checks, and outcome. The
observations below describe the reported local pilot.

## Case 1: Result listener recovery

For a fresh implementation run, use a disposable copy with the pre-fix listener
and isolated test data. The current sample already contains the fix.

1. Discovery: trace POST through the order outbox, Kafka, Inventory, the Orders
   result listener, and GET. Identify the stock and replay safeguards and when
   Redis is used. Separate source evidence from runtime observations.
2. Implementation: keep transient database write failures retryable and reject
   malformed payloads. Bound lock waits, log useful Kafka position and cause
   information at a controlled rate, and preserve the PENDING guard.
3. Verification: hold a row lock on a test order until a timeout warning
   appears. Verify the consumer offset has not advanced. Release the lock and
   verify the terminal status and offset advance without manual replay. Send a
   valid duplicate and check that the row is untouched. Verify malformed
   messages are skipped and a later valid result still processes.

Observed locally: two concurrent orders for the last unit yielded one
confirmation and one rejection. Replay did not decrement stock again.
A stopped Kafka broker left an accepted order pending with an outbox row.
Restarting Kafka allowed the order to finish and the outbox to drain. A
pre-fix injected result write failure exhausted retries and left an order
pending. The first fix recovered after 50 attempts. The follow-up recovered
after a real row lock was released, logged attempts 1 and 10, skipped malformed
records, and left the row unchanged after a valid duplicate, including xmin.

The follow-up evidence comes from the supplied Claude Code run report. A full
PostgreSQL outage, a restart during retry, a confirmed result under the fault,
and cross-provider routing remain outside this evidence.

## Case 2: Routine documentation change

Prompt: Update only README.md to state that Orders caches terminal statuses in
Redis for 60 seconds and leaves PENDING uncached. If it already says both,
report that no change is needed.

Pass when the agent checks the relevant source and README, makes at most the
requested documentation edit, and verifies the final wording or diff. Record
whether it invokes specialists, builds services, or starts infrastructure.
The result should be supported by the focused source and documentation check.
This case is pending a fresh run.

## Case 3: Layered Spring Boot refactor

> /aegis Refactor Place Order → Reserve Stock → Apply Result into clear Spring
> Boot layers. Preserve the REST API and Kafka contracts. Add and run integration
> tests for last-unit concurrency, duplicate delivery, and Kafka outage recovery.

Use the Order and Inventory Reservation sample under Desktop/Aravind.
Capture the original checkout and run the acceptance checks before and
after the refactor. Preserve the existing REST and event payloads,
transaction behavior, and user edits. Record any independent verifier
invocation and which findings changed the implementation.

In the supplied Claude Code run, all seven integration tests passed
against both the original and refactored implementations. The independent
verifier identified a result validation path that could retry indefinitely.
The implementation session removed it and reran the tests. The supplied
report establishes verifier use. Scout use and model override are unknown.

## Case 4: End-to-end reservation

> /aegis Add and run an end-to-end integration test that starts Orders and
> Inventory together. Submit two orders for the last unit and verify that one
> becomes CONFIRMED, the other becomes REJECTED, and stock ends at zero. Use
> isolated test infrastructure.

Pass when both real Spring Boot processes use the test's PostgreSQL,
Kafka, and Redis containers. The test must submit orders over HTTP, observe
terminal states via GET, compare them with Inventory's recorded decisions,
and verify stock is zero. The test processes and containers should exit
after the run. Check the existing service-level suite as well.

The supplied macOS run used Maven Failsafe. The local XML reports corroborate
eight passing tests, with zero failures, errors, or skips. There were
three Orders tests, four Inventory tests, and one end-to-end test.
The agent reported inline verification for the test-only change.

From the sample project root, run `mvn -B verify`. For the targeted run
use `mvn -pl e2e -am verify -Dit.test=OrderReservationE2EIT`. On this Mac,
set DOCKER_HOST to the active Podman machine's macOS socket and
TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE to the socket path inside the VM.
The supplied run used the `aegis-smoke-vm` connection and the rootless VM
socket `/run/user/501/podman/podman.sock`. Resolve these for the current
machine before running. Coverage, Docker image rebuilds, and Kubernetes
deployment were outside these runs.
