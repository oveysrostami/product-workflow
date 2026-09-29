# گزارش بررسی نسخهٔ ۱٫۹

تاریخ: ۲۰۲۶-۰۹-۲۹. محدوده: مرور ادامهٔ request باز محصول با subagent فقط خواندنی و onboarding کامل پروندهٔ منتخب QA/فنی در skill و فرآیند داخلی. این گزارش بررسی قراردادهای workflow و ابزارهای موجود است؛ اجرای پروندهٔ واقعی یا تأیید انسانی کل نسخه نیست.

## بررسی مسیر و حدود رفتار

[قرارداد مرور](../docs/12-request-onboarding.md) پس از انتخاب و پیش از node دریافت/ادامه اجرا می‌شود. محصول گزارش کار انجام‌شده/باقی‌مانده و checkpoint را از subagent می‌گیرد؛ QA و فنی تمام اسناد موجود و مرجع را می‌خوانند و درخواست را با جزئیات رفتاری و زمینهٔ همان تیم توضیح می‌دهند. [راهنمای skill](../skill/product-workflow/references/onboarding.md) روش dispatch، خروجی و writeScope خالی subagent را مشخص می‌کند.

ورودی تیم، قرارداد node، Q01/T01 و راهنماهای تیمی به همین رفتار متصل‌اند. نسخهٔ مصوب، پیش‌نویس، سابقهٔ stale، تصمیم انسان و evidence اجرا در گزارش جدا هستند. انتخاب/گزارش، receipt یا approval نیست؛ checkpoint معتبر و سؤال/پاسخ قبلی حفظ می‌شوند. نبود subagent، دسترسی ناقص، تغییر هم‌زمان، برگشت و دریافت مجدد در [سناریوهای ورود](../examples/team-entry.md) معیار صریح دارند. graph همان ۶۳ node و ۳۸ مسیر تمرینی را دارد؛ gate یا node تازه ساخته نشد.

این بررسی self-review قراردادهاست. سناریوهای مرور از نظر معنایی با راهنما تطبیق داده شدند؛ dispatch واقعی subagent روی پرونده و کیفیت onboarding با آزمون زندهٔ agent بررسی نشده‌اند. validator و آزمون ابزارها enforcement کامل این رفتار گفت‌وگویی نیستند؛ تعداد کارت و ماژول واقعی صفر است.

## بررسی ساختاری و آزمون‌ها

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s skill/product-workflow/scripts/tests -v
```

کارت‌ها با graph منطبق، validator بدون خطا و هر ۱۲ آزمون مجموعه و ۱۶ آزمون skill موفق‌اند. آمار دقیق در [checks](checks.json) است. آزمون‌ها جدایی وضعیت جاری از بستهٔ طراحی، انتشار snapshot، صف معتبر، نسخه/parent منقضی، انتخاب در برابر receipt، checkpoint، مالکیت/مسیر و retry/recovery ثبت را روی fixture موقت می‌سنجند؛ هیچ پروندهٔ واقعی ایجاد نشد.

`quick_validate.py` از skill-creator روی skill محلی اجرا شد و `Skill is valid!` داد. Python پیش‌فرض PyYAML نداشت؛ بررسی با Python 3.14 و PyYAML 6.0.3 در venv موقت خارج مخزن انجام شد. dependency پروژه تغییر نکرد.

## Mermaid

هر ۱۵ نمودار، شامل نمودار ورود اصلاح‌شده، با Mermaid CLI 12.0.0، Node 26.5.0 و Google Chrome headless parse و به SVG رندر شد. [شاهد رندر](mermaid-evidence.json) hash متن و خروجی ابزار را نگه می‌دارد؛ بازرسی بصری تک‌تک نمودارها ادعا نمی‌شود.

## نسخه و محدودهٔ تغییر

نسخهٔ دقیق ۱٫۸، manifest، approvalِ pending و skill پیش از تغییر در [آرشیو](history/workflow-kit-v1.8.zip) و [رکورد hash](history/workflow-kit-v1.8.json) محفوظ‌اند. نسخهٔ ۱٫۹ manifest و approvalِ pending مستقل دارد؛ skill و قرارداد مرور در فهرست منابع و baseline فعال ثبت شدند. مرجع درخواست و writeScope در [ثبت طراحی](design-review.md) است.

diff با writeScope نگهداری workflow و مالکیت خروجی‌ها تطبیق و `git diff --check` بدون خطا بررسی شد. برد، پرونده‌ها، ماژول واقعی و Backend تغییر نکردند. تغییر ازپیش‌موجود `.DS_Store` حفظ شد و جزء کار این اصلاح نیست. رأی انسانی کل نسخه و review مستقل ثبت نشده‌اند.
