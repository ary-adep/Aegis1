"""Manage local findings and explicitly transfer selected project records."""

import argparse
from contextlib import closing
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
import sqlite3
import sys
from uuid import NAMESPACE_URL, uuid4, uuid5


def fingerprint(project: Path, source: str) -> str:
    path = (project / source).resolve(strict=True)
    if Path(source).is_absolute() or not path.is_relative_to(project) or not path.is_file():
        raise ValueError("Source must be a file inside the project")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


PORTABLE_SCHEMA = 'aegis1.project-memory.v1'
MAX_BUNDLE_BYTES = 1024 * 1024


def save_records(store, project, records):
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
        imported = []
        for record_id, finding, pairs in records:
            # The first source stays in findings for older helpers.
            source, saved_hash = pairs[0]
            inserted = db.execute("INSERT OR IGNORE INTO findings VALUES (?, ?, ?, ?, ?)",
                                  (record_id, str(project), source, saved_hash, finding)).rowcount
            if inserted:
                db.executemany("INSERT INTO finding_sources VALUES (?, ?, ?)",
                               [(record_id, name, digest) for name, digest in pairs])
            imported.append(bool(inserted))
    return imported


def read_records(store, project):
    if not store.exists():
        return []
    with closing(sqlite3.connect(store.as_uri() + "?mode=ro", uri=True)) as db:
        db.execute("BEGIN")
        rows = db.execute("""SELECT id, source, fingerprint, finding FROM findings
            WHERE project = ? ORDER BY rowid DESC""", (str(project),)).fetchall()
        cited = {}
        if db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table'"
                      " AND name = 'finding_sources'").fetchone():
            for record_id, source, saved_hash in db.execute(
                    """SELECT s.finding_id, s.source, s.fingerprint FROM finding_sources s
                    JOIN findings f ON f.id = s.finding_id WHERE f.project = ?
                    ORDER BY s.rowid""", (str(project),)):
                cited.setdefault(record_id, []).append((source, saved_hash))
    return [(record_id, finding, cited.get(record_id, [(source, saved_hash)]))
            for record_id, source, saved_hash, finding in rows]


def sources_current(project, pairs):
    for source, expected in pairs:
        try:
            if fingerprint(project, source) != expected:
                return False
        except (OSError, RuntimeError, ValueError):
            return False
    return True


def portable_path(source):
    if not isinstance(source, str) or not source or any(c in source for c in ('\\', '\0')):
        raise ValueError("Expected a portable relative source path")
    path = PurePosixPath(source)
    if (path.is_absolute() or PureWindowsPath(source).drive or not path.parts
            or '..' in path.parts or path.as_posix() != source):
        raise ValueError("Expected a portable relative source path")
    return source


def validate_finding(finding):
    if not isinstance(finding, str) or not 0 < len(finding.strip()) <= 2000:
        raise ValueError("Finding must contain 1 to 2000 characters")
    return finding.strip()


def export_records(store, project, ids, destination):
    records = {record_id: (finding, pairs) for record_id, finding, pairs in read_records(store, project)}
    selected = []
    for record_id in dict.fromkeys(ids):
        if record_id not in records:
            raise ValueError("Requested finding is unavailable in this project")
        finding, pairs = records[record_id]
        sources = {}
        for path, digest in pairs:
            name = portable_path(Path(path).as_posix())
            if name in sources and sources[name] != digest:
                raise ValueError("Conflicting fingerprints for the same portable source")
            sources[name] = digest
        selected.append({'finding': finding, 'sources': [
            {'path': name, 'sha256': digest} for name, digest in sources.items()
        ]})
    payload = json.dumps({'schema': PORTABLE_SCHEMA, 'findings': selected}, indent=2) + '\n'
    encoded = payload.encode('utf-8')
    if len(encoded) > MAX_BUNDLE_BYTES:
        raise ValueError("Selected bundle exceeds the size limit")
    with open(destination, 'xb', opener=lambda name, flags: os.open(name, flags, 0o600)) as output:
        output.write(encoded)
    return {'exported': len(selected)}


def import_records(store, project, bundle):
    if not bundle.is_file():
        raise ValueError("Expected a bundle file")
    with bundle.open('rb') as source:
        content = source.read(MAX_BUNDLE_BYTES + 1)
    if len(content) > MAX_BUNDLE_BYTES:
        raise ValueError("Bundle exceeds the size limit")
    document = json.loads(content)
    if not isinstance(document, dict) or document.get('schema') != PORTABLE_SCHEMA:
        raise ValueError("Unsupported memory bundle schema")
    findings = document.get('findings')
    if not isinstance(findings, list) or not findings:
        raise ValueError("Expected a nonempty list of findings")
    pending = []
    for entry in findings:
        if not isinstance(entry, dict):
            raise ValueError("Expected a finding object")
        finding = validate_finding(entry.get('finding'))
        sources = entry.get('sources')
        if not isinstance(sources, list) or not sources:
            raise ValueError("Each finding must have cited sources")
        pairs = {}
        for source in sources:
            if not isinstance(source, dict):
                raise ValueError("Expected a source object")
            name = portable_path(source.get('path'))
            digest = source.get('sha256')
            if name in pairs or not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
                raise ValueError("Invalid or duplicate source fingerprint")
            if not (project / name).resolve().is_relative_to(project):
                raise ValueError("Source resolves outside the destination project")
            pairs[name] = digest
        content_key = json.dumps([str(project), finding, sorted(pairs.items())], separators=(',', ':'))
        record_id = uuid5(NAMESPACE_URL, 'aegis1:memory:' + content_key).hex
        pending.append((record_id, finding, list(pairs.items())))
    stale = {record_id: not sources_current(project, pairs) for record_id, _, pairs in pending}
    inserted = save_records(store, project, pending)
    return {
        'imported': sum(inserted), 'already_present': len(inserted) - sum(inserted),
        'findings': [{'id': record_id, 'stale': is_stale} for record_id, is_stale in stale.items()],
    }


def read_lesson_rows(store, project):
    if not store.exists():
        return []
    with closing(sqlite3.connect(store.as_uri() + "?mode=ro", uri=True)) as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'lessons'").fetchone():
            return []
        return db.execute("""SELECT l.id, l.finding_id, l.lesson, l.status, l.reviewed_by, l.reviewed_at
            FROM lessons l JOIN findings f ON f.id = l.finding_id
            WHERE f.project = ? ORDER BY l.rowid DESC""", (str(project),)).fetchall()


def task_terms(value):
    return set(re.findall(r"[^\W_]{3,}", value.casefold())) - {
        "and", "for", "from", "the", "this", "with", "when", "what", "how", "can",
    }


def preview_context(store, project, args):
    if not 256 <= args.max_bytes <= 32768:
        raise ValueError("--max-bytes must be between 256 and 32768")
    if not 1 <= args.max_lessons <= 20:
        raise ValueError("--max-lessons must be between 1 and 20")
    terms = task_terms(args.task)
    candidates = []
    for lesson_id, finding_id, lesson, status, _, _ in read_lesson_rows(store, project):
        if status == "approved" and (matched := sorted(terms & task_terms(lesson))):
            candidates.append((lesson_id, finding_id, lesson, matched))
    candidates.sort(key=lambda item: -len(item[3]))

    records = {record_id: pairs for record_id, _, pairs in read_records(store, project)} if candidates else {}
    selected = []
    used_bytes = len(b"[]\n")
    for lesson_id, finding_id, lesson, matched in candidates:
        pairs = records.get(finding_id)
        if not pairs:
            continue
        entry = {"id": lesson_id, "lesson": lesson, "matched_terms": matched,
                 "sources": [source for source, _ in pairs]}
        encoded = json.dumps(entry, separators=(",", ":")).encode("ascii")
        entry_bytes = len(encoded) + bool(selected)
        if used_bytes + entry_bytes <= args.max_bytes and sources_current(project, pairs):
            selected.append(encoded)
            used_bytes += entry_bytes
            if len(selected) == args.max_lessons:
                break
    return b"[" + b",".join(selected) + b"]\n"


def learn(store, project, args):
    records = {record_id: pairs for record_id, _, pairs in read_records(store, project)}
    if args.command == "propose-lesson":
        pairs = records.get(args.finding_id)
        if not pairs or not sources_current(project, pairs):
            raise ValueError("Lesson requires a current finding in this project")
        lesson = validate_finding(args.lesson)
        proposal = uuid4().hex
        with closing(sqlite3.connect(store)) as db, db:
            db.execute("""CREATE TABLE IF NOT EXISTS lessons (
                id TEXT PRIMARY KEY, finding_id TEXT NOT NULL, lesson TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'rejected')),
                reviewed_by TEXT, reviewed_at TEXT
            )""")
            db.execute("""CREATE TRIGGER IF NOT EXISTS delete_finding_lessons
                AFTER DELETE ON findings BEGIN
                    DELETE FROM lessons WHERE finding_id = OLD.id;
                END""")
            inserted = db.execute("""INSERT INTO lessons (id, finding_id, lesson, status)
                SELECT ?, id, ?, 'pending' FROM findings WHERE project = ? AND id = ?""",
                                  (proposal, lesson, str(project), args.finding_id)).rowcount
            if not inserted:
                raise ValueError("Finding is unavailable in this project")
        return {"id": proposal, "status": "pending"}

    entries = [
        {"id": lesson_id, "finding_id": finding_id, "lesson": lesson, "status": status,
         "reviewed_by": reviewer, "reviewed_at": reviewed_at,
         "stale": not sources_current(project, records[finding_id])}
        for lesson_id, finding_id, lesson, status, reviewer, reviewed_at in read_lesson_rows(store, project)
        if finding_id in records
    ]
    if args.command == "list-lessons":
        return entries
    if args.command == "recall-lessons":
        return [entry for entry in entries if entry['status'] == 'approved' and not entry['stale']]

    entry = next((entry for entry in entries if entry['id'] == args.id), None)
    if entry is None or entry['status'] != 'pending':
        raise ValueError("No pending lesson with this ID in the project")
    if args.decision == "approve" and entry['stale']:
        raise ValueError("Cannot approve a lesson backed by stale evidence")
    reviewer = validate_finding(args.by)
    status = {'approve': 'approved', 'reject': 'rejected'}[args.decision]
    with closing(sqlite3.connect(store)) as db, db:
        updated = db.execute("""UPDATE lessons SET status = ?, reviewed_by = ?, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'pending' AND finding_id IN (SELECT id FROM findings WHERE project = ?)""",
                             (status, reviewer, args.id, str(project))).rowcount
        if not updated:
            raise ValueError("Lesson is no longer pending in this project")
    return {"id": args.id, "status": status, "reviewed_by": reviewer}


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
    export = commands.add_parser("export")
    export.add_argument("--id", required=True, action="append", help="finding to export; repeat to select several")
    export.add_argument("--output", required=True, type=Path)
    transfer = commands.add_parser("import")
    transfer.add_argument("bundle", type=Path)
    proposal = commands.add_parser("propose-lesson")
    proposal.add_argument("--finding-id", required=True)
    proposal.add_argument("--lesson", required=True)
    review = commands.add_parser("review-lesson")
    review.add_argument("id")
    review.add_argument("--decision", choices=("approve", "reject"), required=True)
    review.add_argument("--by", required=True)
    commands.add_parser("list-lessons")
    commands.add_parser("recall-lessons")
    preview = commands.add_parser("preview-context", help="show relevant approved lessons for review")
    preview.add_argument("--task", required=True)
    preview.add_argument("--max-bytes", type=int, default=2400)
    preview.add_argument("--max-lessons", type=int, default=3)
    args = parser.parse_args()

    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError("Project must be an existing directory")
        store = Path.home() / ".aegis1" / "memory.sqlite3"
        if args.command == "preview-context":
            sys.stdout.buffer.write(preview_context(store, project, args))
            return 0
        if args.command == "save":
            finding = validate_finding(args.finding)
            sources = list(dict.fromkeys(args.source))
            pairs = [(source, fingerprint(project, source)) for source in sources]
            record_id = uuid4().hex
            save_records(store, project, [(record_id, finding, pairs)])
            result = {"saved": record_id}
        elif args.command == "export":
            result = export_records(store, project, args.id, args.output)
        elif args.command == "import":
            result = import_records(store, project, args.bundle)
        elif args.command in ("propose-lesson", "review-lesson", "list-lessons", "recall-lessons"):
            result = learn(store, project, args)
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
            result = [
                {"id": record_id, "source": pairs[0][0], "sources": [source for source, _ in pairs],
                 "finding": finding, "stale": not sources_current(project, pairs)}
                for record_id, finding, pairs in read_records(store, project)
            ]
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        parser.exit(1, f"Local memory unavailable: {error}\n")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
