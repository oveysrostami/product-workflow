# بررسی منابع و دلیل طراحی

تاریخ snapshot: ۲۰۲۶-۰۹-۲۸. مقصد `product-qa-tech-workflow` در آغاز خالی بود. این درخواست **طراحی فرآیند و قالب‌ها** است؛ تغییر رفتار هیچ ماژول محصول یا پیاده‌سازی Backend در scope آن نیست.

## دامنهٔ بررسی و حدود ادعا

[فهرست منابع](source-inventory.json) شامل **۲۷۵ فایل متنی** است: ۹۲ فایل Product-Doc و ۱۸۳ فایل Backend، شامل تمام Markdownهای قابل دسترسی و JSONهای مصاحبه/قالب/سیاست مرتبط. برای همهٔ این فایل‌ها مسیر، hash، اندازه، تعداد خط و ساختار عنوان‌ها ثبت شد. این inventory با مطالعهٔ معنایی یکسان نیست.

مطالعهٔ عمیق برای طراحی فرآیند بر AGENTSها، workflowهای Product-Doc و تصمیم‌های قبلی، قالب‌ها، قرارداد/پذیرش و نمودارهای OTP، وضعیت و ابهام‌های Account/Notification/Inquiry، handbook و authority/development/verification Backend، قالب‌های فنی و workflowهای agent متمرکز بود. snapshot معماری، profile/binding، مثال‌ها و اسناد ownerها از طریق فهرست و نقاط مرتبط با قرارداد، ownership و evidence بررسی شدند؛ این کار ممیزی خط‌به‌خط همهٔ کدها، همهٔ رفتارهای محصول یا گواهی runtime conformance نیست.

ساختار واقعی با `pom.xml` ریشه و application-host، policy suiteها، script wrapperها و نمونهٔ مسیر `CompleteTask.execute` تطبیق داده شد. هیچ build، تست Backend یا استقرار اجرا نشده است؛ verification این تحویل مربوط به مجموعهٔ مستندات جدید است.

- Backend revision: `bd0eef6821df0e700fea9bb541b731dc61fe4371`
- Product-Doc revision: `8808962ba709e7e7d657ac95be54e3be8132cc5f`
- هر دو مخزن در بررسی اولیه تغییر ثبت‌نشده نداشتند؛ هیچ‌کدام توسط این کار ویرایش نشدند.

## ماژول‌های محصول بررسی‌شده و علت

| ماژول | علت ارتباط با طراحی workflow | نتیجهٔ طراحی، نه تصمیم جدید محصول |
|---|---|---|
| [OTP](../../product-doc/modules/otp/README.md) | نمونهٔ نسبتاً کامل جریان، داده، UC و پذیرش | کیفیت شرح حفظ؛ قالب جدید محصول را از مکانیزم فنی جدا می‌کند |
| [Account](../../product-doc/modules/account/open-questions.md) | چند stakeholder/ماژول، مرز Profile، KYC و جریان مرورگر باز | open item و owner و blocking scope لازم است؛ «ثبت‌شده» معادل approved نیست |
| [Notification](../../product-doc/modules/notification/00-product-contract.md) | stateهای پذیرش/انتظار/ارسال/تحویل، provider و logging | QA باید oracle هر حالت و عدم تکرار اثر برای تکمیل log را بسنجد |
| [Inquiry](../../product-doc/modules/inquiry/README.md) | چند نوع/provider، mapping، immediate/deferred و تصمیم‌های باز | template ارتباط و داده منعطف؛ event از وجود history یا async استنتاج نشود |

## یافته‌های اصلی و پاسخ در نسخهٔ جدید

| مشاهدهٔ مستند | شاهد | اثر | پاسخ طراحی |
|---|---|---|---|
| مسیر عمومی قدیمی محصول→فنی→پیاده‌سازی است | [README Product-Doc](../../product-doc/README.md) | QA مستقل و تحویل رسمی آن دیده نشده | Q01–Q06، G-Q و handover QA |
| workflowها انتهای فاز محصول را می‌بندند | [ساخت ماژول](../../product-doc/workflows/new-module-documentation.md) | مسئولیت و خروجی مراحل بعد به agent واگذار می‌شود | T/D/V nodeهای دقیق با input/output/gate |
| عنوان‌های دیتابیس/Entity/algorithm/endpoint و جزئیات مکانیزمی کنار قرارداد محصول هستند | [داده OTP](../../product-doc/modules/otp/04-database-architecture.md)، [UC OTP](../../product-doc/modules/otp/09-use-cases.md) | خطر تبدیل پیشنهاد تکنیکی به الزام و رفتار پنهان در ضمیمه | contract مرجع رفتار؛ مفاهیم داده در محصول، schema/lock/receipt در فنی؛ source mapping |
| هر بازخورد انسان به مصاحبه‌گر بازمی‌گردد | [ساخت ماژول](../../product-doc/workflows/new-module-documentation.md)، [تغییر](../../product-doc/workflows/existing-module-change.md) | تکرار مصاحبه حتی برای اصلاح نگارش محتمل است | C01 تفکیک نوع feedback و بازگشت هدفمند |
| سه subagent دائمی برای محصول مقرر شده‌اند | [ساخت ماژول](../../product-doc/workflows/new-module-documentation.md) | وابستگی روش اجرا به امکانات ابزار و هزینهٔ ثابت | نقش‌های روشن و review مستقل حفظ؛ مدل اجرای نقش قابل انتخاب، پیشنهاد نیازمند تصویب این نسخه |
| approval جدا و hash اسناد وجود دارد | [approval قدیمی](../../product-doc/templates/approval/README.md) | پایهٔ خوبی برای snapshot است، اما QA/فنی/اجرای کد را پوشش نمی‌دهد | manifest مستقل، approval/receipt جدا، invalidation وابستگی و candidate-bound evidence |
| تصمیم‌های routing صریح قبلی وجود دارند | [WD-01 تا WD-15](../../product-doc/workflows/workflow-design-decisions.md) | نباید گفتهٔ کاربر درباره پیاده‌سازی را مشروط به audit کد کرد | قواعد routing حفظ؛ بررسی کد فقط در فنی |
| گزارش باگ روشن مسیر کوتاه و دریافت فنی دارد | [باگ](../../product-doc/workflows/bug-report.md) | نباید با مصاحبهٔ کامل یا ادعای fixed اشتباه شود | B01–B08 با QA regression و continuation به T/D/V |
| core از reference جداست | [POM](../../backend/pom.xml)، [authority](../../backend/_doc/15-authority-and-traceability.md) | کپی مثال می‌تواند dependency/product scope اشتباه بسازد | T02 capability matrix و ثبت host/owner صریح |
| قواعد و ابزار Backend موجود و نسبتاً دقیق‌اند | [AGENTS](../../backend/AGENTS.md)، [catalog](../../backend/_agent-doc/README.md) | workflow جدید نباید authority فنی دوم بسازد | binding به اسناد canonical و commands موجود |
| اجرای تست با evidence و skip محدود است | [verification](../../backend/_doc/12-verification-and-operations.md)، [policy](../../backend/scripts/ci/policy/verification.v1.json) | exit صفر یا فایل test دلیل readiness نیست | D05 و V02 با report واقعی و fresh؛ release جدا |

## تصمیم‌های پیشنهادی این طراحی

فایل‌ساختار، شناسه‌های node و gate، انتخاب role به‌جای الزام تعداد subagent، سیاست دو چرخهٔ تکراری برای escalation و شکل JSON/CSV انتخاب‌های طراحی این نسخه‌اند؛ تصمیم‌های قبلیِ تأییدشدهٔ سازمان معرفی نشده‌اند. خواستهٔ مستقیم این نوبت ترتیب محصول→QA→فنی→AI developer→review و تعریف nodeبهnode است.

ادعای «نبود تعارض» برای کل منابع قدیمی نداریم. مثلاً جزئیات OTP support docها باید هنگام مهاجرت با contract اصلی تطبیق داده شود؛ boilerplate drift و ابزارهای آینده همواره با authority/status فعلی خوانده شوند. ورود هر ماژول واقعی طبق [adoption](../docs/06-adoption.md) بازبینی و تأیید خودش را لازم دارد.
