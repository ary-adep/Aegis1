ALTER TABLE dispatch_queue
    ADD COLUMN route_group text NOT NULL DEFAULT 'standard';

DROP INDEX dispatch_queue_pending_ticket;
CREATE UNIQUE INDEX dispatch_queue_pending_route
    ON dispatch_queue (ticket_ref, route_group) WHERE sent_at IS NULL;
