from consumer.queued import handle_queued


def replay_retained(records):
    return [handle_queued(raw) for raw in records]
