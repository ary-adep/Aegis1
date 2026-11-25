import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SDD = Path(__file__).resolve().parents[1] / 'skills/aegis/sdd.py'


class SpecWorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.control = Path(directory.name)
        self.work = self.control / 'workspace'
        self.work.mkdir()
        self.git('init', '-q', '--template=')
        (self.work / 'app.txt').write_text('original\n')
        (self.work / 'notes.txt').write_text('original notes\n')
        self.git('add', '--', 'app.txt', 'notes.txt')
        self.git('commit', '-qm', 'fixture')
        self.spec = {
            'schema_version': 1, 'id': 'compatibility', 'title': 'Preserve old inserts',
            'scope': ['app.txt'],
            'requirements': [{'id': 'REQ-1', 'text': 'Old inserts still work'}],
            'criteria': [{'id': 'AC-1', 'requirement': 'REQ-1', 'check': 'Run compatibility check'}],
        }
        self.write('spec.json', self.spec)

    def write(self, name, value):
        (self.control / name).write_text(json.dumps(value), encoding='utf-8')

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.work), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
                        '-c', 'core.hooksPath=/dev/null', *args],
                       check=True, capture_output=True, timeout=10)

    def sdd(self, command, *args, error=None, blocked_stage=None):
        cmd = [sys.executable, '-B', str(SDD), command, str(self.control / 'spec.json')]
        if command != 'validate':
            cmd += ['--workspace', str(self.work), '--approval', str(self.control / 'approval.json')]
        if command in ('verify', 'check', 'status'):
            cmd += ['--review', str(self.control / 'review.json'),
                    '--verification', str(self.control / 'verification.json')]
        result = subprocess.run([*cmd, *args], text=True, capture_output=True, timeout=10)
        if blocked_stage:
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual((report['status'], report['stage']), ('blocked', blocked_stage))
            self.assertIn(error, report['reason'])
            self.assertTrue(report['next_action'])
            return report
        if error:
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn(error, result.stderr)
            return None
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def review(self):
        checked = self.sdd('check-scope')
        self.assertEqual(checked['changed_paths'], ['app.txt'])
        (self.control / 'evidence.txt').write_text('fixture evidence\n')
        return {
            'implemented_by': 'maker', 'reviewed_by': 'checker',
            'workspace_sha256': checked['workspace_sha256'],
            'criteria': {'AC-1': {'result': 'PASS', 'observations': 'fixture observation',
                                  'evidence': ['evidence.txt']}},
        }

    def test_handoff_checks_scope_review_and_artifact_drift(self):
        (self.work / 'notes.txt').write_text('pre-existing edit\n')
        self.sdd('approve', '--by', 'owner')
        (self.work / 'app.txt').write_text('change\n')
        self.write('review.json', self.review())
        self.sdd('verify')
        self.assertEqual(self.sdd('check')['criteria_passed'], 1)
        evidence = self.control / 'evidence.txt'
        evidence.write_text('changed evidence\n')
        self.sdd('check', error='changed after verification')
        evidence.write_text('fixture evidence\n')
        (self.work / 'app.txt').write_text('unreviewed change\n')
        self.sdd('check', error='different workspace snapshot')
        (self.work / 'test.txt').write_text('unapproved file\n')
        self.sdd('check-scope', error='outside approved scope: test.txt')

    def test_status_reuses_gate_and_guides_blocked_handoffs(self):
        self.sdd('status', blocked_stage='approval', error='approval.json')
        self.sdd('approve', '--by', 'owner')
        (self.work / 'app.txt').write_text('change\n')
        self.sdd('status', blocked_stage='review', error='review.json')
        self.write('review.json', self.review())
        evidence = self.control / 'evidence.txt'
        evidence.unlink()
        self.sdd('status', blocked_stage='evidence', error='evidence.txt')
        evidence.write_text('fixture evidence\n')
        self.sdd('status', blocked_stage='verification', error='verification.json')
        self.assertFalse((self.control / 'verification.json').exists())
        self.sdd('verify')
        before = {p.name: p.read_bytes() for p in self.control.iterdir() if p.is_file()}
        self.assertEqual(self.sdd('status'), {'status': 'ready', **self.sdd('check')})
        self.assertEqual({p.name: p.read_bytes() for p in self.control.iterdir() if p.is_file()}, before)
        evidence.write_text('changed evidence\n')
        self.sdd('status', blocked_stage='verification', error='changed after verification')
        (self.work / 'app.txt').write_text('unreviewed change\n')
        self.sdd('status', blocked_stage='review', error='different workspace snapshot')
        (self.work / 'test.txt').write_text('unapproved file\n')
        self.sdd('status', blocked_stage='scope', error='outside approved scope')

    def test_existing_overlap_and_spec_changes_require_approval(self):
        (self.work / 'app.txt').write_text('pre-existing edit\n')
        self.sdd('approve', '--by', 'owner', error='existing changes require explicit scope approval')
        self.spec['allow_existing_changes'] = ['app.txt']
        self.write('spec.json', self.spec)
        self.sdd('approve', '--by', 'owner')
        self.spec['title'] = 'Different spec'
        self.write('spec.json', self.spec)
        self.sdd('check-scope', error='different spec or workspace')

    def test_nonpassing_or_nonindependent_review_blocks_verification(self):
        self.sdd('approve', '--by', 'owner')
        (self.work / 'app.txt').write_text('change\n')
        review = self.review()
        self.write('review.json', {**review, 'reviewed_by': 'maker'})
        self.sdd('verify', error='independent reviewer')
        review['criteria']['AC-1']['result'] = 'SKIPPED'
        self.write('review.json', review)
        self.sdd('verify', error='does not have a passing independent result')
        self.git('add', '--', 'app.txt')
        self.sdd('check-scope', error='Git HEAD or index changed')

    def test_untraced_requirement_blocks_spec(self):
        self.spec['requirements'].append({'id': 'REQ-2', 'text': 'No duplicate retries'})
        self.write('spec.json', self.spec)
        self.sdd('validate', error='every requirement must be covered')

    def test_review_ready_criteria_need_captured_checks_or_an_explicit_gap(self):
        self.sdd('validate', '--review-ready', error='needs a structured verification plan')
        plan = {
            'setup': 'Apply the prior schema and the candidate migration.',
            'action': 'Run the previous insert twice.',
            'expected': 'Both calls succeed and one row remains.',
            'source_paths': ['app.txt'],
            'existing_checks': [],
        }
        self.spec['criteria'][0]['verification'] = plan
        self.write('spec.json', self.spec)
        self.sdd('validate', '--review-ready', error='verification.coverage_gap')
        plan['coverage_gap'] = 'Add a replay assertion.'
        self.write('spec.json', self.spec)
        self.sdd('validate', '--review-ready')
        plan['existing_checks'] = ['missing.sql']
        self.write('spec.json', self.spec)
        self.sdd('approve', '--review-ready', '--by', 'owner', error='missing.sql')
        plan['existing_checks'] = ['notes.txt']
        self.write('spec.json', self.spec)
        self.sdd('approve', '--review-ready', '--by', 'owner')
