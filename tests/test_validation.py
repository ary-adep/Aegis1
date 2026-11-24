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
        self.assertEqual(len(result['inventory']), 12)

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
        self.assertEqual(record['schema_version'], 2)

    def scored_record(self):
        case = self.cases['DISC-01']
        output = prepare(case, self.directory / 'scored')
        record = json.loads((output / 'result.json').read_text(encoding='utf-8'))
        # Synthetic data tests record validation only; never a model run.
        record.update(workflow='aegis1', host='claude-code', host_version='fixture-version',
                      model='synthetic-test-model', model_version='fixture-version',
                      fixture_revision='a' * 40, elapsed_ms=123,
                      usage={'input_tokens': 100, 'output_tokens': 30, 'cached_input_tokens': None},
                      usage_notes='Synthetic usage; cache count unavailable.',
                      effective_permissions='permissions.json',
                      independent_verification='verification.txt',
                      executed=True, result='PASS', terminal_status='DISCOVERY COMPLETE', reviewer='unit-test',
                      observations='Synthetic record tests format only.', transcript='transcript.txt', workspace_after='after.json')
        (output / 'transcript.txt').write_text('Synthetic transcript\nDISCOVERY COMPLETE\n', encoding='utf-8')
        (output / 'after.json').write_text('{}', encoding='utf-8')
        (output / 'permissions.json').write_text('{"fixture_only": true}', encoding='utf-8')
        (output / 'verification.txt').write_text('Synthetic verification evidence.', encoding='utf-8')
        for check in record['checks']:
            check.update(satisfied=True, evidence=['transcript.txt#1'])
        return case, output, record

    def test_complete_record_format_is_accepted(self):
        case, output, record = self.scored_record()
        self.assertEqual(validate_record(record, case, output), [])

    def test_evidence_gate_requires_a_valid_current_pass(self):
        _, output, record = self.scored_record()
        path = output / 'result.json'
        command = [sys.executable, '-B', str(ROOT / 'scripts/evaluate.py'), 'check-record', str(path)]
        receipt = output / 'receipt.json'
        seal = [*command[:3], 'seal-record', str(path), str(receipt)]
        path.write_text(json.dumps(record), encoding='utf-8')
        subprocess.run(seal, capture_output=True, text=True, timeout=10, check=True)
        unsealed = subprocess.run([*command, '--require-pass'], capture_output=True, text=True, timeout=10)
        self.assertEqual(unsealed.returncode, 1)
        self.assertIn('requires a verified receipt', unsealed.stdout)
        records = (
            (record, True),
            ({**record, 'result': 'FAIL'}, False),
            ({**record, 'result': 'BLOCKED'}, False),
            ({**record, 'result': 'NOT_RUN', 'executed': False}, False),
            ({**record, 'schema_version': 1, 'claude_code_version': 'fixture-version'}, False),
            ({**record, 'independent_verification': 'missing.txt'}, False),
        )
        for candidate, expected in records:
            with self.subTest(candidate=candidate['result'], schema=candidate['schema_version']):
                path.write_text(json.dumps(candidate), encoding='utf-8')
                result = subprocess.run([*command, '--receipt', str(receipt), '--require-pass'],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0 if expected else 1, result.stderr)
                self.assertIs(json.loads(result.stdout)['passes_evidence_gate'], expected)

    def test_receipt_detects_changed_transcript_snapshot_and_criterion_artifacts(self):
        _, output, record = self.scored_record()
        (output / 'criterion.txt').write_text('criterion evidence', encoding='utf-8')
        record['checks'][0]['evidence'] = ['criterion.txt#1']
        path = output / 'result.json'
        receipt = output / 'receipt.json'
        path.write_text(json.dumps(record), encoding='utf-8')
        prefix = [sys.executable, '-B', str(ROOT / 'scripts/evaluate.py')]
        seal = [*prefix, 'seal-record', str(path), str(receipt)]
        subprocess.run(seal, capture_output=True, text=True, timeout=10, check=True)
        original_receipt = receipt.read_bytes()
        self.assertNotEqual(subprocess.run(seal, capture_output=True, timeout=10).returncode, 0)
        self.assertEqual(receipt.read_bytes(), original_receipt)
        command = [*prefix, 'check-record', str(path), '--receipt', str(receipt), '--require-pass']
        for name in ('transcript.txt', 'baseline.json', 'after.json', 'verification.txt', 'criterion.txt'):
            with self.subTest(artifact=name):
                artifact = output / name
                original = artifact.read_bytes()
                artifact.write_bytes(original + b' changed')
                result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 1)
                self.assertIn(f'evidence changed: {name}', json.loads(result.stdout)['errors'])
                artifact.write_bytes(original)
        (output / 'criterion.txt').unlink()
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn('path missing: criterion.txt', json.loads(result.stdout)['errors'])

    def test_native_record_can_use_a_non_git_fixture(self):
        case, output, record = self.scored_record()
        record.update(workflow='native', host='codex', fixture_revision=None)
        self.assertEqual(validate_record(record, case, output), [])

    def test_legacy_record_still_validates(self):
        case, output, record = self.scored_record()
        legacy_fields = ('case_id', 'model', 'model_version', 'skill_snapshot', 'agent_snapshot',
                         'executed', 'result', 'terminal_status', 'transcript', 'workspace_after',
                         'reviewer', 'observations', 'checks')
        legacy = {key: record[key] for key in legacy_fields}
        legacy['claude_code_version'] = 'fixture-version'
        self.assertEqual(validate_record(legacy, case, output), [])

    def test_invalid_baseline_metadata_is_rejected(self):
        case, output, record = self.scored_record()
        invalid_values = {
            'schema_version': True,
            'workflow': 'invalid',
            'host_version': '',
            'fixture_revision': 'abcdef',
            'elapsed_ms': True,
            'usage_notes': '',
            'usage': {'input_tokens': 10, 'output_tokens': 5, 'cached_input_tokens': 11},
            'workspace_before': 'missing.json',
            'effective_permissions': '../outside.json',
            'independent_verification': 'missing.txt',
        }
        for key, value in invalid_values.items():
            with self.subTest(field=key):
                self.assertTrue(validate_record({**record, key: value}, case, output))

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
