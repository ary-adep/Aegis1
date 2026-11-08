from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

MEMORY = Path(__file__).resolve().parents[1] / 'skills/aegis/memory.py'


class MemoryChecks(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name) / 'home'
        self.home.mkdir()
        self.project = Path(temp.name) / 'project'
        self.project.mkdir()
        for name in ('a.txt', 'b.txt'):
            (self.project / name).write_text(name, encoding='utf-8')
        self.store = self.home / '.aegis1' / 'memory.sqlite3'

    def run_memory(self, *args, ok=True):
        env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home))
        result = subprocess.run([sys.executable, '-B', str(MEMORY), '--project', str(self.project), *args],
                                capture_output=True, text=True, env=env, timeout=30)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return json.loads(result.stdout) if ok else result.stderr

    def save(self, *sources):
        args = [arg for source in sources for arg in ('--source', source)]
        return self.run_memory('save', *args, '--finding', 'finding')['saved']

    def recall(self):
        return {record['id']: record for record in self.run_memory('recall')}

    def test_single_source_record_is_current_then_stale(self):
        record_id = self.save('a.txt')
        record = self.recall()[record_id]
        self.assertEqual((record['source'], record['sources'], record['stale']), ('a.txt', ['a.txt'], False))
        (self.project / 'a.txt').write_text('changed', encoding='utf-8')
        self.assertTrue(self.recall()[record_id]['stale'])

    def test_multiple_sources_are_recalled_in_order(self):
        record_id = self.save('b.txt', 'a.txt', 'b.txt')
        record = self.recall()[record_id]
        self.assertEqual(record['sources'], ['b.txt', 'a.txt'])
        self.assertEqual(record['source'], 'b.txt')
        self.assertFalse(record['stale'])

    def test_any_changed_source_marks_record_stale(self):
        record_id = self.save('a.txt', 'b.txt')
        (self.project / 'b.txt').write_text('changed', encoding='utf-8')
        self.assertTrue(self.recall()[record_id]['stale'])

    def test_any_missing_source_marks_record_stale(self):
        record_id = self.save('a.txt', 'b.txt')
        (self.project / 'b.txt').unlink()
        self.assertTrue(self.recall()[record_id]['stale'])

    def test_invalid_source_saves_nothing(self):
        self.save('a.txt')
        self.assertIn('Local memory unavailable', self.run_memory('save', '--source', 'a.txt', '--source', 'missing.txt',
                                                                  '--finding', 'x', ok=False))
        self.assertEqual(len(self.recall()), 1)

    def test_delete_removes_record_and_cited_sources(self):
        record_id = self.save('a.txt', 'b.txt')
        self.assertEqual(self.run_memory('delete', record_id), {'deleted': True})
        self.assertEqual(self.recall(), {})
        with closing(sqlite3.connect(self.store)) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM finding_sources').fetchone(), (0,))

    def legacy_record(self, source='a.txt'):
        # Mirrors the single-source schema written before multi-source support.
        self.store.parent.mkdir()
        digest = hashlib.sha256((self.project / source).read_bytes()).hexdigest()
        with closing(sqlite3.connect(self.store)) as db, db:
            db.execute("""CREATE TABLE findings (id TEXT PRIMARY KEY, project TEXT NOT NULL, source TEXT NOT NULL,
                          fingerprint TEXT NOT NULL, finding TEXT NOT NULL)""")
            db.execute('INSERT INTO findings VALUES (?, ?, ?, ?, ?)',
                       ('legacy', str(self.project.resolve()), source, digest, 'old finding'))

    def test_legacy_record_recalls_and_tracks_staleness(self):
        self.legacy_record()
        record = self.recall()['legacy']
        self.assertEqual((record['source'], record['sources'], record['stale']), ('a.txt', ['a.txt'], False))
        (self.project / 'a.txt').unlink()
        self.assertTrue(self.recall()['legacy']['stale'])

    def test_legacy_store_accepts_new_records_and_deletes(self):
        self.legacy_record()
        record_id = self.save('a.txt', 'b.txt')
        records = self.recall()
        self.assertEqual(set(records), {'legacy', record_id})
        self.assertEqual(records['legacy']['sources'], ['a.txt'])
        self.assertEqual(self.run_memory('delete', 'legacy'), {'deleted': True})
        self.assertEqual(set(self.recall()), {record_id})

    def test_delete_on_legacy_store_without_sources_table(self):
        self.legacy_record()
        self.assertEqual(self.run_memory('delete', 'legacy'), {'deleted': True})
        self.assertEqual(self.recall(), {})


if __name__ == '__main__':
    unittest.main()
