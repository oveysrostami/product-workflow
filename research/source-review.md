# منابع داخلی و پوشش نیازمندی‌های workflow

نسخهٔ جاری مستقل است: تمام قواعد لازم برای اجرای مراحل محصول، QA، طراحی فنی، کنترل وضعیت و تحویل در همین مخزن آمده‌اند. [فهرست منابع داخلی](source-inventory.json) مسیر نسبی و hash فایل‌های فعال همین پروژه را نگه می‌دارد؛ وجود checkout دیگری پیش‌نیاز خواندن یا بررسی مجموعه نیست.

## محل هر نیازمندی

| نیاز | مرجع داخلی و خروجی |
|---|---|
| انتخاب تیم و پرونده | [ورودی تیم](../workflows/00-team-entry.md) و [برد JSON](../requests/board.json)؛ انتخاب تیم، نمایش صف معتبر و دریافت واقعی |
| دریافت ایده، routing و تغییر رفتار | [راهنمای محصول](../docs/09-product-authoring.md) و [I nodeها](../workflows/01-intake.md)؛ پروندهٔ واحد، گفتهٔ کاربر دربارهٔ پیاده‌سازی و revision/درخواست مستقل |
| مصاحبه و ثبت تصمیم | [مصاحبه](../templates/shared/interview.md)، [decisions](../templates/shared/decisions.md) و [P nodeها](../workflows/02-product.md)؛ سؤال مؤثر، پاسخ جزئی، موارد باز و منبع تصمیم |
| قرارداد و عمق محصول | [قالب قرارداد](../templates/product/contract.md)، [جریان و داده](../templates/product/flows-and-data.md)، [عملیات/UC](../templates/product/operations-and-use-cases.md)، [پذیرش](../templates/product/acceptance.md) |
| QA مستقل | [Q nodeها](../workflows/03-qa.md) و [قالب‌ها](../templates/README.md)؛ plan/scenarios/coverage و oracle، regression و evidence اجرا |
| طراحی فنی قابل آزمون | [T nodeها](../workflows/04-technical.md)، [ساختار اسناد](../docs/03-artifact-map.md) و [اتصال مخزن کد هدف](../docs/05-backend-binding.md)؛ impact-map، بستهٔ هر ماژول، جریان مشترک و برنامهٔ اجرا |
| توسعه، review و تحویل | [D nodeها](../workflows/05-implementation.md)، [V nodeها](../workflows/06-review-and-acceptance.md) و [release](../workflows/08-release.md)؛ task، evidence واقعی و اختیار اجرای scope |
| approval، receipt و ابطال نسخه | [نسخه و وضعیت](../docs/02-state-and-versioning.md)، [gateها](../docs/04-gates.md) و [قرارداد node](../workflows/00-node-contract.md) |
| برگشت، باگ و اصلاح هدفمند | [C/B nodeها](../workflows/07-change-and-bug.md) و [tracking](../templates/shared/tracking.md)؛ علت، تیم/نسخهٔ مقصد و بستن با دریافت معتبر |
| مرز نوشتن تیم‌ها | [مالکیت فایل‌ها](../docs/08-team-file-ownership.md)؛ فایل تیم دیگر فقط خواندنی و اصلاح با تیم مالک |

## مثال‌ها و حدودشان

[مثال مستقل صدور و replay](../examples/otp-issue/README.md) قرارداد محلی، شش پذیرش، QA و candidate فنی دارد. شناسه‌های DEMO-P/AC/QA در همین مثال تعریف و ردیابی می‌شوند؛ هیچ قاعده‌ای برای فهم آن از مخزن بیرونی خوانده نمی‌شود. مثال slice آموزشی است و approval، کد اجراشده یا سیاست یک محصول واقعی را ادعا نمی‌کند.

[نمونهٔ چندماژولی](../examples/module-impact.md) و [سناریوهای تیم/برگشت](../examples/team-entry.md) اثر direct/dependent/compatibility-only، ادامه از checkpoint و مرز تیم را پوشش می‌دهند.

## مخزن کد به‌عنوان ورودی اجرا

workflow مستقل است؛ اجرای تغییر واقعی همچنان به checkout کدِ هدف و قواعد فعلی آن نیاز دارد. این ورودی در T01/T02 برای همان درخواست معرفی می‌شود؛ نام و محل نصب ثابت ندارد. adapter نمونهٔ [Backend](../docs/05-backend-binding.md) قواعد و commandهای نمونه را در همین پروژه توضیح می‌دهد؛ در هدف متفاوت، مسئول فنی نسخه، ابزار و قابلیت‌های واقعی را بررسی و ثبت می‌کند.

ورود قرارداد قبلی نیز [اختیاری](../docs/06-adoption.md) است. کاربر فایل یا snapshot قابل دسترسی معرفی می‌کند؛ شروع درخواست تازه با قالب‌های داخلی انجام می‌شود.

## تاریخچه و بررسی

نسخه‌های پیشین در Git و بسته‌های history حفظ شده‌اند تا منشأ تغییرها از بین نرود. فایل‌های آرشیوی ورودی اجرا یا مرجع الزامی نسخهٔ جاری نیستند. فهرست جاری فقط فایل‌های محلی فعال را شامل می‌شود؛ self-inventory و خروجی‌های متغیر validation/manifest از آن بیرون‌اند تا وابستگی دوری ایجاد نشود.

checker مقصد لینک‌های محلی را به داخل این مخزن محدود و hash منابع جاری را بررسی می‌کند. [گزارش validation](../records/validation.md) اجرای واقعی بررسی را ثبت می‌کند؛ استقلال clone با کپی مجموعه به محیطی بدون مخزن همسایه آزموده می‌شود. این بررسی اجرای Backend یا تصویب انسانی پرونده‌ای واقعی نیست.
