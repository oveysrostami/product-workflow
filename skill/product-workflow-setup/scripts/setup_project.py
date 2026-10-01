#!/usr/bin/env python3
"""Bind one sibling Backend; only the workflow project/backend.json can be written.

Backend files are never executed/imported. Environment/secret files are not read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

BINDING = 'project/backend.json'
NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z')
SOURCES = (
    'AGENTS.md', 'README.md', 'pom.xml', '_doc/README.md',
    '_doc/01-architecture.md', '_doc/15-authority-and-traceability.md',
    '_doc/18-spec-driven-development.md', '_doc/architecture/README.md',
    '_agent-doc/README.md', '_agent-doc/skills.md', 'application-host/HOST.md',
    'scripts/agent/schemas/spec.v1.schema.json', 'scripts/agent/schemas/tasks.v1.schema.json',
)
CHOICES = {
    'host': {'application-host', 'reference-host'},
    'composition': {'base', 'reference', 'acceptance'},
    'authentication': {'none', 'internal', 'keycloak'},
    'role': {'web', 'worker', 'scheduler', 'control-agent', 'cli', 'migrate'},
    'infrastructure.database': {'postgres'},
    'infrastructure.cache': {'none', 'redis'},
    'infrastructure.metrics': {'none', 'prometheus'},
    'infrastructure.diagnosticTransport': {'none', 'otlp'},
    'infrastructure.errorReporting': {'none', 'sentry'},
    'infrastructure.logbookBackend': {'postgres', 'mongodb', 'elasticsearch'},
    'localization.mode': {'single', 'multilingual'},
    'messaging.mode': {'none', 'kafka'},
}
BOOLEAN_CHOICES = (
    'schedules.deliveryEnabled', 'schedules.workflowWorkerEnabled',
    'logging.integrationMetadata', 'logging.integrationPayload', 'logging.events', 'logging.http',
    'logging.apiCalls.enabled', 'logging.internalServices.enabled', 'logging.http.enabled',
    'logging.events.enabled', 'logging.modelChanges.enabled',
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root: Path, name: str, required: bool = True) -> Path | None:
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Invalid local artifact path')
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Artifact must stay inside its repository')
    path = root / relative
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError('Symlink artifacts are not supported')
    if path.exists() and not path.is_file():
        raise ValueError('Artifact path must name a file')
    if not path.is_file():
        if required:
            raise ValueError('Required local artifact is missing')
        return None
    return path


def workflow_root(value: str | Path) -> Path:
    root = Path(value).expanduser().resolve(strict=True)
    for marker in ('AGENTS.md', 'workflows/graph.json', 'requests/board.json'):
        local(root, marker)
    return root


def backend_root(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not NAME.fullmatch(name) or name in {'.', '..'}:
        raise ValueError('Backend name must be one directory basename')
    backend = root.parent / name
    if backend == root or backend.is_symlink() or not backend.is_dir():
        raise ValueError('Backend must be an existing real sibling directory')
    local(backend, 'AGENTS.md')
    return backend


def read_json(path: Path) -> dict:
    if path.stat().st_size > 2_000_000:
        raise ValueError('JSON artifact exceeds the bounded inspection size')
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError):
        raise ValueError('Invalid JSON artifact; contents omitted') from None
    if not isinstance(value, dict):
        raise ValueError('JSON artifact must be an object')
    return value


def load_binding(root: Path) -> dict | None:
    path = local(root, BINDING, False)
    if path is None:
        return None
    value = read_json(path)
    if (set(value) != {'schemaVersion', 'backendName', 'relativePath', 'access',
                      'technicalDocumentation', 'sourceReference'}
            or type(value['schemaVersion']) is not int or value['schemaVersion'] != 1
            or value['access'] != 'read-only'
            or value['technicalDocumentation'] != 'product-workflow'
            or not isinstance(value['sourceReference'], str) or not value['sourceReference'].strip()):
        raise ValueError('Invalid binding or access policy')
    backend_root(root, value['backendName'])
    if value['relativePath'] != '../' + value['backendName']:
        raise ValueError('Binding path must match the sibling Backend name')
    return value


def value_at(document: dict, key: str):
    value = document
    for part in key.split('.'):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def inspect_backend(root: Path, name: str) -> dict:
    backend = backend_root(root, name)
    sources = []
    for entry in SOURCES:
        path = local(backend, entry, False)
        if path is not None:
            sources.append({'path': entry, 'sha256': digest(path)})
    modules = []
    folder = backend / 'modules'
    if folder.is_symlink():
        raise ValueError('Symlink module directory is not supported')
    if folder.is_dir():
        modules = sorted(p.name for p in folder.iterdir() if p.is_dir() and not p.is_symlink())
    setup = {'recordedState': 'not-observed', 'recordPath': None, 'recordSha256': None,
             'planPath': None, 'planSha256': None, 'recordAndPlanMatch': False,
             'backendPreflight': 'not-executed', 'runtimeActivation': 'unknown', 'selections': {}}
    marker = local(backend, '_agent-doc/project-initialization.json', False)
    if marker is not None:
        record = read_json(marker)
        state = record.get('state')
        setup.update(recordedState=state if isinstance(state, str) and state in {'completed', 'applying', 'failed', 'blocked'} else 'unknown',
                     recordPath=marker.relative_to(backend).as_posix(), recordSha256=digest(marker))
        outputs = record.get('outputs')
        if isinstance(outputs, dict) and isinstance(outputs.get('plan'), str):
            plan_path = local(backend, outputs['plan'], False)
            if plan_path:
                # Do not read an environment/credential file masquerading as a plan.
                if plan_path.suffix != '.json' or plan_path == marker:
                    raise ValueError('Setup plan must be a distinct JSON artifact')
                plan = read_json(plan_path)
                if plan.get('kind') != 'boilerplate-deployment-profile-plan':
                    raise ValueError('Unsupported setup plan; contents omitted')
                setup.update(planPath=plan_path.relative_to(backend).as_posix(), planSha256=digest(plan_path))
                profile = plan.get('profile')
                if isinstance(profile, dict):
                    profile_hash = hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest()
                    setup['recordAndPlanMatch'] = (
                        type(record.get('schemaVersion')) is int and record['schemaVersion'] == 1
                        and type(plan.get('schemaVersion')) is int and plan['schemaVersion'] == 1
                        and record.get('profileSha256') == profile_hash
                        and record.get('productId') == profile.get('productId')
                        and record.get('environment') == profile.get('environment'))
                    for key, allowed in CHOICES.items():
                        value = value_at(profile, key)
                        if isinstance(value, str) and value in allowed:
                            setup['selections'][key] = value
                    for key in BOOLEAN_CHOICES:
                        value = value_at(profile, key)
                        if type(value) is bool:
                            setup['selections'][key] = value
    return {'backendName': name, 'relativePath': '../' + name, 'resolvedPath': str(backend),
            'access': 'read-only', 'sources': sources, 'modulesPresentInSource': modules, 'setup': setup,
            'limitation': 'File inspection only; no Backend tools, environment files or runtime checks executed.'}


def configure(root: Path, name: str, reference: str, apply: bool = False) -> dict:
    observation = inspect_backend(root, name)
    if not reference or not reference.strip():
        raise ValueError('A real user source reference is required')
    binding = {'schemaVersion': 1, 'backendName': name, 'relativePath': '../' + name,
               'access': 'read-only', 'technicalDocumentation': 'product-workflow',
               'sourceReference': reference}
    existing = load_binding(root)
    if existing is not None:
        if existing['backendName'] != name:
            raise ValueError('Existing Backend binding cannot be silently replaced')
        return {'status': 'already-configured', 'binding': existing, 'observation': observation}
    if apply:
        folder = root / 'project'
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            raise ValueError('Unsafe workflow project directory')
        folder.mkdir(exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
        directory = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | getattr(os, 'O_NOFOLLOW', 0))
        try:
            try:
                descriptor = os.open('backend.json', flags, 0o644, dir_fd=directory)
            except FileExistsError:
                raise ValueError('Binding changed concurrently; inspect it and retry') from None
        finally:
            os.close(directory)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
            handle.write(json.dumps(binding, ensure_ascii=False, indent=2) + '\n')
            handle.flush()
            os.fsync(handle.fileno())
    return {'status': 'configured' if apply else 'preview', 'binding': binding, 'observation': observation}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--backend-name')
    parser.add_argument('--source-reference')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--inspect', action='store_true')
    args = parser.parse_args()
    try:
        root = workflow_root(args.root)
        if args.inspect:
            if args.apply or args.backend_name or args.source_reference:
                raise ValueError('Inspect cannot create or replace a binding')
            binding = load_binding(root)
            if binding is None:
                raise ValueError('No Backend binding; run setup with the directory name')
            result = {'status': 'inspected', 'binding': binding,
                      'observation': inspect_backend(root, binding['backendName'])}
        else:
            result = configure(root, args.backend_name, args.source_reference or '', args.apply)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError):
        # ValueError messages are authored above; OS errors may contain sensitive paths.
        message = sys.exc_info()[1]
        print(json.dumps({'status': 'blocked', 'error': str(message) if isinstance(message, ValueError)
                          else 'Filesystem inspection or local binding write failed; contents omitted'}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
