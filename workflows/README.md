# نقشهٔ workflowها و nodeها

شروع هر کار از [انتخاب تیم و پرونده](00-team-entry.md) است. **I01** ورودی درخواست تازه است؛ QA از Q01، فنی از T01 و پروندهٔ موجود از checkpoint معتبر ادامه می‌یابد. چهار gate اصلی G-P، G-Q، G-T و G-D طبق [معیارها](../docs/04-gates.md) اجرا می‌شوند؛ G-R فقط برای انتشار خواسته‌شده است.

قرارداد ورودی/خروجی و توقف همهٔ nodeها در [00](00-node-contract.md) مشترک است. شاخه‌های شکست، نقص و بازگشت در کارت همان node آمده‌اند. مسیر مستقیم تا پیاده‌سازی فقط وقتی مجاز است که baselineهای معتبر پیشین وجود داشته باشند.

| workflow | nodeها | ورودی → خروجی |
|---|---|---|
| [ورود درخواست و تشخیص مسیر](01-intake.md) | I01 تا I04 | ورودی درخواست تازه پس از انتخاب تیم محصول و دریافت شرح آزاد است. QA و فنی برای پرونده‌های موجود از صف تیم خود وارد Q01/T01 یا checkpoint می‌شوند. درخواست چندماژولی یک پرونده و مالکیت روشن دارد؛ تشخیص AI تأیید محصول نیست. |
| [جمع‌آوری نیاز، مصاحبه و قرارداد محصول](02-product.md) | P01 تا P08 | Product نیاز stakeholderها را به AI می‌دهد؛ پیشنهاد AI تا پاسخ صریح تصمیم نیست. کیفیت شرح جریان و پذیرش مهم‌تر از تعداد فایل است. |
| [طراحی QA پیش از طراحی فنی](03-qa.md) | Q01 تا Q08 | دریافت محصول مصوب، گفت‌وگوی QA با AI، تهیه و review اسناد، تأیید انسانی و handover فنی؛ ابهام محصول با اصلاحیه برمی‌گردد. |
| [طراحی فنی مطابق Backend](04-technical.md) | T01 تا T11 | دریافت محصول و QA مصوب، گفت‌وگوی فنی با AI و طراحی مطابق Backend؛ پس از G-T، انتشار modules در T09 و تحویل آمادهٔ پیاده‌سازی در T08. |
| [اجرای AI توسعه‌دهنده](05-implementation.md) | D01 تا D06 | یک vertical slice کوچک را کامل کن و سپس slice بعدی را بساز. تست هر لایه همراه همان لایه است؛ هیچ مرحله‌ای تضمین‌های لازم را به بعد از تحویل موکول نمی‌کند. |
| [review، اجرای QA و تحویل](06-review-and-acceptance.md) | V01 تا V07 | review مستقل پیش از پذیرش نهایی است. کد و شواهد بعد از تغییر باید دوباره متناسب بررسی شوند. نبود یافتهٔ AI جای پذیرش QA/فنی/محصول نیست. |
| [تغییر، باگ و بازگشت هدفمند](07-change-and-bug.md) | C01 تا B07 | C nodeها نسخه و scope را مدیریت می‌کنند؛ B nodeها گزارش خلاف قرارداد را. مسیر کوتاه باگ قرارداد محصول را دوباره اختراع نمی‌کند و دریافت فنی با رفع نهایی فرق دارد. |
| [انتشار و عملیات، در صورت درخواست](08-release.md) | R01 تا R07 | این مسیر فقط پس از تحویل و با اختیار صریح انتشار اجرا می‌شود. آماده‌بودن فنی یا approval اسناد به‌تنهایی اختیار merge/deploy نیست. |

## فهرست سریع نقش‌ها

| node | کار | نوع | مسئول |
|---|---|---|---|
| [I01](01-intake.md#i01) | ثبت مسئله و زمینه | AI | Coordinator |
| [I02](01-intake.md#i02) | طبقه‌بندی و فهرست اثر | AI | Coordinator |
| [I03](01-intake.md#i03) | تعیین مسئول و رفع ابهام ورود | Human | درخواست‌کننده با نمایندهٔ محصول |
| [I04](01-intake.md#i04) | ساخت پرونده و اندازهٔ بسته | AI | Coordinator |
| [P01](02-product.md#p01) | ترکیب نیاز stakeholderها | AI | Product interviewer با ورودی Product owner |
| [P02](02-product.md#p02) | انتخاب ابهام و ساخت batch | AI | Product interviewer |
| [P03](02-product.md#p03) | پاسخ و حل تعارض محصول | Human | درخواست‌کننده / Product owner در حدود نقش |
| [P04](02-product.md#p04) | نگارش رفتار و پذیرش | AI | Product writer |
| [P05](02-product.md#p05) | بازبینی مستقل نیاز و سند | AI | Reviewer مستقل یا reviewer انسانی جایگزین |
| [P06](02-product.md#p06) | بررسی لینک، نمودار و پوشش | Tool | Check runner با تفسیر Coordinator |
| [P07](02-product.md#p07) | تأیید نسخهٔ محصول | Human | همان درخواست‌کننده |
| [P08](02-product.md#p08) | تحویل محصول به QA | AI | Coordinator |
| [Q01](03-qa.md#q01) | پذیرش دریافت محصول | Human | QA owner |
| [Q02](03-qa.md#q02) | تحلیل ریسک و راهبرد آزمون | AI | QA analyst |
| [Q03](03-qa.md#q03) | سناریو و دادهٔ آزمون مستقل | AI | QA analyst |
| [Q04](03-qa.md#q04) | چالش پوشش و oracle | AI | QA reviewer مستقل یا reviewer انسانی |
| [Q05](03-qa.md#q05) | تأیید طراحی QA | Human | QA owner |
| [Q06](03-qa.md#q06) | تحویل QA به فنی | AI | Coordinator |
| [Q07](03-qa.md#q07) | پرسش‌های تصمیم QA | AI | QA interviewer |
| [Q08](03-qa.md#q08) | پاسخ انسان QA | Human | QA owner یا صاحب تصمیم منصوب در QA |
| [T01](04-technical.md#t01) | دریافت بسته توسط فنی | Human | Tech lead |
| [T02](04-technical.md#t02) | کشف فنی و نقشهٔ اثر ماژولی | AI | Technical designer |
| [T03](04-technical.md#t03) | مدل، مالکیت و قرارداد اولیه | AI | Technical designer |
| [T04](04-technical.md#t04) | طراحی تغییر هر ماژول و برنامهٔ مشترک | AI | Technical designer |
| [T05](04-technical.md#t05) | بازبینی قابلیت آزمون | Human | QA owner با تحلیل QA agent |
| [T06](04-technical.md#t06) | review طراحی ماژول‌ها و کل درخواست | AI | Technical reviewer مستقل یا reviewer انسانی |
| [T07](04-technical.md#t07) | تصویب طرح و دامنهٔ اجرا | Human | Tech lead و مسئولان فنی ماژول‌های متأثر؛ owner زیرساخت برای انتخاب عملیاتی |
| [T08](04-technical.md#t08) | تحویل بستهٔ اجرایی | AI | Coordinator |
| [T09](04-technical.md#t09) | انتشار وضعیت مصوب ماژول‌ها | AI | Technical publisher؛ تیم فعال فنی |
| [T10](04-technical.md#t10) | پرسش‌های تصمیم فنی | AI | Technical interviewer |
| [T11](04-technical.md#t11) | پاسخ انسان فنی | Human | Tech lead یا مسئول فنی منصوب؛ owner عملیاتی برای انتخاب خودش |
| [D01](05-implementation.md#d01) | دریافت task ماژولی و preflight | AI | Developer |
| [D02](05-implementation.md#d02) | Domain و Application با تست | AI | Developer |
| [D03](05-implementation.md#d03) | adapter، persistence و durability | AI | Developer |
| [D04](05-implementation.md#d04) | Presentation و composition | AI | Developer |
| [D05](05-implementation.md#d05) | verification مطابق اثر تغییر | Tool | Check runner زیر مسئولیت Developer |
| [D06](05-implementation.md#d06) | آماده‌کردن candidate برای review | AI | Developer |
| [V01](06-review-and-acceptance.md#v01) | review مستقل ماژول‌ها و جریان کامل | AI | Code reviewer مستقل یا reviewer انسانی |
| [V02](06-review-and-acceptance.md#v02) | اجرای مستقل سناریوهای QA | AI | QA executor با ابزار و نظارت QA owner |
| [V03](06-review-and-acceptance.md#v03) | حکم کیفیت QA | Human | QA owner |
| [V04](06-review-and-acceptance.md#v04) | پذیرش فنی candidate | Human | Tech lead با رأی مسئولان فنی targetهای متأثر |
| [V05](06-review-and-acceptance.md#v05) | پذیرش نتیجهٔ محصول | Human | همان درخواست‌کننده با نمایندهٔ محصول |
| [V06](06-review-and-acceptance.md#v06) | تحویل نهایی پیاده‌سازی | AI | Coordinator |
| [V07](06-review-and-acceptance.md#v07) | دریافت تحویل و تعیین پایان scope | Human | مسئول دریافت فنی / درخواست‌کننده |
| [C01](07-change-and-bug.md#c01) | طبقه‌بندی بازخورد و تحلیل اثر | AI | Coordinator با owner مرحلهٔ گزارش‌دهنده |
| [C02](07-change-and-bug.md#c02) | تصمیم درباره تغییر یا ابهام | Human | درخواست‌کننده؛ Product owner جمع‌بندی می‌کند |
| [C03](07-change-and-bug.md#c03) | نسخه‌سازی و بازکردن بخش متأثر | AI | Coordinator |
| [C04](07-change-and-bug.md#c04) | ادامهٔ scope قبلی پس از رد تغییر | AI | Coordinator |
| [B01](07-change-and-bug.md#b01) | ثبت و تطبیق گزارش با قرارداد | AI | Coordinator / QA analyst |
| [B02](07-change-and-bug.md#b02) | روشن‌کردن مستقیم انتظار باگ | Human | همان درخواست‌کننده |
| [B03](07-change-and-bug.md#b03) | تأیید گزارش باگ | Human | همان درخواست‌کننده |
| [B04](07-change-and-bug.md#b04) | بازتولید و سناریوی regression | AI | QA analyst با ابزار |
| [B08](07-change-and-bug.md#b08) | تأیید بستهٔ regression باگ | Human | QA owner |
| [B05](07-change-and-bug.md#b05) | دریافت فنی گزارش | Human | Tech lead |
| [B06](07-change-and-bug.md#b06) | تحقیق علت و طرح اصلاح محدود | AI | Technical designer / Developer در نقش investigation |
| [B07](07-change-and-bug.md#b07) | تصمیم درباره گزارش حل‌نشده | Human | QA owner و درخواست‌کننده با Tech lead |
| [R01](08-release.md#r01) | آماده‌سازی انتشار قابل review | AI | Developer / Coordinator |
| [R02](08-release.md#r02) | تصمیم و اختیار انتشار | Human | Release owner مجاز |
| [R03](08-release.md#r03) | دروازهٔ کامل انتشار | Tool | Release check runner |
| [R04](08-release.md#r04) | اجرای اعمال مجاز انتشار | Human | Operator / agent با اختیار همان operator |
| [R05](08-release.md#r05) | بررسی پس از انتشار | Tool | QA / عملیات |
| [R06](08-release.md#r06) | تصمیم recovery در محدوده اختیار | Human | Release owner / operator |
| [R07](08-release.md#r07) | ثبت رخداد و تحویل ادامه | AI | Coordinator |

## شروع‌های متداول

- ایدهٔ تازه: I01 → I04 → P01؛ سپس محصول، QA، فنی، پیاده‌سازی و پذیرش.
- تغییر رفتار: I01 → I04 → C01؛ نسخهٔ جاری حفظ و بخش متأثر باز می‌شود.
- باگ با انتظار روشن: I01 → I04 → B01؛ گزارش کوتاه، QA regression، دریافت و بررسی فنی.
- refactor بدون تغییر رفتار: I01 → I04 → T01 با baseline معتبر محصول و QA.
- درخواست صرفاً طراحی مستندات: در handover مرحلهٔ خواسته‌شده با journal توقف ثبت می‌شود؛ ادامهٔ کد از این درخواست استنتاج نمی‌شود.
- صف تیم‌ها، انتخاب پرونده و برگشت با اصلاحیه: [ورودی تیم](00-team-entry.md) و [برد](../requests/board.json). این ورودی یک gate یا موتور جدید نیست.

[نمونه و تمرین مسیرها](../examples/otp-issue/README.md) · [قالب‌ها](../templates/README.md)
