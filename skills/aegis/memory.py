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
    save.add_argument("--source", required=True, action="append",
                      help="file the finding cites; repeat to cite several files")
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
            sources = list(dict.fromkeys(args.source))
            hashes = [fingerprint(project, source) for source in sources]
            record_id = uuid4().hex
            store.parent.mkdir(mode=0o700, exist_ok=True)
            with closing(sqlite3.connect(store)) as db, db:
                db.execute("""CREATE TABLE IF NOT EXISTS findings (
                    id TEXT PRIMARY KEY, project TEXT NOT NULL, source TEXT NOT NULL,
                    fingerprint TEXT NOT NULL, finding TEXT NOT NULL
                )""")
                db.execute("""CREATE TABLE IF NOT EXISTS finding_sources (
                    finding_id TEXT NOT NULL, source TEXT NOT NULL, fingerprint TEXT NOT NULL,
                    PRIMARY KEY (finding_id, source)
                )""")
                db.execute("""CREATE TRIGGER IF NOT EXISTS delete_finding_sources
                    AFTER DELETE ON findings BEGIN
                        DELETE FROM finding_sources WHERE finding_id = OLD.id;
                    END""")
                # The first source stays in findings so records remain readable by older helpers.
                db.execute("INSERT INTO findings VALUES (?, ?, ?, ?, ?)",
                           (record_id, str(project), sources[0], hashes[0], finding))
                db.executemany("INSERT INTO finding_sources VALUES (?, ?, ?)",
                               [(record_id, s, h) for s, h in zip(sources, hashes)])
            result = {"saved": record_id}
        elif not store.exists():
            result = [] if args.command == "recall" else {"deleted": False}
        elif args.command == "delete":
            with closing(sqlite3.connect(store)) as db, db:
                deleted = db.execute("DELETE FROM findings WHERE project = ? AND id = ?",
                                     (str(project), args.id)).rowcount
                if deleted and db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table'"
                                          " AND name = 'finding_sources'").fetchone():
                    db.execute("DELETE FROM finding_sources WHERE finding_id = ?", (args.id,))
            result = {"deleted": bool(deleted)}
        else:
            with closing(sqlite3.connect(store.as_uri() + "?mode=ro", uri=True)) as db:
                db.execute("BEGIN")
                rows = db.execute("""SELECT id, source, fingerprint, finding FROM findings
                    WHERE project = ? ORDER BY rowid DESC""", (str(project),)).fetchall()
                cited = {}
                if db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table'"
                              " AND name = 'finding_sources'").fetchone():
                    for finding_id, source, saved_hash in db.execute(
                            """SELECT s.finding_id, s.source, s.fingerprint FROM finding_sources s
                            JOIN findings f ON f.id = s.finding_id WHERE f.project = ?
                            ORDER BY s.rowid""", (str(project),)):
                        cited.setdefault(finding_id, []).append((source, saved_hash))
            result = []
            for record_id, source, saved_hash, finding in rows:
                stale = False
                pairs = cited.get(record_id, [(source, saved_hash)])
                for cited_source, cited_hash in pairs:
                    try:
                        stale = stale or fingerprint(project, cited_source) != cited_hash
                    except (OSError, RuntimeError, ValueError):
                        stale = True
                result.append({"id": record_id, "source": pairs[0][0],
                               "sources": [s for s, _ in pairs], "finding": finding, "stale": stale})
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        parser.exit(1, f"Local memory unavailable: {error}\n")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
