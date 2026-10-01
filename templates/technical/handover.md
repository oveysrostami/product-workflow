# تحویل technical به توسعه‌دهنده AI

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

از [قالب کامل handover](../shared/handover.md) استفاده و آن را در پرونده تکمیل کنید. فیلدهای زیر برای این مرحله الزامی‌اند:

- شناسه/مسیر manifest همین بسته؛ parent baselineهای دقیق با digest؛ digest خود manifest و approval در رکوردهای بیرون بسته.
- revisionId و مسیر مقصد modules/، hash plan و فایل‌های snapshot هر ماژول، قواعد و revision Backend، task dependency، file/layer map، commands و migration/recovery.
- نتیجه و digest wrapper انتشار T09 پس از G-T فقط در journal تحویل T08 ثبت می‌شود؛ افزودن آن به این handover مصوب چرخهٔ hash و تغییر bytes ایجاد می‌کند.
- read order و لینک canonical هر سند؛ در پرونده لینک‌ها نسبت به محل جدید بازنویسی شوند.
- انتظار از توسعه‌دهنده AI، owner مسئول دریافت و معیار پذیرش ورودی.
- open itemها با اثر و owner؛ blocker جاری نباید زیر عبارت «بعداً» پنهان شود.
- receipt جدا با وضعیت pending تا اعلام واقعی دریافت.
- اتصال project/backend.json و نام/path/hash منابع معماری/setup Backend؛ وضعیت source/selected/configured/verified-runtime و محدودیت مشاهده. Backend برای agent تحویل‌دهنده فقط خواندنی بوده؛ هیچ فایل یا command آن تغییر/اجرا نشده است.
- اختیار اجرای مستقل گیرندهٔ Backend جدا از G-T: مرجع واقعی scope آینده یا «در scope فعلی نیست». در هر دو حالت agent product-workflow در T08 به HOLD با resumeNode=D01 می‌رود و Backend را تغییر نمی‌دهد. گیرندهٔ مستقل پس از preflight/review، Spec/Plan/Task را ایجاد و فعال می‌کند.

این فایل راهنمای انتخاب است؛ در پروندهٔ واقعی باید **تمام متن قالب کامل** با محتوای مرحله جایگزین شود، نه اینکه صرفاً همین پنج خط تحویل شوند.


بسته باید impact-map، cross-module-flows، index همه change-spec/test-mappingهای ماژولی، نتیجهٔ review مسئولان ماژول و جمع‌بندی کل درخواست را داشته باشد. ترتیب dependency و مسیر task هر ماژول، taskهای مشترک و مسئول integration، QAهای محلی/مشترک و وضعیت readiness مشخص باشند. handover مستقل برای هر ماژول الزام نیست؛ یک تحویل یکپارچهٔ قابل ردیابی کافی است.
