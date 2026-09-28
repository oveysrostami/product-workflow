# سناریوهای مستقل QA

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

## کاتالوگ

| QA-ID | عنوان | source RULE/AC یا Backend rule | UC | risk/priority | سطح پیشنهادی | automated/manual | status طراحی |
|---|---|---|---|---|---|---|---|
| {{QA-01}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{draft/reviewed}} |

## QA-ID — شرح مستقل

- هدف و failure مورد شکار: {{...}}
- baseline و source oracle: {{...}}
- actor/scope/permission و preconditions: {{...}}
- fixture ساختگی و reset/cleanup: {{...}}
- Given: {{state دقیق و وابستگی}}
- When: {{گام‌های مرتب، زمان نسبی/مرز دقیق و action}}
- Then: {{output/state/result دقیق و قابل سنجش}}
- Must not: {{اثر دوباره، partial write، افشا، تغییر وضعیت غیرمجاز}}
- مشاهده نتیجه: {{API/public state/report امن؛ طراحی مکان دقیق با فنی}}
- fault/concurrency: {{نقطه قطع، دو actor، barrier و نتیجه‌های مجاز؛ یا N/A}}
- تکرار و استقلال تست: {{کلید/داده تازه یا همان intent و دلیل}}
- evidence مورد انتظار: {{چه artifact و assertهایی؛ نه pass ادعایی}}
- ابهام‌ها: {{OPEN-ID یا ندارد}}

در تست رقابت یک sleep حدسی جای synchronization مشخص نیست. در تست حد زمانی `<`، `=` و `>` را از rule مبنا استخراج کنید؛ اگر قرارداد مرز را مشخص نکرده به محصول برگردانید. برای داده malformed/absence/null/empty و pagination/bounds در صورت ارتباط scenario مستقل یا parameter matrix دقیق بسازید.


## انتساب ماژولی سناریو

برای هر QA-ID، `scenario_scope` یکی از module/integration/end-to-end، targetهای محتمل و پس از T05 قطعی، IMPACT-ID/EDGE/FLOW و مسئول execution ثبت شود. در مرحله QA انتساب فنی نامعلوم می‌تواند pending-T05 باشد؛ oracle باید مستقل روشن باشد. سناریوی مشترک یک بار اینجا نوشته و از test-mapping چند ماژول لینک می‌شود.
