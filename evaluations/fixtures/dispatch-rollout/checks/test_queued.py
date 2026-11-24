from unittest import TestCase

from consumer.queued import handle_queued
from worker.producer import enqueue_event


class QueuedTest(TestCase):
    def test_current_producer_and_consumer_agree(self):
        topic, raw = enqueue_event("ticket-1")
        self.assertEqual(topic, "dispatch.queued.v1")
        self.assertEqual(handle_queued(raw), "ticket-1")
