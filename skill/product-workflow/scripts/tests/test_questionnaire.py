"""Structural/count and continuation checks using synthetic questionnaire data."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_questionnaire import check, inspect
from record_progress import check_gate


def questionnaire(kind='new', modules=('alpha',), sizes=None):
    sizes = sizes or ([50] if kind == 'new' else [20]*len(modules))
    questions = []
    for module, size in zip(modules, sizes):
        for number in range(size):
            questions.append({'id': f'QNR-{len(questions)+1:03}', 'revision': 1, 'moduleId': module,
                              'topic': 'Synthetic behavior topic', 'kind': 'single-choice',
                              'prompt': f'Synthetic {module} question {number}?', 'rationale': 'Synthetic distinct decision',
                              'options': [{'id': choice, 'text': 'Synthetic option '+choice} for choice in 'ABCD'],
                              'recommendedOptionId': 'A', 'recommendationReason': 'Synthetic recommendation only',
                              'sourceReferences': ['Synthetic user definition']})
    return {'schemaVersion': 1, 'requestId': 'REQ-test', 'requestType': kind, 'revisionId': 'QNR-v1',
            'definition': {'summary': 'Synthetic module/feature', 'purpose': 'Synthetic outcome',
                           'expectedOutcome': 'Synthetic observable result', 'sourceReference': 'Fixture only'},
            'impactReference': 'product/feature-impact.md' if kind == 'feature' else None,
            'moduleIds': list(modules), 'questions': questions, 'questionHistory': [], 'responses': []}


def response(q, number):
    return {'id': f'ANS-{number:03}', 'questionId': q['id'], 'questionRevision': q['revision'],
            'respondentReference': 'Synthetic appointed product owner', 'reference': 'Fixture message '+str(number),
            'disposition': 'answered', 'selectedOptionId': 'B', 'text': None, 'reason': None, 'supersedes': None}


class QuestionnaireTests(unittest.TestCase):
    def test_new_threshold_is_fifty_and_recommendations_are_not_answers(self):
        data = questionnaire(sizes=[49])
        with self.assertRaisesRegex(ValueError, 'at least 50'):
            inspect(data, 'REQ-test')
        data = questionnaire()
        report = inspect(data, 'REQ-test')
        self.assertEqual(report['totalQuestions'], 50)
        self.assertEqual(report['answeredCount'], 0)
        self.assertFalse(report['readyForInterview'])

    def test_change_has_questionnaire_without_inventing_feature_quota(self):
        data = questionnaire('change', sizes=[2])
        self.assertEqual(inspect(data, 'REQ-test')['totalQuestions'], 2)
        with self.assertRaisesRegex(ValueError, 'Unanswered'):
            inspect(data, 'REQ-test', True)
        data['responses'] = [response(q, n) for n, q in enumerate(data['questions'], 1)]
        self.assertTrue(inspect(data, 'REQ-test', True)['readyForInterview'])
        data['questions'] = []; data['responses'] = []
        with self.assertRaisesRegex(ValueError, 'nonempty'):
            inspect(data, 'REQ-test')

    def test_feature_quota_is_per_module_and_shared_questions_do_not_count(self):
        data = questionnaire('feature', ('alpha', 'beta'), [20, 19])
        shared = copy.deepcopy(data['questions'][0]); shared.update(id='SHARED-01', moduleId=None, prompt='Shared synthetic question?')
        data['questions'].append(shared)
        with self.assertRaisesRegex(ValueError, 'Each feature module'):
            inspect(data, 'REQ-test')
        data['questions'][-1]['moduleId'] = 'beta'
        self.assertEqual(inspect(data, 'REQ-test')['moduleCounts'], {'alpha': 20, 'beta': 20})

    def test_partial_answers_and_unknown_then_interview(self):
        data = questionnaire()
        data['responses'] = [response(q, n) for n, q in enumerate(data['questions'][:3], 1)]
        report = inspect(data, 'REQ-test')
        self.assertEqual(report['unansweredQuestionIds'][0], 'QNR-004')
        with self.assertRaisesRegex(ValueError, 'Unanswered'):
            inspect(data, 'REQ-test', True)
        data['responses'] = [response(q, n) for n, q in enumerate(data['questions'], 1)]
        data['responses'][0].update(disposition='unknown', selectedOptionId=None, text='Synthetic human has not decided')
        report = inspect(data, 'REQ-test', True)
        self.assertTrue(report['readyForInterview'])
        self.assertEqual(report['openDecisionQuestionIds'], ['QNR-001'])

    def test_answer_revision_preserves_history_and_requires_linear_supersedes(self):
        data = questionnaire(); first = response(data['questions'][0], 1)
        second = {**first, 'id': 'ANS-002', 'selectedOptionId': 'C'}
        data['responses'] = [first, second]
        with self.assertRaisesRegex(ValueError, 'supersede'):
            inspect(data, 'REQ-test')
        second['supersedes'] = first['id']
        before = copy.deepcopy(data)
        self.assertEqual(inspect(data, 'REQ-test')['answeredCount'], 1)
        self.assertEqual(data, before)

    def test_changed_question_invalidates_old_answer_without_deleting_it(self):
        data = questionnaire(); q = data['questions'][0]
        data['responses'] = [response(q, 1)]
        data['questionHistory'] = [{'question': copy.deepcopy(q), 'reason': 'Synthetic scope changed', 'reference': 'Fixture change message'}]
        q.update(revision=2, prompt='Synthetic revised behavior question?')
        report = inspect(data, 'REQ-test')
        self.assertIn(q['id'], report['unansweredQuestionIds'])
        self.assertEqual(len(data['responses']), 1)

    def test_four_options_long_text_and_actual_answer_references(self):
        data = questionnaire(); q = data['questions'][0]
        q['options'].append({'id': 'E', 'text': 'Extra option'})
        with self.assertRaisesRegex(ValueError, 'four'):
            inspect(data, 'REQ-test')
        q.update(kind='long-text', options=[], recommendedOptionId=None, recommendationReason=None)
        answer = response(q, 1); answer.update(selectedOptionId=None, text='Synthetic actual explanation')
        data['responses'] = [answer]
        self.assertEqual(inspect(data, 'REQ-test')['answeredCount'], 1)
        answer['reference'] = None
        with self.assertRaisesRegex(ValueError, 'reference'):
            inspect(data, 'REQ-test')

    def test_duplicate_questions_cannot_fill_quota(self):
        data = questionnaire()
        data['questions'][-1]['prompt'] = data['questions'][0]['prompt']
        with self.assertRaisesRegex(ValueError, 'Duplicate active question text'):
            inspect(data, 'REQ-test')

    def test_disk_checks_and_progress_cannot_bypass_unanswered_questions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); product = root/'requests/REQ-test/product'; product.mkdir(parents=True)
            path = product/'questionnaire.json'; data = questionnaire('feature')
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'Missing file'):
                check(root, 'REQ-test')
            (product/'feature-impact.md').write_text('Synthetic evidence only')
            before = path.read_bytes()
            check_gate(root, {'requestId': 'REQ-test'}, {'status': 'completed', 'nodeId': 'P09', 'nextNode': 'P10'}, {})
            with self.assertRaisesRegex(ValueError, 'Unanswered'):
                check_gate(root, {'requestId': 'REQ-test'}, {'status': 'completed', 'nodeId': 'P10', 'nextNode': 'P02'}, {})
            self.assertEqual(path.read_bytes(), before)
            data['responses'] = [response(q, n) for n, q in enumerate(data['questions'], 1)]
            path.write_text(json.dumps(data))
            check_gate(root, {'requestId': 'REQ-test'}, {'status': 'completed', 'nodeId': 'P10', 'nextNode': 'P02'}, {})


if __name__ == '__main__':
    unittest.main()
