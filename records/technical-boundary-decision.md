# تصمیم محل معماری فنی و اتصال SDD

تاریخ: ۲۰۲۶-۱۰-۰۱. وضعیت: محل مستندسازی و دسترسی Backend توسط درخواست‌کننده انتخاب شد؛ تصویب سازمانی کل مجموعه جدا و pending است.

## انتخاب واقعی درخواست‌کننده

منبع: پیام همین گفت‌وگو که خواست یک skill setup نام دایرکتوری Backend را بگیرد، Backend همیشه در ../BackendName نسبت به product-workflow باشد، مستندسازی فنی داخل product-workflow انجام شود، agent ساختار/معماری/ویژگی‌های پروژه را در آن مسیر بخواند و «اجازه تغییر توی backend رو نداره» صریح ثبت شود.

مدل منتخب B است: معماری و طرح فنی درخواست در product-workflow؛ Backend شاهد معماری موجود، setup و قرارداد زندهٔ کنار کد و برای agent این scope فقط خواندنی. پیشنهاد قبلی AI برای مدل A انتخاب نشد؛ مقایسهٔ قبلی در [آرشیو نسخهٔ ۱٫۱۲](history/workflow-kit-v1.12.zip) حفظ شده است. این انتخاب مرزبندی، gate پرونده یا تصویب کل نسخه نیست.

## محدودهٔ اجرا

تیم فعال و مالک خروجی‌ها نگهداری workflow است. writeScope: AGENTS/README، docs قراردادها، workflows graph و کارت‌ها، templates، skill setup و skill اجرای فرآیند، helper/validator و آزمون‌های fixture، project/README ثابت، records/research نسخه/hash و آرشیو قبلی. Backend، requests/board، پرونده‌ها و modules عملیاتی خواندنی‌اند. skill قابل استفادهٔ شخصی از منبع همین repository نصب می‌شود؛ هیچ اتصال واقعی از نام نمونه یا مسیر قبلی جلسه ساخته نمی‌شود.

## قرارداد منتخب

- [Skill setup](../skill/product-workflow-setup/SKILL.md) نام انتخاب‌شده را در project/backend.json با access=read-only ثبت می‌کند؛ مسیر همیشه ../BackendName است. نام و منبع پیام واقعی حفظ و retry همان اتصال بی‌اثر است.
- [قرارداد setup](../docs/16-project-setup.md) تفاوت setup اتصال و initial setup Backend و مرز منع نوشتن/اجرای ابزار را مشخص می‌کند. نام نمونه core_backend به‌تنهایی انتخاب Backend این checkout نیست.
- طراحی فنی با [baseline معماری و setup](../docs/15-setup-bound-architecture.md) در technical/ همان درخواست و کتابخانهٔ ماژول‌ها در همین workflow است. پرسش‌های معماری از تصمیم‌های ثبت‌شده شروع می‌شوند.
- capability موجود در source، انتخاب plan، config معلوم و evidence runtime جدا گزارش می‌شوند؛ مقدار secret/environment خوانده یا کپی نمی‌شود و نام فعال/verified بدون شاهد داده نمی‌شود.
- T08 پایان مستندسازی و HOLD است. گیرندهٔ مستقل Backend طبق قرارداد همان مخزن، scope، preflight، review و نگاشت به Spec/Plan/Task را انجام می‌دهد. agent این workflow هیچ فایل Backend را برای هماهنگی، آماده‌سازی آزمون یا رفع خطا تغییر نمی‌دهد.

## ادامهٔ اتصال SDD

بستهٔ فنی باید ورودی نسخه‌دار و قابل ردیابی Spec/Plan/Task باشد؛ نگاشت AC/QA/TECH و مسیر/test/reportهای آینده در technical ثبت می‌شوند. schemaهای بستهٔ Backend با فیلد ساختگی تغییر نمی‌کنند. تبدیل/واردکردن بسته و activation به محیط مستقل Backend تحویل می‌شود؛ آماده‌بودن طرح با ready Spec/change active یا evidence runtime یکی نیست. تغییر Backend یا پایلوت واقعی آن در این scope انجام نمی‌شود.
