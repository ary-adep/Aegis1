"""Inspect explicitly named Claude Code or Codex project configuration files."""

import argparse
import json
from pathlib import Path
import sys

try:
    import tomllib
except ImportError:
    tomllib = None


FILES = {
    'claude': {'.claude/settings.json', '.claude/settings.local.json', '.mcp.json', '.claude/mcp.json'},
    'codex': {'.codex/config.toml', '.codex/hooks.json'},
}
MAX_BYTES = 1024 * 1024


def unique_object(pairs):
    document = {}
    for key, value in pairs:
        if key in document:
            raise ValueError('duplicate JSON key')
        document[key] = value
    return document


def declarations(host, document):
    if host == 'claude':
        if document.get('hooks'):
            yield 'hooks_declared', 'notice'
        if document.get('mcpServers') or document.get('enabledMcpjsonServers') or document.get('enableAllProjectMcpServers'):
            yield 'mcp_declared', 'notice'
        permissions = document.get('permissions')
        if permissions:
            yield 'permissions_declared', 'notice'
            if isinstance(permissions, dict) and permissions.get('defaultMode') == 'bypassPermissions':
                yield 'approval_bypass_declared', 'warning'
    else:
        features = document.get('features')
        if document.get('hooks') or (isinstance(features, dict) and features.get('codex_hooks') is True):
            yield 'hooks_declared', 'notice'
        if document.get('mcp_servers'):
            yield 'mcp_declared', 'notice'
        if any(key in document for key in ('approval_policy', 'sandbox_mode', 'permissions', 'default_permissions')):
            yield 'permissions_declared', 'notice'
        if document.get('sandbox_mode') == 'danger-full-access':
            yield 'full_access_sandbox_declared', 'warning'
        if document.get('approval_policy') == 'never':
            yield 'approval_prompting_disabled', 'notice'


def inspect(root, host, name):
    path = root / name
    try:
        resolved = path.resolve(strict=False)
        if not resolved.is_relative_to(root):
            return [('configuration_link_escapes_root', 'blocked')]
        if not resolved.is_file():
            return [('configuration_missing_or_not_file', 'blocked')]
        if path.suffix == '.toml' and tomllib is None:
            return [('toml_requires_python_3_11', 'blocked')]
        with resolved.open('rb') as stream:
            content = stream.read(MAX_BYTES + 1)
    except (OSError, RuntimeError):
        return [('configuration_unreadable', 'blocked')]
    if len(content) > MAX_BYTES:
        return [('configuration_too_large', 'blocked')]
    try:
        text = content.decode('utf-8')
        document = (tomllib.loads(text) if path.suffix == '.toml'
                    else json.loads(text, object_pairs_hook=unique_object))
        if not isinstance(document, dict):
            return [('configuration_must_be_an_object', 'blocked')]
    except (ValueError, RecursionError):
        return [('malformed_configuration', 'blocked')]
    return list(declarations(host, document))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--host', choices=tuple(FILES), required=True)
    parser.add_argument('--file', action='append', required=True, help='known project config path; repeat to select more')
    args = parser.parse_args()
    if set(args.file) - FILES[args.host]:
        parser.error('file must be one of: ' + ', '.join(sorted(FILES[args.host])))
    try:
        root = args.project.resolve(strict=True)
        if not root.is_dir():
            raise ValueError()
    except (OSError, RuntimeError, ValueError):
        parser.error('project must resolve to an existing directory')
    files = sorted(set(args.file))
    findings = [
        {'path': name, 'id': finding, 'level': level}
        for name in files for finding, level in inspect(root, args.host, name)
    ]
    levels = {finding['level'] for finding in findings}
    status = 'blocked' if 'blocked' in levels else 'warnings' if 'warning' in levels else 'complete'
    print(json.dumps({
        'host': args.host, 'selected_files': files, 'status': status, 'findings': findings,
        'limitation': 'Static declarations only. Effective runtime permissions were not tested.',
    }, indent=2))
    return {'complete': 0, 'warnings': 1, 'blocked': 2}[status]


if __name__ == '__main__':
    sys.exit(main())
