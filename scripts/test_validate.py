"""Regression checks for mutable request state and the frozen workflow kit."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='workflow-validator-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)/'kit'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))

    def read_json(self, name):
        return json.loads((self.root/name).read_text())

    def write_json(self, name, data):
        (self.root/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

    def validate(self):
        result = subprocess.run(
            [sys.executable, 'scripts/validate.py'], cwd=self.root,
            capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0 if report['status'] == 'passed' else 1)
        return report

    def add_draft_card(self):
        request_id = 'validator-fixture'
        request = self.root/'requests'/request_id
        request.mkdir()
        for name in ('request.md', 'tracking.md'):
            (request/name).write_text('# Synthetic validator fixture\n')
        card = self.read_json('templates/shared/board-card.json')
        card.update(
            requestId=request_id, title='Synthetic validator fixture',
            requestPath=f'requests/{request_id}/request.md',
            trackingPath=f'requests/{request_id}/tracking.md',
            authorizationReference='Temporary fixture; no real request or approval',
        )
        board = self.read_json('requests/board.json')
        board['cards'].append(card)
        self.write_json('requests/board.json', board)
        return board


class RequestStateValidationTests(ValidatorFixture):
    def test_new_card_and_valid_movement_preserve_design_baseline(self):
        frozen = (self.root/'records/design-manifest.json').read_bytes()
        board = self.add_draft_card()
        self.assertEqual(self.validate()['errors'], [])
        board['cards'][-1].update(
            state='product-draft', action='continue', currentNode='P01', nextNode='P02',
        )
        self.write_json('requests/board.json', board)
        self.assertEqual(self.validate()['errors'], [])
        self.assertEqual((self.root/'records/design-manifest.json').read_bytes(), frozen)

    def test_invalid_card_is_still_rejected(self):
        board = self.add_draft_card()
        board['cards'][-1]['state'] = 'invalid-state'
        self.write_json('requests/board.json', board)
        self.assertIn('Invalid board value: validator-fixture/state', self.validate()['errors'])

    def test_changed_design_document_is_still_rejected(self):
        document = self.root/'docs/01-principles-and-roles.md'
        document.write_text(document.read_text()+'\nSynthetic unversioned change.\n')
        self.assertIn(
            'Design baseline changed: docs/01-principles-and-roles.md',
            self.validate()['errors'],
        )

    def test_operational_board_cannot_be_frozen_again(self):
        manifest = self.read_json('records/design-manifest.json')
        manifest['artifacts'].append({
            'path': 'requests/board.json',
            'sha256': hashlib.sha256((self.root/'requests/board.json').read_bytes()).hexdigest(),
        })
        self.write_json('records/design-manifest.json', manifest)
        approval = self.read_json('records/design-approval.json')
        approval['manifestSha256'] = hashlib.sha256(
            (self.root/'records/design-manifest.json').read_bytes(),
        ).hexdigest()
        self.write_json('records/design-approval.json', approval)
        self.assertIn(
            'Operational file in design baseline: requests/board.json',
            self.validate()['errors'],
        )

    def test_operational_board_cannot_enter_static_inventory(self):
        inventory = self.read_json('research/source-inventory.json')
        inventory['files'].append({
            'repository': 'product-workflow', 'path': 'requests/board.json',
            'sha256': hashlib.sha256((self.root/'requests/board.json').read_bytes()).hexdigest(),
        })
        self.write_json('research/source-inventory.json', inventory)
        self.assertIn(
            'Operational file in local source inventory: requests/board.json',
            self.validate()['errors'],
        )


class ModulePublicationTests(ValidatorFixture):
    """All identities/decisions below are synthetic fixtures in temporary copies."""

    def prepare_snapshot(self, request_id='module-fixture', revision='r1', base=None):
        folder = self.root/f'requests/{request_id}/technical/modules/demo/snapshot'
        folder.mkdir(parents=True)
        (folder/'README.md').write_text('# Synthetic module snapshot\n\nRevision '+revision+'.\n')
        plan_name = str((folder/'snapshot-plan.json').relative_to(self.root))
        plan = {'schemaVersion': 1, 'moduleId': 'demo', 'revisionId': revision,
                'baseRevision': base, 'observedImplementation': {
                    'status': 'unknown', 'sourceRevision': None, 'limitation': 'Synthetic fixture; no code inspected'},
                'artifacts': [{'path': 'README.md', 'sha256': hashlib.sha256((folder/'README.md').read_bytes()).hexdigest()}]}
        self.write_json(plan_name, plan)
        manifest_name = f'requests/{request_id}/technical-manifest.json'
        manifest = {'schemaVersion': 1, 'requestId': request_id, 'baselineId': revision+'-technical',
                    'stage': 'technical', 'parents': [], 'openBlockers': [],
                    'artifacts': [{'path': str(path.relative_to(self.root)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                                  for path in (folder/'README.md', folder/'snapshot-plan.json')]}
        self.write_json(manifest_name, manifest)
        approval_name = f'requests/{request_id}/approval.json'
        self.write_json(approval_name, {
            'schemaVersion': 1, 'requestId': request_id, 'baselineId': revision+'-technical',
            'gate': 'G-T', 'status': 'approved',
            'manifestSha256': hashlib.sha256((self.root/manifest_name).read_bytes()).hexdigest(),
            'requiredRoles': ['tech-lead'], 'decisions': [{
                'role': 'tech-lead', 'identity': 'Synthetic fixture role; no real person',
                'decision': 'approved', 'reference': 'temporary-fixture', 'text': 'Synthetic decision for checker testing only'}],
        })
        return plan_name, manifest_name, approval_name

    def publish_snapshot(self, sources, apply=True):
        command = [sys.executable, 'scripts/publish_module.py']
        for option, value in zip(('plan', 'manifest', 'approval'), sources):
            command += ['--'+option, value]
        if apply:
            command += ['--apply']
        return subprocess.run(command, cwd=self.root, capture_output=True, text=True)

    def test_approved_snapshot_preview_publication_and_retry(self):
        sources = self.prepare_snapshot()
        self.assertEqual(self.publish_snapshot(sources, apply=False).returncode, 0)
        self.assertFalse((self.root/'modules/demo').exists())
        self.assertEqual(self.publish_snapshot(sources).returncode, 0)
        self.assertEqual(self.validate()['errors'], [])
        pointer = (self.root/'modules/demo/current.json').read_bytes()
        self.assertEqual(self.publish_snapshot(sources).stdout.strip(), 'already-current')
        self.assertEqual((self.root/'modules/demo/current.json').read_bytes(), pointer)

    def test_pending_approval_cannot_publish(self):
        sources = self.prepare_snapshot()
        approval = self.read_json(sources[2])
        approval['status'] = 'pending'
        self.write_json(sources[2], approval)
        self.assertNotEqual(self.publish_snapshot(sources).returncode, 0)
        self.assertFalse((self.root/'modules/demo').exists())

    def test_symlink_destination_cannot_write_outside_module_scope(self):
        sources = self.prepare_snapshot()
        outside = self.root.parent/'other-scope'
        outside.mkdir()
        (self.root/'modules/demo').symlink_to(outside, target_is_directory=True)
        result = self.publish_snapshot(sources)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsafe module destination', result.stderr)
        self.assertEqual(list(outside.iterdir()), [])

    def test_unapproved_artifact_change_cannot_publish(self):
        sources = self.prepare_snapshot()
        (self.root/Path(sources[0]).parent/'README.md').write_text('# Changed outside approved bytes\n')
        self.assertNotEqual(self.publish_snapshot(sources).returncode, 0)
        self.assertFalse((self.root/'modules/demo').exists())

    def test_new_revision_keeps_history_and_rejects_stale_base(self):
        sources = self.prepare_snapshot()
        self.assertEqual(self.publish_snapshot(sources).returncode, 0)
        previous = self.read_json('modules/demo/current.json')
        second = self.prepare_snapshot('module-fixture-next', 'r2', {
            'revisionId': previous['revisionId'], 'manifestSha256': previous['manifestSha256']})
        self.assertEqual(self.publish_snapshot(second).returncode, 0)
        self.assertTrue((self.root/'modules/demo/revisions/r1/README.md').is_file())
        self.assertEqual(self.validate()['errors'], [])
        stale = self.prepare_snapshot('module-fixture-stale', 'r3', {
            'revisionId': previous['revisionId'], 'manifestSha256': previous['manifestSha256']})
        result = self.publish_snapshot(stale)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('return to T02', result.stderr)
        self.assertEqual(self.read_json('modules/demo/current.json')['revisionId'], 'r2')

    def test_published_design_tampering_is_detected(self):
        sources = self.prepare_snapshot()
        self.assertEqual(self.publish_snapshot(sources).returncode, 0)
        (self.root/'modules/demo/revisions/r1/README.md').write_text('# Tampered snapshot\n')
        self.assertTrue(any('Published artifact changed' in error for error in self.validate()['errors']))

    def test_implementation_without_revision_cannot_claim_acceptance(self):
        self.assertEqual(self.publish_snapshot(self.prepare_snapshot()).returncode, 0)
        pointer = self.read_json('modules/demo/current.json')
        folder = self.root/'modules/demo/implementation/observations'
        folder.mkdir(parents=True)
        record = self.read_json('templates/modules/implementation-observation.json')
        record.update(observationId='fixture', moduleId='demo', designRevisionId='r1',
                      designManifestSha256=pointer['manifestSha256'], status='accepted',
                      limitation='Synthetic negative fixture; no actual implementation')
        self.write_json('modules/demo/implementation/observations/fixture.json', record)
        self.write_json('modules/demo/implementation/current.json', {
            'observationId': 'fixture', 'sha256': hashlib.sha256((folder/'fixture.json').read_bytes()).hexdigest()})
        self.assertTrue(any('no source revision' in error for error in self.validate()['errors']))


if __name__ == '__main__':
    unittest.main()
