"""Summarize token counters from one explicitly supplied host JSONL log.

Claude message deduplication and cache accounting are adapted from ECC 2.2.3
scripts/hooks/cost-tracker.js at 4adeee6732a12d1540f49a4d50a38ce8c97f9a53.
Copyright (c) 2026 Affaan Mustafa. See docs/ecc/LICENSE-ECC.
"""

import json

FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'cache_write_input_tokens')
MAX_RECORD_BYTES = 16 * 1024 * 1024


def counter(usage, key):
    value = usage.get(key)
    return value if type(value) is int and value >= 0 else None


def normalize(host, usage):
    usage = usage if isinstance(usage, dict) else {}
    total = counter(usage, 'input_tokens')
    read = counter(usage, 'cached_input_tokens')
    written = counter(usage, 'cache_write_input_tokens')
    if host == 'claude':
        read = counter(usage, 'cache_read_input_tokens')
        written = counter(usage, 'cache_creation_input_tokens')
        parts = (total, read, written)
        total = sum(parts) if None not in parts else None
    elif total is not None and read is not None and read > total:
        read = None
    return dict(zip(FIELDS, (total, read, counter(usage, 'output_tokens'), written)))


def summarize_usage(path, host):
    if not path.is_file():
        raise ValueError('usage input must be a regular JSONL file')
    records = {}
    issues = set()
    open_turns = 0
    threads = 0
    with path.open('rb') as stream:
        for number, raw in enumerate(iter(lambda: stream.readline(MAX_RECORD_BYTES + 1), b''), 1):
            if len(raw) > MAX_RECORD_BYTES:
                raise ValueError(f'usage JSONL line {number} exceeds the size limit')
            if not raw.strip():
                continue
            try:
                event = json.loads(raw)
            except (ValueError, UnicodeError):
                issues.add('Malformed JSONL makes overall totals unknown.')
                continue
            if not isinstance(event, dict):
                issues.add('Malformed JSONL makes overall totals unknown.')
                continue
            kind = event.get('type')
            if host == 'claude' and kind == 'assistant':
                message = event.get('message')
                key = message.get('id') if isinstance(message, dict) else None
                if not isinstance(key, str) or not key:
                    issues.add('Claude assistant records without a message ID cannot be deduplicated.')
                    continue
                usage = message.get('usage')
                if isinstance(usage, dict) or key not in records:
                    records[key] = normalize(host, usage)
            elif host == 'codex':
                if kind == 'thread.started':
                    threads += 1
                elif kind == 'turn.started':
                    open_turns += 1
                elif kind in ('turn.completed', 'turn.failed'):
                    open_turns = max(0, open_turns - 1)
                    if kind == 'turn.failed':
                        issues.add('A failed Codex turn may include unreported usage.')
                    else:
                        records[number] = normalize(host, event.get('usage'))
    if host == 'codex' and open_turns:
        issues.add('A started Codex turn has no terminal record.')
    if threads > 1:
        issues.add('Expected a single Codex thread rather than concatenated logs.')
    totals = {}
    for field in FIELDS:
        values = [record[field] for record in records.values()]
        totals[field] = sum(values) if values and None not in values and not issues else None
    notes = sorted(issues)
    if not records:
        notes.append('No supported usage records found.')
    missing = [field for field, total in totals.items() if total is None]
    if missing:
        notes.append('Unavailable totals: ' + ', '.join(missing) + '.')
    notes.append('Counts cover only the supplied log and may omit separate subagent or failed calls.')
    return {'host': host, 'usage': {field: totals[field] for field in FIELDS[:3]},
            'cache_write_input_tokens': totals[FIELDS[3]], 'usage_records': len(records),
            'usage_notes': ' '.join(notes)}
