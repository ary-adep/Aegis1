-- Run after applying migrations in an empty disposable PostgreSQL database.
INSERT INTO dispatch_queue(ticket_ref) VALUES ('compat-case')
ON CONFLICT (ticket_ref) WHERE sent_at IS NULL DO NOTHING;
INSERT INTO dispatch_queue(ticket_ref) VALUES ('compat-case')
ON CONFLICT (ticket_ref) WHERE sent_at IS NULL DO NOTHING;

DO $$
BEGIN
    IF (SELECT count(*) FROM dispatch_queue WHERE ticket_ref = 'compat-case') <> 1 THEN
        RAISE EXCEPTION 'legacy replay did not leave one pending dispatch';
    END IF;
END $$;
