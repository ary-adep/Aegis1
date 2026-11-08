"""Save, recall, and delete local Aegis1 findings scoped to one checkout."""

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
from uuid import uuid4


def fingerprint(project: Path, source: str) -> str:
    path = (project / source).resolve(strict=True)
    if Path(source).is_absolute() or not path.is_relative_to(project) or not path.is_file():
        raise ValueError("Source must be a file inside the project")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    save = commands.add_parser("save")
    save.add_argument("--source", required=True)
    save.add_argument("--finding", required=True)
    commands.add_parser("recall")
    delete = commands.add_parser("delete")
    delete.add_argument("id")
    args = parser.parse_args()

    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError("Project must be an existing directory")
        store = Path.home() / ".aegis1" / "memory.sqlite3"
        if args.command == "save":
            finding = args.finding.strip()
            if not 0 < len(finding) <= 2000:
                raise ValueError("Finding must contain 1 to 2000 characters")
            source_hash = fingerprint(project, args.source)
            record_id = uuid4().hex
            store.parent.mkdir(mode=0o700, exist_ok=True)
            with closing(sqlite3.connect(store)) as db, db:
                db.execute("""CREATE TABLE IF NOT EXISTS findings (
                    id TEXT PRIMARY KEY, project TEXT NOT NULL, source TEXT NOT NULL,
                    fingerprint TEXT NOT NULL, finding TEXT NOT NULL
                )""")
                db.execute("INSERT INTO findings VALUES (?, ?, ?, ?, ?)",
                           (record_id, str(project), args.source, source_hash, finding))
            result = {"saved": record_id}
        elif not store.exists():
            result = [] if args.command == "recall" else {"deleted": False}
        elif args.command == "delete":
            with closing(sqlite3.connect(store)) as db, db:
                deleted = db.execute("DELETE FROM findings WHERE project = ? AND id = ?",
                                     (str(project), args.id)).rowcount
            result = {"deleted": bool(deleted)}
        else:
            with closing(sqlite3.connect(store.as_uri() + "?mode=ro", uri=True)) as db:
                rows = db.execute("""SELECT id, source, fingerprint, finding FROM findings
                    WHERE project = ? ORDER BY rowid DESC""", (str(project),)).fetchall()
            result = []
            for record_id, source, saved_hash, finding in rows:
                try:
                    stale = fingerprint(project, source) != saved_hash
                except (OSError, RuntimeError, ValueError):
                    stale = True
                result.append({"id": record_id, "source": source, "finding": finding, "stale": stale})
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        parser.exit(1, f"Local memory unavailable: {error}\n")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
