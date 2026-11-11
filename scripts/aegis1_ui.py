"""Local browser interface for read-only discovery through signed-in coding hosts."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
from threading import Lock

if __package__:
    from .aegis1_hosts import installed_hosts, run_read_only
else:
    from aegis1_hosts import installed_hosts, run_read_only

SOURCE = Path(__file__).resolve().parents[1]
MAX_REQUEST = 196_608
FOLDER_DIALOG_LOCK = Lock()


def native_folder_dialog(root: Path) -> str | None:
    """Return a selected folder, None on cancel, or raise if unavailable."""
    if sys.platform == "darwin":
        command = [
            "/usr/bin/osascript", "-e",
            'on run argv\nreturn POSIX path of (choose folder with prompt "Select Aegis1 workspace" '
            'default location (POSIX file (item 1 of argv) as alias))\nend run',
            str(root),
        ]
    elif sys.platform == "win32":
        powershell = shutil.which("powershell.exe")
        if not powershell:
            raise OSError("Windows folder picker unavailable")
        script = (
            '[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); '
            'Add-Type -AssemblyName System.Windows.Forms; '
            '$dialog = New-Object System.Windows.Forms.FolderBrowserDialog; '
            '$dialog.Description = "Select Aegis1 workspace"; '
            '$dialog.SelectedPath = (Get-Location).ProviderPath; '
            '$dialog.ShowNewFolderButton = $false; '
            'if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) '
            '{ [Console]::WriteLine($dialog.SelectedPath) }'
        )
        command = [powershell, "-NoProfile", "-STA", "-Command", script]
    elif sys.platform.startswith("linux"):
        if zenity := shutil.which("zenity"):
            command = [zenity, "--file-selection", "--directory",
                       "--title=Select Aegis1 workspace", f"--filename={root}/"]
        elif kdialog := shutil.which("kdialog"):
            command = [kdialog, "--getexistingdirectory", str(root), "--title", "Select Aegis1 workspace"]
        else:
            raise OSError("Linux folder picker unavailable")
    else:
        raise OSError("Native folder picker unavailable")
    result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=120)
    if result.returncode:
        if (sys.platform == "darwin" and "(-128)" in result.stderr
                or sys.platform.startswith("linux") and result.returncode == 1 and not result.stderr.strip()):
            return None
        raise OSError("Native folder picker unavailable")
    return result.stdout.rstrip("\r\n") or None


def run_discovery(host, executable, repo, task, history=()):
    instructions = (
        "The Aegis1 governance, system-discovery skill, and relevant references "
        "are loaded below from the Aegis1 installation. Treat the supplied bodies as already "
        "read. Their relative instruction links resolve in the installation. Apply the skill for read-only workspace questions. "
        "Keep the scope within the workspace. Cite source with Markdown links using complete "
        "workspace-relative paths and #L line anchors. Distinguish "
        "confirmed facts from assumptions.\n\n"
    )
    for name in ("agents/aegis1.md", "skills/system-discovery/SKILL.md",
                 "skills/system-discovery/references/evidence-model.md",
                 "skills/system-discovery/references/workspace-mapping.md"):
        instructions += f"Instruction file {name}\n" + (SOURCE / name).read_text(encoding="utf-8") + "\n\n"
    if history:
        instructions += (
            "Earlier turns from this chat are context. Treat prior findings as claims "
            "and recheck relevant source before relying on them. Earlier host tool and skill claims "
            "apply only to the host that made them.\n"
            + json.dumps(history, ensure_ascii=False) + "\n\n"
        )
    prompt = instructions + (
        "For this turn, use the discovery skill and its status lines only when the "
        "latest message calls for inspecting the workspace. Answer general questions "
        "and questions about this conversation directly, without inspecting files "
        "or appending a discovery status. Attribute earlier replies to the host "
        "that wrote them when known.\n\nLatest user message:\n" + task
    )
    return run_read_only(host, executable, repo, prompt)


class DiscoveryUI(BaseHTTPRequestHandler):
    def permitted_host(self):
        return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

    def respond(self, status, body, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def json_response(self, status, data):
        self.respond(status, json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if not self.permitted_host():
            self.send_error(403)
            return
        if self.path == "/":
            self.respond(200, (SOURCE / "scripts/aegis1_ui.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/options":
            root = self.server.workspace_root
            folders = ["."] + sorted(path.name for path in root.iterdir()
                                     if not path.name.startswith(".") and not path.is_symlink() and path.is_dir())
            self.json_response(200, {"hosts": list(installed_hosts()), "folders": folders, "root": str(root)})
        else:
            self.send_error(404)

    def do_POST(self):
        origin = f"http://127.0.0.1:{self.server.server_port}"
        if (not self.permitted_host() or self.headers.get("Origin") != origin
                or self.headers.get_content_type() != "application/json"):
            self.send_error(403)
            return
        if self.path not in {"/run", "/source", "/folders", "/pick-folder"}:
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_REQUEST:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(length))
            root = self.server.workspace_root
            if self.path == "/pick-folder":
                if not FOLDER_DIALOG_LOCK.acquire(blocking=False):
                    self.json_response(409, {"error": "A folder picker is already open."})
                    return
                try:
                    selected = native_folder_dialog(root)
                except (OSError, subprocess.TimeoutExpired):
                    self.json_response(200, {"status": "unavailable"})
                    return
                finally:
                    FOLDER_DIALOG_LOCK.release()
                if selected is None:
                    self.json_response(200, {"status": "cancelled"})
                    return
                path = Path(selected).resolve(strict=True)
                if not path.is_relative_to(root) or not path.is_dir():
                    raise ValueError("Select a directory inside the configured workspace root.")
                self.json_response(200, {"status": "selected", "path": str(path)})
                return
            selection = payload["folder"]
            if not isinstance(selection, str) or not selection.strip():
                raise ValueError("Enter a workspace path.")
            repo = (root / Path(selection.strip()).expanduser()).resolve(strict=True)
            if not repo.is_relative_to(root) or not repo.is_dir():
                raise ValueError("Choose a directory inside the configured workspace root.")
            if self.path == "/folders":
                children = [
                    {"name": path.name, "path": path.relative_to(root).as_posix()}
                    for path in sorted(repo.iterdir(), key=lambda path: path.name.casefold())
                    if not path.name.startswith(".") and path.is_dir()
                    and path.resolve() == path
                ]
                self.json_response(200, {
                    "path": repo.relative_to(root).as_posix(),
                    "location": str(repo),
                    "parent": repo.parent.relative_to(root).as_posix() if repo != root else None,
                    "children": children,
                })
                return
            if self.path == "/source":
                name = Path(payload["path"])
                path = (repo / name).resolve(strict=True)
                if (name.is_absolute() or not path.is_relative_to(repo)
                        or any(part.startswith(".") for part in name.parts)
                        or not path.is_file()):
                    raise ValueError("Source is outside the visible workspace files.")
                line = int(payload.get("line") or 1)
                if not 1 <= line <= 100_000:
                    raise ValueError("Invalid source line.")
                with path.open("rb") as source:
                    lines = source.read(262145).decode("utf-8").splitlines()
                if line > len(lines):
                    raise ValueError("Source line is unavailable in the preview.")
                start = max(1, line - 8)
                self.json_response(200, {"path": name.as_posix(), "line": line, "start": start,
                                         "lines": lines[start - 1:line + 8]})
                return
            host = payload["host"]
            task = payload["task"].strip()
            if not task:
                raise ValueError("Choose a workspace folder and enter a discovery task.")
            greeting = " ".join(task.casefold().strip("!?. ").split())
            if greeting in {"hi", "hello", "hey", "hi there", "hello there", "hey there",
                            "good morning", "good afternoon", "good evening"}:
                self.json_response(200, {"report": "What would you like to find in this workspace?",
                                         "models": [], "started": False})
                return
            if greeting in {"provide your skills", "list your skills", "what are your skills",
                            "show your skills", "what can you do", "what skills do you have"}:
                self.json_response(200, {
                    "report": (
                        "### Aegis1 in this chat\n"
                        "The active skill is **system-discovery**. It can trace entry points, "
                        "dependencies, APIs, event flows, data stores, and configuration. "
                        "It cites source and identifies what still needs verification.\n\n"
                        "Other Aegis1 specialists are available in the project distribution: "
                        "requirements analysis, architecture analysis, implementation planning, "
                        "implementation, testing verification, code review, and debugging. "
                        "This browser chat runs read-only discovery.\n\n"
                        "Choose Claude Code or Codex to run a workspace question."
                    ),
                    "models": [], "started": False,
                })
                return
            executable = installed_hosts().get(host)
            if executable is None:
                raise ValueError("The selected host is unavailable.")
            previous = payload.get("history", [])
            if not isinstance(previous, list):
                raise ValueError("Invalid chat history.")
            history = [
                {"role": turn["role"], "text": turn["text"][:4000]}
                for turn in previous[-6:]
                if isinstance(turn, dict) and turn.get("role") in {"user", "assistant"}
                and isinstance(turn.get("text"), str)
            ]
            result = run_discovery(host, executable, repo, task, history)
        except subprocess.TimeoutExpired:
            self.json_response(504, {"error": "The host did not finish within three minutes."})
            return
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            self.json_response(400, {"error": str(error)})
            return
        self.json_response(200, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    root = args.workspace_root.resolve(strict=True)
    if not root.is_dir():
        parser.error("--workspace-root must be a directory")
    with ThreadingHTTPServer(("127.0.0.1", args.port), DiscoveryUI) as server:
        server.workspace_root = root
        print(f"Open http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
