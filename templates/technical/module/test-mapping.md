# نگاشت QA و evidence یک ماژول

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. این سند به‌تنهایی approval یا evidence اجرا نیست.

- request / targetType / targetId / IMPACT-ID / مسئول QA و فنی: {{...}}
- product/QA/technical baselines: {{...}}

| QA-ID یا Backend rule | scope module/integration/end-to-end | TECH-ID/operation | TASK-ID | test/suite/fixture | assertion متعلق به این target | oracle مرجع واحد | candidate/evidence/status |
|---|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{planned/not-run/pass/fail/blocked}} |

## سناریوهای مشترک

برای هر scenario integration/end-to-end، EDGE/FLOW، همه targetهای مشارکت‌کننده، مسئول اجرای مشترک و محل evidence کل را معرفی کنید: {{...}}. همین scenario در test-mapping سایر targetها با همان QA-ID ارجاع می‌گیرد؛ متن سناریو در QA تک‌مرجع می‌ماند.

## target بدون تغییر کد

تحلیل سازگاری، assertionهای regression، suiteهای موجود قابل استفاده، شرط reuse شواهد candidate و موارد نیازمند اجرای تازه: {{...}}. اگر test تازه لازم است یک task تست تعریف کنید؛ success ادعایی یا تولید کد بی‌نیاز مجاز نیست.

## readiness

پیش از G-T mapping و testability کامل؛ پیش از G-D شواهد واقعی تازه برای همه سناریوهای لازم. skipped/blocked/not-run معادل pass نیستند. N/A همراه دلیل و owner: {{...}}.
