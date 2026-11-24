import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallPlanTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.project = Path(directory.name).resolve()
        self.claude = self.project / '.claude'

    def installer(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'install-aegis.py'),
             '--project', str(self.project), *args],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def plan(self, *args):
        return json.loads(self.installer('--plan', *args).stdout)

    def test_fresh_claude_plan_is_read_only_and_matches_install(self):
        self.claude.mkdir()
        settings = self.claude / 'settings.json'
        settings.write_bytes(b'{"custom":true}\n')
        plan = self.plan()
        self.assertEqual(plan['status'], 'ready')
        self.assertIn('settings.json', plan['existing_configuration'])
        self.assertEqual(sorted(p.name for p in self.claude.iterdir()), ['settings.json'])
        self.installer()
        actual = self.plan()
        self.assertEqual(actual['unchanged'], plan['add'])
        self.assertFalse(actual['manifest_update_needed'])
        self.assertEqual(settings.read_bytes(), b'{"custom":true}\n')

    def test_plan_and_install_identify_user_owned_conflict(self):
        self.installer()
        agent = self.claude / 'agents/aegis1.md'
        agent.write_bytes(b'User-owned modification\n')
        plan = self.plan()
        self.assertEqual(plan['status'], 'blocked')
        self.assertEqual(plan['conflicts'], ['agents/aegis1.md'])
        result = self.installer(expected=1)
        self.assertIn(str(agent), result.stderr)
        self.assertEqual(agent.read_bytes(), b'User-owned modification\n')

    def test_manifest_recognized_content_is_planned_as_an_update(self):
        self.installer()
        agent = self.claude / 'agents/aegis1.md'
        manifest = self.claude / '.aegis1-install.json'
        state = json.loads(manifest.read_text())
        old = b'Recorded distribution version\n'
        state['files']['agents/aegis1.md'] = hashlib.sha256(old).hexdigest()
        agent.write_bytes(old)
        original_manifest = json.dumps(state).encode()
        manifest.write_bytes(original_manifest)
        plan = self.plan()
        self.assertEqual(plan['update'], ['agents/aegis1.md'])
        self.assertEqual(plan['conflicts'], [])
        self.assertEqual(agent.read_bytes(), old)
        self.assertEqual(manifest.read_bytes(), original_manifest)

    def test_legacy_link_preview_does_not_move_the_link(self):
        entry = self.claude / 'agents/aegis1.md'
        entry.parent.mkdir(parents=True)
        try:
            entry.symlink_to(ROOT / 'agents/aegis1.md')
        except OSError as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        plan = self.plan()
        self.assertEqual(plan['backup_legacy_links'], ['agents/aegis1.md'])
        self.assertIn('agents/aegis1.md', plan['add'])
        self.assertTrue(entry.is_symlink())
        self.assertFalse((self.claude / '.aegis1-link-backups').exists())

    def test_codex_inventory_does_not_parse_or_modify_configuration(self):
        codex = self.project / '.codex'
        codex.mkdir()
        content = b'intentionally invalid toml with private fixture text'
        config = codex / 'config.toml'
        config.write_bytes(content)
        inventory = self.plan('--host', 'codex')
        self.assertEqual(inventory['status'], 'inventory_only')
        self.assertEqual(inventory['existing_configuration'], ['config.toml'])
        self.assertNotIn('private fixture text', json.dumps(inventory))
        self.installer('--host', 'codex', expected=2)
        self.assertEqual(config.read_bytes(), content)
        self.assertFalse(self.claude.exists())
