"""Validate, approve, and verify a bounded specification against a Git workspace."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def load(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError(f'{path.name} must contain a JSON object')
    return data


def write_new(path, data):
    # Exclusive creation keeps previous approval and verification evidence intact.
    with path.open('x', encoding='utf-8') as output:
        json.dump(data, output, indent=2, sort_keys=True)
        output.write('\n')


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def relative_path(value):
    value = text(value, 'path')
    path = PurePosixPath(value)
    if (path.is_absolute() or not path.parts or path.as_posix() != value
            or '..' in path.parts or '.git' in path.parts or '\\' in value or '\0' in value):
        raise ValueError(f'unsafe relative path: {value!r}')
    return value


def items(data, field, prefix):
    entries = data.get(field)
    if not isinstance(entries, list) or not entries:
        raise ValueError(f'{field} must be a nonempty list')
    result = {}
    for entry in entries:
        key = entry.get('id') if isinstance(entry, dict) else None
        if not isinstance(key, str) or not re.fullmatch(prefix + r'-[1-9][0-9]*', key) or key in result:
            raise ValueError(f'{field} needs unique {prefix}-number identifiers')
        result[key] = entry
    return result


def validate_verification(criterion):
    key = criterion['id']
    plan = criterion.get('verification')
    if not isinstance(plan, dict):
        raise ValueError(f'{key} needs a structured verification plan')
    for field in ('setup', 'action', 'expected'):
        text(plan.get(field), f'{key} verification.{field}')
    for field in ('source_paths', 'existing_checks'):
        paths = plan.get(field)
        if not isinstance(paths, list) or (field == 'source_paths' and not paths):
            raise ValueError(f'{key} verification.{field} must list project paths')
        paths = list(map(relative_path, paths))
        if len(set(paths)) != len(paths):
            raise ValueError(f'{key} verification.{field} contains duplicate paths')
    if 'coverage_gap' in plan or not plan['existing_checks']:
        text(plan.get('coverage_gap'), f'{key} verification.coverage_gap')


def validate_spec(spec, review_ready=False):
    if type(spec.get('schema_version')) is not int or spec['schema_version'] != 1:
        raise ValueError('unsupported spec schema_version')
    text(spec.get('id'), 'spec id')
    text(spec.get('title'), 'spec title')
    scope = spec.get('scope')
    if not isinstance(scope, list) or not scope:
        raise ValueError('scope must list exact paths')
    paths = [relative_path(path) for path in scope]
    if len(paths) != len(set(paths)):
        raise ValueError('scope contains duplicate paths')
    existing = spec.get('allow_existing_changes', [])
    if not isinstance(existing, list) or not set(map(relative_path, existing)) <= set(paths):
        raise ValueError('allow_existing_changes must list paths in scope')
    requirements = items(spec, 'requirements', 'REQ')
    criteria = items(spec, 'criteria', 'AC')
    covered = set()
    for requirement in requirements.values():
        text(requirement.get('text'), 'requirement text')
    for criterion in criteria.values():
        reference = text(criterion.get('requirement'), 'criterion requirement')
        if reference not in requirements:
            raise ValueError(f'criterion references unknown requirement: {reference}')
        covered.add(reference)
        text(criterion.get('check'), 'verification method')
        if review_ready or 'verification' in criterion:
            validate_verification(criterion)
    if covered != set(requirements):
        raise ValueError('every requirement must be covered by an acceptance criterion')
    return criteria


def check_verification_paths(state, criteria, fields):
    for criterion in criteria.values():
        plan = criterion.get('verification')
        if plan is None:
            continue
        for field in fields:
            for name in plan[field]:
                if state['files'].get(name, [None])[0] != 'file':
                    raise ValueError(f"{criterion['id']} verification path is not a captured project file: {name}")


def git(root, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args],
                          capture_output=True, check=True).stdout


def fingerprint(path):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(mode):
        return ['symlink', sha(os.fsencode(os.readlink(path)))]
    if stat.S_ISREG(mode):
        with path.open('rb') as stream:
            checksum = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                checksum.update(chunk)
        return ['file', bool(mode & stat.S_IXUSR), checksum.hexdigest()]
    raise ValueError(f'unsupported workspace entry: {path}')


def snapshot(root):
    if Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel').rstrip(b'\n'))).resolve() != root:
        raise ValueError('workspace must be the Git worktree root')
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    index = sha(git(root, 'ls-files', '--stage', '-z'))
    names = git(root, 'ls-files', '--cached', '--others', '--exclude-standard', '-z')
    files = {}
    for name in set(names.split(b'\0')) - {b''}:
        path = root / relative_path(os.fsdecode(name))
        if path.parent.resolve() != path.parent:
            raise ValueError(f'redirected parent directory: {path}')
        value = fingerprint(path)
        if value is not None:
            files[path.relative_to(root).as_posix()] = value
    return {'head': head, 'index': index, 'files': files}


def scope_check(root, spec, approval):
    if approval.get('spec_sha256') != digest(spec) or approval.get('workspace') != str(root):
        raise ValueError('approval is for a different spec or workspace')
    text(approval.get('approved_by'), 'approver')
    before = approval['baseline']
    after = snapshot(root)
    if (before['head'], before['index']) != (after['head'], after['index']):
        raise ValueError('Git HEAD or index changed since approval')
    old, new = before['files'], after['files']
    changed = sorted(path for path in old.keys() | new.keys() if old.get(path) != new.get(path))
    outside = sorted(set(changed) - set(spec['scope']))
    if outside:
        raise ValueError('changes outside approved scope: ' + ', '.join(outside))
    return after, changed


def review_artifacts(review, criteria, directory):
    results = review.get('criteria')
    if not isinstance(results, dict) or results.keys() != criteria.keys():
        raise ValueError('review must cover exactly the approved acceptance criteria')
    evidence = {}
    for key, result in results.items():
        if not isinstance(result, dict) or result.get('result') != 'PASS':
            raise ValueError(f'{key} does not have a passing independent result')
        text(result.get('observations'), f'{key} observations')
        paths = result.get('evidence')
        if not isinstance(paths, list) or not paths:
            raise ValueError(f'{key} requires evidence')
        evidence[key] = {}
        for name in paths:
            path = (directory / relative_path(name)).resolve(strict=True)
            if not path.is_relative_to(directory) or not path.is_file() or not path.stat().st_size:
                raise ValueError(f'{key} has invalid evidence: {name}')
            evidence[key][name] = fingerprint(path)[2]
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('validate', 'approve', 'check-scope', 'verify', 'check'):
        action = sub.add_parser(command)
        action.add_argument('spec', type=Path)
        if command in ('validate', 'approve'):
            action.add_argument('--review-ready', action='store_true',
                                help='Require a structured verification plan for every criterion')
        if command != 'validate':
            action.add_argument('--workspace', type=Path, required=True)
            action.add_argument('--approval', type=Path, required=True)
        if command == 'approve':
            action.add_argument('--by', required=True)
        if command in ('verify', 'check'):
            action.add_argument('--review', type=Path, required=True)
            action.add_argument('--verification', type=Path, required=True)
    args = parser.parse_args()
    spec = load(args.spec)
    criteria = validate_spec(spec, getattr(args, 'review_ready', False))
    if args.command == 'validate':
        return {'spec': spec['id'], 'criteria': len(criteria), 'spec_sha256': digest(spec)}
    root = args.workspace.resolve(strict=True)
    for key in ('spec', 'approval', 'review', 'verification'):
        path = getattr(args, key, None)
        if path is not None and path.resolve().is_relative_to(root):
            raise ValueError(f'{key} must be outside the implementation workspace')
    if args.command == 'approve':
        status = git(root, 'status', '--porcelain=v1', '-z', '--no-renames', '--untracked-files=all')
        dirty = {os.fsdecode(entry[3:]) for entry in status.split(b'\0') if entry}
        overlap = sorted((dirty & set(spec['scope'])) - set(spec.get('allow_existing_changes', [])))
        if overlap:
            raise ValueError('existing changes require explicit scope approval: ' + ', '.join(overlap))
        baseline = snapshot(root)
        check_verification_paths(baseline, criteria, ('source_paths', 'existing_checks'))
        approval = {'approved_by': text(args.by, 'approver'), 'spec_sha256': digest(spec),
                    'workspace': str(root), 'baseline': baseline}
        write_new(args.approval, approval)
        return {'spec': spec['id'], 'approval': str(args.approval)}
    approval = load(args.approval)
    state, changed = scope_check(root, spec, approval)
    state_digest = digest(state)
    if args.command == 'check-scope':
        return {'spec': spec['id'], 'changed_paths': changed, 'workspace_sha256': state_digest}
    check_verification_paths(state, criteria, ('existing_checks',))
    review = load(args.review)
    if review.get('workspace_sha256') != state_digest:
        raise ValueError('review is for a different workspace snapshot')
    reviewer = text(review.get('reviewed_by'), 'reviewer')
    implementer = text(review.get('implemented_by'), 'implementer')
    if reviewer.strip().casefold() == implementer.strip().casefold():
        raise ValueError('independent reviewer must differ from the implementer')
    evidence = review_artifacts(review, criteria, args.review.resolve().parent)
    verification = {'approval_sha256': digest(approval), 'review_sha256': digest(review),
                    'workspace_sha256': state_digest, 'artifacts': evidence}
    if args.command == 'verify':
        write_new(args.verification, verification)
    elif load(args.verification) != verification:
        raise ValueError('workspace, approval, review, or evidence changed after verification')
    return {'spec': spec['id'], 'changed_paths': changed, 'criteria_passed': len(criteria)}


if __name__ == '__main__':
    try:
        print(json.dumps(main(), indent=2))
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f'SDD blocked: {error}', file=sys.stderr)
        sys.exit(1)
