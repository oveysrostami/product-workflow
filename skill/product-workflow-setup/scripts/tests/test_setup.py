"""Exercise relocated read-only binding; all Backends here are synthetic fixtures."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'setup_project.py'
SPEC = importlib.util.spec_from_file_location('workflow_setup_test_subject', SCRIPT)
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)


class ReadOnlySetupTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='workflow-setup-fixture-')
        self.addCleanup(directory.cleanup)
        self.parent = Path(directory.name)
        self.root = self.parent / 'product-workflow'
        self.backend = self.parent / 'core_backend'
        for name in ('AGENTS.md', 'workflows/graph.json', 'requests/board.json'):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{}\n')
        self.backend.mkdir()
        (self.backend / 'AGENTS.md').write_text('# Synthetic Backend rules\n')
        (self.backend / 'credential.env').write_text('SYNTHETIC_SECRET=fixture-secret-do-not-copy\n')
        (self.backend / 'modules/demo').mkdir(parents=True)

    def snapshot(self, root):
        return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mode)
                for p in root.rglob('*') if p.is_file() and not p.is_symlink()}

    def cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), *arguments],
                              cwd=self.parent, capture_output=True, text=True)

    def create_plan(self, state='completed', match=True):
        folder = self.backend / '_agent-doc'
        folder.mkdir(exist_ok=True)
        profile = {'host': 'application-host', 'composition': 'base', 'authentication': 'none',
                   'role': 'web', 'productId': 'fixture', 'environment': 'test',
                   'infrastructure': {'cache': 'redis', 'metrics': 'prometheus'},
                   'unexpectedSecret': 'fixture-secret-do-not-copy'}
        plan = {'schemaVersion': 1, 'kind': 'boilerplate-deployment-profile-plan', 'profile': profile}
        (self.backend / 'setup.plan.json').write_text(json.dumps(plan))
        record = {'schemaVersion': 1, 'state': state, 'productId': 'fixture', 'environment': 'test',
                  'profileSha256': hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest()
                  if match else '0'*64,
                  'outputs': {'plan': 'setup.plan.json', 'environment': 'credential.env'}}
        (folder / 'project-initialization.json').write_text(json.dumps(record))

    def test_preview_and_inspection_never_mutate_either_repository(self):
        before = self.snapshot(self.parent)
        result = self.cli('--backend-name', 'core_backend', '--source-reference', 'synthetic-fixture')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'preview')
        self.assertEqual(report['observation']['resolvedPath'], str(self.backend.resolve()))
        self.assertEqual(before, self.snapshot(self.parent))

    def test_apply_writes_only_local_binding_and_retry_preserves_source(self):
        before_backend = self.snapshot(self.backend)
        before_workflow = self.snapshot(self.root)
        result = self.cli('--backend-name', 'core_backend', '--source-reference', 'synthetic-first', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(self.backend), before_backend)
        self.assertEqual(set(self.snapshot(self.root)) - set(before_workflow), {'project/backend.json'})
        frozen = (self.root / setup.BINDING).read_bytes()
        retry = self.cli('--backend-name', 'core_backend', '--source-reference', 'synthetic-second', '--apply')
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(json.loads(retry.stdout)['status'], 'already-configured')
        self.assertEqual((self.root / setup.BINDING).read_bytes(), frozen)
        inspect = self.cli('--inspect')
        self.assertEqual(inspect.returncode, 0, inspect.stderr)
        self.assertEqual(self.snapshot(self.backend), before_backend)

    def test_missing_backend_or_invalid_name_cannot_create_binding(self):
        before = self.snapshot(self.parent)
        for name in ('missing_backend', '../core_backend', '/tmp/core_backend', '.', '..',
                     'core_backend/sub', 'core_backend\\sub', 'product-workflow', ' core_backend'):
            result = self.cli('--backend-name', name, '--source-reference', 'synthetic-fixture', '--apply')
            self.assertNotEqual(result.returncode, 0, name)
        self.assertEqual(before, self.snapshot(self.parent))

    def test_symlink_backend_and_workflow_output_cannot_escape(self):
        (self.parent / 'alias').symlink_to(self.backend, target_is_directory=True)
        result = self.cli('--backend-name', 'alias', '--source-reference', 'synthetic-fixture', '--apply')
        self.assertNotEqual(result.returncode, 0)
        (self.root / 'project').symlink_to(self.backend, target_is_directory=True)
        before = self.snapshot(self.backend)
        result = self.cli('--backend-name', 'core_backend', '--source-reference', 'synthetic-fixture', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(self.backend), before)

    def test_changed_binding_or_access_cannot_be_accepted(self):
        setup.configure(self.root, 'core_backend', 'synthetic-fixture', True)
        other = self.parent / 'other_backend'
        other.mkdir()
        (other / 'AGENTS.md').write_text('# Other synthetic Backend\n')
        before = self.snapshot(self.parent)
        result = self.cli('--backend-name', 'other_backend', '--source-reference', 'synthetic-fixture', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(self.parent), before)
        path = self.root / setup.BINDING
        binding = json.loads(path.read_text())
        binding['access'] = 'read-write'
        path.write_text(json.dumps(binding))
        result = self.cli('--inspect')
        self.assertNotEqual(result.returncode, 0)

    def test_recorded_setup_choices_never_claim_runtime_or_copy_secrets(self):
        self.create_plan()
        before = self.snapshot(self.backend)
        report = setup.configure(self.root, 'core_backend', 'synthetic-fixture')['observation']
        self.assertTrue(report['setup']['recordAndPlanMatch'])
        self.assertEqual(report['setup']['recordedState'], 'completed')
        self.assertEqual(report['setup']['selections']['infrastructure.cache'], 'redis')
        self.assertEqual(report['setup']['runtimeActivation'], 'unknown')
        self.assertEqual(report['setup']['backendPreflight'], 'not-executed')
        self.assertNotIn('fixture-secret-do-not-copy', json.dumps(report))
        self.assertEqual(self.snapshot(self.backend), before)

    def test_stale_or_partial_setup_is_reported_without_repair(self):
        for state, match in (('completed', False), ('failed', True), (['invalid'], True)):
            self.create_plan(state, match)
            before = self.snapshot(self.backend)
            report = setup.inspect_backend(self.root, 'core_backend')['setup']
            self.assertEqual(report['recordAndPlanMatch'], match)
            self.assertEqual(report['runtimeActivation'], 'unknown')
            if state == ['invalid']:
                self.assertEqual(report['recordedState'], 'unknown')
            self.assertEqual(self.snapshot(self.backend), before)

    def test_unsafe_plan_and_inspect_apply_are_rejected(self):
        self.create_plan()
        path = self.backend / '_agent-doc/project-initialization.json'
        record = json.loads(path.read_text())
        record['outputs']['plan'] = '../outside.json'
        path.write_text(json.dumps(record))
        result = self.cli('--backend-name', 'core_backend', '--source-reference', 'synthetic-fixture', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('fixture-secret-do-not-copy', result.stderr)
        self.assertFalse((self.root / setup.BINDING).exists())
        result = self.cli('--inspect', '--apply')
        self.assertNotEqual(result.returncode, 0)

    def test_backend_scripts_are_not_executed_or_imported(self):
        scripts = self.backend / 'scripts/agent'
        scripts.mkdir(parents=True)
        (scripts / 'init_project.py').write_text("raise RuntimeError('Must never execute or import Backend code')\n")
        before = self.snapshot(self.backend)
        setup.configure(self.root, 'core_backend', 'synthetic-fixture', True)
        self.assertEqual(before, self.snapshot(self.backend))
        self.assertFalse(list(self.backend.rglob('__pycache__')))


if __name__ == '__main__':
    unittest.main()
