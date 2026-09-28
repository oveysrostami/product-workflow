#!/usr/bin/env python3
"""Read structural queue candidates; human authority and semantic readiness need review."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

TEAMS = {'product', 'qa', 'tech', 'development', 'review', 'release'}
STATES = {'intake', 'product-draft', 'product-review', 'product-approved', 'qa-design',
          'qa-approved', 'technical-design', 'technical-approved', 'implementing',
          'verifying', 'accepted', 'release-pending', 'releasing', 'closed',
          'waiting-human', 'blocked', 'paused', 'cancelled', 'bug-triage', 'change-analysis'}
ACTIONS = {'start', 'continue', 'return', 'waiting', 'blocked', 'done'}
STAGES = {'product': 'G-P', 'qa': 'G-Q', 'technical': 'G-T'}
MARKERS = ('AGENTS.md', 'README.md', 'workflows/graph.json', 'workflows/00-team-entry.md',
           'workflows/00-node-contract.md', 'docs/08-team-file-ownership.md',
           'docs/11-documentation-cycle.md', 'requests/board.json',
           'templates/shared/board-card.json', 'templates/shared/node-run.json')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def concrete(value):
    return isinstance(value, str) and bool(value.strip()) and '{{' not in value


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value) is not None


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return sha_bytes(path.read_bytes())


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def local(root, name, exists=True):
    require(isinstance(name, str) and name and '\\' not in name and ':' not in name, 'Invalid local path')
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe local path: '+name)
    result = root/path
    cursor = root
    for part in path.parts:
        cursor = cursor/part
        require(not cursor.is_symlink(), 'Symlink path is not supported: '+name)
    require(result.resolve().is_relative_to(root.resolve()), 'Path escapes repository: '+name)
    if exists:
        require(result.is_file(), 'Missing file: '+name)
    return result


def find_root(value=None):
    start = Path(value).expanduser().resolve() if value else Path.cwd().resolve()
    candidates = [start] if value else [start, *start.parents]
    for root in candidates:
        if all((root/name).is_file() for name in MARKERS):
            return root
    raise ValueError('Workflow repository not found; provide --root with the workflow checkout')


def repositories(root, values):
    result = {root.name: root, 'product-workflow': root, 'product-qa-tech-workflow': root}
    for value in values:
        name, sep, location = value.partition('=')
        require(sep and concrete(name) and Path(location).expanduser().is_absolute(), 'Use --repository ID=/absolute/path')
        path = Path(location).expanduser().resolve()
        require(path.is_dir(), 'Repository directory is missing: '+name)
        require(name not in result or result[name] == path, 'Conflicting repository mapping: '+name)
        result[name] = path
    return result


def context(root):
    board = read(local(root, 'requests/board.json'))
    graph = read(local(root, 'workflows/graph.json'))
    require(board.get('schemaVersion') == 1 and graph.get('schemaVersion') == 1, 'Unsupported board or graph schema')
    require(isinstance(board.get('cards'), list) and isinstance(board.get('columns'), list), 'Invalid board arrays')
    nodes = {n['id']: n for flow in graph['workflows'] for n in flow['nodes']}
    require(all(identifier(c.get('requestId')) for c in board['cards']), 'Invalid request id on board')
    require(len({c['requestId'] for c in board['cards']}) == len(board['cards']), 'Duplicate request id on board')
    return board, nodes, set(graph['terminals'])


def validate_card(root, board, nodes, terminals, card):
    template = read(local(root, 'templates/shared/board-card.json'))
    require(set(card) == set(template), 'Card fields do not match the repository template')
    rid = card['requestId']
    require(identifier(rid) and concrete(card['title']), 'Invalid request id/title')
    require(card['team'] in TEAMS or card['team'] is None, 'Invalid card team')
    require(card['state'] in STATES and card['action'] in ACTIONS, 'Invalid card state/action')
    require(card['columnId'] in {c['id'] for c in board['columns']}, 'Invalid board column')
    require(card['scope'] in {'documentation', 'implementation', 'review', 'release'}, 'Invalid scope')
    require(concrete(card['authorizationReference']), 'Missing original scope authorization reference')
    require(isinstance(card['modules'], list) and all(concrete(m) for m in card['modules']), 'Invalid modules')
    require(isinstance(card['openReturnIds'], list) and all(identifier(i) for i in card['openReturnIds']), 'Invalid return ids')
    for key in ('currentNode', 'nextNode', 'resumeNode'):
        allowed = set(nodes) | (terminals if key == 'nextNode' else set())
        require(card[key] is None or card[key] in allowed, 'Invalid '+key)
    require(isinstance(card['baselines'], dict) and set(card['baselines']) == set(STAGES), 'Invalid baseline slots')
    for key in ('requestPath', 'trackingPath'):
        require(card[key] == f'requests/{rid}/'+('request.md' if key == 'requestPath' else 'tracking.md'), 'Invalid '+key)
    for key in ('documentPath', 'journalPath'):
        if card[key] is not None:
            require(card[key].startswith(f'requests/{rid}/'), 'Cross-request '+key)
    for stage, binding in card['baselines'].items():
        if binding is not None:
            require(isinstance(binding, dict) and set(binding) == {'manifestPath', 'approvalPath', 'receiptPath'}, 'Invalid '+stage+' binding')
            for key, value in binding.items():
                if value is not None:
                    require(isinstance(value, str) and value.startswith(f'requests/{rid}/'), 'Cross-request baseline path')


def baseline(root, card, stage, repo_map):
    binding = card['baselines'][stage]
    require(binding is not None, 'Missing '+stage+' baseline')
    manifest_path = local(root, binding['manifestPath'])
    manifest = read(manifest_path)
    approval = read(local(root, binding['approvalPath']))
    stamp = digest(manifest_path)
    require(manifest.get('schemaVersion') == 1 and manifest.get('requestId') == card['requestId'] and manifest.get('stage') == stage, 'Wrong '+stage+' manifest identity')
    require(concrete(manifest.get('baselineId')) and manifest.get('openBlockers') == [], 'Missing baseline id or open blockers in '+stage)
    require(approval.get('gate') == STAGES[stage] and approval.get('status') == 'approved', 'Missing approved '+STAGES[stage])
    require(approval.get('requestId') == card['requestId'] and approval.get('baselineId') == manifest['baselineId'] and approval.get('manifestSha256') == stamp, 'Approval does not match '+stage+' bytes')
    declared = approval.get('manifestPath')
    if declared:
        options = {binding['manifestPath'], str(Path(binding['manifestPath']).relative_to(Path(binding['approvalPath']).parent))} if Path(binding['manifestPath']).is_relative_to(Path(binding['approvalPath']).parent) else {binding['manifestPath']}
        require(declared in options, 'Approval manifestPath differs from board binding')
    roles, decisions = approval.get('requiredRoles'), approval.get('decisions')
    require(isinstance(roles, list) and roles and all(concrete(r) for r in roles) and isinstance(decisions, list), 'Missing required human roles/decisions')
    for role in roles:
        matches = [d for d in decisions if isinstance(d, dict) and d.get('role') == role]
        require(matches and all(d.get('decision') == 'approved' and all(concrete(d.get(k)) for k in ('identity', 'reference', 'text')) for d in matches), 'Missing or conflicting decision for '+role)
    artifacts = manifest.get('artifacts')
    require(isinstance(artifacts, list) and artifacts, 'Manifest has no artifacts')
    seen, handover = set(), False
    for item in artifacts:
        repository = item.get('repository')
        require(repository in repo_map, 'Unmapped repository: '+str(repository))
        key = (repository, item.get('path'))
        require(key not in seen, 'Duplicate manifest artifact')
        seen.add(key)
        artifact = local(repo_map[repository], item['path'])
        require(digest(artifact) == item.get('sha256'), 'Changed artifact: '+item['path'])
        if artifact.suffix == '.md':
            require(not re.search(r'\{\{[^}]+\}\}', artifact.read_text(encoding='utf-8')), 'Unresolved placeholder: '+item['path'])
        if repo_map[repository] == root and item['path'] == f'requests/{card["requestId"]}/{stage}/handover.md':
            handover = True
    require(handover, 'Approved '+stage+' handover is absent from manifest')
    if binding['receiptPath']:
        receipt = read(local(root, binding['receiptPath']))
        require(receipt.get('baselineId') == manifest['baselineId'] and receipt.get('manifestSha256') == stamp, 'Receipt references a different baseline')
        require(receipt.get('status') in {'pending', 'accepted'}, 'Receipt was returned or invalid')
        if receipt['status'] == 'accepted':
            require(concrete(receipt.get('decisionReference')) and all(concrete(receipt.get('recipient', {}).get(k)) for k in ('identity', 'role')), 'Receipt has no actual recipient/decision reference')
    return {'baselineId': manifest['baselineId'], 'manifestSha256': stamp, 'parents': manifest.get('parents', [])}


def prerequisites(root, card, stages, repo_map):
    result = {stage: baseline(root, card, stage, repo_map) for stage in stages}
    for stage, parents in (('qa', ('product',)), ('technical', ('product', 'qa'))):
        if stage in result:
            for parent in parents:
                require(parent in result and any(p.get('baselineId') == result[parent]['baselineId'] and p.get('manifestSha256') == result[parent]['manifestSha256'] for p in result[stage]['parents']), stage+' has a stale or missing '+parent+' parent')
    return result


def check_modules(root, card, technical):
    for slug in card['modules']:
        require(re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug), 'Invalid module slug')
        folder = 'modules/'+slug
        pointer = read(local(root, folder+'/current.json'))
        revision = pointer.get('revisionId')
        require(identifier(revision) and pointer.get('moduleId') == slug, 'Invalid module pointer')
        manifest_path = local(root, folder+'/revisions/'+revision+'/manifest.json')
        require(digest(manifest_path) == pointer.get('manifestSha256'), 'Changed module manifest')
        manifest = read(manifest_path)
        source = manifest.get('source', {})
        require(source.get('requestId') == card['requestId'] and source.get('manifestSha256') == technical['manifestSha256'], 'Module is not published from this technical approval: '+slug)
        for item in manifest['artifacts']:
            artifact = local(root, folder+'/revisions/'+revision+'/'+item['path'])
            require(digest(artifact) == item['sha256'], 'Changed module artifact: '+slug)


def inspect_card(root, card, board, nodes, terminals, repo_map):
    errors = []
    try:
        validate_card(root, board, nodes, terminals, card)
        local(root, card['requestPath'])
        tracking = local(root, card['trackingPath']).read_text(encoding='utf-8')
        pending = local(root, f'requests/{card["requestId"]}/runs/.progress-pending.json', exists=False)
        require(not pending.exists(), 'Interrupted progress transaction needs recovery')
        if card['documentPath']:
            local(root, card['documentPath'])
        if card['journalPath']:
            journal = read(local(root, card['journalPath']))
            require(journal.get('requestId') == card['requestId'] and journal.get('nodeId') == card['currentNode'], 'Journal and current card disagree')
            require(journal.get('nextNode') == card['nextNode'] and journal.get('resumeNode') == card['resumeNode'], 'Journal checkpoint differs from board')
            require(journal.get('status') in {'pending', 'running', 'waiting-human', 'blocked', 'completed', 'failed', 'cancelled'}, 'Invalid journal status')
            if journal['status'] == 'completed':
                require(journal['nextNode'] in {t['target'] for t in nodes[card['currentNode']]['transitions']}, 'Journal transition is absent from graph')
            if journal.get('progress'):
                require(journal['progress']['card'] == card, 'Board changed without matching progress journal')
        elif card['action'] == 'continue':
            raise ValueError('Continuation requires a recorded journal checkpoint')
        if card['lastMovementId']:
            require(card['lastMovementId'] in tracking, 'Last movement is absent from tracking')
        if card['columnId'] in {'ready-qa', 'ready-tech', 'technical-ready'}:
            require(card['journalPath'] and card['lastMovementId'] and card['documentPath'] and card['ownerReference'], 'Readiness lacks journal/movement/document/owner')
            require(not card['blocker'] and not card['openReturnIds'], 'Readiness has an unresolved blocker/return')
            require(journal.get('status') == 'completed', 'Handover node is not completed')
            if card['columnId'] == 'ready-qa':
                require((card['team'], card['state'], card['currentNode'], card['nextNode'], card['action']) == ('qa', 'product-approved', 'P08', 'Q01', 'start'), 'Inconsistent QA entry card')
                prerequisites(root, card, ('product',), repo_map)
            elif card['columnId'] == 'ready-tech':
                require((card['team'], card['state'], card['currentNode'], card['nextNode'], card['action']) == ('tech', 'qa-approved', 'Q06', 'T01', 'start'), 'Inconsistent technical entry card')
                prerequisites(root, card, ('product', 'qa'), repo_map)
            else:
                require(card['state'] == 'technical-approved' and card['currentNode'] == 'T08', 'Technical handover is incomplete')
                versions = prerequisites(root, card, ('product', 'qa', 'technical'), repo_map)
                check_modules(root, card, versions['technical'])
        elif card['team'] == 'qa':
            prerequisites(root, card, ('product',), repo_map)
            if card['state'] == 'qa-design' and card['currentNode'] != 'Q01' and card['columnId'] != 'returned':
                receipt = card['baselines']['product']['receiptPath']
                require(receipt and read(local(root, receipt)).get('status') == 'accepted', 'QA continuation needs the accepted product receipt')
        elif card['team'] == 'tech':
            prerequisites(root, card, ('product', 'qa'), repo_map)
            if card['state'] == 'technical-design' and card['currentNode'] != 'T01' and card['columnId'] != 'returned':
                receipt = card['baselines']['qa']['receiptPath']
                require(receipt and read(local(root, receipt)).get('status') == 'accepted', 'Technical continuation needs the accepted QA receipt')
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        errors.append(str(exc))
    group = 'inProgress'
    if card.get('columnId') == 'returned' or card.get('action') == 'return':
        group = 'returned'
    elif errors or card.get('blocker') or card.get('action') == 'blocked':
        group = 'blocked'
    elif card.get('columnId') == 'waiting' or card.get('action') == 'waiting':
        group = 'waiting'
    elif card.get('columnId') == 'technical-ready' or card.get('action') == 'done':
        group = 'completed'
    elif card.get('columnId') in {'ready-qa', 'ready-tech'}:
        group = 'readyCandidates'
    return group, {'card': card, 'issues': errors, 'humanReviewRequired': ['role appointment and actual decision references', 'independent review, semantic scope and unresolved changes', 'freshness and any returned-item resolution']}


def queue(root, team, repo_map, request_id=None):
    board, nodes, terminals = context(root)
    groups = {k: [] for k in ('readyCandidates', 'inProgress', 'returned', 'waiting', 'blocked', 'completed')}
    recovery = []
    for path in sorted((root/'requests').glob('*/runs/.progress-pending.json')):
        name = str(path.relative_to(root))
        pending = read(local(root, name))
        recovery.append({'requestId': path.parent.parent.name, 'pendingPath': name,
                         'journalPath': pending.get('journalPath'),
                         'eventSha256': pending.get('eventSha256')})
    found = False
    for card in board['cards']:
        if card.get('team') != team or (request_id and card['requestId'] != request_id):
            continue
        found = True
        group, item = inspect_card(root, card, board, nodes, terminals, repo_map)
        groups[group].append(item)
    require(not request_id or found or any(p['requestId'] == request_id for p in recovery), 'Selected request is absent from this team queue')
    return {'schemaVersion': 1, 'root': str(root), 'team': team, 'boardSha256': digest(root/'requests/board.json'),
            'groups': groups, 'recoveryRequired': recovery,
            'scope': 'Structural candidates only. Review human authority, semantics and freshness before displaying ready work.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    parser.add_argument('--team', choices=['product', 'qa', 'tech'], required=True)
    parser.add_argument('--request')
    parser.add_argument('--repository', action='append', default=[], metavar='ID=/absolute/path')
    args = parser.parse_args()
    try:
        root = find_root(args.root)
        print(json.dumps(queue(root, args.team, repositories(root, args.repository), args.request), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
