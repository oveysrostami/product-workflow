#!/usr/bin/env python3
"""Read-only structural/count checks. Does not certify question quality or human identity."""
import argparse
import json
import sys

from read_queue import concrete, find_root, identifier, local, read, require


QUESTION_FIELDS = {'id', 'revision', 'moduleId', 'topic', 'kind', 'prompt', 'rationale',
                   'options', 'recommendedOptionId', 'recommendationReason', 'sourceReferences'}
RESPONSE_FIELDS = {'id', 'questionId', 'questionRevision', 'respondentReference', 'reference',
                   'disposition', 'selectedOptionId', 'text', 'reason', 'supersedes'}


def inspect(data, request_id, require_answered=False):
    fields = {'schemaVersion', 'requestId', 'requestType', 'revisionId', 'definition',
              'impactReference', 'moduleIds', 'questions', 'questionHistory', 'responses'}
    require(isinstance(data, dict) and set(data) == fields, 'Invalid questionnaire fields')
    require(data['schemaVersion'] == 1 and data['requestId'] == request_id, 'Wrong questionnaire identity')
    require(data['requestType'] in {'new', 'feature', 'change'} and identifier(data['revisionId']), 'Invalid type/revision')
    definition = data['definition']
    require(isinstance(definition, dict) and set(definition) == {'summary', 'purpose', 'expectedOutcome', 'sourceReference'}
            and all(concrete(v) for v in definition.values()), 'Actual initial definition is required')
    modules = data['moduleIds']
    require(isinstance(modules, list) and modules and all(identifier(m) for m in modules)
            and len(set(modules)) == len(modules), 'A concrete unique module list is required')
    require(data['impactReference'] == 'product/feature-impact.md' if data['requestType'] == 'feature'
            else data['impactReference'] is None, 'Wrong feature impact reference')
    for field in ('questions', 'questionHistory', 'responses'):
        require(isinstance(data[field], list), 'Invalid '+field)

    def question(q):
        require(isinstance(q, dict) and set(q) == QUESTION_FIELDS, 'Invalid question fields')
        require(identifier(q['id']) and type(q['revision']) is int and q['revision'] > 0, 'Invalid question id/revision')
        require(q['moduleId'] is None or identifier(q['moduleId']), 'Invalid question module')
        require(all(concrete(q[k]) for k in ('topic', 'prompt', 'rationale')), 'Question text/rationale required')
        require(isinstance(q['sourceReferences'], list) and q['sourceReferences']
                and all(concrete(v) for v in q['sourceReferences']), 'Question source references required')
        require(isinstance(q['options'], list), 'Invalid options')
        if q['kind'] == 'single-choice':
            require(len(q['options']) == 4 and all(isinstance(o, dict) and set(o) == {'id', 'text'}
                    and concrete(o['text']) for o in q['options']), 'Exactly four real options required')
            require([o['id'] for o in q['options']] == ['A', 'B', 'C', 'D'], 'Option ids must be A/B/C/D')
            require(len({o['text'].strip() for o in q['options']}) == 4, 'Duplicate option text')
            require(q['recommendedOptionId'] is None or q['recommendedOptionId'] in {'A', 'B', 'C', 'D'}, 'Invalid recommendation')
            require((q['recommendedOptionId'] is None and q['recommendationReason'] is None)
                    or (q['recommendedOptionId'] is not None and concrete(q['recommendationReason'])), 'Recommendation needs a reason')
        else:
            require(q['kind'] == 'long-text' and q['options'] == [] and q['recommendedOptionId'] is None
                    and q['recommendationReason'] is None, 'Long text must have no options/recommendation')
        return q['id'], q['revision']

    versions, active = {}, {}
    for item in data['questionHistory']:
        require(isinstance(item, dict) and set(item) == {'question', 'reason', 'reference'}
                and concrete(item['reason']) and concrete(item['reference']), 'History needs actual reason/reference')
        q = item['question']; key = question(q)
        require(key not in versions, 'Duplicate historical question revision')
        versions[key] = q
    prompts = set()
    counts = {m: 0 for m in modules}
    for q in data['questions']:
        key = question(q)
        require(q['id'] not in active and key not in versions, 'Duplicate active question/revision')
        require(q['moduleId'] is None or q['moduleId'] in modules, 'Question outside current module list')
        prompt = ' '.join(q['prompt'].split())
        require(prompt not in prompts, 'Duplicate active question text')
        prompts.add(prompt)
        older = [revision for qid, revision in versions if qid == q['id']]
        require(not older or max(older) < q['revision'], 'Active revision must follow its history')
        versions[key] = q; active[q['id']] = key
        if q['moduleId'] is not None:
            counts[q['moduleId']] += 1
    if data['requestType'] == 'new':
        require(len(active) >= 50, 'A new module request requires at least 50 questions')
    elif data['requestType'] == 'feature':
        require(all(count >= 20 for count in counts.values()), 'Each feature module requires at least 20 questions: '+str(counts))
    else:
        require(active, 'A change request requires a nonempty complete questionnaire; size is scope-based')

    latest, answer_ids = {}, set()
    for answer in data['responses']:
        require(isinstance(answer, dict) and set(answer) == RESPONSE_FIELDS, 'Invalid response fields')
        require(identifier(answer['id']) and answer['id'] not in answer_ids, 'Duplicate/invalid answer id')
        require(identifier(answer['questionId']) and type(answer['questionRevision']) is int,
                'Invalid response question identity')
        key = answer['questionId'], answer['questionRevision']
        require(key in versions, 'Answer references an unknown question revision')
        require(concrete(answer['respondentReference']) and concrete(answer['reference']), 'Actual respondent/message reference required')
        previous = latest.get(key)
        require(answer['supersedes'] == (previous['id'] if previous else None), 'Response must supersede the latest answer of this revision')
        disposition, option, text = answer['disposition'], answer['selectedOptionId'], answer['text']
        require(disposition in {'answered', 'unknown', 'not-applicable'}, 'Invalid response disposition')
        require(text is None or concrete(text), 'Invalid response text')
        if disposition == 'answered':
            q = versions[key]
            require(option is None or (q['kind'] == 'single-choice' and option in {'A', 'B', 'C', 'D'}), 'Invalid selected option')
            require(option is not None or concrete(text), 'An actual choice or free-text answer is required')
            require(answer['reason'] is None, 'Reason field is reserved for N/A')
        else:
            require(option is None and concrete(text), 'Unknown/N/A needs the actual human text')
            require(concrete(answer['reason']) if disposition == 'not-applicable' else answer['reason'] is None,
                    'N/A needs a reason; unknown uses its text')
        latest[key] = answer; answer_ids.add(answer['id'])
    unanswered = [qid for qid, key in active.items() if key not in latest]
    open_decisions = [qid for qid, key in active.items() if key in latest and latest[key]['disposition'] == 'unknown']
    require(not require_answered or not unanswered, 'Unanswered current questions: '+', '.join(unanswered))
    return {'requestId': request_id, 'revisionId': data['revisionId'], 'requestType': data['requestType'],
            'totalQuestions': len(active), 'moduleCounts': counts, 'answeredCount': len(active)-len(unanswered),
            'unansweredQuestionIds': unanswered, 'openDecisionQuestionIds': open_decisions,
            'readyForInterview': not unanswered}


def check(root, request_id, require_answered=False):
    require(identifier(request_id), 'Invalid request id')
    prefix = 'requests/'+request_id+'/'
    data = read(local(root, prefix+'product/questionnaire.json'))
    report = inspect(data, request_id, require_answered)
    if data['requestType'] == 'feature':
        local(root, prefix+data['impactReference'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    parser.add_argument('--request', required=True)
    parser.add_argument('--require-answered', action='store_true')
    args = parser.parse_args()
    try:
        report = check(find_root(args.root), args.request, args.require_answered)
        print(json.dumps({'status': 'passed', **report}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
