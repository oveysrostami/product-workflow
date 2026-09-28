# جریان‌ها و قراردادهای مشترک درخواست

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. این سند به‌تنهایی approval یا evidence اجرا نیست.

- request، impact-map revision و مسئول integration: {{...}}
- آیا تعامل بین ماژول‌ها در scope هست؟ {{بله / در این نسخه ندارد با دلیل و شاهد}}

## FLOW-ID — شرح مستقل هر جریان

- RULE/UC/AC و QAهای مشترک: {{...}}
- actor و trigger، ماژول‌های مشارکت‌کننده و مسئول نتیجه: {{...}}
- مسیر اصلی گام‌به‌گام با اشاره به OP/TECH هر ماژول: {{...}}
- commit هر owner، عدم وجود transaction مشترک و نتیجه قابل مشاهده: {{...}}
- رد، قطع dependency، timeout/unknown، duplicate/late/out-of-order: {{...}}
- owner retry/reconcile/compensation و اثر ممنوع: {{...}}

برای جریان واقعی sequenceDiagram مسیر اصلی و شاخه‌های failure لازم است؛ در صورت process پایدار flowchart/stateDiagram نیز اضافه شود. source dependency، synchronous call و durable/recovery graphهای طراحی canonical را با reference نسخه‌دار معرفی کنید؛ یک نمودار مبهم به‌جای هر سه نباشد.

## قرارداد هر edge

| EDGE-ID | provider / consumer | operation/message و version | input/output/error delta | compatibility و old/new overlap | مرحله rollout/شرط شروع | مراجع canonical |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## پذیرش کل درخواست

| QA-ID | scope integration/end-to-end | targetهای مشارکت‌کننده | oracle واحد و محل تعریف | محیط و evidence واقعی | task مشترک/مسئول |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

موفقیت تست‌های داخلی چند ماژول، evidence این جدول نیست. برای همین سناریوی مشترک چند test-mapping به همان QA-ID ارجاع می‌دهند؛ oracle در چند فایل بازنویسی نشود.
