ENQUEUE_SQL = """
INSERT INTO dispatch_queue(ticket_ref) VALUES (%s)
ON CONFLICT (ticket_ref) WHERE sent_at IS NULL DO NOTHING
"""


def enqueue(cursor, ticket_ref):
    cursor.execute(ENQUEUE_SQL, (ticket_ref,))
