# Setup اتصال فقط خواندنی پروژه

تصمیم درخواست‌کننده: مستندسازی فنی در product-workflow انجام شود؛ Backend برای شناخت ساختار، معماری، قابلیت‌ها و setup فقط خواندنی است. skill [product-workflow-setup](../skill/product-workflow-setup/SKILL.md) نام دایرکتوری Backend را می‌گیرد و اتصال پروژه را ثبت می‌کند. این setup با initial project/setup خود Backend متفاوت است و آن را اجرا نمی‌کند.

## مسیر ثابت نسبی

برای ریشهٔ `~/project/product-workflow` و نام انتخاب‌شدهٔ `core_backend`، Backend دقیقاً در `~/project/core_backend` است؛ قاعدهٔ عمومی `WORKFLOW_ROOT/../<BackendName>` است. نام از انسان گرفته می‌شود، نه از مثال یا آخرین جلسه. بعد از ثبت نام، مسیر همسایه از ریشهٔ واقعی workflow محاسبه می‌شود، نه از cwd یا محل نصب skill. نام یک basename است؛ مسیر مطلق، slash، traversal و Backend symlink پذیرفته نمی‌شوند.

نام و مرجع پیام واقعی در `project/backend.json` ثبت می‌شوند. این فایل وضعیت پروژه است و داخل بستهٔ immutable طراحی workflow یا inventory ثابت آن قرار نمی‌گیرد. قالب آن در [backend-binding.json](../templates/shared/backend-binding.json) است. sourceReference انتخاب واقعی نام را ثبت می‌کند؛ approval و receipt نیست. فقط access=read-only و technicalDocumentation=product-workflow معتبرند.

مالک این کنترل‌فایل setup/Coordinator است؛ آن را با درخواست setup و نام صریح می‌سازد و حق تغییر فایل‌های تیمی ندارد. preview چیزی نمی‌نویسد؛ apply فقط همین فایل محلی را ایجاد می‌کند. retry همان اتصال بی‌اثر است؛ نام تازه، تغییر policy یا overwrite اتصال موجود در اجرای معمول مجاز نیست و به اصلاح اتصال با مرجع انسانی و تحلیل اثر نیاز دارد. پرونده و برد واقعی با setup ساخته نمی‌شوند.

## مرز خواندن و نوشتن

**تمام مسیرهای Backend فقط خواندنی‌اند؛ agent product-workflow و setup حق ایجاد، ویرایش، حذف، انتقال، format یا بازتولید هیچ فایل Backend را ندارند.** این ممنوعیت شامل docs، Spec/Plan/Task، کد، تست، config، setup record، Git و فایل‌های generated است. اشاره به Backend در task، تأیید G-T یا انتخاب تیم فنی این مرز را تغییر نمی‌دهد.

اجرای ابزارهای Backend نیز در این scope مجاز نیست: init/scaffold، doctor/verify، build/test، formatter/generator، migration و Git mutation می‌توانند فایل یا اثر بسازند؛ dry-run به‌تنهایی تضمین فقط خواندن نیست. helper فقط فایل‌ها را می‌خواند و هیچ کد Backend را اجرا یا import نمی‌کند. environment، credential، token و raw payload خوانده یا به پرونده کپی نمی‌شوند. permissionهای سیستم‌عامل برای اعمال این قرارداد عوض نمی‌شوند؛ این قرارداد و محدودیت helper به معنی sandbox همهٔ ابزارهای agent نیست.

محصول/QA/فنی اسناد متعلق به خود را داخل همین workflow می‌نویسند. پایان T08 تحویل مستندات و HOLD است. workflowهای توسعه/review/release مسیر اجرای مستقل آینده در Backend را توصیف می‌کنند؛ agent این scope آن‌ها را برای نوشتن Backend ادامه نمی‌دهد. گیرندهٔ Backend در scope جدا، قراردادهای آن مخزن و اختیار واقعی خود را بررسی و پس از review، artifactهای SDD را ایجاد/فعال می‌کند. تطبیق همین معنا با Spec کنار کد لازم است؛ تحویل بسته جای activation SDD نیست.

## مطالعهٔ وضعیت و قابلیت‌ها

helper اتصال، مسیر/hash entrypointهای موجود، اسامی ماژول‌های موجود در source و انتخاب‌های allowlistشدهٔ setup plan را گزارش می‌کند. agent باید AGENTS، فهرست docs، معماری/authority، setup record/plan غیرحساس، config غیرحساس و اسناد ownerهای مرتبط را بخواند. بعد از setup، پاسخ‌های موجود و قواعد معماری baseline پرسش T10 هستند؛ سؤال دربارهٔ تصمیم باز باید در همان چارچوب باشد. capability غایب یا تعارض به owner مربوط برای اقدام در Backend تحویل می‌شود؛ agent آن را اصلاح نمی‌کند.

| نوع مشاهده | آنچه مجاز است بگوییم | آنچه نیاز به شاهد بیشتر دارد |
|---|---|---|
| کد یا مستند capability موجود | قابلیت در source/مستندات وجود دارد؛ reference/optional/unavailable با منبع | فعال‌بودن محصول یا محیط |
| انتخاب ثبت‌شده در setup plan | capability در setup انتخاب شده، همراه path/hash | انطباق تمام خروجی‌ها و verification محیط |
| config غیرحساس با مقدار معلوم | در همان config فعال/غیرفعال است؛ override نامعلوم مشخص شود | config مؤثر runtime یا سلامت قابلیت |
| evidence اجرایی معتبر برای revision/environment | نتیجهٔ اثبات‌شده در همان محدوده | سلامت فعلی یا محیط دیگر |
| شاهد ناکافی/منقضی/متعارض | unknown یا blocked، با owner و منبع لازم | ادعای فعال، pass یا اجراشده |

helper فیلد backendPreflight=not-executed و runtimeActivation=unknown دارد. recordAndPlanMatch فقط تطبیق محدود hash/metadata record و plan است؛ preflight کامل Backend یا تأیید semantics profile نیست. حتی state=completed این تمایز را حذف نمی‌کند. در technical/index.md، وضعیت مشاهده‌شده و محدودیت‌ها ثبت و در handover شواهد لازم برای preflight گیرنده معرفی شوند.

## آغاز و ادامهٔ workflow

skill setup در راه‌اندازی پروژه استفاده می‌شود؛ اتصال موجود از `project/backend.json` خوانده و نام دوباره پرسیده نمی‌شود. در ورود فنی، اتصال معتبر لازم است؛ در نبود آن setup فقط نام را می‌گیرد. product و QA می‌توانند اسناد مستقل خود را آماده کنند؛ Backend پیش‌نیاز خواندن راهنمای مجموعه یا نوشتن نیاز محصول نیست. انتخاب تیم و کارت، onboarding، review و gateهای پرونده همچنان قرارداد خود را دارند.

هر بار منبع معماری/setup یا کد مؤثر تغییر کند، technical/index و baseline مربوط باید دوباره با شاهد خواندنی بررسی شوند؛ refresh hash بدون تحلیل اثر معتبر نیست. لینک Markdown فعال این مجموعه از مخزن خارج نمی‌رود؛ مرجع Backend با نام repository، مسیر نسبی، revision و hash در متن/index/manifest ثبت می‌شود. اگر پوشهٔ ثبت‌شده غایب است، اتصال blocked است و agent Backend دیگری را انتخاب یا clone نمی‌کند.
