"""Run a read-only task through a signed-in local coding host."""

import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryFile
from time import monotonic


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


def activity(event):
    kind = event.get("type")
    if kind == "assistant":
        blocks = event.get("message", {}).get("content", [])
        if any(block.get("type") == "tool_use" for block in blocks):
            return "Inspecting workspace files…"
    if kind == "item.started":
        if event.get("item", {}).get("type") in {"command_execution", "mcp_tool_call"}:
            return "Running a read-only check…"
    if kind == "turn.started":
        return "Working on your request…"
    if kind == "tool_result" or kind == "user":
        return "Reviewing tool results…"
    return None


UI_TIMEOUT = 900


def reply_update(event):
    if event.get("type") == "stream_event":
        message = event.get("event", {})
        if message.get("type") == "message_start":
            return "replace", ""
        delta = message.get("delta", {})
        if message.get("type") == "content_block_delta" and delta.get("type") == "text_delta":
            return "append", delta.get("text", "")
    item = event.get("item", {})
    if event.get("type") in {"item.updated", "item.completed"} and item.get("type") == "agent_message":
        return "replace", item.get("text", "")
    return None


def run_with_progress(command, repo, prompt, run):
    from threading import Thread

    stopped, update = run
    with TemporaryFile() as input_file:
        input_file.write(prompt.encode("utf-8"))
        input_file.seek(0)
        with subprocess.Popen(
            command, cwd=repo, stdin=input_file, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace",
        ) as process:
            lines = []

            def read_output():
                for line in process.stdout:
                    lines.append(line)
                    try:
                        event = json.loads(line)
                        label = activity(event)
                        reply = reply_update(event)
                    except (ValueError, AttributeError, TypeError):
                        continue
                    if label:
                        update("activity", label)
                    if reply:
                        update(*reply)

            reader = Thread(target=read_output, daemon=True)
            reader.start()
            deadline = monotonic() + UI_TIMEOUT
            try:
                while process.poll() is None:
                    if stopped.wait(0.1):
                        raise InterruptedError("Run stopped.")
                    if monotonic() >= deadline:
                        raise subprocess.TimeoutExpired(command, UI_TIMEOUT)
                if stopped.is_set():
                    raise InterruptedError("Run stopped.")
            finally:
                if process.poll() is None:
                    process.kill()
                process.wait()
                reader.join()
            return subprocess.CompletedProcess(command, process.returncode, "".join(lines))


def run_read_only(host, executable, repo, prompt, run=None):
    if host == "claude":
        command = [
            executable, "--print", "--no-session-persistence", "--output-format", "stream-json" if run else "json",
            "--disable-slash-commands", "--max-turns", "15",
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
            "--tools", "Read", "Glob", "Grep",
        ]
        if run:
            command.extend(["--verbose", "--include-partial-messages"])
    else:
        command = [executable, "exec", "--sandbox", "read-only", "--skip-git-repo-check",
                   "--ephemeral", "--json", "-"]
    if run:
        result = run_with_progress(command, repo, prompt, run)
    else:
        result = subprocess.run(command, cwd=repo, input=prompt, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=180)
    if result.returncode:
        raise ValueError(f"{host} could not complete the run. Check its sign-in and permissions.")
    if host == "claude":
        if run:
            events = (json.loads(line) for line in result.stdout.splitlines() if line.strip())
            response = next((event for event in events if event.get("type") == "result"), {})
        else:
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
