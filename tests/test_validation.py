import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import frontmatter, validate, SPECIALISTS
from evaluate import load_cases, prepare, hashes, validate_record, safe_file


class DistributionChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'candidate'
        shutil.copytree(ROOT, self.root)

    def test_distribution_is_structurally_valid(self):
        result = validate(self.root)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual(len(result['inventory']), 10)

    def test_missing_agent_is_detected(self):
        (self.root / 'agents/aegis1.md').unlink()
        self.assertTrue(any('agent' in e for e in validate(self.root)['errors']))

    def test_broken_reference_is_detected(self):
        (self.root / 'skills/debugging/references/diagnosis-method.md').unlink()
        self.assertTrue(any('broken link' in e for e in validate(self.root)['errors']))

    def test_orphan_reference_is_detected(self):
        (self.root / 'skills/debugging/references/orphan.md').write_text('Unlinked reference', encoding='utf-8')
        self.assertTrue(any('unlinked reference' in e for e in validate(self.root)['errors']))

    def test_traversal_link_is_rejected(self):
        p = self.root / 'README.md'
        p.write_text(p.read_text(encoding='utf-8') + '\n[escape](../../outside.md)\n', encoding='utf-8')
        self.assertTrue(any('escapes distribution' in e for e in validate(self.root)['errors']))

    def test_duplicate_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            frontmatter('---\nname: "x"\nname: "y"\n---\n')

    def test_boolean_string_is_rejected(self):
        p = self.root / 'skills/aegis/SKILL.md'
        p.write_text(p.read_text(encoding='utf-8').replace('disable-model-invocation: true', 'disable-model-invocation: "true"'), encoding='utf-8')
        self.assertTrue(any('disable-model-invocation must be boolean' in e for e in validate(self.root)['errors']))

    def test_truncated_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unclosed'):
            frontmatter('---\nname: "x"\n')

    def test_long_reference_needs_contents(self):
        p = self.root / 'skills/debugging/references/diagnosis-method.md'
        p.write_text('\n'.join(['text'] * 101), encoding='utf-8')
        self.assertTrue(any('needs contents' in e for e in validate(self.root)['errors']))


class EvaluationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.cases = {c['id']: c for c in load_cases()}

    def test_every_specialist_and_orchestrator_has_three_categories(self):
        for skill in ('aegis', *SPECIALISTS):
            kinds = {c['category'] for c in self.cases.values() if c['skill'] == skill}
            self.assertTrue({'normal', 'boundary', 'failure'} <= kinds, skill)

    def test_every_packet_prepares_without_expected_answers_in_task(self):
        before = hashes(ROOT / 'evaluations/fixtures')
        for case in self.cases.values():
            output = prepare(case, self.directory / case['id'])
            task = (output / 'task.md').read_text(encoding='utf-8')
            self.assertNotIn('expected_statuses', task)
            self.assertNotIn('grading.json', task)
            self.assertTrue((output / 'workspace').is_dir())
            result = json.loads((output / 'result.json').read_text(encoding='utf-8'))
            self.assertFalse(result['executed'])
            self.assertEqual(result['result'], 'NOT_RUN')
        self.assertEqual(before, hashes(ROOT / 'evaluations/fixtures'))

    def test_existing_destination_is_preserved(self):
        output = self.directory / 'existing'
        output.mkdir()
        marker = output / 'user.txt'
        marker.write_text('keep', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            prepare(self.cases['DISC-01'], output)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'keep')

    def test_preparation_cannot_write_into_distribution(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            prepare(self.cases['DISC-01'], ROOT / 'evaluations/unsafe-run')

    def test_evidence_path_cannot_escape(self):
        with self.assertRaisesRegex(ValueError, 'escapes'):
            safe_file(self.directory, '../outside.txt')

    def run_fixture(self, case_id):
        directory = prepare(self.cases[case_id], self.directory / case_id)
        return subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', '.', '-v'],
                              cwd=directory / 'workspace', capture_output=True, text=True, timeout=30)

    def test_baseline_fixture_passes_all_five_tests(self):
        result = self.run_fixture('VERIFY-01')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Ran 5 tests', result.stderr)
        self.assertNotIn('skipped', result.stderr)

    def test_bug_fixture_fails_at_full_stock(self):
        result = self.run_fixture('VERIFY-03')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('test_full_stock', result.stderr)
        self.assertIn('ValueError: insufficient stock', result.stderr)
        self.assertIn('errors=1', result.stderr)

    def test_skipped_fixture_has_zero_exit_but_no_acceptance_execution(self):
        result = self.run_fixture('REG-02')
        self.assertEqual(result.returncode, 0)
        self.assertIn('skipped=5', result.stderr)

    def test_valid_unrun_template_does_not_claim_success(self):
        output = prepare(self.cases['DISC-01'], self.directory / 'unrun')
        record = json.loads((output / 'result.json').read_text(encoding='utf-8'))
        self.assertEqual(validate_record(record, self.cases['DISC-01'], output), [])
        self.assertEqual(record['result'], 'NOT_RUN')

    def scored_record(self):
        case = self.cases['DISC-01']
        output = prepare(case, self.directory / 'scored')
        record = json.loads((output / 'result.json').read_text(encoding='utf-8'))
        # Synthetic data tests record validation only; never a model run.
        record.update(model='synthetic-test-model', model_version='fixture-version', claude_code_version='fixture-version',
                      executed=True, result='PASS', terminal_status='DISCOVERY COMPLETE', reviewer='unit-test',
                      observations='Synthetic record tests format only.', transcript='transcript.txt', workspace_after='after.json')
        (output / 'transcript.txt').write_text('Synthetic transcript\nDISCOVERY COMPLETE\n', encoding='utf-8')
        (output / 'after.json').write_text('{}', encoding='utf-8')
        for check in record['checks']:
            check.update(satisfied=True, evidence=['transcript.txt#1'])
        return case, output, record

    def test_complete_record_format_is_accepted(self):
        case, output, record = self.scored_record()
        self.assertEqual(validate_record(record, case, output), [])

    def test_pass_without_execution_is_rejected(self):
        case, output, record = self.scored_record()
        record['executed'] = False
        self.assertTrue(validate_record(record, case, output))

    def test_pass_without_evidence_is_rejected(self):
        case, output, record = self.scored_record()
        record['checks'][0]['evidence'] = []
        self.assertTrue(validate_record(record, case, output))

    def test_pass_with_failed_criterion_is_rejected(self):
        case, output, record = self.scored_record()
        record['checks'][0]['satisfied'] = False
        self.assertTrue(validate_record(record, case, output))

    def test_pass_with_wrong_status_is_rejected(self):
        case, output, record = self.scored_record()
        record['terminal_status'] = 'IMPLEMENTATION COMPLETE'
        self.assertTrue(validate_record(record, case, output))

    def test_missing_or_escaping_evidence_is_rejected(self):
        case, output, record = self.scored_record()
        for evidence in ('missing.txt', '../external.txt'):
            record['checks'][0]['evidence'] = [evidence]
            self.assertTrue(validate_record(record, case, output))

    def test_removed_grading_criterion_is_rejected(self):
        case, output, record = self.scored_record()
        record['checks'].pop()
        self.assertTrue(validate_record(record, case, output))


if __name__ == '__main__':
    unittest.main()
