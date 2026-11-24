import json

TOPIC = "dispatch.queued.v1"


def enqueue_event(ticket_ref):
    return TOPIC, json.dumps({"ticketRef": ticket_ref})
