#!/usr/bin/env python3
"""Render readable node cards from the local workflow specification; no execution."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def documents(graph):
    location = {n['id']: f['id'] for f in graph['workflows'] for n in f['nodes']}
    result = {}
    for flow in graph['workflows']:
        lines = [f"# {flow['title']}", '', flow['description'], '',
                 '> کارت‌ها از [graph.json](graph.json) تولید می‌شوند. توقف، انتظار و retry مشترک در [قرارداد node](00-node-contract.md) اعمال می‌شود.', '',
                 '```mermaid', 'flowchart TD']
        local = {n['id'] for n in flow['nodes']}
        external = set()
        for n in flow['nodes']:
            lines.append(f'    {n["id"]}["{n["id"]} · {n["actor"]} · {n["title"]}"]')
            external.update(t['target'] for t in n['transitions'] if t['target'] not in local)
        for target in sorted(external):
            lines.append(f'    {target}["{target} · ادامه در مسیر مربوط"]')
        for n in flow['nodes']:
            for t in n['transitions']:
                lines.append(f'    {n["id"]} -->|"{t["condition"]}"| {t["target"]}')
        lines += ['```', '']
        for n in flow['nodes']:
            lines += [f'<a id="{n["id"].lower()}"></a>', f'## {n["id"]} — {n["title"]}', '',
                      f'**مجری:** {n["actor"]} — {n["role"]}', '',
                      f'**ورودی:** {n["inputs"]}', '', f'**کار دقیق:** {n["action"]}', '',
                      f'**خروجی:** {n["outputs"]}', '', f'**شرط پایان:** {n["done"]}', '',
                      '| نتیجه | node بعدی |', '|---|---|']
            for t in n['transitions']:
                target = t['target']
                link = target if target in graph['terminals'] else f'[{target}]({location[target]}.md#{target.lower()})'
                lines.append(f'| {t["condition"]} | {link} |')
            lines += ['']
        result[f'workflows/{flow["id"]}.md'] = '\n'.join(lines).rstrip() + '\n'
    lines = ['# نقشهٔ workflowها و nodeها', '',
             'شروع هر کار از [انتخاب تیم و پرونده](00-team-entry.md) است. **I01** ورودی درخواست تازه است؛ QA از Q01، فنی از T01 و پروندهٔ موجود از checkpoint معتبر ادامه می‌یابد. چهار gate اصلی G-P، G-Q، G-T و G-D طبق [معیارها](../docs/04-gates.md) اجرا می‌شوند؛ G-R فقط برای انتشار خواسته‌شده است.', '',
             'قرارداد ورودی/خروجی و توقف همهٔ nodeها در [00](00-node-contract.md) مشترک است. شاخه‌های شکست، نقص و بازگشت در کارت همان node آمده‌اند. مسیر مستقیم تا پیاده‌سازی فقط وقتی مجاز است که baselineهای معتبر پیشین وجود داشته باشند.', '',
             '| workflow | nodeها | ورودی → خروجی |', '|---|---|---|']
    for f in graph['workflows']:
        lines.append(f'| [{f["title"]}]({f["id"]}.md) | {f["nodes"][0]["id"]} تا {f["nodes"][-1]["id"]} | {f["description"]} |')
    lines += ['', '## فهرست سریع نقش‌ها', '', '| node | کار | نوع | مسئول |', '|---|---|---|---|']
    for f in graph['workflows']:
        for n in f['nodes']:
            lines.append(f'| [{n["id"]}]({f["id"]}.md#{n["id"].lower()}) | {n["title"]} | {n["actor"]} | {n["role"]} |')
    lines += ['', '## شروع‌های متداول', '',
              '- ماژول تازه: پس از I01 تا I04 و P01، پرسش‌نامهٔ حداقل ۵۰ سؤالی P09/P10؛ سپس interview و نگارش محصول.',
              '- فیچر تازه: پس از کنترل baseline در صورت نیاز و P01، تحلیل مستنداتی subagent در P11 و حداقل ۲۰ سؤال برای هر ماژول در P09/P10؛ سپس interview.',
              '- تغییر رفتار تازه: کنترل اثر/نسخه در C01–C03، سپس P01 و پرسش‌نامهٔ P09/P10 قبل از interview؛ نسخهٔ جاری محفوظ است.',
              '- باگ با انتظار روشن: I01 → I04 → B01؛ گزارش کوتاه، QA regression، دریافت و بررسی فنی.',
              '- refactor بدون تغییر رفتار: T01 با baseline معتبر، سپس کشف T02 و فقط interview فنی T10/T11؛ پرسش‌نامهٔ محصول ندارد.',
              '- درخواست صرفاً طراحی مستندات: در handover مرحلهٔ خواسته‌شده با journal توقف ثبت می‌شود؛ ادامهٔ کد از این درخواست استنتاج نمی‌شود.',
              '- صف تیم‌ها، انتخاب پرونده و برگشت با اصلاحیه: [ورودی تیم](00-team-entry.md) و [برد](../requests/board.json). این ورودی یک gate یا موتور جدید نیست.',
              '', '[نمونه و تمرین مسیرها](../examples/otp-issue/README.md) · [قالب‌ها](../templates/README.md)', '']
    result['workflows/README.md'] = '\n'.join(lines)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    graph = json.loads((ROOT/'workflows/graph.json').read_text())
    bad = []
    for name, content in documents(graph).items():
        path = ROOT/name
        if args.check:
            if not path.exists() or path.read_text() != content:
                bad.append(name)
        else:
            path.write_text(content)
    if bad:
        raise SystemExit('Generated cards differ: ' + ', '.join(bad))
    print('Workflow cards match graph.' if args.check else 'Workflow cards rendered.')

if __name__ == '__main__':
    main()
