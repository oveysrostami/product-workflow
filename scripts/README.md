# بررسی مستندات

این ابزارها validator همین مجموعه‌اند؛ موتور workflow، validator کامل پروندهٔ واقعی یا اجرای تست Backend نیستند. ابزار ساختار/لینک را می‌سنجد؛ gate انسانی همچنان باید منبع تصمیم، authority، scope و معنای شواهد را بررسی کند.

از ریشهٔ این مخزن:

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
```

`validate.py` وجود لینک و anchor، ساختار و یکتایی nodeها، مقصد edgeها، reachable بودن، امکان رسیدن به terminal، برابری کارت‌ها با graph، مسیرهای تمرینی OTP و انتخاب تیم، fenceها و syntax JSON/CSV را بررسی می‌کند. semantic correctness یا approval واقعی را ثابت نمی‌کند.

برای ویرایش nodeها، `workflows/graph.json` را تغییر دهید و سپس `python3 scripts/render_workflows.py` را اجرا کنید. کارت‌های Markdown generated هستند؛ متن آن‌ها در review انسانی خوانده می‌شود. سایر Markdownها دستی ویرایش می‌شوند.

Mermaid باید جداگانه با parser/renderer واقعی بررسی شود:

```sh
python3 scripts/check_mermaid.py --mmdc /path/to/mmdc --browser /path/to/chromium --output /tmp/workflow-diagrams
```

این دستور همهٔ diagramها را از Markdownها استخراج، با mermaid-cli در مرورگر headless رندر و گزارش شامل hash هر نمودار و خروجی ابزار می‌سازد. dependency خودکار نصب نمی‌کند. نسخه و محیط اجرای واقعی در [گزارش validation](../records/validation.md) ثبت شده است. اگر ابزار موجود نیست، «Mermaid بررسی نشده» ثبت کنید؛ شمردن fenceها جای parse واقعی نیست.

در پرونده‌های واقعی علاوه بر این ابزار، ID/source/coverage، approval digest، نبود placeholder، freshness شواهد و موارد gate با review بررسی می‌شوند. ابزار فعلی برای آن‌ها enforcement کامل خودکار ادعا نمی‌کند.

ورودی تیم و برد، قرارداد اجرای انسان/AI روی پرونده‌هاست. برد به‌صورت خودکار توسط سرویس به‌روز نمی‌شود؛ Coordinator هنگام کار آن را با tracking و مدارک تطبیق می‌دهد و جدول صف را از JSON می‌سازد. سناریوهای [انتخاب تیم](../examples/team-entry.md) معیار review رفتارند؛ validator فقط دنباله‌های صریح nodeها را می‌سنجد، نه صلاحیت واقعی صف یا پاسخ انسان.

برد عملیاتی در [board.json](../requests/board.json) است. validator ساختار columns/cards، یکتایی requestId، فیلدها و مقادیر وضعیت/تیم/node، وجود مسیرهای ارجاعی و پیش‌نیازهای ساختاری ستون آماده را نیز بررسی می‌کند. این بررسی به‌تنهایی اعتبار gate یا hash پروندهٔ واقعی را اثبات نمی‌کند.

محدودیت [مالکیت تیمی فایل‌ها](../docs/08-team-file-ownership.md) با بررسی scope و diff توسط agent/reviewer اعمال می‌شود؛ validator فعلی sandbox یا کنترل دسترسی فایل نیست و از pass آن رعایت همهٔ writeها استنتاج نمی‌شود.
