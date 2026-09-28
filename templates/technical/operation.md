# قرارداد اجرایی هر operation

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

یک نسخه مستقل برای **هر operation** انسانی/داخلی/مدیریتی/job/query نوشته شود.

- TECH/OP/UC-ID، owner، name/version، read-only یا mutation: {{...}}
- ingressها، audience، public facade یا private، caller/permission/resource: {{...}}
- RULE/AC/QA و Backend ruleها: {{...}}

## DTO و مرز داده

| boundary/type | field/type | required/absent/null/empty | bounds/unit/precision | normalization | trusted یا user-supplied | failure |
|---|---|---|---|---|---|---|
| {{HTTP/execute/public/persistence/provider}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

mapper source→target و محل، unknown/duplicate fields، collection/copy، entity/proxy ممنوع، valid/missing/null/invalid examples: {{...}}. actor/scope از body ساخته نمی‌شود.

## مسیر گام‌به‌گام

1. decode/bounds و trusted ingress context: {{...}}
2. action authorization، logical validation و resolved time/ID: {{...}}
3. خواندن dependencyهای لازم خارج write transaction با deadline: {{...}}
4. آغاز Work owner، audit gate و resource authorization: {{...}}
5. receipt identity/fingerprint و replay با authorization جاری: {{...}}
6. invariant/expectedVersion، تغییر، conditional save/flush: {{...}}
7. required audit/receipt/Outbox همراه state در commit: {{...}}
8. confirmed completion و response mapping؛ diagnostic پس از commit: {{...}}

گام نامرتبط با دلیل حذف شود؛ ترتیب واقعی همین operation جایگزین اسکلت شود. sequenceDiagram مسیر عادی و flowchart/stateDiagram failure/duplicate/unknown لازم است؛ مشخص کنید کدام اثر قبل/بعد commit است.

## outcomes

| وضعیت | category/code | output و completion meaning | state/effect | retry مجاز | recovery owner | QA |
|---|---|---|---|---|---|---|
| {{success/denied/malformed/not-found/conflict/dependency/unknown}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## transaction و idempotency

Work lifetime/isolation/participants؛ key identity و canonical intent fields/excluded metadata؛ same/different intent؛ replay authorization؛ TTL/retry horizon با source تصمیم؛ concurrent arbitration و atomicity: {{...}}. failure cache policy، confirmed rollback در برابر UNKNOWN و reconcile identity: {{...}}.

## transport و اجرا

HTTP method/path/status/error/auth/bounds و OpenAPI group internal یا BFF audience: {{...}}. اگر HTTP ندارد دلیل و binding in-process/CLI/message را مشخص کنید. message ACK/disposition و job checkpoint در صورت ارتباط: {{...}}.

## implementation و evidence

port/adapter/class/test paths، composition registration و commands؛ fake/unit در برابر real-store/contract/entrypoint assertions: {{...}}. scenarioهای QA بدون mapping باقی نمانند.
