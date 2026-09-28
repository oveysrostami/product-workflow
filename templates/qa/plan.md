# راهبرد QA و ریسک

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- QA owner / P baseline و digest / scope / version: {{...}}
- اهداف آزمون و non-goal: {{...}}

## ریسک و انتخاب آزمون

| RISK-ID | failure و اثر | likelihood/impact و دلیل | اولویت تست | scenarioها | نوع evidence | N/A با دلیل |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای هر UC بررسی کنید: happy/negative، boundary و normalization، نقش/مجوز و عدم افشا، state transition، تکرار/replay، race، dependency/unknown، persistence/restart، integration/compatibility، migration/retention، observation، performance و UI/accessibility اگر داخل scope. هیچ‌کدام بی‌دلیل اجباری یا حذف نمی‌شود.

## محیط و داده

| نیاز | رفتار واقعی/fixture مجاز | owner تهیه | محدودیت | readiness evidence |
|---|---|---|---|---|
| {{DB/provider/time/client}} | {{...}} | {{...}} | {{...}} | {{...}} |

داده ساختگی، seed ثابت، clock کنترل‌شده، روش reset/cleanup، access roles و isolation میان اجراها: {{...}}. fake برای منطق؛ commit/durability روی store واقعی. credential در report نیاید.

## entry و exit

شروع طراحی: G-P معتبر و receipt. شروع execution: candidate قابل دسترس، schema/config و fixture معلوم و test mapping T تأییدشده. خروج: همهٔ required scenarioها pass، blocker صفر، coverage کامل و evidence تازه. threshold کارایی/ریسک فقط با reference تصمیم.

## نحوه اجرا

automated/manual/exploratory و owner هرکدام، ترتیب smoke→focused→regression، browser/device در صورت وجود UI: {{...}}. flaky policy: ثبت علت، repeat تشخیصی بدون پاک‌کردن fail، تصمیم QA؛ rerun سبز به‌تنهایی failure اولیه را حذف نمی‌کند.
