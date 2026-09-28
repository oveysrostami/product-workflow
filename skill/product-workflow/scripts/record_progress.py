#!/usr/bin/env python3
"""Preview or record one journal/tracking/board movement. Does not create approvals or team documents."""
import argparse
from contextlib import contextmanager
import copy
import json
import os
from pathlib import Path
import sys
import tempfile

from read_queue import (concrete, context, digest, find_root, identifier, local,
                        prerequisites, check_modules, read, repositories, require,
                        sha_bytes, validate_card)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.workflow-write-', delete=False) as out:
            temporary = Path(out.name)
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        temporary.replace(path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


@contextmanager
def writer_lock(root):
    try:
        import fcntl
    except ImportError:
        raise ValueError('Apply requires POSIX advisory locking; preview remains available')
    path = local(root, 'requests/.workflow-state.lock', exists=False)
    with path.open('a+b') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Another progress writer holds the board lock')
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def check_gate(root, card, journal, repo_map):
    if journal['status'] != 'completed':
        return
    node = journal['nodeId']
    if node in {'P07', 'P08'} and journal['nextNode'] in {'P08', 'Q01'}:
        prerequisites(root, card, ('product',), repo_map)
    if node in {'Q05', 'Q06'} and journal['nextNode'] in {'Q06', 'T01'}:
        prerequisites(root, card, ('product', 'qa'), repo_map)
    if node in {'T07', 'T09', 'T08'} and journal['nextNode'] in {'T09', 'T08', 'HOLD', 'D01'}:
        versions = prerequisites(root, card, ('product', 'qa', 'technical'), repo_map)
        if node == 'T08':
            check_modules(root, card, versions['technical'])
    if node in {'Q01', 'T01'} and journal['nextNode'] in {'Q02', 'T02'}:
        stage = 'product' if node == 'Q01' else 'qa'
        prerequisites(root, card, ('product',) if node == 'Q01' else ('product', 'qa'), repo_map)
        binding = card['baselines'][stage]
        require(binding.get('receiptPath'), 'Receiving node requires an actual receipt')
        require(read(local(root, binding['receiptPath'])).get('status') == 'accepted', 'Receiving node requires an accepted receipt')


def build(root, event, repo_map):
    board, nodes, terminals = context(root)
    require(event.get('schemaVersion') == 1, 'Unsupported event schema')
    fields = {'schemaVersion', 'requestId', 'movementId', 'expectedBoardSha256', 'activeTeam',
              'selectionReference', 'sourceReference', 'reason', 'journal', 'card'}
    require(set(event) == fields, 'Event fields differ; use --example')
    require(identifier(event['requestId']) and identifier(event['movementId']), 'Invalid request or movement id')
    require(event['activeTeam'] in {'product', 'qa', 'tech'}, 'Active team must be product, qa or tech')
    require(all(concrete(event[k]) for k in ('selectionReference', 'sourceReference', 'reason')), 'Actual selection/source/reason references are required')
    require(event['expectedBoardSha256'] == digest(root/'requests/board.json'), 'Board changed; reread and reconcile before making a new event')
    rid, mid = event['requestId'], event['movementId']
    card, journal = copy.deepcopy(event['card']), copy.deepcopy(event['journal'])
    require(card.get('requestId') == rid and journal.get('requestId') == rid, 'Event, card and journal request ids differ')
    validate_card(root, board, nodes, terminals, card)
    require(card['scope'] == 'documentation', 'This helper records the documentation scope only')
    local(root, card['requestPath'])
    if card['documentPath']:
        local(root, card['documentPath'])
    node_id = journal.get('nodeId')
    require(node_id in nodes and node_id[0] in 'IPQTC', 'Node is outside the documentation workflow')
    node = nodes[node_id]
    require(set(read(root/'templates/shared/node-run.json')) <= set(journal), 'Journal is missing fields from the repository template')
    require(journal.get('schemaVersion') == 1 and isinstance(journal.get('attempt'), int) and journal['attempt'] > 0, 'Invalid journal schema/attempt')
    require(journal.get('status') in {'pending', 'running', 'waiting-human', 'blocked', 'completed', 'failed', 'cancelled'}, 'Invalid node status')
    executor = journal.get('executor', {})
    require(all(concrete(executor.get(k)) for k in ('type', 'role', 'identity', 'team')), 'Actual node executor is required')
    require(executor['type'] in {'AI', 'Human', 'Tool'}, 'Invalid executor type')
    scope = journal.get('writeScope', {})
    require(isinstance(scope.get('allowedPaths'), list) and scope['allowedPaths'] and concrete(scope.get('ownershipReference')), 'Node writeScope must be recorded')
    for name in scope['allowedPaths']:
        local(root, name, exists=False)
    require(scope.get('outOfScopeChanges') == [], 'Out-of-scope changes require resolution before recording progress')
    require(card['currentNode'] == node_id and card['nextNode'] == journal.get('nextNode') and card['resumeNode'] == journal.get('resumeNode'), 'Card and journal checkpoints differ')
    if journal['status'] == 'completed':
        require(journal['nextNode'] in {e['target'] for e in node['transitions']}, 'Transition is absent from graph')
        if node['actor'] == 'Human':
            require(executor['type'] == 'Human' and concrete(journal.get('decisionReference')), 'Human node completion needs the actual human decision reference')
    else:
        require(journal.get('nextNode') is None, 'Unfinished node cannot advance to a next node')
        require(journal.get('resumeNode') == node_id, 'Unfinished node must resume at the same node')
    existing = next((c for c in board['cards'] if c['requestId'] == rid), None)
    if existing:
        require(existing['team'] == event['activeTeam'], 'Active team does not own this card; team selection is not a card transfer')
        prior = read(local(root, existing['journalPath'])) if existing['journalPath'] else None
        if prior:
            require(prior.get('requestId') == rid and prior.get('nodeId') == existing['currentNode'] and
                    prior.get('nextNode') == existing['nextNode'] and prior.get('resumeNode') == existing['resumeNode'], 'Existing journal and board need reconciliation')
            if prior.get('progress'):
                require(prior['progress']['card'] == existing, 'Existing card differs from its progress journal')
        if prior and prior.get('status') == 'completed':
            expected = existing['nextNode']
        else:
            expected = existing['resumeNode'] or existing['nextNode'] or existing['currentNode']
        require(node_id == expected, 'Node does not match the recorded checkpoint')
        require(existing['trackingPath'] == card['trackingPath'], 'Tracking path cannot change')
    else:
        require(event['activeTeam'] == 'product' and card['team'] == 'product' and node_id == 'I01'
                and journal['status'] in {'pending', 'running'} and card['state'] == 'intake', 'A new card starts with the actual product intake only')
    if journal['status'] != 'completed':
        require(card['team'] == event['activeTeam'], 'An unfinished node cannot transfer a card to another team')
    if card['team'] != event['activeTeam']:
        require(node_id in {'P08', 'Q06', 'C01', 'C02', 'C03', 'C04', 'Q01', 'T01', 'T05'}, 'Team transfer requires a handover or return node')
    if card['columnId'] in {'ready-qa', 'ready-tech', 'technical-ready'}:
        required_node, required_next = {'ready-qa': ('P08', 'Q01'), 'ready-tech': ('Q06', 'T01'), 'technical-ready': ('T08', 'HOLD')}[card['columnId']]
        require(node_id == required_node and journal['status'] == 'completed', 'Readiness requires completed handover')
        require(card['nextNode'] == required_next, 'Documentation handover has the wrong next node')
        require(card['documentPath'] and card['ownerReference'] and not card['blocker'] and not card['openReturnIds'], 'Readiness has missing metadata or open blockers/returns')
        expected = {'ready-qa': ('qa', 'product-approved', 'start'),
                    'ready-tech': ('tech', 'qa-approved', 'start'),
                    'technical-ready': ('tech', 'technical-approved', 'done')}[card['columnId']]
        require((card['team'], card['state'], card['action']) == expected, 'Ready card team/state/action are inconsistent')
    check_gate(root, card, journal, repo_map)
    journal_name = f'requests/{rid}/runs/{mid}.json'
    require(card['journalPath'] == journal_name and card['lastMovementId'] == mid, 'Card must reference this movement journal')
    journal_path = local(root, journal_name, exists=False)
    require(not journal_path.exists(), 'Movement journal already exists; use the original event for retry')
    journal['progress'] = {'movementId': mid, 'eventSha256': sha_bytes(encoded(event)), 'card': card,
                           'previousJournalPath': existing['journalPath'] if existing else None,
                           'recordedBy': {'team': 'coordination', 'sourceReference': event['sourceReference']}}
    tracking_path = local(root, card['trackingPath'], exists=False)
    before_tracking = tracking_path.read_bytes() if tracking_path.exists() else b''
    require(existing is None or before_tracking, 'Existing card has no tracking history')
    history = {'movementId': mid, 'from': {k: existing[k] for k in ('team', 'state', 'currentNode')} if existing else None,
               'to': {k: card[k] for k in ('team', 'state', 'currentNode')},
               'reason': event['reason'], 'sourceReference': event['sourceReference'],
               'selectionReference': event['selectionReference'], 'journalPath': journal_name}
    prefix = before_tracking or f'# تاریخچهٔ پرونده {rid}\n\nوضعیت جاری در requests/board.json است.\n'.encode('utf-8')
    after_tracking = prefix+('\n### '+mid+'\n\n```json\n').encode('utf-8')+encoded(history)+b'```\n'
    next_board = copy.deepcopy(board)
    if existing:
        next_board['cards'][next(i for i,c in enumerate(board['cards']) if c['requestId'] == rid)] = card
    else:
        next_board['cards'].append(card)
    return {'event': event, 'eventSha256': sha_bytes(encoded(event)), 'journalPath': journal_name, 'journal': journal,
            'trackingPath': card['trackingPath'], 'trackingBeforeSha256': sha_bytes(before_tracking),
            'trackingAfter': after_tracking.decode('utf-8'), 'boardBeforeSha256': event['expectedBoardSha256'],
            'boardAfter': next_board}


def validate_pending(root, pending_path, plan):
    event = plan['event']
    rid, mid = event['requestId'], event['movementId']
    require(identifier(rid) and identifier(mid) and plan['eventSha256'] == sha_bytes(encoded(event)), 'Corrupt pending event')
    require(pending_path == local(root, f'requests/{rid}/runs/.progress-pending.json', exists=False), 'Pending transaction belongs to another request')
    require(plan['journalPath'] == f'requests/{rid}/runs/{mid}.json' and plan['trackingPath'] == f'requests/{rid}/tracking.md', 'Pending paths escape control-file scope')
    journal = dict(plan['journal']); progress = journal.pop('progress')
    require(journal == event['journal'] and progress['card'] == event['card'] and progress['eventSha256'] == plan['eventSha256'], 'Pending journal differs from original event')
    require(plan['boardBeforeSha256'] == event['expectedBoardSha256'], 'Pending board digest differs from original event')
    require(next((c for c in plan['boardAfter']['cards'] if c['requestId'] == rid), None) == event['card'], 'Pending board differs from original event')
    if digest(root/'requests/board.json') == plan['boardBeforeSha256']:
        before = read(root/'requests/board.json')
        after = copy.deepcopy(plan['boardAfter'])
        before['cards'] = [c for c in before['cards'] if c['requestId'] != rid]
        after['cards'] = [c for c in after['cards'] if c['requestId'] != rid]
        require(before == after, 'Pending event would change unrelated board cards')


def finish(root, pending_path, plan, repo_map):
    validate_pending(root, pending_path, plan)
    board_path = local(root, 'requests/board.json')
    journal_path = local(root, plan['journalPath'], exists=False)
    tracking_path = local(root, plan['trackingPath'], exists=False)
    journal_bytes = encoded(plan['journal'])
    tracking_bytes = plan['trackingAfter'].encode('utf-8')
    board_bytes = encoded(plan['boardAfter'])
    require(digest(board_path) in {plan['boardBeforeSha256'], sha_bytes(board_bytes)}, 'Board changed during interrupted transaction; reconcile without deleting pending evidence')
    before_tracking = tracking_path.read_bytes() if tracking_path.exists() else b''
    require(sha_bytes(before_tracking) in {plan['trackingBeforeSha256'], sha_bytes(tracking_bytes)}, 'Tracking changed during transaction')
    if journal_path.exists():
        require(journal_path.read_bytes() == journal_bytes, 'Immutable journal conflicts with retry')
    # Recheck gate bytes immediately before completing an interrupted handover.
    check_gate(root, plan['journal']['progress']['card'], plan['journal'], repo_map)
    if not journal_path.exists():
        atomic_write(journal_path, journal_bytes)
    if before_tracking != tracking_bytes:
        atomic_write(tracking_path, tracking_bytes)
    if board_path.read_bytes() != board_bytes:
        require(digest(board_path) == plan['boardBeforeSha256'], 'Board changed before commit')
        atomic_write(board_path, board_bytes)
    require(read(board_path) == plan['boardAfter'] and digest(tracking_path) == sha_bytes(tracking_bytes), 'Progress readback failed')
    pending_path.unlink()


def record(root, event, repo_map, apply=False):
    rid, mid = event.get('requestId'), event.get('movementId')
    require(identifier(rid) and identifier(mid), 'Invalid request or movement id')
    pending_path = local(root, f'requests/{rid}/runs/.progress-pending.json', exists=False)
    journal_path = local(root, f'requests/{rid}/runs/{mid}.json', exists=False)
    stamp = sha_bytes(encoded(event))
    if pending_path.exists():
        plan = read(pending_path)
        validate_pending(root, pending_path, plan)
        require(plan.get('eventSha256') == stamp, 'Retry the same pending event before creating another movement')
        if apply:
            finish(root, pending_path, plan, repo_map)
        return {'status': 'recovered' if apply else 'recovery-ready', 'journalPath': plan['journalPath']}
    if journal_path.exists():
        journal = read(journal_path)
        require(journal.get('progress', {}).get('eventSha256') == stamp, 'Movement id already belongs to a different event')
        board, _, _ = context(root)
        card = next((c for c in board['cards'] if c['requestId'] == rid), None)
        require(card == journal['progress']['card'] and mid in local(root, card['trackingPath']).read_text(encoding='utf-8'), 'An older movement cannot replace the current checkpoint')
        return {'status': 'already-recorded', 'journalPath': str(journal_path.relative_to(root))}
    plan = build(root, event, repo_map)
    if apply:
        atomic_write(pending_path, encoded(plan))
        finish(root, pending_path, plan, repo_map)
    return {'status': 'recorded' if apply else 'ready-to-record', 'journalPath': plan['journalPath'],
            'card': plan['journal']['progress']['card'],
            'writes': [str(pending_path.relative_to(root)), plan['journalPath'], plan['trackingPath'], 'requests/board.json'],
            'scope': 'Control metadata only; no approvals, receipts, or team documents are created.'}


def example(root):
    return {'schemaVersion': 1, 'requestId': '{{actual-request-id}}', 'movementId': '{{unique-movement-id}}',
            'expectedBoardSha256': digest(root/'requests/board.json'), 'activeTeam': 'product',
            'selectionReference': '{{actual-team-and-request-selection-message}}',
            'sourceReference': '{{actual-work-or-human-response-reference}}', 'reason': '{{reason-for-this-movement}}',
            'journal': read(root/'templates/shared/node-run.json'),
            'card': read(root/'templates/shared/board-card.json')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--event', help='JSON event file; see --example')
    mode.add_argument('--example', action='store_true')
    mode.add_argument('--recover', metavar='REQUEST_ID', help='Preview or finish the persisted interrupted transaction')
    parser.add_argument('--apply', action='store_true', help='Default is a read-only preview')
    parser.add_argument('--repository', action='append', default=[], metavar='ID=/absolute/path')
    args = parser.parse_args()
    try:
        root = find_root(args.root)
        if args.example:
            require(not args.apply, '--example cannot be applied')
            result = example(root)
        else:
            if args.recover:
                require(identifier(args.recover), 'Invalid recovery request id')
                pending = read(local(root, f'requests/{args.recover}/runs/.progress-pending.json'))
                event = pending['event']
            else:
                event = read(Path(args.event))
            repo_map = repositories(root, args.repository)
            if args.apply:
                with writer_lock(root):
                    result = record(root, event, repo_map, apply=True)
            else:
                result = record(root, event, repo_map)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
