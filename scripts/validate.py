#!/usr/bin/env python3
"""Check this documentation kit. Does not certify approvals or backend behavior."""
import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from render_workflows import documents
from publish_module import digest, local, read, reading_entry, verify_revision
ROOT = Path(__file__).resolve().parents[1]
errors = []
stats = {'markdownFiles': 0, 'localLinks': 0, 'diagrams': 0, 'nodes': 0, 'walkthroughs': 0}

def fail(message):
    errors.append(message)

def is_operational_state_file(path):
    return any(path.is_relative_to((ROOT/name).resolve()) and path != (ROOT/name/'README.md').resolve()
               for name in ('requests', 'modules', 'project'))

def check_project_binding():
    path = ROOT/'project/backend.json'
    stats['projectBound'] = False
    if path.exists() or path.is_symlink():
        spec = importlib.util.spec_from_file_location('workflow_setup_validator', ROOT/'skill/product-workflow-setup/scripts/setup_project.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            module.load_binding(ROOT)
        except (ValueError, OSError) as exc:
            fail('Invalid project Backend binding: '+str(exc))
        else:
            stats['projectBound'] = True

def check_graph():
    g = json.loads((ROOT/'workflows/graph.json').read_text())
    nodes = {}
    for f in g['workflows']:
        for n in f['nodes']:
            if n['id'] in nodes:
                fail('Duplicate node: '+n['id'])
            nodes[n['id']] = n
            for key in ('id','title','actor','role','inputs','action','outputs','done','transitions'):
                if not n.get(key):
                    fail(f"Missing {key}: {n.get('id')}")
            if n['actor'] not in ('AI','Human','Tool'):
                fail('Invalid actor: '+n['id'])
            if len({t['condition'] for t in n['transitions']}) != len(n['transitions']):
                fail('Ambiguous identical conditions: '+n['id'])
    for n in nodes.values():
        for t in n['transitions']:
            if not t.get('condition') or t['target'] not in nodes and t['target'] not in g['terminals']:
                fail(f"Invalid transition: {n['id']} -> {t}")
    seen, todo = set(), [g['entry']]
    while todo:
        id = todo.pop()
        if id in seen or id in g['terminals']:
            continue
        seen.add(id)
        if id in nodes:
            todo.extend(t['target'] for t in nodes[id]['transitions'])
    for missing in set(nodes)-seen:
        fail('Unreachable node: '+missing)
    # Each node must have at least one possible route to an explicit terminal.
    reaching = set(g['terminals'])
    while True:
        new = {id for id,n in nodes.items() if any(t['target'] in reaching for t in n['transitions'])}
        if new <= reaching:
            break
        reaching |= new
    for id in set(nodes)-reaching:
        fail('No terminal route: '+id)
    for path, expected in documents(g).items():
        p = ROOT/path
        if not p.exists() or p.read_text() != expected:
            fail('Cards out of sync; run render_workflows.py: '+path)
    stats['nodes'] = len(nodes)
    # Walkthrough paths are documentation regression cases, not runtime simulations.
    for line in ((ROOT/'examples/otp-issue/walkthroughs.md').read_text() + '\n' + (ROOT/'examples/team-entry.md').read_text()).splitlines():
        if '→' not in line:
            continue
        token = r'(?:[IPQTDVCBR]\d{2}|END|HOLD)'
        for sequence in re.findall(r'\b' + token + r'(?:\s*→\s*' + token + r')+\b', line):
            path = re.findall(token, sequence)
            stats['walkthroughs'] += 1
            for a,b in zip(path,path[1:]):
                if a not in nodes or b not in {t['target'] for t in nodes[a]['transitions']}:
                    fail(f'Walkthrough edge absent: {a} -> {b}')
    return g

def slug(s):
    s = re.sub(r'[^\w\-\s]', '', s.lower()).strip()
    return re.sub(r'\s', '-', s)

def check_markdown():
    for path in sorted(ROOT.rglob('*.md')):
        stats['markdownFiles'] += 1
        s = path.read_text()
        fences = re.findall(r'^```.*$',s,re.M)
        if len(fences)%2:
            fail(f'Unbalanced fences: {path.relative_to(ROOT)}')
        stats['diagrams'] += len(re.findall(r'^```mermaid\s*$',s,re.M))
        # Ignore fenced code where links and placeholders are literal examples.
        prose = re.sub(r'```[^\n]*\n[\s\S]*?```', '', s)
        for target in re.findall(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',prose):
            target = target.strip().strip('<>')
            if '{{' in target:
                continue
            u = urlsplit(target)
            if u.scheme or target.startswith('//'):
                continue
            resolved = (path.parent/unquote(u.path)).resolve() if u.path else path
            stats['localLinks'] += 1
            if not resolved.is_relative_to(ROOT.resolve()):
                fail(f'Link outside this repository {path.relative_to(ROOT)}: {target}')
            elif not resolved.exists():
                fail(f'Broken link {path.relative_to(ROOT)}: {target}')
            elif u.fragment and resolved.is_file() and resolved.suffix == '.md':
                text = resolved.read_text()
                anchors = set(re.findall(r'<a id="([^"]+)"',text))
                anchors |= {slug(h) for h in re.findall(r'^#{1,6}\s+(.+)',text,re.M)}
                if unquote(u.fragment) not in anchors:
                    fail(f'Missing anchor {path.relative_to(ROOT)}: {target}')
        if 'templates' not in path.relative_to(ROOT).parts and re.search(r'\{\{[^}]+\}\}',prose):
            fail(f'Template placeholder outside template: {path.relative_to(ROOT)}')

def check_json_and_templates():
    for path in ROOT.rglob('*.json'):
        try:
            json.loads(path.read_text())
        except (ValueError,UnicodeError) as exc:
            fail(f'Invalid JSON: {path.relative_to(ROOT)}: {exc}')
    for name in ('approval','manifest','receipt','node-run'):
        data=json.loads((ROOT/f'templates/shared/{name}.json').read_text())
        if data.get('schemaVersion') != 1:
            fail('Invalid template schemaVersion: '+name)
    with (ROOT/'templates/shared/traceability.csv').open() as f:
        rows=list(csv.reader(f))
    if not rows or any(len(row)!=len(rows[0]) for row in rows):
        fail('Malformed traceability CSV')
    # The design kit itself must never imply an unreceived human approval.
    approval=ROOT/'records/design-approval.json'
    if approval.exists():
        d=json.loads(approval.read_text())
        if d.get('status')=='approved' and not d.get('decisions'):
            fail('Design approved without a recorded human decision')

def check_design_baseline():
    path = ROOT/'records/design-manifest.json'
    if not path.exists():
        return
    manifest = json.loads(path.read_text())
    for item in manifest['artifacts']:
        file = (ROOT/item['path']).resolve()
        if is_operational_state_file(file):
            fail('Operational file in design baseline: '+item['path'])
        elif not file.is_relative_to(ROOT) or not file.is_file():
            fail('Invalid design baseline path: '+item['path'])
        elif hashlib.sha256(file.read_bytes()).hexdigest() != item['sha256']:
            fail('Design baseline changed: '+item['path'])
    approval = json.loads((ROOT/'records/design-approval.json').read_text())
    if approval.get('manifestSha256') != hashlib.sha256(path.read_bytes()).hexdigest():
        fail('Design approval references a different manifest digest')

def check_source_inventory():
    inventory = json.loads((ROOT/'research/source-inventory.json').read_text())
    seen = set()
    for item in inventory['files']:
        name = item['path']
        path = (ROOT/name).resolve()
        if is_operational_state_file(path):
            fail('Operational file in local source inventory: '+name)
        elif item.get('repository') != 'product-workflow' or name in seen or not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            fail('Invalid local source inventory entry: '+name)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            fail('Local source inventory changed: '+name)
        seen.add(name)
    stats['localSourceFiles'] = len(seen)

def check_module_library():
    count = 0
    for module in sorted((ROOT/'modules').iterdir()):
        if not module.is_dir():
            continue
        try:
            pointer = read(local(module, 'current.json'))
            if set(pointer) != {'moduleId', 'revisionId', 'manifestSha256'} or pointer['moduleId'] != module.name:
                raise ValueError('Invalid current module pointer')
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', pointer['revisionId']):
                raise ValueError('Invalid current revision id')
            folder = module/'revisions'/pointer['revisionId']
            if digest(local(folder, 'manifest.json')) != pointer['manifestSha256']:
                raise ValueError('Module pointer digest mismatch')
            for revision in sorted((module/'revisions').iterdir()):
                if revision.is_dir() and not revision.name.startswith('.'):
                    verify_revision(ROOT, revision)
            if local(module, 'README.md').read_text() != reading_entry(module.name, pointer['revisionId']):
                raise ValueError('Module reading entry and current pointer disagree')
            implementation = module/'implementation'
            if implementation.exists():
                state = read(local(implementation, 'current.json'))
                record_path = local(implementation, 'observations/'+state['observationId']+'.json')
                if digest(record_path) != state['sha256']:
                    raise ValueError('Implementation pointer digest mismatch')
                record = read(record_path)
                design_id = record['designRevisionId']
                if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', design_id) or record['moduleId'] != module.name or record['observationId'] != state['observationId']:
                    raise ValueError('Implementation record belongs to another module or revision')
                design = local(module, 'revisions/'+design_id+'/manifest.json')
                if digest(design) != record['designManifestSha256']:
                    raise ValueError('Implementation evidence is bound to a different design digest')
                if record['status'] not in {'unknown', 'not-implemented', 'in-progress', 'verified-candidate', 'accepted', 'released'} or not record['limitation']:
                    raise ValueError('Invalid implementation status or missing limitation')
                if record['status'] != 'unknown' and not record['sourceRevision']:
                    raise ValueError('Implementation status has no source revision')
                if record['status'] in {'verified-candidate', 'accepted', 'released'}:
                    local(ROOT, record['candidateManifestPath'])
                    if not record['evidence'] or not record['decisionReferences']:
                        raise ValueError('Implementation verdict has no evidence or decisions')
                for evidence in record['evidence']:
                    if digest(local(ROOT, evidence['path'])) != evidence['sha256']:
                        raise ValueError('Implementation evidence changed')
            count += 1
        except (ValueError, KeyError, TypeError, OSError) as exc:
            fail('Invalid module '+module.name+': '+str(exc))
    stats['publishedModules'] = count

def check_board():
    """Structural checks only; this does not certify a card's approvals or readiness."""
    board = json.loads((ROOT/'requests/board.json').read_text())
    template = json.loads((ROOT/'templates/shared/board-card.json').read_text())
    graph = json.loads((ROOT/'workflows/graph.json').read_text())
    nodes = {n['id'] for f in graph['workflows'] for n in f['nodes']}
    columns = {'product-draft','product-review','ready-qa','qa-design','ready-tech',
               'technical-design','technical-ready','returned','waiting','downstream'}
    states = {'intake','product-draft','product-review','product-approved','qa-design',
              'qa-approved','technical-design','technical-approved','implementing',
              'verifying','accepted','release-pending','releasing','closed',
              'waiting-human','blocked','paused','cancelled','bug-triage','change-analysis'}
    if not isinstance(board, dict) or set(board) != {'schemaVersion','columns','cards'}:
        fail('Invalid board root fields'); return
    if type(board['schemaVersion']) is not int or board['schemaVersion'] != 1:
        fail('Invalid board schemaVersion')
    if not isinstance(board['columns'], list) or not isinstance(board['cards'], list):
        fail('Board columns/cards must be arrays'); return
    ids = []
    for column in board['columns']:
        if not isinstance(column, dict) or set(column) != {'id','title'} or not all(isinstance(v,str) and v.strip() for v in column.values()):
            fail('Invalid board column'); continue
        ids.append(column['id'])
    if set(ids) != columns or len(ids) != len(set(ids)):
        fail('Board columns missing, unknown or duplicated')

    def local_file(value, label, nullable=False):
        if value is None and nullable:
            return
        if not isinstance(value,str) or not value or '{{' in value:
            fail('Invalid board file reference: '+label); return
        p = Path(value)
        if p.is_absolute() or '..' in p.parts or ':' in value or '#' in value or not (ROOT/p).resolve().is_relative_to(ROOT.resolve()) or not (ROOT/p).is_file():
            fail('Missing or unsafe board file reference: '+label)

    seen = set()
    for card in board['cards']:
        if not isinstance(card,dict) or set(card) != set(template):
            fail('Invalid board card fields'); continue
        rid = card['requestId']
        if not isinstance(rid,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',rid):
            fail('Invalid board requestId'); continue
        if rid in seen:
            fail('Duplicate board requestId: '+rid)
        seen.add(rid)
        if not isinstance(card['title'],str) or not card['title'].strip() or '{{' in card['title']:
            fail('Missing board title: '+rid)
        for field in ('modules','openReturnIds'):
            values = card[field]
            if not isinstance(values,list) or not all(isinstance(v,str) and v.strip() and '{{' not in v for v in values):
                fail('Invalid board list: '+rid+'/'+field)
            elif len(set(values)) != len(values):
                fail('Duplicate board list item: '+rid+'/'+field)
        choices = {'columnId':columns,'state':states,
                   'team':{'product','qa','tech','development','review','release',None},
                   'action':{'start','continue','return','waiting','blocked','done'},
                   'scope':{'documentation','implementation','review','release'},
                   'currentNode':nodes|{None},'nextNode':nodes|set(graph['terminals'])|{None},
                   'resumeNode':nodes|{None}}
        for field,allowed in choices.items():
            value=card[field]
            if value is not None and not isinstance(value,str) or value not in allowed:
                fail('Invalid board value: '+rid+'/'+field)
        for field in ('ownerReference','authorizationReference','blocker','lastMovementId'):
            value=card[field]
            if value is not None and (not isinstance(value,str) or not value.strip() or '{{' in value):
                fail('Invalid board reference/text: '+rid+'/'+field)
        for field in ('requestPath','trackingPath','documentPath','journalPath'):
            local_file(card[field],rid+'/'+field,field in ('documentPath','journalPath'))
        for field,filename in [('requestPath','request.md'),('trackingPath','tracking.md')]:
            if card[field] != f'requests/{rid}/{filename}':
                fail('Board path belongs to another request: '+rid+'/'+field)
        baselines=card['baselines']
        if not isinstance(baselines,dict) or set(baselines) != {'product','qa','technical'}:
            fail('Invalid board baselines: '+rid); continue
        for stage,baseline in baselines.items():
            if baseline is None:
                continue
            if not isinstance(baseline,dict) or set(baseline) != {'manifestPath','approvalPath','receiptPath'}:
                fail('Invalid board baseline references: '+rid+'/'+stage); continue
            for field,value in baseline.items():
                local_file(value,rid+'/'+stage+'/'+field,field=='receiptPath')
        # These are necessary structural prerequisites, not proof that gates passed.
        ready = {'ready-qa':('product-approved','qa','Q01',('product',)),
                 'ready-tech':('qa-approved','tech','T01',('product','qa'))}
        if isinstance(card['columnId'],str) and card['columnId'] in ready:
            state,team,node,parents=ready[card['columnId']]
            if (card['state'],card['team'],card['nextNode']) != (state,team,node) or card['blocker'] is not None or any(baselines[k] is None for k in parents) or card['action'] != 'start' or not all(card[k] for k in ('documentPath','journalPath','lastMovementId')):
                fail('Board ready column lacks structural prerequisites: '+rid)
    stats['boardCards'] = len(board['cards'])

def main():
    try:
        check_graph();check_markdown();check_json_and_templates();check_board();check_module_library();check_project_binding();check_source_inventory();check_design_baseline()
    except (KeyError,ValueError,OSError) as exc:
        fail(str(exc))
    print(json.dumps({'status':'failed' if errors else 'passed','checks':stats,'errors':errors,'scope':'repository-local links/anchors, graph, generated cards, walkthrough edges, JSON/CSV syntax, board card structure/references, module publication sources/digests, optional read-only sibling Backend binding, local source inventory and design baseline hashes; Mermaid must be checked separately'},ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
