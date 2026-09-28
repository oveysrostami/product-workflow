#!/usr/bin/env python3
"""Extract and render every Mermaid diagram with an explicitly supplied mmdc."""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--mmdc',required=True,help='Path to installed mermaid-cli mmdc')
p.add_argument('--browser',required=True,help='Chromium/Chrome executable path')
p.add_argument('--output',help='Directory for rendered SVGs and evidence; default temporary')
a=p.parse_args()
out=Path(a.output).resolve() if a.output else Path(tempfile.mkdtemp(prefix='workflow-mermaid-'))
out.mkdir(parents=True,exist_ok=True)
config=out/'puppeteer.json';config.write_text(json.dumps({'executablePath':a.browser}))
# Batch markdown rendering starts one browser and parses/renders every diagram.
blocks=[]; sources=[]
for path in sorted(ROOT.rglob('*.md')):
    for number,match in enumerate(re.finditer(r'^```mermaid\s*\n([\s\S]*?)^```',path.read_text(),re.M),1):
        blocks.append('```mermaid\n'+match.group(1)+'```')
        sources.append({'path':str(path.relative_to(ROOT)),'diagram':number,'sha256':hashlib.sha256(match.group(1).encode()).hexdigest()})
input_path=out/'all-diagrams.md';input_path.write_text('\n\n'.join(blocks)+'\n')
cmd=[a.mmdc,'-i',str(input_path),'-o',str(out/'rendered.md'),'-p',str(config),'-e','svg']
r=subprocess.run(cmd,capture_output=True,text=True)
report={'status':'passed' if r.returncode==0 else 'failed','count':len(blocks),'sourceDiagrams':sources,'command':cmd,'stdout':r.stdout,'stderr':r.stderr}
(out/'mermaid-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'count':len(blocks),'report':str(out/'mermaid-report.json')},ensure_ascii=False))
if r.returncode:
    print(r.stdout);print(r.stderr)
raise SystemExit(r.returncode)
