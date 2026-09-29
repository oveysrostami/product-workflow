# بررسی مستندات

این ابزارها validator همین مجموعه‌اند؛ موتور workflow، validator کامل پروندهٔ واقعی یا اجرای تست Backend نیستند. ابزار ساختار/لینک را می‌سنجد؛ gate انسانی همچنان باید منبع تصمیم، authority، scope و معنای شواهد را بررسی کند.

از ریشهٔ این مخزن:

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
```

`validate.py` وجود لینک و anchor داخل همین مخزن، ساختار و یکتایی nodeها، مقصد edgeها، reachable بودن، امکان رسیدن به terminal، برابری کارت‌ها با graph، مسیرهای تمرینی OTP و انتخاب تیم، fenceها و syntax JSON/CSV و hash فهرست منابع محلی را بررسی می‌کند. semantic correctness یا approval واقعی را ثابت نمی‌کند.

برای ویرایش nodeها، `workflows/graph.json` را تغییر دهید و سپس `python3 scripts/render_workflows.py` را اجرا کنید. کارت‌های Markdown generated هستند؛ متن آن‌ها در review انسانی خوانده می‌شود. سایر Markdownها دستی ویرایش می‌شوند.

Mermaid باید جداگانه با parser/renderer واقعی بررسی شود:

```sh
python3 scripts/check_mermaid.py --mmdc /path/to/mmdc --browser /path/to/chromium --output /tmp/workflow-diagrams
```

این دستور همهٔ diagramها را از Markdownها استخراج، با mermaid-cli در مرورگر headless رندر و گزارش شامل hash هر نمودار و خروجی ابزار می‌سازد. dependency خودکار نصب نمی‌کند. نسخه و محیط اجرای واقعی در [گزارش validation](../records/validation.md) ثبت شده است. اگر ابزار موجود نیست، «Mermaid بررسی نشده» ثبت کنید؛ شمردن fenceها جای parse واقعی نیست.

در پرونده‌های واقعی علاوه بر این ابزار، ID/source/coverage، approval digest، نبود placeholder، freshness شواهد و موارد gate با review بررسی می‌شوند. ابزار فعلی برای آن‌ها enforcement کامل خودکار ادعا نمی‌کند.

ورودی تیم و برد، قرارداد اجرای انسان/AI روی پرونده‌هاست. برد به‌صورت خودکار توسط سرویس به‌روز نمی‌شود؛ Coordinator هنگام کار آن را با tracking و مدارک تطبیق می‌دهد و جدول صف را از JSON می‌سازد. سناریوهای [انتخاب تیم](../examples/team-entry.md) معیار review رفتارند؛ validator فقط دنباله‌های صریح nodeها را می‌سنجد، نه صلاحیت واقعی صف یا پاسخ انسان.

[مرور و onboarding](../docs/12-request-onboarding.md) نیز پیش از node و مطابق [skill](../skill/product-workflow/SKILL.md) اجرا می‌شود؛ validator، dispatch واقعی subagent یا کامل‌بودن توضیح به کاربر را enforce نمی‌کند. سناریوهای محصول/QA/فنی در مثال ورود معیار بررسی این رفتارند. آزمون‌های موجود ابزارهای صف و ثبت skill، در fixture موقت اجرا می‌شوند:

```sh
python3 -m unittest discover -s skill/product-workflow/scripts/tests -v
```

برای پروندهٔ new/feature/change، ابزار read-only [پرسش‌نامه](../skill/product-workflow/scripts/check_questionnaire.py) از داخل skill اجرا می‌شود:

```sh
python3 skill/product-workflow/scripts/check_questionnaire.py --root WORKFLOW_ROOT --request REQUEST_ID
python3 skill/product-workflow/scripts/check_questionnaire.py --root WORKFLOW_ROOT --request REQUEST_ID --require-answered
```

ساختار، حداقل ۵۰ سؤال new یا ۲۰ سؤال به‌ازای هر ماژول feature و مجموعهٔ غیرخالی change متناسب با scope، گزینه‌ها، history و پاسخ revision جاری بررسی می‌شوند؛ record_progress همین بررسی را در گذارهای P09 به P10 و P10 به P02 اعمال می‌کند. ابزار سؤال طراحی نمی‌کند، چیزی نمی‌نویسد و صحت معنایی/هویت منبع را اثبات نمی‌کند. سناریوهای [پرسش‌نامه](../examples/team-entry.md) و [قرارداد](../docs/13-product-questionnaire.md) معیار بررسی انسانی کیفیت/رفتارند.

برد عملیاتی در [board.json](../requests/board.json) است. validator ساختار columns/cards، یکتایی requestId، فیلدها و مقادیر وضعیت/تیم/node، وجود مسیرهای ارجاعی و پیش‌نیازهای ساختاری ستون آماده را نیز بررسی می‌کند. این بررسی به‌تنهایی اعتبار gate یا hash پروندهٔ واقعی را اثبات نمی‌کند.

فایل‌های عملیاتی `requests/` و `modules/` به‌جز راهنماهای ثابت README همان مسیرها بیرون manifest طراحی و فهرست منابع ثابت مجموعه‌اند؛ validator ثبت آن‌ها در این دو بسته را رد می‌کند. برای آزمون regression جدایی وضعیت جاری از طراحی و حفظ کنترل کارت نامعتبر و hash اسناد ثابت اجرا کنید:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
```

این آزمون‌ها در کپی موقت اجرا می‌شوند و برد واقعی را تغییر نمی‌دهند.

محدودیت [مالکیت تیمی فایل‌ها](../docs/08-team-file-ownership.md) با بررسی scope و diff توسط agent/reviewer اعمال می‌شود؛ validator فعلی sandbox یا کنترل دسترسی فایل نیست و از pass آن رعایت همهٔ writeها استنتاج نمی‌شود.

## بررسی استقلال مجموعه

تمام لینک‌های محلی باید داخل همین مخزن resolve شوند؛ لینک به فایل خارج مخزن حتی اگر روی دستگاه نویسنده وجود داشته باشد، خطاست. clone یا کپی مستقل مجموعه نیز باید با `python3 scripts/validate.py` و `python3 scripts/render_workflows.py --check` موفق باشد. مسیر checkout کد هدف فقط ورودی اجرای پرونده است و در متن به‌عنوان دستور/مرجع نسبی هدف معرفی می‌شود، نه لینک ثابت به دایرکتوری همسایه.

## انتشار و بررسی snapshot ماژول

[قرارداد کتابخانه](../docs/10-module-library.md) و [راهنمای modules](../modules/README.md) مبنا هستند. scripts/publish_module.py با plan/manifest/approval پیش‌فرض فقط preview می‌کند؛ --apply تنها در writeScope فنی T09 و با G-T معتبر اجرا می‌شود. این ابزار engine یا تصمیم‌گیر gate نیست. validator نسخه‌ها، digest و اتصال bytes به G-T را می‌سنجد؛ اعتبار معنایی snapshot و authority انسان با review/gate است. آزمون‌های regression، انتشار/preview/retry، حفظ تاریخچه، pending approval، تغییر bytes و base منقضی را نیز پوشش می‌دهند.

## ترتیب بازبینی مستندات

[review دومرحله‌ای](../docs/14-document-review.md) در graph به P05→P12→P06، Q04→Q09→Q05 و T06→T12→T07 متصل است. record_progress گذار خارج graph را رد می‌کند؛ تکمیل node انسانی به executor=Human و decisionReference غیرخالی نیاز دارد و node منتظر پاسخ فقط از همان node ادامه می‌یابد. آزمون‌های skill این گذارها و رد تکمیل توسط AI/بدون مرجع را روی fixture موقت می‌سنجند. این کنترل‌ها صحت هویت/انتصاب، مطالعهٔ کامل یا dispatch واقعی subagent و تطبیق معنایی review را اثبات نمی‌کنند؛ آن‌ها طبق قرارداد در اجرای پرونده بررسی می‌شوند.
