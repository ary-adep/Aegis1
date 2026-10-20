# Supplied architecture evidence

The checkout service writes orders to a primary SQL database. An outbox relay publishes events to a broker with at-least-once delivery. Reporting consumes those events into a separate read model. This is a document fixture, not deployed infrastructure.

Order acceptance is confirmed only after the primary transaction commits. Reporting may lag by up to 60 seconds under normal operation; no freshness promise is supplied for a broker outage. The relay retries unacknowledged messages. Consumer deduplication and reconciliation implementation are unavailable.

The architecture decision owner has not decided whether checkout may accept orders when the primary database is unreachable. No evidence supports exactly-once processing, partition-time availability, or any specific replication configuration.
