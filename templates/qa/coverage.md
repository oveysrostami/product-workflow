# پوشش و testability

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

| RULE/AC | UC | QA scenarioها | happy/negative/boundary/race/recovery | gap یا N/A با دلیل | owner |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## QA → فنی → evidence

| QA-ID | TECH-ID/operation | suite/test path برنامه‌ریزی‌شده | seam/fixture/fault | observable oracle | environment | owner |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

در مرحله QA ستون‌های فنی `pending-T05` هستند؛ G-Q این را gap oracle نمی‌داند. پیش از G-T mapping کامل می‌شود. در G-D شناسهٔ evidence واقعی به traceability اضافه می‌شود.

## بررسی دوطرفه

rule بدون QA: {{...}}؛ QA بدون منبع: {{...}}؛ تست فقط متکی به mock برای durability: {{...}}؛ scenarioهای فنی مستقل با source backend-rule: {{...}}. نامرتبط‌ها از شمار لازم کنار گذاشته می‌شوند، ولی دلیل و owner حفظ می‌شود.


## پوشش targetها و جریان کامل

| QA-ID | scope module/integration/end-to-end | targetType / targetId | IMPACT-ID | EDGE/FLOW | test-mapping target | مسئول execution مشترک |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای یک سناریوی مشترک چند ردیف با QA-ID یکسان مجاز است؛ oracle تک‌مرجع می‌ماند. QA قبل طراحی فقط ماژول‌های محتمل را مشخص می‌کند؛ فنی T02 و T05 فهرست نهایی را با شواهد پر می‌کنند. coverage باید اثر مستقیم، consumer وابسته و compatibility-only را شامل شود. scope تک‌ماژولی به سناریوی مشترک ساختگی نیاز ندارد.
