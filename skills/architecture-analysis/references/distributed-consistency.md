# Distributed Consistency Analysis

## Contents

- Applicability
- CAP
- Consistency models
- Availability
- Partition scenarios
- Replication
- Messaging
- Idempotency
- Reconciliation
- Analysis checklist

## Applicability

Use this reference only when distributed state or communication failure can affect correctness or availability.

## CAP

CAP concerns distributed systems during network partition.

Analyze:

- C: what consistency guarantee is required?
- A: what availability must remain during partition?
- P: what partition scenario must be tolerated?

In a partition, a distributed system cannot simultaneously provide arbitrary strong consistency and uninterrupted availability. The architectural question is which guarantee is required for the affected operation and what behavior is acceptable.

Do not treat CAP as a universal two-checkbox selection.

## Consistency models

Distinguish the actual guarantee, such as:

- strong/linearizable
- serializable transaction behavior
- read-your-writes
- monotonic reads
- causal
- eventual

Use only a model supported by evidence or an explicit decision.

## Availability

Define availability in terms of the operation:

- must accept writes?
- may serve stale reads?
- may return an explicit unavailable outcome?
- may queue work?
- may degrade functionality?

## Partition scenarios

For each important path ask:

1. Which communication link can fail?
2. Which state becomes unreachable?
3. Which component remains available?
4. What can safely continue?
5. What must stop?
6. What can become stale?
7. How is state reconciled?

## Replication

Identify:

- source of truth
- replica
- replication direction
- lag
- conflict handling
- failover
- recovery

## Messaging

Consider:

- at-least-once delivery
- duplicates
- ordering
- delayed delivery
- poison messages
- consumer outage
- replay

Do not assume exactly-once semantics without evidence.

## Idempotency

Where retries or duplicate delivery are possible, identify whether the operation is idempotent and how duplicate effects are prevented.

## Reconciliation

If temporary divergence is accepted, identify:

- reconciliation trigger
- authoritative state
- conflict rule
- detection
- repair
- auditability

## Analysis checklist

- [ ] Is distributed consistency actually relevant?
- [ ] What is authoritative state?
- [ ] What can be stale?
- [ ] What happens during partition?
- [ ] What happens during dependency outage?
- [ ] Can requests/messages duplicate?
- [ ] What ordering is required?
- [ ] How does recovery work?
- [ ] Which choices are explicit human decisions?
