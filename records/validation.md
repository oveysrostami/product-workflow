# گزارش بررسی نسخهٔ ۱٫۱۰

تاریخ: ۲۰۲۶-۰۹-۲۹. محدوده: پرسش‌نامهٔ کامل و قابل ادامه پیش از interview محصول برای new/feature/change، تحلیل مستنداتی ماژول‌های فیچر با subagent و مصاحبهٔ متمرکز باگ. اجرای پروندهٔ واقعی، review مستقل و تصویب انسانی کل نسخه ادعا نمی‌شود.

## مسیر و قرارداد

[قرارداد پرسش‌نامه](../docs/13-product-questionnaire.md) تعریف کلی، حداقل ۵۰ سؤال new و حداقل ۲۰ سؤال مستقل برای هر ماژول feature را مشخص می‌کند. P11 تحلیل مستنداتی subagent فقط خواندنی، P09 طراحی/ذخیرهٔ کل مجموعه و P10 دریافت پاسخ/ادامه پس از وقفه‌اند؛ پس از پاسخ‌های اولیه، P02/P03 فقط follow-up و ابهام مؤثر باقی‌مانده را پیگیری می‌کنند. نوع feature روی baseline موجود از C03 به P01 متصل می‌شود و با routing نسخه به change تغییر نام نمی‌دهد.

سؤال‌ها و پاسخ/history از [قالب JSON](../templates/product/questionnaire.json) و اثر اولیه از [قالب محصولی](../templates/product/feature-impact.md) داخل request ذخیره می‌شوند. سؤال تغییرکرده revision تازه دارد؛ پاسخ قبلی خودکار منتقل نمی‌شود. پاسخ unknown واقعی مورد باز interview است؛ سکوت/پیشنهاد AI پاسخ نیست. توقف زودهنگام فقط پیش‌نویس با موارد باز می‌دهد. bug فقط interview متمرکز B01/B02 دارد؛ مطابق پاسخ تکمیلی کاربر، change هم پرسش‌نامهٔ متناسب با دامنه قبل از interview دارد و technical-only پس از T02 فقط interview فنی T10/T11 دارد. حداقل عددی جدا برای change تعیین نشده است.

skill، ورودی تیم، onboarding ادامه، چرخهٔ اسناد، ownership موجود، قالب request و G-P به این مسیر متصل‌اند. [سناریوهای ورود](../examples/team-entry.md) ماژول تازه، فیچر چندماژولی، baseline موجود، پاسخ جزئی، تغییر دامنه، توقف زودهنگام، unknown، چهارگزینه‌ای/تشریحی و subagent غایب را پوشش می‌دهند. graph شامل ۶۶ node و ۵۰ مسیر تمرینی است.

## ابزار و آزمون‌ها

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s skill/product-workflow/scripts/tests -v
```

کارت‌های generated منطبق و validator بدون خطا است؛ آمار در [checks](checks.json) ثبت شد. ۱۲ آزمون مجموعه و ۲۵ آزمون skill پاس شدند. نه آزمون تازهٔ [پرسش‌نامه](../skill/product-workflow/scripts/tests/test_questionnaire.py) مرز ۴۹/۵۰، change بدون سهمیهٔ عددی اختراع‌شده، سهمیهٔ مستقل ماژول‌ها، سؤال مشترک، پاسخ جزئی/unknown، supersedes، تغییر revision، چهار گزینه/تشریحی، مرجع پاسخ، سؤال تکراری و جلوگیری از عبور P10 با سؤال بی‌پاسخ را روی دادهٔ ساختگی می‌سنجند.

[ابزار read-only](../skill/product-workflow/scripts/check_questionnaire.py) ساختار/شمارش/اتصال پاسخ به revision فعال را بررسی می‌کند. record_progress در گذارهای P09 به P10 و P10 به P02 آن را اجرا می‌کند؛ ابزار هیچ فایل یا approval نمی‌نویسد. این کنترل تمام تصمیم‌های معنایی routing یا کیفیت سؤال و اصالت منبع/هویت انسان را خودکار اثبات نمی‌کند.

`quick_validate.py` از skill-creator روی skill محلی موفق بود. مانند بررسی قبل، Python پیش‌فرض PyYAML نداشت و از Python 3.14 و PyYAML 6.0.3 در venv موقت بیرون مخزن استفاده شد؛ dependency پروژه تغییر نکرد. هیچ پرسش‌نامهٔ واقعی ۵۰/۲۰ سؤالی یا dispatch زندهٔ subagent در این بررسی اجرا نشده؛ کیفیت طراحی سؤال و استقلال review همچنان معیار بررسی‌اند.

## Mermaid و نسخه

هر ۱۵ نمودار با Mermaid CLI 12.0.0، Node 26.5.0 و Google Chrome headless parse و به SVG رندر شد؛ [شاهد](mermaid-evidence.json) hash و خروجی واقعی دارد. بازرسی بصری تک‌تک نمودارها ادعا نمی‌شود.

نسخهٔ دقیق ۱٫۹ و approvalِ pending در [آرشیو](history/workflow-kit-v1.9.zip) و [رکورد hash](history/workflow-kit-v1.9.json) حفظ و hashها با manifest قدیمی تطبیق داده شدند. نسخهٔ ۱٫۱۰ manifest و approvalِ pending مستقل دارد. منبع درخواست و writeScope در [ثبت طراحی](design-review.md) است. diff با scope نگهداری workflow تطبیق و git diff --check بدون خطا بررسی شد؛ برد/پرونده/ماژول واقعی و Backend تغییر نکردند. این بررسی self-review است.
