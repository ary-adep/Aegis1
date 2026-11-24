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

    def run_memory(self, *args, ok=True, project=None):
        result = self.memory_process(*args, project=project)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return json.loads(result.stdout) if ok else result.stderr.decode()

    def memory_process(self, *args, project=None):
        env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home))
        return subprocess.run([sys.executable, '-B', str(MEMORY), '--project', str(project or self.project), *args],
                              capture_output=True, env=env, timeout=30)

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

    def test_legacy_delete_also_removes_cited_sources(self):
        record_id = self.save('a.txt', 'b.txt')
        with closing(sqlite3.connect(self.store)) as db, db:
            db.execute('DELETE FROM findings WHERE project = ? AND id = ?',
                       (str(self.project.resolve()), record_id))
            self.assertEqual(db.execute('SELECT COUNT(*) FROM finding_sources').fetchone(), (0,))
        self.assertEqual(self.recall(), {})

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

    def test_explicit_transfer_preserves_fingerprints_and_destination_scope(self):
        selected = self.save('b.txt', 'a.txt')
        self.save('a.txt')
        bundle = self.project.parent / 'transfer.json'
        target = self.project.parent / 'other-checkout'
        target.mkdir()
        for name in ('a.txt', 'b.txt'):
            (target / name).write_text(name, encoding='utf-8')
        self.assertEqual(self.run_memory('recall', project=target), [])
        self.assertEqual(self.run_memory('export', '--id', selected, '--output', str(bundle)), {'exported': 1})
        self.assertNotIn(str(self.project), bundle.read_text(encoding='utf-8'))
        self.assertIn('unavailable in this project', self.run_memory(
            'export', '--id', selected, '--output', str(bundle), project=target, ok=False))
        initial = self.run_memory('import', str(bundle), project=target)
        imported = initial['findings'][0]['id']
        self.assertEqual(initial['imported'], 1)
        self.assertFalse(initial['findings'][0]['stale'])
        self.assertEqual(self.run_memory('recall', project=target)[0]['sources'], ['b.txt', 'a.txt'])
        self.assertNotIn(imported, self.recall())
        (target / 'a.txt').write_text('different', encoding='utf-8')
        duplicate = self.run_memory('import', str(bundle), project=target)
        self.assertEqual(duplicate['already_present'], 1)
        self.assertEqual(duplicate['findings'], [{'id': imported, 'stale': True}])
        self.assertTrue(self.run_memory('recall', project=target)[0]['stale'])

    def test_invalid_bundle_import_is_atomic(self):
        record_id = self.save('a.txt')
        bundle = self.project.parent / 'transfer.json'
        self.run_memory('export', '--id', record_id, '--output', str(bundle))
        original = bundle.read_bytes()
        self.run_memory('export', '--id', record_id, '--output', str(bundle), ok=False)
        self.assertEqual(bundle.read_bytes(), original)
        content = json.loads(original)
        content['findings'].append({'finding': 'invalid', 'sources': [
            {'path': '../outside.txt', 'sha256': '0' * 64}]})
        bundle.write_text(json.dumps(content), encoding='utf-8')
        self.assertIn('portable relative source path', self.run_memory('import', str(bundle), ok=False))
        self.assertEqual(set(self.recall()), {record_id})

    def test_only_approved_current_lessons_are_recalled(self):
        record_id = self.save('a.txt', 'b.txt')
        proposal = self.run_memory('propose-lesson', '--finding-id', record_id, '--lesson', 'Check both inputs')
        rejected = self.run_memory('propose-lesson', '--finding-id', record_id, '--lesson', 'Other advice')
        self.assertEqual(proposal['status'], 'pending')
        self.assertEqual(self.run_memory('recall-lessons'), [])
        self.run_memory('review-lesson', rejected['id'], '--decision', 'reject', '--by', 'Owner')
        self.run_memory('review-lesson', proposal['id'], '--decision', 'approve', '--by', 'Owner')
        self.assertEqual([lesson['id'] for lesson in self.run_memory('recall-lessons')], [proposal['id']])
        self.assertEqual({lesson['status'] for lesson in self.run_memory('list-lessons')}, {'approved', 'rejected'})
        (self.project / 'b.txt').write_text('changed', encoding='utf-8')
        self.assertEqual(self.run_memory('recall-lessons'), [])
        self.assertTrue(all(lesson['stale'] for lesson in self.run_memory('list-lessons')))
        self.run_memory('delete', record_id)
        self.assertEqual(self.run_memory('list-lessons'), [])
        with closing(sqlite3.connect(self.store)) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM lessons').fetchone(), (0,))

    def test_review_rejects_cross_project_stale_and_repeated_decisions(self):
        record_id = self.save('a.txt')
        proposal = self.run_memory('propose-lesson', '--finding-id', record_id, '--lesson', 'Check source')
        other = self.project.parent / 'other'
        other.mkdir()
        approve = ('review-lesson', proposal['id'], '--decision', 'approve', '--by', 'Owner')
        self.assertIn('No pending lesson', self.run_memory(*approve, project=other, ok=False))
        self.assertEqual(self.run_memory('list-lessons', project=other), [])
        (self.project / 'a.txt').write_text('different', encoding='utf-8')
        self.assertIn('stale evidence', self.run_memory(*approve, ok=False))
        self.assertIn('current finding', self.run_memory(
            'propose-lesson', '--finding-id', record_id, '--lesson', 'Try again', ok=False))
        (self.project / 'a.txt').write_text('a.txt', encoding='utf-8')
        self.run_memory(*approve)
        self.assertIn('No pending lesson', self.run_memory(*approve, ok=False))


    def test_context_preview_filters_ranks_and_bounds_output(self):
        def lesson(source, content, decision='approve'):
            proposal = self.run_memory('propose-lesson', '--finding-id', self.save(source), '--lesson', content)
            if decision:
                self.run_memory('review-lesson', proposal['id'], '--decision', decision, '--by', 'Owner')
            return proposal['id']

        short = lesson('a.txt', 'Check payment')
        long = lesson('a.txt', 'Check payment retries ' + 'é' * 60)
        lesson('a.txt', 'Check payment retries pending', None)
        lesson('a.txt', 'Check payment retries rejected', 'reject')
        lesson('a.txt', 'Check customer records')
        lesson('b.txt', 'Check payment retries stale')
        (self.project / 'b.txt').write_text('changed', encoding='utf-8')
        before = self.store.read_bytes()
        args = ('preview-context', '--task', 'PAYMENT retries')
        preview = self.run_memory(*args)
        self.assertEqual([entry['id'] for entry in preview], [long, short])
        self.assertEqual(preview[0]['matched_terms'], ['payment', 'retries'])
        self.assertEqual(preview[0]['sources'], ['a.txt'])
        result = self.memory_process(*args, '--max-bytes', '256')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len(result.stdout), 256)
        self.assertEqual([entry['id'] for entry in json.loads(result.stdout)], [short])
        self.assertEqual(self.run_memory(*args, '--max-lessons', '1'), preview[:1])
        self.assertEqual(self.run_memory(*args, project=self.home), [])
        self.assertEqual(self.store.read_bytes(), before)

    def test_context_preview_without_memory_does_not_create_store(self):
        self.assertEqual(self.run_memory('preview-context', '--task', 'payment'), [])
        self.assertFalse(self.store.parent.exists())


if __name__ == '__main__':
    unittest.main()
