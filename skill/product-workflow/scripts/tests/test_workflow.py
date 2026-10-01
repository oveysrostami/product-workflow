"""Behavior tests in disposable checkouts; fixture decisions are not real approvals.

Run from an actual workflow checkout:
python3 -m unittest discover -s /path/to/skill/scripts/tests -v
"""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import read_queue as rq
import record_progress as rp

SOURCE = rq.find_root()


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='product-workflow-skill-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'workflow'
        for name in rq.MARKERS:
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE/name, target)
        board = rq.read(self.root/'requests/board.json')
        board['cards'] = []
        self.write('requests/board.json', board)
        self.repos = rq.repositories(self.root, [])

    def write(self, name, data):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(rp.encoded(data) if not isinstance(data, str) else data.encode())
        return path

    def card(self, rid='REQ-test'):
        card = rq.read(self.root/'templates/shared/board-card.json')
        card.update(requestId=rid, title='Synthetic test request', requestPath=f'requests/{rid}/request.md',
                    trackingPath=f'requests/{rid}/tracking.md', ownerReference='Fixture appointment only',
                    authorizationReference='Synthetic fixture, not a real user instruction')
        self.write(card['requestPath'], '# Synthetic fixture\n')
        self.write(card['trackingPath'], '# Synthetic tracking\nMOVE-fixture\n')
        return card

    def put_card(self, card):
        board = rq.read(self.root/'requests/board.json')
        board['cards'] = [c for c in board['cards'] if c['requestId'] != card['requestId']]+[card]
        self.write('requests/board.json', board)

    def baseline(self, card, stage, parents=None, status='approved'):
        rid = card['requestId']
        artifact_name = f'requests/{rid}/{stage}/handover.md'
        artifact = self.write(artifact_name, '# Synthetic handover\nTest fixture only.\n')
        manifest_name = f'requests/{rid}/baselines/{stage}-1.json'
        manifest = {'schemaVersion': 1, 'requestId': rid, 'baselineId': f'{rid}-{stage}-1', 'stage': stage,
                    'parents': parents or [], 'openBlockers': [],
                    'artifacts': [{'repository': self.root.name, 'path': artifact_name, 'sha256': rq.digest(artifact),
                                   'revision': 'synthetic-snapshot', 'role': 'canonical'}]}
        path = self.write(manifest_name, manifest)
        approval_name = f'requests/{rid}/approvals/{stage}-1.json'
        self.write(approval_name, {'schemaVersion': 1, 'requestId': rid, 'approvalId': 'synthetic',
                   'gate': rq.STAGES[stage], 'status': status, 'baselineId': manifest['baselineId'],
                   'manifestPath': manifest_name, 'manifestSha256': rq.digest(path), 'requiredRoles': ['fixture-owner'],
                   'decisions': [{'role': 'fixture-owner', 'decision': 'approved', 'identity': 'Synthetic person',
                                  'reference': 'Synthetic temporary fixture; no real approval', 'text': 'Fixture decision only'}]})
        card['baselines'][stage] = {'manifestPath': manifest_name, 'approvalPath': approval_name, 'receiptPath': None}
        return {'baselineId': manifest['baselineId'], 'manifestSha256': rq.digest(path)}

    def ready(self, team='qa'):
        card = self.card()
        p = self.baseline(card, 'product')
        if team == 'tech':
            self.baseline(card, 'qa', parents=[p])
        node, nxt = ('P08', 'Q01') if team == 'qa' else ('Q06', 'T01')
        card.update(team=team, state='product-approved' if team=='qa' else 'qa-approved', columnId='ready-'+team,
                    currentNode=node, nextNode=nxt, resumeNode=None, action='start',
                    documentPath=f'requests/{card["requestId"]}/{"product" if team=="qa" else "qa"}/handover.md',
                    journalPath=f'requests/{card["requestId"]}/runs/MOVE-fixture.json', lastMovementId='MOVE-fixture')
        self.write(card['journalPath'], {'requestId': card['requestId'], 'nodeId': node, 'nextNode': nxt,
                                        'resumeNode': None, 'status': 'completed'})
        self.put_card(card)
        return card

    def event(self, card=None, mid='MOVE-1'):
        card = copy.deepcopy(card or self.card())
        rid = card['requestId']
        card.update(currentNode='I01', nextNode=None, resumeNode='I01', action='continue',
                    journalPath=f'requests/{rid}/runs/{mid}.json', lastMovementId=mid)
        journal = rq.read(self.root/'templates/shared/node-run.json')
        journal.update(requestId=rid, nodeId='I01', status='running', nextNode=None, resumeNode='I01',
                       executor={'type': 'AI', 'role': 'Product writer', 'identity': 'Synthetic test agent', 'team': 'product'},
                       workUnit={'targetType': 'request', 'targetId': rid, 'sliceId': None, 'taskId': None},
                       writeScope={'allowedPaths': [f'requests/{rid}/request.md'], 'ownershipReference': 'AGENTS.md',
                                   'reviewedOutputPaths': [], 'outOfScopeChanges': []})
        return {'schemaVersion': 1, 'requestId': rid, 'movementId': mid,
                'expectedBoardSha256': rq.digest(self.root/'requests/board.json'), 'activeTeam': 'product',
                'selectionReference': 'Synthetic selection only', 'sourceReference': 'Synthetic source only',
                'reason': 'Synthetic intake checkpoint', 'journal': journal, 'card': card}

    def test_empty_queue_has_no_writes(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = rq.queue(self.root, 'qa', self.repos)
        self.assertFalse(any(result['groups'].values()))
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_only_frozen_approved_product_enters_candidate_queue(self):
        card = self.ready()
        self.assertEqual(len(rq.queue(self.root, 'qa', self.repos)['groups']['readyCandidates']), 1)
        approval_path = card['baselines']['product']['approvalPath']
        approval = rq.read(self.root/approval_path); approval['status'] = 'pending'; self.write(approval_path, approval)
        result = rq.queue(self.root, 'qa', self.repos)['groups']
        self.assertFalse(result['readyCandidates'])
        self.assertIn('G-P', result['blocked'][0]['issues'][0])

    def test_changed_artifact_is_blocked(self):
        card = self.ready()
        self.write(card['documentPath'], '# Changed after approval\n')
        self.assertIn('Changed artifact', rq.queue(self.root, 'qa', self.repos)['groups']['blocked'][0]['issues'][0])

    def test_stale_product_parent_blocks_technical_queue(self):
        card = self.ready('tech')
        self.assertEqual(len(rq.queue(self.root, 'tech', self.repos)['groups']['readyCandidates']), 1)
        binding = card['baselines']['qa']; manifest = rq.read(self.root/binding['manifestPath'])
        manifest['parents'][0]['manifestSha256'] = '0'*64
        self.write(binding['manifestPath'], manifest)
        approval = rq.read(self.root/binding['approvalPath']); approval['manifestSha256'] = rq.digest(self.root/binding['manifestPath'])
        self.write(binding['approvalPath'], approval)
        self.assertIn('stale', rq.queue(self.root, 'tech', self.repos)['groups']['blocked'][0]['issues'][0])

    def test_returned_work_is_separate_from_ready(self):
        card = self.ready(); card.update(columnId='returned', action='return', openReturnIds=['RET-1'], blocker='Fixture missing oracle')
        self.put_card(card)
        result = rq.queue(self.root, 'qa', self.repos)['groups']
        self.assertFalse(result['readyCandidates']); self.assertEqual(len(result['returned']), 1)

    def test_selection_is_not_receipt(self):
        card = self.ready()
        event = self.event(card, 'MOVE-receive')
        event['activeTeam'] = 'qa'
        event['card'].update(columnId='qa-design', state='qa-design', currentNode='Q01', nextNode='Q02', resumeNode=None)
        event['journal'].update(nodeId='Q01', status='completed', nextNode='Q02', resumeNode=None,
                                decisionReference='Synthetic selected item only',
                                executor={'type': 'Human', 'role': 'QA owner', 'identity': 'Synthetic person', 'team': 'qa'})
        with self.assertRaisesRegex(ValueError, 'actual receipt'):
            rp.record(self.root, event, self.repos)

    def test_preview_apply_retry_and_other_cards_preserved(self):
        other = self.card('REQ-other'); self.put_card(other)
        event = self.event()
        board_before = (self.root/'requests/board.json').read_bytes()
        self.assertEqual(rp.record(self.root, event, self.repos)['status'], 'ready-to-record')
        self.assertEqual((self.root/'requests/board.json').read_bytes(), board_before)
        self.assertFalse((self.root/event['card']['journalPath']).exists())
        self.assertEqual(rp.record(self.root, event, self.repos, True)['status'], 'recorded')
        tracking = (self.root/event['card']['trackingPath']).read_bytes()
        self.assertEqual(rp.record(self.root, event, self.repos, True)['status'], 'already-recorded')
        self.assertEqual((self.root/event['card']['trackingPath']).read_bytes(), tracking)
        board = rq.read(self.root/'requests/board.json')
        self.assertEqual(next(c for c in board['cards'] if c['requestId']=='REQ-other'), other)

    def test_waiting_checkpoint_resumes_same_node(self):
        event = self.event(); rp.record(self.root, event, self.repos, True)
        second = self.event(event['card'], 'MOVE-2')
        second['journal']['status'] = 'waiting-human'; second['card'].update(action='waiting', columnId='waiting')
        rp.record(self.root, second, self.repos, True)
        self.assertEqual(rq.queue(self.root, 'product', self.repos)['groups']['waiting'][0]['card']['resumeNode'], 'I01')
        third = self.event(second['card'], 'MOVE-3')
        third['journal'].update(status='completed', nextNode='I02', resumeNode=None)
        third['card'].update(nextNode='I02', resumeNode=None, columnId='product-draft')
        self.assertEqual(rp.record(self.root, third, self.repos, True)['status'], 'recorded')

    def test_stale_board_rejected_without_journal_write(self):
        event = self.event(); self.put_card(self.card('REQ-concurrent'))
        with self.assertRaisesRegex(ValueError, 'Board changed'):
            rp.record(self.root, event, self.repos, True)
        self.assertFalse((self.root/event['card']['journalPath']).exists())

    def test_path_escape_and_symlink_rejected(self):
        event = self.event(); event['card']['trackingPath'] = '../outside.md'
        with self.assertRaisesRegex(ValueError, 'trackingPath'):
            rp.record(self.root, event, self.repos, True)
        event = self.event(); runs = self.root/'requests/REQ-test/runs'
        outside = Path(self.tmp.name)/'outside'; outside.mkdir(); runs.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            rp.record(self.root, event, self.repos, True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_interrupted_write_recovers_same_event(self):
        event = self.event(); original = rp.atomic_write
        def fail_tracking(path, data):
            if path.name == 'tracking.md':
                raise OSError('Synthetic interruption after journal')
            original(path, data)
        with patch.object(rp, 'atomic_write', side_effect=fail_tracking):
            with self.assertRaisesRegex(OSError, 'Synthetic interruption'):
                rp.record(self.root, event, self.repos, True)
        self.assertTrue((self.root/'requests/REQ-test/runs/.progress-pending.json').exists())
        recovery = rq.queue(self.root, 'product', self.repos)['recoveryRequired']
        self.assertEqual(recovery[0]['requestId'], 'REQ-test')
        process = subprocess.run([sys.executable, str(Path(rp.__file__)), '--root', str(self.root),
                                  '--recover', 'REQ-test', '--apply'], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stdout+process.stderr)
        self.assertEqual(json.loads(process.stdout)['status'], 'recovered')
        self.assertFalse((self.root/'requests/REQ-test/runs/.progress-pending.json').exists())
        self.assertEqual(rp.record(self.root, event, self.repos, True)['status'], 'already-recorded')

    def test_wrong_team_cannot_continue_card(self):
        event = self.event(); rp.record(self.root, event, self.repos, True)
        second = self.event(event['card'], 'MOVE-2'); second['activeTeam'] = 'qa'
        with self.assertRaisesRegex(ValueError, 'Active team'):
            rp.record(self.root, second, self.repos, True)

    def test_corrupt_recovery_cannot_write_team_document(self):
        event = self.event(); original = rp.atomic_write
        def interrupt(path, data):
            if path.name == 'tracking.md':
                raise OSError('Synthetic interruption')
            original(path, data)
        with patch.object(rp, 'atomic_write', side_effect=interrupt):
            with self.assertRaises(OSError):
                rp.record(self.root, event, self.repos, True)
        pending_path = self.root/'requests/REQ-test/runs/.progress-pending.json'
        pending = rq.read(pending_path); pending['journalPath'] = event['card']['requestPath']
        pending_path.write_bytes(rp.encoded(pending))
        before = (self.root/event['card']['requestPath']).read_bytes()
        with self.assertRaisesRegex(ValueError, 'control-file scope'):
            rp.record(self.root, event, self.repos, True)
        self.assertEqual((self.root/event['card']['requestPath']).read_bytes(), before)

    def test_cli_discovers_parent_repository_without_hardcoded_path(self):
        process = subprocess.run([sys.executable, str(Path(rq.__file__)), '--team', 'qa'],
                                  cwd=self.root/'requests', capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stdout+process.stderr)
        self.assertEqual(json.loads(process.stdout)['root'], str(self.root.resolve()))

    def test_skipping_graph_node_is_rejected(self):
        event = self.event(); rp.record(self.root, event, self.repos, True)
        second = self.event(event['card'], 'MOVE-2')
        second['journal'].update(status='completed', nextNode='P07', resumeNode=None)
        second['card'].update(nextNode='P07', resumeNode=None)
        with self.assertRaisesRegex(ValueError, 'Transition'):
            rp.record(self.root, second, self.repos, True)

    def review_event(self, node, team, next_node=None, human=False, reference=None):
        """A synthetic resumable review checkpoint; no real review or approval."""
        card = self.card()
        card.update(team=team, currentNode=node, nextNode=None, resumeNode=node,
                    journalPath=f'requests/{card["requestId"]}/runs/MOVE-fixture.json',
                    lastMovementId='MOVE-fixture', action='continue')
        self.write(card['journalPath'], {'requestId': card['requestId'], 'nodeId': node,
                   'nextNode': None, 'resumeNode': node, 'status': 'running'})
        self.put_card(card)
        event = self.event(card)
        event['activeTeam'] = team
        event['card'].update(currentNode=node, nextNode=next_node,
                             resumeNode=None if next_node else node)
        event['journal'].update(nodeId=node, status='completed' if next_node else 'waiting-human',
                                nextNode=next_node, resumeNode=None if next_node else node,
                                executor={'type': 'Human' if human else 'AI',
                                          'role': 'Fixture reviewer', 'identity': 'Synthetic reviewer', 'team': team},
                                decisionReference=reference)
        return event

    def test_document_review_cannot_skip_human_review(self):
        for ai, human, after, team in [('P05', 'P12', 'P06', 'product'),
                                       ('Q04', 'Q09', 'Q05', 'qa'),
                                       ('T06', 'T12', 'T07', 'tech')]:
            with self.subTest(node=ai):
                event = self.review_event(ai, team, after)
                with self.assertRaisesRegex(ValueError, 'Transition'):
                    rp.build(self.root, event, self.repos)
                event['card']['nextNode'] = human
                event['journal']['nextNode'] = human
                rp.build(self.root, event, self.repos)

    def test_technical_documentation_handover_cannot_launch_backend(self):
        event = self.review_event('T08', 'tech', 'D01')
        before = (self.root/'requests/board.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'must HOLD'):
            rp.record(self.root, event, self.repos, True)
        self.assertEqual((self.root/'requests/board.json').read_bytes(), before)
        self.assertFalse((self.root/event['card']['journalPath']).exists())

    def test_human_review_needs_human_executor_and_decision(self):
        for node, after, team in [('P12', 'P06', 'product'), ('Q09', 'Q05', 'qa'),
                                  ('T12', 'T07', 'tech')]:
            with self.subTest(node=node):
                event = self.review_event(node, team, after, reference='Fixture decision only')
                with self.assertRaisesRegex(ValueError, 'actual human decision reference'):
                    rp.build(self.root, event, self.repos)
                event['journal']['executor']['type'] = 'Human'
                event['journal']['decisionReference'] = None
                with self.assertRaisesRegex(ValueError, 'actual human decision reference'):
                    rp.build(self.root, event, self.repos)
                event['journal']['decisionReference'] = 'Synthetic actual decision reference; fixture only'
                rp.build(self.root, event, self.repos)

    def test_waiting_human_review_preserves_checkpoint(self):
        for node, team in [('P12', 'product'), ('Q09', 'qa'), ('T12', 'tech')]:
            with self.subTest(node=node):
                event = self.review_event(node, team)
                rp.build(self.root, event, self.repos)
                event['card']['resumeNode'] = 'P04'
                event['journal']['resumeNode'] = 'P04'
                with self.assertRaisesRegex(ValueError, 'same node'):
                    rp.build(self.root, event, self.repos)

    def test_approval_files_never_written_by_recorder(self):
        event = self.event(); rp.record(self.root, event, self.repos, True)
        request = self.root/'requests/REQ-test'
        self.assertFalse((request/'approvals').exists())
        self.assertFalse((request/'receipts').exists())
        self.assertFalse((request/'qa').exists())
        self.assertFalse((request/'technical').exists())


if __name__ == '__main__':
    unittest.main()
