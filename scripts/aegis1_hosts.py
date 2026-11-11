"""Run a read-only task through a signed-in local coding host."""

import json
from pathlib import Path
import shutil
import subprocess


def installed_hosts():
    codex = shutil.which("codex")
    if not codex:
        bundled = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")
        codex = str(bundled) if bundled.is_file() else None
    claude = shutil.which("claude")
    if not claude:
        extensions = Path.home() / ".vscode" / "extensions"
        binaries = [path for name in ("claude", "claude.exe")
                    for path in extensions.glob(f"anthropic.claude-code-*/resources/native-binary/{name}")
                    if path.is_file()]
        if binaries:
            claude = str(max(binaries, key=lambda path: path.stat().st_mtime))
    return {name: executable for name, executable in (("claude", claude), ("codex", codex))
            if executable}


def run_read_only(host, executable, repo, prompt):
    if host == "claude":
        command = [
            executable, "--print", "--no-session-persistence", "--output-format", "json",
            "--disable-slash-commands", "--max-turns", "15",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--tools", "Read", "Glob", "Grep",
        ]
    else:
        command = [executable, "exec", "--sandbox", "read-only", "--skip-git-repo-check",
                   "--ephemeral", "--json", "-"]
    result = subprocess.run(command, cwd=repo, input=prompt, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=180)
    if result.returncode:
        raise ValueError(f"{host} could not complete the run. Check its sign-in and permissions.")
    if host == "claude":
        response = json.loads(result.stdout)
        if response.get("is_error"):
            raise ValueError("Claude Code could not complete the run. Check its sign-in and permissions.")
        return {"report": response["result"], "models": list(response.get("modelUsage", {}))}
    events = (json.loads(line) for line in result.stdout.splitlines() if line.strip())
    messages = [event["item"]["text"] for event in events
                if event.get("type") == "item.completed"
                and event.get("item", {}).get("type") == "agent_message"]
    if not messages:
        raise ValueError("Codex returned no report.")
    return {"report": messages[-1], "models": []}
