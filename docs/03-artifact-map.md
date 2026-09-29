# ساختار و مرجع اسناد

```text
requests/<request-id>/
  request.md                  # شرح و routing، stakeholder و owner
  tracking.md                 # تاریخچهٔ حرکت/اصلاحیه و ارجاع به کارت JSON
  decisions.md                # تصمیم، منبع، open item و تاریخچه
  interview.md                # متن کامل batch و پاسخ‌های پالایش‌شده
  applicability.md            # اسناد لازم/نامرتبط با دلیل
  traceability.csv            # RULE → UC → AC → QA → TECH → TASK → EVIDENCE
  product/                    # رفتار محصول و handover به QA
    questionnaire.json        # کل پرسش‌نامهٔ اولیهٔ new/feature/change، تاریخچه و پاسخ‌های واقعی
    feature-impact.md         # اثر اولیهٔ مستنداتی فیچر با گزارش subagent؛ نه impact-map فنی
  qa/                         # strategy، سناریو، coverage و handover به فنی
    interview.md              # سؤال، پاسخ و تصمیم QA یا دلیل کفایت اطلاعات
  technical/
    index.md                  # فهرست ماژول‌ها و مراجع دقیق Backend
    interview.md              # سؤال، پاسخ و تصمیم فنی یا دلیل کفایت اطلاعات
    impact-map.md             # نوع و علت اثر درخواست بر هر ماژول
    cross-module-flows.md     # قراردادها، جریان‌ها و شکست‌های بین ماژول‌ها
    implementation-plan.md    # ترتیب sliceها و dependencyهای کل درخواست
    modules/<module-slug>/
      change-spec.md          # تغییرات همین درخواست روی این ماژول
      test-mapping.md         # QA → طراحی → task → evidence این ماژول
      snapshot/               # نسخهٔ کامل نامزد و plan؛ منتشرشدن فقط پس از G-T
    components/<component-id>/ # فقط اگر host/platform هم متأثر باشد
    handover.md               # تحویل یکپارچه با فهرست بسته‌های ماژولی
  development/
    modules/<module-slug>/tasks/<task-id>.md
    cross-module-tasks/<task-id>.md  # یک مسئول مشخص برای wiring/integration مشترک
    delivery.md               # نتیجهٔ یکپارچهٔ درخواست
  baselines/                  # manifestهای immutable هر مرحله
  approvals/                  # تصمیم‌های انسانی append-only
  receipts/                   # اعلام دریافت بسته
  reviews/                    # گزارش subagent و رأی reviewer انسانی در رکوردهای جدا، یافته و حل
  runs/                       # journal nodeها و evidence امن
  changes/                    # تغییر scope، نسخه یا defect مرتبط
```

آخرین طرح کامل مصوب هر ماژول در `modules/<slug>/revisions/<revision-id>/` همین مخزن است؛ `current.json` نسخهٔ جاری را مشخص می‌کند. در هر درخواست change-spec فقط delta است و `technical/modules/<slug>/snapshot/` وضعیت کامل پیشنهادی را دارد؛ این candidate تا G-T جاری نمی‌شود. T09 همان bytes مصوب را منتشر و T08 تحویل می‌دهد. اسناد کنار کد Backend و وضعیت پیاده‌سازی با revision/evidence خودشان شناخته می‌شوند؛ [قرارداد کتابخانه](10-module-library.md) رابطهٔ مرجع طراحی، شاهد کد و مالکیت را تعیین می‌کند.

[برد JSON مشترک](../requests/board.json) تنها محل وضعیت جاری کارت‌هاست؛ [قالب کارت](../templates/shared/board-card.json) و [قرارداد فیلدها](07-board-json.md) نحوهٔ نگهداری را تعیین می‌کنند. tracking فقط تاریخچه است. board، tracking، journal، review، approval و receipt فایل‌های کنترلی بیرون manifest محتوای تحویلی هستند تا حرکت کارت hash بسته را تغییر ندهد؛ نسخه و علت هر حرکت در تاریخچه محفوظ می‌ماند.

[جدول مالکیت فایل‌ها](08-team-file-ownership.md) تعیین می‌کند چه تیمی هر مسیر را می‌نویسد. اشتراک یک پرونده به معنی اختیار مشترک ویرایش همهٔ فایل‌ها نیست؛ فایل‌های کنترلی با Coordinator و محتوای هر مرحله با همان تیم است.

## حداقل بسته و توسعهٔ مشروط

| مرحله | همیشه لازم | فقط در صورت ارتباط |
|---|---|---|
| مشترک | کارت در board.json، request، tracking، decisions، applicability، traceability، manifest، approval و receipt مرحله؛ گزارش subagent و رأی reviewer انسانی برای مستندات محصول/QA/فنی | interview اگر سؤال، impact اگر تغییر، finding اگر review نقص دارد |
| محصول | contract، شرح مستقل UC/operation، acceptance، handover | questionnaire و پاسخ‌ها برای new/feature/change تازه؛ feature-impact برای feature؛ flows/data/تعاملات متناسب؛ N/A صریح در applicability |
| QA | interview با پاسخ‌ها یا دلیل کفایت، plan، scenarioهای دارای oracle، coverage، handover | performance/security/recovery/migration برای ریسک موجود؛ UI در صورت وجود کلاینت |
| فنی | index، impact-map، cross-module-flows، بسته change-spec/test-mapping هر ماژول متأثر، implementation plan و handover؛ snapshot کامل تجمعی هر ماژول و plan نسخهٔ انتشار؛ ارجاع به قواعد و revision Backend | domain، data/migration، communication/message، recording، deployment/ADR متناسب با اثر |
| توسعه | taskهای ماژولی و task مشترک دارای مسئول در صورت نیاز، execution evidence، review ماژول و کل درخواست، delivery و receipt | bug record، release/rollback در scope انتشار |

«نامرتبط» برای موضوع است، نه رفع الزام با فایل کوتاه. یک query بدون state به aggregate مصنوعی نیاز ندارد، اما authorization، DTO، bounded query و failure لازم دارد. اسناد کوچک را می‌توان در فایل واحد با section و ID مستقل نوشت؛ handover و approval همیشه مستقل و قابل پیدا کردن‌اند.

بستهٔ فنی نیز technical/interview.md با تصمیم‌های گفت‌وگو یا دلیل کفایت اطلاعات دارد؛ مصاحبه‌ها با [قالب تیمی](../templates/shared/team-interview.md) و طبق [چرخهٔ مستندسازی](11-documentation-cycle.md) تکمیل و در manifest همان تیم freeze می‌شوند.

## تفکیک محصول از فنی

| مفهوم | محصول | فنی |
|---|---|---|
| داده | دلیل جمع‌آوری، دسترسی، عمر، حذف و رابطهٔ مفهومی | schema، SQL type، index، JPA، transaction و migration |
| عملیات | actor، input/output معنایی، مراحل، خطا و تکرار قابل مشاهده | signature، HTTP/status/schema، port و error mapping |
| هم‌زمانی | کدام نتیجه مجاز است و چه چیزی نباید دوبار رخ دهد | version، lock، receipt و atomicity |
| رویداد | چه واقعیت قطعی برای چه مصرف‌کننده لازم است | envelope، Outbox/Inbox، version، retry و DLQ/quarantine |
| پذیرش | مثال‌های نتیجهٔ مطلوب و ممنوع | QA روش سنجش؛ فنی مکان تست؛ توسعه evidence اجرا |

## قواعد traceability

هر rule پذیرفته‌شده حداقل یک UC و AC دارد. هر AC در scope حداقل یک QA scenario دارد. هر QA scenario یا test/evidence دارد یا وضعیت `not-run/blocked` با دلیل؛ حذف ردیف مجاز نیست. هر task به TECH و QA/AC متصل است. هر الزام صرفاً معماری می‌تواند `source=backend-rule` داشته باشد و نیاز به ساخت rule محصول جعلی ندارد. رابطه‌ها چندبه‌چندند؛ یک ردیف برای هر مسیر پوشش ثبت کنید و IDها را مستقل از شمارهٔ خط نگه دارید.

در پروندهٔ چندماژولی یک قرارداد مشترک و یک traceability اصلی نگه دارید؛ owner هر قاعده و اثر بر مصرف‌کننده مشخص باشد. تحویل یک owner قبل از dependency لازم فقط به‌عنوان slice مستقل با پذیرش مستقل مجاز است.

## نقشهٔ اثر و تقسیم فنی

واحد پرونده همچنان **درخواست** است؛ ماژول‌های متأثر داخل آن بستهٔ جدا دارند. I02 فهرست اولیهٔ ماژول‌ها را از نیاز محصول می‌سازد؛ T02 با source، caller، contract، data و config آن را دقیق می‌کند. هر ردیف `impact-map` یک `IMPACT-ID` پایدار، slug واقعی ماژول، علت/شاهد، نوع اثر، مسئول فنی، حوزه تغییر، نیاز تغییر کد و QAهای مربوط دارد.

| نوع اثر | معیار | بسته لازم |
|---|---|---|
| direct | رفتار/داده/قرارداد یا کد همین ماژول باید تغییر کند | change-spec کامل و test-mapping؛ taskهای تغییر واقعی |
| dependent | مصرف‌کننده/ارائه‌دهندهٔ قرارداد ماژول تغییرکرده است | تحلیل سازگاری و تصمیم صریح نیاز یا عدم نیاز به کد؛ test-mapping |
| compatibility-only | تغییر کد پیش‌بینی نشده ولی قرارداد یا جریان وابسته باید دوباره سنجیده شود | change-spec کوتاه با دلیل بدون تغییر و test-mapping؛ فقط task سنجش لازم |

نامرتبط‌ها در impact-map با شاهد عدم اثر ثبت می‌شوند و پوشهٔ مصنوعی نمی‌گیرند. نوع اثر از «code change لازم؟» جداست؛ یک consumer وابسته ممکن است با همان کد سازگار بماند. module بدون تغییر کد از پوشش تست حذف نمی‌شود. تعداد فایل/agent به‌جای تحلیل اثر تصمیم نمی‌گیرد.

`cross-module-flows.md` در سطح request برای هر edge مالک provider/consumer، contract/version، state/commit مستقل، failure/unknown، ترتیب rollout و scenario integration/end-to-end را مشخص می‌کند. درخواست واقعاً تک‌ماژولی همین فایل را با «در این نسخه ندارد» و دلیل نگه می‌دارد. ارتباط بیرونی با provider یا actor را به ماژول داخلی ساختگی تبدیل نکنید.

تغییر host/platform در `technical/components/<component-id>/` با همین change-spec/test-mapping و targetType مشخص ثبت می‌شود؛ کد آن به پوشهٔ موجود خودش می‌رود. task مشترک زیر `development/cross-module-tasks/` یک مسئول و allowed paths دقیق دارد. این ساختار مجوز ساخت owner جدید یا transaction مشترک نیست.

## QA، اجرا و review در دو سطح

سناریوهای QA شناسهٔ یکتا و scope از نوع `module`، `integration` یا `end-to-end` دارند. QA در مرحلهٔ محصول ماژول‌های محتمل را ثبت می‌کند و T05 انتساب فنی و test seamها را نهایی می‌کند؛ تعیین owner فنی شرط زودهنگام G-Q نیست. یک سناریوی مشترک به‌جای کپی متن در چند فایل، از test-mapping ماژول‌ها به همان QA-ID ارجاع می‌گیرد.

D01 از implementation-plan یک slice و taskهای ماژولی آن را برمی‌دارد. D02–D05 برای هر task لازم اجرا می‌شوند؛ وابستگی contract/migration/wiring پیش از consumer رعایت می‌شود. آماده‌شدن چند ماژول به‌تنهایی آماده‌شدن درخواست نیست: D05 و V02 باید integration/end-to-end لازم را هم روی candidate مشترک بسنجند.

T06 و V01 ابتدا هر ماژول، سپس سازگاری کل درخواست را review می‌کنند. T07 و V04 نتیجهٔ هر مسئول فنی ماژول را همراه رأی یکپارچهٔ Tech lead ثبت می‌کنند؛ یک انسان می‌تواند با مرجع انتصاب چند نقش را پوشش دهد. G-T و G-D همچنان gateهای سطح درخواست‌اند. عبور مستقل یک slice فقط با scope و baseline جدا و وابستگی‌های بسته‌شده ممکن است.

در traceability علاوه بر شناسه‌های رفتار، `impact_id`، `target_type`، `target_id`، `scenario_scope` و `relationship_id` ثبت می‌شود. برای سناریوی مشترک چند ردیف با همان QA-ID و target متفاوت بنویسید؛ متن oracle تک‌مرجع می‌ماند.

[نمونهٔ آموزشی چندماژولی](../examples/module-impact.md) انواع اثر و task بدون تغییر کد را نشان می‌دهد.
