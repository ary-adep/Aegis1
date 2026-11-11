"""Read the model menu from Claude Code without submitting a task."""

import json
from pathlib import Path
import shutil
import subprocess
import sys


def claude_binary():
    executable = shutil.which("claude")
    if executable:
        return executable
    extensions = Path.home() / ".vscode" / "extensions"
    binaries = [
        path for name in ("claude", "claude.exe")
        for path in extensions.glob(f"anthropic.claude-code-*/resources/native-binary/{name}")
        if path.is_file()
    ]
    if not binaries:
        raise ValueError("Claude Code executable unavailable")
    return str(max(binaries, key=lambda path: path.stat().st_mtime))


def inventory(executable):
    request = {"type": "control_request", "request_id": "aegis-models",
               "request": {"subtype": "initialize"}}
    command = [executable, "--print", "--input-format", "stream-json",
               "--output-format", "stream-json", "--verbose", "--no-session-persistence"]
    result = subprocess.run(command, input=json.dumps(request) + "\n",
                            capture_output=True, text=True, timeout=10)
    if result.returncode:
        raise ValueError("Claude Code model inventory unavailable")
    for line in result.stdout.splitlines():
        event = json.loads(line)
        if event.get("type") != "control_response":
            continue
        response = event["response"]
        if response.get("request_id") != request["request_id"] or response.get("subtype") != "success":
            continue
        return [
            {"alias": item["value"], "name": item.get("displayName", item["value"])}
            for item in response["response"]["models"]
            if item["value"] in {"haiku", "sonnet", "opus", "fable"}
        ]
    raise ValueError("Claude Code returned no model inventory")


if __name__ == "__main__":
    try:
        print(json.dumps({"models": inventory(claude_binary())}))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        print(json.dumps({"models": [], "status": "unavailable"}))
        sys.exit(1)
