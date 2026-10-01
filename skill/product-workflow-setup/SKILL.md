---
name: product-workflow-setup
description: راه‌اندازی اتصال product-workflow به Backend همسایه با دریافت نام دایرکتوری، ذخیرهٔ مسیر نسبی و مطالعهٔ فقط خواندنی ساختار، معماری و انتخاب‌های setup؛ برای شروع پروژه یا بررسی اتصال موجود. setup خود Backend و پیاده‌سازی کد را انجام نمی‌دهد.
---

# اتصال فقط خواندنی Backend

این skill تنظیم پروژهٔ product-workflow را انجام می‌دهد؛ هیچ فایل یا ابزار تولیدکنندهٔ اثر در Backend را اجرا یا تغییر نده. مستندسازی محصول، QA و فنی در خود workflow است. قواعد Backend ورودی تحلیل‌اند و اختیار نوشتن آن مخزن نمی‌سازند.

## اتصال پروژه

ریشهٔ workflow را از مسیر کاربر یا نزدیک‌ترین والد دارای AGENTS.md، workflows/graph.json و requests/board.json پیدا کن. README، AGENTS و docs/16-project-setup.md آن پروژه را بخوان. نام Backend از ورودی واقعی کاربر می‌آید؛ نمونهٔ `core_backend` نام پروژهٔ واقعی نیست مگر کاربر آن را انتخاب کند.

اگر project/backend.json معتبر موجود است، آن را بخوان و نام دوباره نپرس. در نبود اتصال و نام، فقط بپرس «نام دایرکتوری Backend چیست؟». نام یک جزء مسیر است؛ checkout Backend همیشه نسبت به ریشهٔ workflow در `../<BackendName>` قرار دارد، مستقل از cwd فعلی. پوشهٔ غایب، symlink یا نام شامل مسیر را گزارش کن؛ clone، mkdir، جست‌وجوی جایگزین یا انتخاب خودکار Backend انجام نده.

helper زیر نسبت به محل همین skill است. preview فقط می‌خواند؛ --apply فقط project/backend.json داخل workflow را ایجاد می‌کند. source-reference مرجع پیام واقعی انتخاب نام است، نه approval. پیش از apply خروجی را بررسی کن؛ درخواست setup و نام صریح اختیار این ثبت داخلی است و تأیید تکراری نمی‌خواهد.

```sh
python3 scripts/setup_project.py --root WORKFLOW_ROOT --backend-name BACKEND_NAME --source-reference MESSAGE_REFERENCE
python3 scripts/setup_project.py --root WORKFLOW_ROOT --backend-name BACKEND_NAME --source-reference MESSAGE_REFERENCE --apply
python3 scripts/setup_project.py --root WORKFLOW_ROOT --inspect
```

اتصال موجود overwrite نمی‌شود؛ retry همان نام بدون تغییر منبع اولیه بی‌اثر است. تغییر نامِ خواسته‌شده را با سابقه و تحلیل اثر به نگهداری اتصال ارجاع بده؛ خطای ابزار را با ویرایش دستی یا تغییر access به read-write دور نزن. وضعیت اتصال داخل skill یا تنظیمات global ذخیره نشود.

## شناخت Backend

بعد از اتصال، از مسیر resolveشده AGENTS، فهرست اسناد، معماری و authority، setup record و plan غیرحساس و اسناد ماژول‌های مرتبط را فقط بخوان. helper مسیر/hash منابع، نام ماژول‌ها و گزیدهٔ allowlistشدهٔ انتخاب‌های plan را می‌دهد؛ agent باید متن منابع مربوط را برای تحلیل بخواند. environment، credential، token، raw payload و PII خوانده یا کپی نشوند؛ تست‌ها و اسناد نیز دادهٔ حساس را به گزارش وارد نکنند.

در گزارش ساختار، مرز owner/لایه‌ها، محدودیت معماری، قابلیت موجود در source، انتخاب setup، config فعال و evidence runtime را جدا کن. recorded-completed، انتخاب یک قابلیت در plan و وجود کد، اثبات فعال یا سالم‌بودن runtime نیستند. plan با hash ناسازگار، setup ناقص، config/override نامعلوم یا evidence غایب را صریح گزارش کن؛ سؤال‌های setup پاسخ‌داده‌شده دوباره پرسیده نشوند.

helper هیچ command یا module از Backend اجرا/import نمی‌کند. agent نیز init/scaffold، build، test، formatter، generator، migration، git checkout/commit یا ابزارهای doctor/verify را در Backend اجرا نکند؛ حتی dry-run می‌تواند اثر داشته باشد. رفع setup ناقص و هر تغییر Backend به تیم/جلسهٔ Backend با scope جدا تحویل می‌شود. file permissions سیستم‌عامل را تغییر نده.

## ادامه و پایان

گزارش اتصال و وضعیت خوانده‌شده را با محدودیت‌ها به کاربر بده. setup نه انتخاب تیم، نه دریافت request و نه gate است؛ کارت، approval یا شخص ساختگی نساز. در شروع کار واقعی بعدی، skill product-workflow قرارداد انتخاب تیم و درخواست را اجرا می‌کند و از همین اتصال فقط خواندنی استفاده می‌کند. مستندات فنی فقط در technical/ درخواست و snapshotهای مصوب در modules/ همین workflow نوشته می‌شوند؛ تا تحویل مستندات پیش برو و پایان را HOLD برای اجرای مستقل Backend نگه دار.
