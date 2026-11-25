"""Report token usage from an explicitly selected Claude Code or Codex log."""

import json

INPUT = 'input_tokens'
CACHED = 'cached_input_tokens'
OUTPUT = 'output_tokens'
WRITTEN = 'cache_write_input_tokens'
COUNTERS = (INPUT, CACHED, OUTPUT, WRITTEN)
MAX_RECORD_BYTES = 16 * 1024 * 1024


def _events(path, issues):
    if not path.is_file():
        raise ValueError('usage input must be a regular JSONL file')
    with path.open('rb') as log:
        for line_number, line in enumerate(iter(lambda: log.readline(MAX_RECORD_BYTES + 1), b''), start=1):
            if len(line) > MAX_RECORD_BYTES:
                raise ValueError(f'usage JSONL line {line_number} exceeds the size limit')
            if not line.strip():
                continue
            try:
                event = json.loads(line.decode('utf-8'))
            except (ValueError, RecursionError):
                event = None
            if isinstance(event, dict):
                yield event
            else:
                issues.add('Malformed JSONL makes overall totals unknown.')


def _claude_reports(events, issues):
    by_message = {}
    for event in events:
        if event.get('type') != 'assistant':
            continue
        message = event.get('message')
        message_id = message.get('id') if isinstance(message, dict) else None
        if not isinstance(message_id, str) or not message_id:
            issues.add('Claude assistant records without a message ID cannot be deduplicated.')
            continue
        usage = message.get('usage')
        if isinstance(usage, dict):
            by_message[message_id] = usage
        else:
            by_message.setdefault(message_id, {})
    return by_message.values()


def _codex_reports(events, issues):
    pending = 0
    threads = 0
    for event in events:
        kind = event.get('type')
        if kind == 'thread.started':
            threads += 1
        elif kind == 'turn.started':
            pending += 1
        elif kind in ('turn.completed', 'turn.failed'):
            pending = max(0, pending - 1)
            if kind == 'turn.completed':
                usage = event.get('usage')
                yield usage if isinstance(usage, dict) else {}
            else:
                issues.add('A failed Codex turn may include unreported usage.')
    if pending:
        issues.add('A started Codex turn has no terminal record.')
    if threads > 1:
        issues.add('Expected a single Codex thread rather than concatenated logs.')


def _count(report, key):
    value = report.get(key)
    return value if type(value) is int and value >= 0 else None


def _counts(report, host):
    counts = {key: _count(report, key) for key in COUNTERS}
    if host == 'claude':
        counts[CACHED] = _count(report, 'cache_read_input_tokens')
        counts[WRITTEN] = _count(report, 'cache_creation_input_tokens')
        parts = (counts[INPUT], counts[CACHED], counts[WRITTEN])
        counts[INPUT] = sum(parts) if None not in parts else None
    elif counts[INPUT] is not None and counts[CACHED] is not None and counts[CACHED] > counts[INPUT]:
        counts[CACHED] = None
    return counts


def summarize_usage(path, host):
    issues = set()
    events = _events(path, issues)
    collect = _claude_reports if host == 'claude' else _codex_reports
    totals = dict.fromkeys(COUNTERS, 0)
    unavailable = set()
    records = 0
    for report in collect(events, issues):
        records += 1
        for key, value in _counts(report, host).items():
            if value is None:
                unavailable.add(key)
            else:
                totals[key] += value
    if issues or not records:
        unavailable.update(COUNTERS)
    notes = sorted(issues)
    if not records:
        notes.append('No supported usage records found.')
    if unavailable:
        missing = [key for key in COUNTERS if key in unavailable]
        notes.append('Unavailable totals: ' + ', '.join(missing) + '.')
        for key in missing:
            totals[key] = None
    notes.append('Counts cover only the supplied log and may omit separate subagent or failed calls.')
    return {
        'host': host,
        'usage': {key: totals[key] for key in (INPUT, CACHED, OUTPUT)},
        WRITTEN: totals[WRITTEN],
        'usage_records': records,
        'usage_notes': ' '.join(notes),
    }
