"""Publish the exact module snapshot in a recorded G-T approval; no gate decisions."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name, within=None):
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or not name or ':' in name:
        raise ValueError('Unsafe local path: '+str(name))
    resolved = (root/path).resolve()
    if not resolved.is_relative_to((within or root).resolve()) or not resolved.is_file():
        raise ValueError('Missing or unsafe file: '+name)
    return resolved


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def reading_entry(module_id, revision_id):
    return (f"# {module_id}\n\n"
            f"[آخرین طرح تأییدشده: {revision_id}](revisions/{revision_id}/README.md)\n\n"
            "نسخه و digest در current.json است. وضعیت اجرای کد مستقل در implementation/، در صورت وجود شاهد، ثبت می‌شود.\n")


def approved_snapshot(root, plan_name, manifest_name, approval_name):
    plan_path = local(root, plan_name)
    manifest_path = local(root, manifest_name)
    approval_path = local(root, approval_name)
    plan, manifest, approval = read(plan_path), read(manifest_path), read(approval_path)
    if set(plan) != {'schemaVersion', 'moduleId', 'revisionId', 'baseRevision', 'observedImplementation', 'artifacts'} or plan['schemaVersion'] != 1:
        raise ValueError('Invalid snapshot plan')
    for key in ('moduleId', 'revisionId'):
        if not isinstance(plan[key], str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', plan[key]):
            raise ValueError('Invalid snapshot '+key)
    request_id = manifest['requestId']
    if not isinstance(request_id, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', request_id):
        raise ValueError('Invalid source request id')
    request = root/'requests'/request_id
    expected = request/'technical/modules'/plan['moduleId']/'snapshot'
    if plan_path.parent != expected.resolve() or not manifest_path.is_relative_to(request.resolve()) or not approval_path.is_relative_to(request.resolve()):
        raise ValueError('Snapshot sources belong to another request or module')
    if (manifest.get('stage') != 'technical' or manifest.get('openBlockers') != []
            or approval.get('gate') != 'G-T' or approval.get('status') != 'approved'
            or approval.get('requestId') != request_id or approval.get('baselineId') != manifest.get('baselineId')
            or approval.get('manifestSha256') != digest(manifest_path)):
        raise ValueError('Valid recorded G-T approval is required')
    required = approval.get('requiredRoles', [])
    decisions = approval.get('decisions', [])
    def concrete(value):
        return isinstance(value, str) and bool(value.strip()) and '{{' not in value
    if not isinstance(required, list) or not required or not all(concrete(role) for role in required) or any(not any(
        d.get('role') == role and d.get('decision') == 'approved'
        and all(concrete(d.get(field)) for field in ('identity', 'reference', 'text')) for d in decisions
    ) for role in required):
        raise ValueError('G-T required human decisions are missing')
    observed = plan['observedImplementation']
    if (set(observed) != {'status', 'sourceRevision', 'limitation'}
            or observed['status'] not in {'unknown', 'not-implemented', 'partial', 'implemented'}
            or not isinstance(observed['limitation'], str) or not observed['limitation'].strip()
            or '{{' in observed['limitation']
            or (observed['status'] != 'unknown' and not observed['sourceRevision'])):
        raise ValueError('Implementation observation needs a revision and limitation')
    base = plan['baseRevision']
    if base is not None and (set(base) != {'revisionId', 'manifestSha256'}
                            or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', base['revisionId'])
                            or not re.fullmatch(r'[0-9a-f]{64}', base['manifestSha256'])):
        raise ValueError('Invalid base revision')
    frozen = {item['path']: item['sha256'] for item in manifest['artifacts']}
    if frozen.get(plan_name) != digest(plan_path):
        raise ValueError('Snapshot plan is not frozen in the approved technical manifest')
    names = set()
    for item in plan['artifacts']:
        name = item['path']
        if name in names or name in {'manifest.json', 'snapshot-plan.json'}:
            raise ValueError('Duplicate or reserved snapshot artifact: '+name)
        names.add(name)
        artifact = local(plan_path.parent, name)
        if digest(artifact) != item['sha256'] or frozen.get(str(artifact.relative_to(root))) != item['sha256']:
            raise ValueError('Snapshot artifact differs from approved bytes: '+name)
        if artifact.suffix == '.md' and re.search(r'\{\{[^}]+\}\}', artifact.read_text()):
            raise ValueError('Unresolved placeholder in snapshot: '+name)
    if 'README.md' not in names:
        raise ValueError('A complete module README is required')
    published = dict(plan, source={
        'requestId': request_id, 'planPath': plan_name, 'manifestPath': manifest_name,
        'manifestSha256': digest(manifest_path), 'approvalPath': approval_name,
    })
    return plan_path.parent, published


def verify_revision(root, folder):
    published = read(folder/'manifest.json')
    source = published['source']
    _, expected = approved_snapshot(root, source['planPath'], source['manifestPath'], source['approvalPath'])
    if published != expected:
        raise ValueError('Published manifest differs from its approved snapshot: '+str(folder))
    if folder != root/'modules'/published['moduleId']/'revisions'/published['revisionId']:
        raise ValueError('Published revision has the wrong module or directory')
    for item in published['artifacts']:
        if digest(local(folder, item['path'])) != item['sha256']:
            raise ValueError('Published artifact changed: '+item['path'])
    base = published['baseRevision']
    if base is not None:
        previous = local(root, f"modules/{published['moduleId']}/revisions/{base['revisionId']}/manifest.json")
        if digest(previous) != base['manifestSha256']:
            raise ValueError('Previous module revision changed')
    return published


def publish(root, plan_name, manifest_name, approval_name, apply=False):
    source_folder, published = approved_snapshot(root, plan_name, manifest_name, approval_name)
    module = root/'modules'/published['moduleId']
    revision = module/'revisions'/published['revisionId']
    if (not revision.resolve().is_relative_to((root/'modules').resolve())
            or module.is_symlink() or (module/'revisions').is_symlink()
            or any((module/name).is_symlink() for name in ('README.md', 'current.json'))
            or revision.is_symlink()):
        raise ValueError('Unsafe module destination')
    current_path = module/'current.json'
    current = read(current_path) if current_path.exists() else None
    if current is not None and (set(current) != {'moduleId', 'revisionId', 'manifestSha256'}
            or current['moduleId'] != published['moduleId']
            or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', current['revisionId'])
            or not re.fullmatch(r'[0-9a-f]{64}', current['manifestSha256'])):
        raise ValueError('Invalid current module pointer')
    manifest_bytes = (json.dumps(published, ensure_ascii=False, indent=2)+'\n').encode()
    target = {'moduleId': published['moduleId'], 'revisionId': published['revisionId'],
              'manifestSha256': hashlib.sha256(manifest_bytes).hexdigest()}
    if current == target:
        verify_revision(root, revision)
        if apply and (not (module/'README.md').is_file() or
                      (module/'README.md').read_text() != reading_entry(published['moduleId'], published['revisionId'])):
            (module/'README.md').write_text(reading_entry(published['moduleId'], published['revisionId']))
        return 'already-current'
    expected_base = None if current is None else {
        'revisionId': current['revisionId'], 'manifestSha256': current['manifestSha256'],
    }
    if published['baseRevision'] != expected_base:
        raise ValueError('Current module revision changed; return to T02 before reapproval')
    if current is not None:
        previous_folder = module/'revisions'/current['revisionId']
        verify_revision(root, previous_folder)
        if digest(previous_folder/'manifest.json') != current['manifestSha256']:
            raise ValueError('Current pointer has a different manifest digest')
    if revision.exists():
        if read(revision/'manifest.json') != published:
            raise ValueError('An immutable revision cannot be overwritten')
        verify_revision(root, revision)
    if not apply:
        return 'ready-to-publish'
    # T09 requires one writer and journal/writeScope; stage immutable bytes before the pointer.
    if not revision.exists():
        revision.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.module-stage-', dir=revision.parent) as temporary:
            staged = Path(temporary)/'snapshot'
            staged.mkdir()
            for item in published['artifacts']:
                destination = staged/item['path']
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(local(source_folder, item['path']), destination)
                if digest(destination) != item['sha256']:
                    raise ValueError('Source artifact changed during publication')
            (staged/'manifest.json').write_bytes(manifest_bytes)
            staged.rename(revision)
    verify_revision(root, revision)
    (module/'README.md').write_text(reading_entry(published['moduleId'], published['revisionId']))
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=module,
                                     prefix='.current-', delete=False) as temporary:
        temporary.write(json.dumps(target, ensure_ascii=False, indent=2)+'\n')
    Path(temporary.name).replace(current_path)
    return 'published'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ('plan', 'manifest', 'approval'):
        parser.add_argument('--'+option, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(publish(ROOT, args.plan, args.manifest, args.approval, args.apply))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
