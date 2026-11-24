"""Install Aegis1 into a Claude Code project or personal configuration."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
import os
import sys
from pathlib import Path
from shutil import copy2
from tempfile import NamedTemporaryFile, mkdtemp

from scripts.aegis1_hosts import installed_hosts

INSTALL_VERSION = "0.2.6"
SOURCE = Path(__file__).resolve().parent
SKILLS = (
    "aegis", "architecture-analysis", "code-review", "debugging",
    "implementation", "implementation-planning", "requirements-analysis",
    "system-discovery", "testing-verification",
)


def replace_file(destination: Path, content: bytes) -> None:
    with NamedTemporaryFile(dir=destination.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(content)
            output.close()
            temporary.replace(destination)
        finally:
            output.close()
            temporary.unlink(missing_ok=True)


@dataclass
class InstallPlan:
    manifest: Path
    prior_manifest: bytes | None
    next_manifest: bytes
    pending: dict
    replacements: dict
    conflicts: list
    unchanged: list


def plan_install(target: Path, previous: Path = None, relocated=()) -> InstallPlan:
    paths = [Path("agents/aegis1.md"), Path("agents/aegis1-scout.md"),
             Path("agents/aegis1-verifier.md"), Path("skills/aegis/memory.py"),
             Path("skills/aegis/claude_models.py"), Path("skills/aegis/sdd.py")]
    for skill in SKILLS:
        folder = SOURCE / "skills" / skill
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {folder}")
        paths.extend(
            path.relative_to(SOURCE) for path in sorted(folder.rglob("*.md"))
            if path.is_file()
        )

    manifest = target / ".aegis1-install.json"
    if manifest.resolve() != manifest:
        raise ValueError(f"Redirected install path: {manifest}")
    recorded = {}
    prior_manifest = manifest.read_bytes() if manifest.exists() else None
    if prior_manifest is not None:
        state = json.loads(prior_manifest)
        if (not isinstance(state, dict) or state.get("schema") != 1
                or not isinstance(state.get("files"), dict)
                or not isinstance(state.get("version"), str)):
            raise ValueError(f"Invalid installer manifest: {manifest}")
        installed_version = tuple(int(part) for part in state["version"].split("."))
        if installed_version > tuple(int(part) for part in INSTALL_VERSION.split(".")):
            raise ValueError(f"Installed version {state['version']} is newer than {INSTALL_VERSION}")
        recorded = state["files"]

    legacy = {}
    if prior_manifest is None:
        legacy = json.loads((SOURCE / "legacy-install-fingerprints.json").read_text(
            encoding="utf-8"))["files"]

    fingerprints = {}
    pending = {}
    replacements = {}
    conflicts = []
    unchanged = []
    for relative in paths:
        source = SOURCE / relative
        destination = target / relative
        will_move = any(destination.is_relative_to(entry) for entry in relocated)
        if source.resolve() != source or (not will_move and destination.resolve() != destination):
            raise ValueError(f"Redirected install path: {relative}")
        content = source.read_bytes()
        key = relative.as_posix()
        fingerprints[key] = sha256(content).hexdigest()
        if will_move or not destination.exists():
            pending[destination] = content
            continue
        if not destination.is_file():
            raise ValueError(f"Expected a file: {destination}")
        installed = destination.read_bytes()
        if installed == content:
            unchanged.append(destination)
            continue
        original = previous / relative if previous is not None else None
        if key in recorded:
            matches_previous = recorded[key] == sha256(installed).hexdigest()
        else:
            matches_previous = (
                legacy.get(key) == sha256(installed.replace(b"\r\n", b"\n")).hexdigest()
                or (original is not None and original.resolve() == original and original.is_file()
                    and original.read_bytes().replace(b"\r\n", b"\n") == installed.replace(b"\r\n", b"\n"))
            )
        if not matches_previous:
            conflicts.append(destination)
        replacements[destination] = (installed, content)

    next_manifest = (json.dumps({"schema": 1, "version": INSTALL_VERSION, "files": fingerprints},
                                indent=2, sort_keys=True) + "\n").encode("utf-8")
    return InstallPlan(manifest, prior_manifest, next_manifest, pending, replacements, conflicts, unchanged)


def install(target: Path, previous: Path = None) -> tuple[int, int]:
    plan = plan_install(target, previous)
    manifest, prior_manifest = plan.manifest, plan.prior_manifest
    pending, replacements, conflicts = plan.pending, plan.replacements, plan.conflicts
    if conflicts:
        paths = "\n".join(str(path) for path in conflicts)
        if prior_manifest is not None or not sys.stdin.isatty():
            raise ValueError(f"Existing files differ from the expected version:\n{paths}")
        print(f"These unversioned Aegis1 files differ from the installer:\n{paths}")
        try:
            answer = input("Back up these files and install the new Aegis1 copies? [y/N] ")
        except EOFError:
            answer = ""
        if answer.strip().lower() not in {"y", "yes"}:
            raise ValueError("Upgrade declined. Existing files were kept.")

    backup = None
    if replacements:
        backup_root = Path.home() / ".aegis1" / "install-backups"
        backup_root.mkdir(parents=True, mode=0o700, exist_ok=True)
        backup = Path(mkdtemp(prefix="upgrade-", dir=backup_root))
        for destination, (installed, _) in replacements.items():
            saved = backup / destination.relative_to(target)
            saved.parent.mkdir(parents=True, exist_ok=True)
            copy2(destination, saved)
            if saved.read_bytes() != installed:
                raise ValueError(f"Installed file changed during backup: {destination}")
        if prior_manifest is not None:
            (backup / manifest.name).write_bytes(prior_manifest)
        print(f"Backed up replaced files to {backup}", flush=True)

    created = []
    replaced = []
    try:
        for destination, content in pending.items():
            if destination.resolve() != destination:
                raise ValueError(f"Redirected install path: {destination}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as output:
                created.append(destination)
                output.write(content)
        for destination, (installed, content) in replacements.items():
            if destination.resolve() != destination or destination.read_bytes() != installed:
                raise ValueError(f"Installed file changed during upgrade: {destination}")
            replace_file(destination, content)
            replaced.append(destination)
        next_manifest = plan.next_manifest
        if next_manifest != prior_manifest:
            current_manifest = manifest.read_bytes() if manifest.exists() else None
            if manifest.resolve() != manifest or current_manifest != prior_manifest:
                raise ValueError(f"Installer manifest changed during upgrade: {manifest}")
            replace_file(manifest, next_manifest)
    except (OSError, ValueError):
        for destination in reversed(replaced):
            replace_file(destination, (backup / destination.relative_to(target)).read_bytes())
        for destination in reversed(created):
            destination.unlink(missing_ok=True)
        raise
    return len(created), len(replaced)


def legacy_links(target: Path, previous: Path = None) -> list[Path]:
    for parent in (target, target / "agents", target / "skills"):
        if parent.resolve() != parent:
            raise ValueError(f"Redirected configuration directory: {parent}")

    entries = [target / "agents/aegis1.md"]
    entries.extend(target / "skills" / skill for skill in SKILLS)
    linked = [entry for entry in entries if entry.is_symlink() or entry.resolve() != entry]
    if not linked:
        return []

    if (target / ".aegis1-install.json").exists():
        raise ValueError("Found linked files in an already versioned installation")
    legacy = json.loads((SOURCE / "legacy-install-fingerprints.json").read_text(
        encoding="utf-8"))["files"]
    for entry in linked:
        resolved = entry.resolve(strict=True)
        relative = entry.relative_to(target)
        if resolved.is_dir() and relative.parts[0] == "skills":
            files = [path for path in resolved.rglob("*") if not path.is_dir() or path.is_symlink()]
            if not (resolved / "SKILL.md").is_file():
                raise ValueError(f"Missing legacy skill: {entry}")
            candidates = [(path, relative / path.relative_to(resolved)) for path in files]
        elif resolved.is_file() and relative.parts[0] == "agents":
            candidates = [(resolved, relative)]
        else:
            raise ValueError(f"Unexpected legacy link: {entry}")
        for path, name in candidates:
            if path.resolve() != path or not path.is_file():
                raise ValueError(f"Unexpected entry in legacy link: {path}")
            content = path.read_bytes().replace(b"\r\n", b"\n")
            known = legacy.get(name.as_posix()) == sha256(content).hexdigest()
            if not known:
                for checkout in (SOURCE, previous):
                    original = checkout / name if checkout is not None else None
                    if original is not None and original.is_file():
                        if original.read_bytes().replace(b"\r\n", b"\n") == content:
                            known = True
                            break
            if not known:
                raise ValueError(f"Unrecognized or customized legacy file: {path}")

    backup_root = target / ".aegis1-link-backups"
    if backup_root.resolve() != backup_root:
        raise ValueError(f"Redirected backup directory: {backup_root}")
    return linked


def migrate_install(target: Path, previous: Path = None) -> tuple[int, int]:
    """Move recognized legacy link entries aside before copying independent files."""
    linked = legacy_links(target, previous)
    if not linked:
        return install(target, previous)
    backup_root = target / ".aegis1-link-backups"
    backup_root.mkdir(mode=0o700, exist_ok=True)
    backup = Path(mkdtemp(prefix="migration-", dir=backup_root))
    moved = []
    try:
        for entry in linked:
            saved = backup / entry.relative_to(target)
            saved.parent.mkdir(parents=True, exist_ok=True)
            entry.rename(saved)
            moved.append((entry, saved))
        result = install(target, previous)
    except (OSError, ValueError, RuntimeError):
        for entry, saved in reversed(moved):
            if entry.is_dir():
                for directory in sorted(entry.rglob("*"), key=lambda path: len(path.parts), reverse=True):
                    if directory.is_dir():
                        directory.rmdir()
                entry.rmdir()
            saved.rename(entry)
        raise
    print(f"Backed up legacy link entries to {backup}")
    return result


def preview(host, root, personal, previous):
    target = root / ('.claude' if host == 'claude' else '.codex')
    if host == 'codex' and personal:
        target = Path(os.environ.get('CODEX_HOME') or target).expanduser().absolute()
    config_names = (
        ('settings.json', 'settings.local.json', 'hooks', 'agents', 'skills')
        if host == 'claude' else ('config.toml', 'hooks.json', 'rules', 'agents', 'skills')
    )
    result = {
        'host': host,
        'scope': 'personal' if personal else 'project',
        'target': str(target),
        'executable_found': host in installed_hosts(),
        'existing_configuration': [
            name for name in config_names
            if (target / name).exists() or (target / name).is_symlink()
        ],
        'settings_or_hooks_written': False,
    }
    if host == 'codex':
        result.update(status='inventory_only', install_supported=False,
                      capabilities=['Standalone read-only discovery through the Codex CLI',
                                    'Host-neutral SDD commands from the Aegis1 checkout'])
        return result
    links = legacy_links(target, previous)
    plan = plan_install(target, previous, relocated=links)
    conflicts = set(plan.conflicts)
    status = 'ready'
    if conflicts:
        status = 'blocked' if plan.prior_manifest is not None else 'interactive_approval_required'

    def paths(entries):
        return sorted(entry.relative_to(target).as_posix() for entry in entries)

    result.update(status=status, install_supported=True,
                  capabilities=['Project or personal skill and agent installation',
                                'Standalone read-only discovery through Claude Code'],
                  add=paths(plan.pending), update=paths(plan.replacements.keys() - conflicts),
                  unchanged=paths(plan.unchanged), conflicts=paths(conflicts),
                  backup_legacy_links=paths(links),
                  manifest_update_needed=plan.next_manifest != plan.prior_manifest)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"Aegis1 installer {INSTALL_VERSION}")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Existing project directory")
    scope.add_argument("--personal", action="store_true", help="Install under your home directory")
    parser.add_argument("--plan", action="store_true", help="Print a read-only JSON preview")
    parser.add_argument("--host", choices=("claude", "codex"), default="claude",
                        help="Host to inspect; Codex is inventory-only")
    parser.add_argument("--upgrade-from", type=Path, help="Checkout matching the installed version")
    args = parser.parse_args()
    if args.host == "codex" and not args.plan:
        parser.error("Codex is supported for --plan inventory only")
    if args.host == "codex" and args.upgrade_from is not None:
        parser.error("--upgrade-from applies to Claude Code installations")

    try:
        root = (Path.home() if args.personal else args.project).resolve(strict=True)
        if not root.is_dir():
            raise ValueError(f"Expected a directory: {root}")
        target = root / ".claude"
        previous = args.upgrade_from.resolve(strict=True) if args.upgrade_from else None
        if previous is not None and not (previous / "agents/aegis1.md").is_file():
            raise ValueError("--upgrade-from must point to a prior Aegis1 checkout")
        if args.plan:
            print(json.dumps(preview(args.host, root, args.personal, previous), indent=2))
            return 0
        added, updated = migrate_install(target, previous)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Installation stopped: {error}\n")

    print(f"Aegis1 {INSTALL_VERSION}: installed {added} new and updated {updated} files in {target}. Restart Claude Code and run /aegis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
