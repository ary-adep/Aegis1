"""Install Aegis1 into a Claude Code project or personal configuration."""

import argparse
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
SKILLS = (
    "aegis", "architecture-analysis", "code-review", "debugging",
    "implementation", "implementation-planning", "requirements-analysis",
    "system-discovery", "testing-verification",
)


def install(target: Path) -> int:
    paths = [Path("agents/aegis1.md")]
    for skill in SKILLS:
        folder = SOURCE / "skills" / skill
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {folder}")
        paths.extend(
            path.relative_to(SOURCE) for path in sorted(folder.rglob("*.md"))
            if path.is_file()
        )

    pending = {}
    for relative in paths:
        source = SOURCE / relative
        destination = target / relative
        if source.resolve() != source or destination.resolve() != destination:
            raise ValueError(f"Redirected install path: {relative}")
        content = source.read_bytes()
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != content:
                raise ValueError(f"Existing file differs: {destination}")
        else:
            pending[destination] = content

    created = []
    try:
        for destination, content in pending.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as output:
                created.append(destination)
                output.write(content)
    except OSError:
        for destination in reversed(created):
            destination.unlink(missing_ok=True)
        raise
    return len(created)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Existing project directory")
    scope.add_argument("--personal", action="store_true", help="Install under your home directory")
    args = parser.parse_args()

    try:
        root = (Path.home() if args.personal else args.project).resolve(strict=True)
        if not root.is_dir():
            raise ValueError(f"Expected a directory: {root}")
        target = root / ".claude"
        count = install(target)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Installation stopped: {error}\n")

    print(f"Installed {count} new files in {target}. Restart Claude Code and run /aegis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
