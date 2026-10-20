"""Read-only structural validation for Aegis1's deliberately small YAML subset.

This validates distribution structure, not model behavior or Claude's loader.
Frontmatter is restricted to JSON-quoted strings and booleans, both valid YAML.
No third-party packages or external commands are required.
"""
import argparse
import json
import re
from pathlib import Path

SPECIALISTS = (
    'system-discovery', 'requirements-analysis', 'architecture-analysis',
    'implementation-planning', 'implementation', 'testing-verification',
    'code-review', 'debugging',
)
SKILL_FIELDS = {'name', 'description', 'argument-hint', 'context', 'agent',
                'background', 'disable-model-invocation', 'disallowed-tools'}


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('missing frontmatter')
    try:
        end = lines.index('---', 1)
    except ValueError as exc:
        raise ValueError('unclosed frontmatter') from exc
    fields = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, sep, value = line.partition(':')
        if not sep or not re.fullmatch(r'[a-z][A-Za-z-]*', key):
            raise ValueError(f'invalid field: {line}')
        if key in fields:
            raise ValueError(f'duplicate field: {key}')
        try:
            parsed = json.loads(value.strip())
        except json.JSONDecodeError as exc:
            raise ValueError(f'{key}: use a JSON-quoted string or boolean (valid YAML)') from exc
        if type(parsed) not in (str, bool):
            raise ValueError(f'{key}: unsupported field type')
        fields[key] = parsed
    return fields, '\n'.join(lines[end + 1:])


def validate(root):
    root = Path(root).resolve()
    errors = []
    inventory = []

    def error(path, message):
        errors.append(f'{Path(path).relative_to(root).as_posix()}: {message}')

    required = [root / 'agents/aegis1.md'] + [root / f'skills/{n}/SKILL.md' for n in ('aegis', *SPECIALISTS)]
    for path in required:
        if not path.is_file():
            error(path, 'required file missing')
    for path in sorted((root / 'skills').glob('*/SKILL.md')) + sorted((root / 'agents').glob('*.md')):
        try:
            text = path.read_text(encoding='utf-8')
            fields, body = frontmatter(text)
        except (ValueError, UnicodeError) as exc:
            error(path, str(exc))
            continue
        is_skill = path.name == 'SKILL.md'
        allowed = SKILL_FIELDS if is_skill else {'name', 'description'}
        if set(fields) - allowed:
            error(path, f'unsupported fields in this distribution: {sorted(set(fields) - allowed)}')
        name = fields.get('name')
        expected_name = path.parent.name if is_skill else path.stem
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != expected_name:
            error(path, 'invalid name or name/path mismatch')
        desc = fields.get('description')
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            error(path, 'description must be nonempty text, at most 1024 characters')
        for key in ('background', 'disable-model-invocation'):
            if key in fields and type(fields[key]) is not bool:
                error(path, f'{key} must be boolean')
        for key in ('argument-hint', 'context', 'agent', 'disallowed-tools'):
            if key in fields and not isinstance(fields[key], str):
                error(path, f'{key} must be text')
        if 'context' in fields and fields['context'] != 'fork':
            error(path, 'context must be fork')
        if 'agent' in fields:
            agent = fields['agent']
            if not isinstance(agent, str) or not re.fullmatch(r'[a-z0-9-]+', agent):
                error(path, 'invalid agent reference')
            elif not (root / 'agents' / f'{agent}.md').is_file():
                error(path, 'referenced custom agent missing')
            if fields.get('context') != 'fork':
                error(path, 'agent requires context: fork')
        if 'background' in fields and fields.get('context') != 'fork':
            error(path, 'background requires context: fork')
        if is_skill and len(body.splitlines()) >= 500:
            error(path, 'skill body must be under 500 lines')
        if re.search(r'\[TODO[^\]]*\]', body):
            error(path, 'unfinished scaffold')
        inventory.append({'file': path.relative_to(root).as_posix(), 'body_lines': len(body.splitlines())})

    # Check static local Markdown links in authored documentation only.
    docs = [root / 'README.md'] + list((root / 'skills').rglob('*.md')) + list((root / 'agents').glob('*.md')) + list((root / 'evaluations').glob('*.md'))
    for path in docs:
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        targets = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
        resolved = set()
        for target in targets:
            if target.startswith(('https://', 'http://', '#')):
                continue
            if '\\' in target:
                error(path, f'link uses backslash: {target}')
            local = (path.parent / target.split('#', 1)[0]).resolve()
            if not local.is_relative_to(root):
                error(path, f'link escapes distribution: {target}')
            elif not local.is_file():
                error(path, f'broken link: {target}')
            resolved.add(local)
        if path.name == 'SKILL.md':
            refs = path.parent / 'references'
            for ref in refs.rglob('*') if refs.exists() else []:
                if not ref.is_file():
                    continue
                if ref.parent != refs:
                    error(path, f'reference deeper than one level: {ref.name}')
                if ref.resolve() not in resolved:
                    error(path, f'unlinked reference: {ref.name}')
                ref_text = ref.read_text(encoding='utf-8')
                if len(ref_text.splitlines()) > 100 and '## Contents' not in ref_text:
                    error(ref, 'reference over 100 lines needs contents')
    return {'passed': not errors, 'errors': errors, 'inventory': inventory,
            'limitation': 'Static structure only; no Claude model or loader was executed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate(args.root)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
