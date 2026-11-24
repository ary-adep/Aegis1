import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / 'scripts/config_check.py'


class ConfigCheckTests(unittest.TestCase):
    def setUp(self):
        fixture = tempfile.TemporaryDirectory()
        self.addCleanup(fixture.cleanup)
        self.project = Path(fixture.name) / 'project'
        self.project.mkdir()

    def put(self, name, content):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def scan(self, host, *paths, expected=0):
        args = [sys.executable, '-B', str(CHECKER), '--project', str(self.project), '--host', host]
        for path in paths:
            args += ['--file', path]
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout)

    def test_claude_reports_declarations_without_values_or_writes(self):
        rel = '.claude/settings.json'
        content = json.dumps({'permissions': {'defaultMode': 'bypassPermissions'},
                              'hooks': {'PostToolUse': [{'command': 'private fixture marker'}]},
                              'mcpServers': {'private fixture marker': {}}})
        config = self.put(rel, content)
        ignored = self.put('.claude/settings.local.json', '{invalid')
        before = {config: (config.read_bytes(), config.stat().st_mtime_ns),
                  ignored: (ignored.read_bytes(), ignored.stat().st_mtime_ns)}
        result = self.scan('claude', rel, expected=1)
        self.assertEqual({finding['id'] for finding in result['findings']},
                         {'hooks_declared', 'mcp_declared', 'permissions_declared', 'approval_bypass_declared'})
        self.assertNotIn('private fixture marker', json.dumps(result))
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in before}, before)
        self.assertEqual(set((self.project / '.claude').iterdir()), set(before))

    def test_malformed_json_and_duplicate_keys_do_not_echo_contents(self):
        for content in ('{"private fixture marker":', '{"duplicate":1,"duplicate":2}'):
            with self.subTest(content=content):
                rel = '.claude/settings.json'
                self.put(rel, content)
                result = self.scan('claude', rel, expected=2)
                self.assertEqual(result['findings'][0]['id'], 'malformed_configuration')
                self.assertNotIn('private fixture marker', json.dumps(result))

    def test_outside_links_and_missing_paths_are_blocked(self):
        outside = self.project.parent / 'outside.json'
        outside.write_text('{"hooks":{"private fixture marker":[]}}', encoding='utf-8')
        link = self.project / '.mcp.json'
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        result = self.scan('claude', '.mcp.json', '.claude/mcp.json', expected=2)
        self.assertEqual({finding['id'] for finding in result['findings']},
                         {'configuration_missing_or_not_file', 'configuration_link_escapes_root'})
        self.assertNotIn(str(outside), json.dumps(result))

    def test_codex_json_hooks_and_toml_runtime_coverage_are_distinct(self):
        self.put('.codex/hooks.json', '{"hooks":{"SessionStart":[]}}')
        self.assertEqual(self.scan('codex', '.codex/hooks.json')['findings'][0]['id'], 'hooks_declared')
        rel = '.codex/config.toml'
        config = self.put(rel, 'approval_policy = "never"\nsandbox_mode = "danger-full-access"\n'
                               '[mcp_servers.example]\ncommand = "private fixture marker"\n')
        original = config.read_bytes()
        if importlib.util.find_spec('tomllib') is None:
            result = self.scan('codex', rel, expected=2)
            self.assertEqual(result['findings'][0]['id'], 'toml_requires_python_3_11')
        else:
            result = self.scan('codex', rel, expected=1)
            self.assertEqual({finding['id'] for finding in result['findings']},
                             {'approval_prompting_disabled', 'permissions_declared',
                              'full_access_sandbox_declared', 'mcp_declared'})
            self.assertNotIn('private fixture marker', json.dumps(result))
        self.assertEqual(config.read_bytes(), original)
