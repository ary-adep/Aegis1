import json


def handle_queued(raw):
    event = json.loads(raw)
    return event["ticketRef"]
