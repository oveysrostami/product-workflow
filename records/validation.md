# گزارش بررسی نسخهٔ ۱٫۱۱

تاریخ: ۲۰۲۶-۰۹-۲۹. محدوده: بازبینی کامل subagent مستقل پس از نگارش مستندات محصول، QA و فنی، سپس تأیید reviewer انسانی. اجرای پروندهٔ واقعی یا تصویب انسانی کل نسخه ادعا نمی‌شود.

## مسیر و قرارداد

[قرارداد review](../docs/14-document-review.md) ترتیب بستهٔ کامل، بازبینی subagent، اصلاح توسط تیم مالک و بازبینی نسخهٔ اصلاحی، سپس رأی واقعی reviewer انسانی و gate نهایی را مشخص می‌کند. P05→P12→P06، Q04→Q09→Q05 و T06→T12→T07 مسیرهای موفقیت‌اند. سؤال اجازهٔ تکراری subagent یا انتخاب بین AI و انسان حذف شده است؛ در نبود ابزار/منع واقعی محیط، node review مسدود می‌ماند.

subagent فقط خواندنی و متفاوت از نویسنده است؛ برای فنی، همهٔ targetها و جریان کل درخواست بررسی می‌شوند. گزارش و رأی انسانی در reviews/ جدا و append-only، بیرون manifest محتوای تیم و با digest همان بسته ثبت می‌شوند. تا پاسخ واقعی انسان، waiting-human و resumeNode همان P12/Q09/T12 باقی می‌مانند. معرفی reviewer مجهول پس از آماده‌شدن بسته و گزارش است؛ رأی reviewer، gate نهایی و receipt ثبت‌های جدا هستند. تغییر bytes، از جمله اصلاح نگارشی، review و رأی نسخهٔ تازه می‌خواهد و مصاحبهٔ کامل را خودکار تکرار نمی‌کند.

AGENTS، نقش‌ها، مالکیت، قرارداد node، چرخهٔ مستندسازی، authoring، versioning، قالب review و راهنمای skill به این ترتیب متصل‌اند. [سناریوهای ورود](../examples/team-entry.md) هر سه تیم، نبود انتصاب/ابزار، رد انسان، اصلاح و waiting را پوشش می‌دهند. graph شامل ۶۹ node و ۵۶ مسیر تمرینی است. routing پرسش‌نامه، باگ و technical-only حفظ شده است.

## ابزار و آزمون‌ها

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s skill/product-workflow/scripts/tests -v
```

کارت‌های generated منطبق و validator بدون خطا است؛ آمار در [checks](checks.json) ثبت شد. ۱۲ آزمون مجموعه و ۲۸ آزمون skill پاس شدند. سه regression تازه در [آزمون workflow](../skill/product-workflow/scripts/tests/test_workflow.py) برای هر سه تیم جلوگیری از عبور مستقیم AI به gate، رد تکمیل review انسانی با executor=AI یا بدون decisionReference و ادامهٔ انتظار در همان node را روی fixture موقت می‌سنجند. کنترل عمومی موجود record_progress با nodeهای Human تازه اعمال می‌شود؛ تغییر تولیدی زائد در recorder لازم نبود.

این ابزارها dispatch واقعی، کامل‌بودن مطالعه، هویت/انتصاب انسان یا معنای تصمیم و تطبیق همهٔ digestهای یک request واقعی را اثبات نمی‌کنند. `quick_validate.py` از skill-creator روی skill محلی موفق بود؛ از venv موجود بیرون مخزن با Python 3.14 و PyYAML 6.0.3 استفاده شد و dependency پروژه تغییر نکرد. نسخهٔ نصب‌شدهٔ شخصی skill بدون تغییر محلی با منبع مخزن همگام شد.

## بازبینی مستقل

subagent مستقل `/root/review_review_sequence` به‌صورت فقط خواندنی تغییرات نگهداری را بررسی کرد: AGENTS/README، ورودی/node، docs نقش/نسخه/ساختار/gate/مالکیت/authoring/چرخه/onboarding/review، graph و کارت‌های P/Q/T، قالب review، SKILL و references تیم‌ها و review، diff و کنترل ثبت پیشرفت. مسیر دورزدن review انسانی یا یافتهٔ blocking/major گزارش نشد. موارد تکمیل، همگام‌سازی نسخهٔ نصب‌شده، سازگاری نتیجهٔ قالب و صراحت مسیر اصلاح نگارشی بودند و اصلاح شدند؛ همان subagent پس از بازخوانی، رفع هر سه مورد و نبود یافتهٔ حل‌نشده در دامنهٔ بررسی را تأیید کرد.

این review استاتیکِ تغییرات مجموعه است؛ بررسی یک بستهٔ واقعی، آزمون زندهٔ delegation یا رأی واقعی انسان نیست. version/hash refresh و آزمون‌ها توسط agent اصلی بررسی شدند. تصویب کل نسخه همچنان pending است.

## Mermaid و نسخه

هر ۱۵ نمودار با Mermaid CLI 12.0.0، Node 26.5.0 و Google Chrome headless parse و به SVG رندر شد؛ [شاهد](mermaid-evidence.json) hash و خروجی واقعی دارد. بازرسی بصری تک‌تک نمودارها ادعا نمی‌شود.

نسخهٔ دقیق ۱٫۱۰ و approvalِ pending در [آرشیو](history/workflow-kit-v1.10.zip) و [رکورد hash](history/workflow-kit-v1.10.json) حفظ و hash آرشیو، manifest، approval و همهٔ artifacts قدیمی تطبیق داده شدند. نسخهٔ ۱٫۱۱ manifest و approvalِ pending مستقل دارد. منبع درخواست و writeScope در [ثبت طراحی](design-review.md) است. diff با scope نگهداری workflow تطبیق و git diff --check بدون خطا بررسی شد؛ برد/پرونده/ماژول واقعی و Backend تغییر نکردند.
