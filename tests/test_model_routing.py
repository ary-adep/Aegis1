import unittest

from scripts.aegis1 import select_discovery_model


class DiscoveryModelRoutingTests(unittest.TestCase):
    def test_single_available_model(self):
        self.assertEqual(select_discovery_model({"openai/gpt-5"}), "openai/gpt-5")

    def test_prefers_light_model_for_discovery(self):
        models = {"openai/gpt-5", "openai/gpt-5-mini", "openai/text-embedding-3-small"}
        self.assertEqual(select_discovery_model(models), "openai/gpt-5-mini")

    def test_respects_approval_filter(self):
        models = {"openai/gpt-5", "openai/gpt-5-mini"}
        self.assertEqual(select_discovery_model(models, {"openai/gpt-5"}), "openai/gpt-5")

    def test_rejects_unavailable_or_unrecognized_choices(self):
        with self.assertRaises(ValueError):
            select_discovery_model({"openai/gpt-5"}, {"openai/gpt-5-mini"})
        with self.assertRaises(ValueError):
            select_discovery_model({"openai/text-embedding-3-small"})


class DiscoveryHandoffTests(unittest.TestCase):
    def test_mocked_claude_to_openai_resume_checks_current_evidence(self):
        import io
        import json
        import os
        from pathlib import Path
        import subprocess
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        from scripts import aegis1

        task = "Find the entry point"
        with TemporaryDirectory() as scratch:
            root = Path(scratch)
            repo = root / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            for name in ("README.md", "main.py"):
                (repo / name).write_text("Original " + name, encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "README.md", "main.py"], check=True)
            checkpoint = root / "run.json"
            reads = [
                {"stop_reason": "end_turn", "content": [
                    {"type": "text", "text": json.dumps({"action": "read", "path": name})}
                ]}
                for name in ("README.md", "main.py")
            ]
            with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test", "OPENAI_API_KEY": "test"}):
                with patch.object(aegis1, "urlopen", side_effect=[
                    io.StringIO(json.dumps(response)) for response in reads
                ]):
                    paused = aegis1.discover(repo, task, aegis1.ClaudeModel("test"),
                                             checkpoint=checkpoint, pause_after=2)
                self.assertEqual(paused["status"], "DISCOVERY PAUSED")
                self.assertNotIn("Original", checkpoint.read_text(encoding="utf-8"))
                (repo / "main.py").write_text("Changed", encoding="utf-8")
                report = {"action": "report", "evidence": [
                    {"path": "README.md", "excerpt": "Original README.md"}
                ], "unknowns": [], "summary": "Entry point", "complete": True}
                response = {"status": "completed", "output": [{"type": "message", "content": [
                    {"type": "output_text", "text": json.dumps(report)}
                ]}]}
                with patch.object(aegis1, "urlopen", return_value=io.StringIO(json.dumps(response))) as call:
                    resumed = aegis1.discover(repo, task, aegis1.OpenAIModel("test"),
                                              checkpoint=checkpoint, resume=True)
                evidence = json.loads(json.loads(call.call_args.args[0].data)["input"])["read_prefixes"]
                self.assertEqual(evidence, {"README.md": "Original README.md"})
                self.assertEqual(resumed["stale_sources"], ["main.py"])
                self.assertEqual(resumed["status"], "DISCOVERY COMPLETE")
