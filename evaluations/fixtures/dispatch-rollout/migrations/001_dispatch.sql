CREATE TABLE dispatch_queue (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_ref text NOT NULL,
    sent_at timestamptz
);

CREATE UNIQUE INDEX dispatch_queue_pending_ticket
    ON dispatch_queue (ticket_ref) WHERE sent_at IS NULL;
