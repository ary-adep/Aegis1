import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TokenUsageTests(unittest.TestCase):
    def summarize(self, host, *events):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / 'run.jsonl'
            log.write_text(''.join(
                (event if isinstance(event, str) else json.dumps(event)) + '\n'
                for event in events
            ), encoding='utf-8')
            completed = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'scripts/evaluate.py'),
                 'usage', '--host', host, str(log)],
                capture_output=True, text=True, timeout=10, check=True,
            )
            self.assertNotIn('private fixture text', completed.stdout)
            return json.loads(completed.stdout)

    def test_claude_deduplicates_message_ids_and_includes_both_cache_counters(self):
        def message(key, input_count, output_count, read, written):
            return {'type': 'assistant', 'message': {
                'id': key, 'content': 'private fixture text', 'usage': {
                    'input_tokens': input_count, 'output_tokens': output_count,
                    'cache_read_input_tokens': read, 'cache_creation_input_tokens': written,
                },
            }}
        result = self.summarize('claude',
                                message('first', 4, 3, 10, 6),
                                message('first', 4, 7, 10, 6),
                                message('second', 3, 2, 0, 2))
        self.assertEqual(result['usage'], {'input_tokens': 25, 'cached_input_tokens': 10, 'output_tokens': 9})
        self.assertEqual(result['cache_write_input_tokens'], 8)
        self.assertEqual(result['usage_records'], 2)

    def test_codex_counts_completed_turns_without_adding_cached_tokens_twice(self):
        result = self.summarize('codex',
                                {'type': 'thread.started', 'thread_id': 'one'},
                                {'type': 'turn.started'},
                                {'type': 'turn.completed', 'usage': {
                                    'input_tokens': 22, 'cached_input_tokens': 10, 'output_tokens': 3}},
                                {'type': 'turn.started'},
                                {'type': 'turn.completed', 'usage': {
                                    'input_tokens': 20, 'cached_input_tokens': 0, 'output_tokens': 5}})
        self.assertEqual(result['usage'], {'input_tokens': 42, 'cached_input_tokens': 10, 'output_tokens': 8})
        self.assertIsNone(result['cache_write_input_tokens'])

    def test_missing_and_invalid_counters_stay_unknown(self):
        result = self.summarize('codex', {'type': 'turn.completed', 'usage': {
            'input_tokens': 10, 'cached_input_tokens': 11, 'output_tokens': True}})
        self.assertEqual(result['usage'], {'input_tokens': 10, 'cached_input_tokens': None, 'output_tokens': None})
        result = self.summarize('claude', {'type': 'assistant', 'message': {
            'id': 'one', 'usage': {'input_tokens': 3, 'output_tokens': 0}}})
        self.assertEqual(result['usage'], {'input_tokens': None, 'cached_input_tokens': None, 'output_tokens': 0})

    def test_codex_reports_cache_writes_when_present(self):
        result = self.summarize('codex', {'type': 'turn.completed', 'usage': {
            'input_tokens': 10, 'cached_input_tokens': 2, 'output_tokens': 4,
            'cache_write_input_tokens': 3}})
        self.assertEqual(result['usage']['input_tokens'], 10)
        self.assertEqual(result['cache_write_input_tokens'], 3)

    def test_incomplete_logs_do_not_report_undercounts_as_totals(self):
        completed = {'type': 'turn.completed', 'usage': {
            'input_tokens': 10, 'cached_input_tokens': 2, 'output_tokens': 4}}
        for tail in ('{broken input', {'type': 'turn.started'}, {'type': 'turn.failed'}):
            with self.subTest(tail=tail):
                result = self.summarize('codex', completed, tail)
                self.assertTrue(all(counter is None for counter in result['usage'].values()))
                self.assertEqual(result['usage_records'], 1)
        result = self.summarize('claude', {'type': 'assistant', 'message': {
            'usage': {'input_tokens': 3, 'output_tokens': 1}}})
        self.assertIn('cannot be deduplicated', result['usage_notes'])
