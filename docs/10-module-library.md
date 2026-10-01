# کتابخانهٔ وضعیت جاری ماژول‌ها

## معنا و محل حقیقت

`modules/` در همین مخزن، آخرین طرح کامل و تأییدشدهٔ هر ماژول modular monolith را نگه می‌دارد. ماژول مرز تصمیم، زبان، داده و commit است؛ پوشهٔ جدول یا CRUD نیست. قواعد معماری و AGENTS خود Backend همچنان حاکم‌اند.

سند هر ماژول باید بدون خواندن requestهای قبلی قابل فهم باشد: مسئولیت و خارج scope، زبان و bounded context، قواعد پذیرفته‌شدهٔ محصول و پذیرش، aggregate/value/invariant و lifecycle، عملیات و DTO/error/auth، مالکیت داده/transaction، قراردادهای عمومی و context map، communication/recovery، configuration/composition و پوشش آزمون را کامل بیان کند. منبع هر قاعده قابل ردیابی است؛ لینک به درخواست فقط شاهد تصمیم است و جای شرح رفتار جاری را نمی‌گیرد. موارد نامرتبط دلیل و مالک دارند.

سه محل از هم متمایزند:

| محل | محتوا و اعتبار |
|---|---|
| `requests/<id>/technical/modules/<slug>/change-spec.md` | delta، دلیل و scope همین درخواست |
| `requests/<id>/technical/modules/<slug>/snapshot/` | پیش‌نویس کاملِ وضعیت ماژول پس از اعمال delta؛ تا G-T منتشر نمی‌شود |
| `modules/<slug>/revisions/<revision-id>/` | نسخهٔ کامل و immutable منتشرشده از همان bytes تأییدشده؛ current به آخرین نسخه اشاره می‌کند |

اسناد `backend/modules/<owner>/docs/` قرارداد لازم برای کار کنار کد و شاهد وضعیت آن revision هستند؛ تمام Backend ثبت‌شده برای agent این workflow فقط خواندنی است. طراحی جدید در snapshot درخواست review می‌شود؛ نسخهٔ منتشرشدهٔ این کتابخانه مرجع طرح تأییدشده است. نگاشت به Spec و هماهنگی اسناد کنار کد به گیرندهٔ مستقل Backend با scope/اختیار همان مخزن تحویل می‌شود. نسخهٔ پیاده‌شده می‌تواند تا اجرای تغییر از طرح جدید عقب باشد. اختلاف معنا با قواعد Backend پیش از G-T ثبت و حل شود؛ agent این workflow برای رفع آن Backend را تغییر نمی‌دهد.

## ساختار

```text
modules/<module-slug>/
  README.md                       # ورودی تولیدشده از pointer؛ تعریف مستقل نیست
  current.json                    # moduleId، revisionId و manifestSha256
  revisions/<revision-id>/
    README.md                     # شرح تجمعی و کامل آخرین طرح
    ...                           # جزئیات لازم و لینک‌های داخلی همین نسخه
    manifest.json                 # فایل‌ها، parent، وضعیت مشاهده‌شده و منشأ G-T
  implementation/
    current.json                  # اشاره به آخرین observation معتبر؛ اختیاری
    observations/<id>.json         # رکوردهای append-only اجرای واقعی
```

`snapshot-plan.json` در پوشهٔ snapshot درخواست، نام نسخه، baseRevision و SHA-256 تمام اسناد snapshot را دارد. manifest فنی درخواست باید هم plan و هم تک‌تک فایل‌های آن را freeze کند. wrapper انتشار بعد از G-T ساخته می‌شود و digest manifest فنی و approval را به همان bytes وصل می‌کند؛ wrapper داخل manifest فنی نیست تا چرخهٔ hash ساخته نشود. publication، journal و pointer تصمیم محصول جدید نیستند.

moduleId و revisionId با حرف کوچک انگلیسی یا رقم آغاز می‌شوند و فقط حرف کوچک، رقم و خط تیره دارند؛ مانند `wallet` و `r2`. نام نسخهٔ منتشرشده دوباره استفاده نمی‌شود.

لینک جزئیات محتوا درون خود snapshot نسبی است تا bytes هنگام انتشار تغییر نکنند. منشأ بیرونی در متن با مسیر/revision/hash/section امن ثبت می‌شود؛ package منتشرشده نباید برای شرح رفتار به خواندن فایل دیگری وابسته باشد. `implementation/current.json` شامل observationId و sha256 رکورد است؛ evidence در رکورد با path نسبی ریشه و sha256 معرفی می‌شود.

handover فنیِ داخل manifest فقط revisionId، مسیر مقصد و hash plan/فایل‌های snapshot را دارد. digest wrapper انتشار از manifest T تأثیر می‌گیرد و پیش از G-T داخل همان handover درج نمی‌شود؛ نتیجه و digest واقعی انتشار در journal تحویل T08 خارج بستهٔ مصوب ثبت می‌شوند.

## ترتیب کار و نقطهٔ به‌روزرسانی

1. **T02:** نسخهٔ جاری ماژول و digest آن، checkout و وضعیت مشاهده‌شدهٔ کد ثبت شوند. ماژول تازه baseRevision=null دارد؛ نمونهٔ آموزشی به ماژول واقعی تبدیل نمی‌شود.
2. **T04:** برای هر ماژول متأثر، وضعیت کامل فعلی با delta ادغام و snapshot نامزد تهیه شود. source RULE/AC/QA و قسمت‌های بدون تغییر حفظ شوند. تغییر فایل جاری modules در این مرحله ممنوع است. برای compatibility-only نیز نتیجهٔ تحلیل در نسخهٔ تجمعی می‌آید؛ کد ساختگی تولید نمی‌شود.
3. **T05/T06:** قابلیت آزمون، تمام snapshotهای نامزد و سازگاری کل درخواست review شوند. G-T candidate شامل plan و bytes کامل است؛ placeholder و تصمیم باز مؤثر باقی نماند.
4. **T07:** مسئولان فنی و Tech lead همان بسته را طبق G-T تصویب کنند. رأی pending/ردشده/منقضی اجازهٔ به‌روزرسانی modules نمی‌دهد.
5. **T09:** تیم فنی فقط نسخه‌های مصوب را منتشر کند؛ pointer و ورودی خواندن پس از تأیید hashها و base تغییر کنند. این گام gate انسانی تازه ندارد و به معنی مجوز اجرای کد نیست.
6. **T08:** پس از انتشار تمام ماژول‌های impact-map در همین workflow، مستندات تحویل و HOLD ثبت شود؛ D01 مقصد اجرای مستقل آینده در Backend است.

ابزار کمکی زیر پیش‌فرض فقط بررسی می‌کند؛ با `--apply` نسخهٔ immutable و pointer همان ماژول را می‌نویسد. استفاده از ابزار نیازمند تیم فنی، journal و writeScope معتبر T09 است؛ ابزار نقش یا اختیار انسانی ایجاد نمی‌کند.

```sh
python3 scripts/publish_module.py --plan requests/REQ-ID/technical/modules/MODULE/snapshot/snapshot-plan.json --manifest requests/REQ-ID/baselines/T1.json --approval requests/REQ-ID/approvals/G-T.json
# همان فرمان با --apply فقط پس از ثبت اختیار نوشتن T09
```

ابزار status/digest/تصمیم‌های ثبت‌شدهٔ G-T، عضویت تمام فایل‌ها در manifest فنی و baseRevision را کنترل می‌کند؛ authority واقعی انسان و freshness معنایی با reviewer/Coordinator است. revision موجود با محتوای متفاوت overwrite نمی‌شود. retry روی نسخهٔ جاری با همان digest بی‌اثر است. تغییر هم‌زمان base به T02 و review/approval نسخهٔ تازه برمی‌گردد؛ merge پنهان پس از approval ممنوع است.

T09 برای هر ماژول workUnit محدود دارد. یک writer، scope صریح و کنترل مجدد همهٔ baseها لازم‌اند. تا تکمیل انتشار همه targetها، تحویل T08 انجام نمی‌شود؛ قطع جلسه با journal و readback ادامه می‌یابد. نسخهٔ منتشرشده در اثر اصلاحیه پاک نمی‌شود؛ جایگزینی معنایی فقط از snapshot و G-T نسخهٔ تازه می‌گذرد. host/platform در بستهٔ component درخواست می‌مانند و به ماژول کسب‌وکار ساختگی تبدیل نمی‌شوند.

## وضعیت پیاده‌سازی

manifest هر طرح وضعیت مشاهده‌شده در زمان طراحی را با sourceRevision و limitation نگه می‌دارد. این مشاهده شاهد استقرار نیست. پیشرفت بعدی در `implementation/` ثبت کنترلی مستقل است و bytes طرح تأییدشده را تغییر نمی‌دهد.

Coordinator فقط از خروجی واقعی توسعه، QA و تصمیم‌های فنی/محصول رکورد observation را ثبت می‌کند؛ مالک معنای طرح و نویسندهٔ اسناد ماژول نیست. هر رکورد moduleId، designRevisionId و designManifestSha256، candidate/source revision، وضعیت، زمان واقعی یا null، مرجع تصمیم و مسیر/hash شواهد و محدودیت دارد. pointer اجرای جاری فقط به رکورد append-only همان ماژول اشاره می‌کند. فقدان رکورد یا عدم تطابق طرح/شاهد، وضعیت «نامشخص» یا «شاهد برای نسخهٔ قدیمی» دارد.

| وضعیت | حداقل شاهد |
|---|---|
| unknown | نبود evidence معتبر، همراه علت؛ فرض اجرا ممنوع |
| not-implemented / in-progress | بررسی revision/diff واقعی و محدودهٔ task؛ نبود فایل به‌تنهایی کل ماژول را ثابت نمی‌کند |
| verified-candidate | candidate ثابت، review مستقل، نتایج QA و پذیرش فنی V04 |
| accepted | G-D همان candidate، پذیرش QA/فنی/محصول و تحویل V06/V07 |
| released | G-R و receipt اجرای انتشار و بررسی پس از انتشار همان target؛ approved یا merged به‌تنهایی deployed نیست |

V06 خروجی G-D و R07 شواهد انتشار را برای این ثبت کنترلی می‌دهند. تنها metadata اجرای واقعی تغییر می‌کند؛ اصلاح رفتار/طراحی به تیم فنی و G-T تازه برمی‌گردد. خلاصهٔ status باید revision مربوط را نشان دهد؛ اجرای طرح قدیمی، پیاده‌شدن طرح جاری معرفی نشود.

## مالکیت و بستهٔ ثابت workflow

snapshot و pointer طراحی و ورودی module با تیم فنی‌اند. محصول و QA فایل‌های منبع خود را می‌نویسند و review/finding می‌دهند؛ فنی در snapshot، قواعد/انتظارهای مصوب را با منشأ روشن توضیح می‌دهد و معنای آن‌ها را تغییر نمی‌دهد. `implementation/` فقط کنترل‌فایل Coordinator است. انتساب تیم خودکار عوض نمی‌شود.

تمام داده‌های واقعی `modules/<slug>/`، مانند requests، بیرون manifest طراحی خودِ workflow و inventory ثابت آن‌اند. فقط `modules/README.md` راهنمای ثابت است؛ قالب‌ها، قرارداد و ابزارها نسخه‌دارند. validator ساختار، gate/digest و bytes منتشرشده را بررسی می‌کند؛ pass ابزار تأیید انسانی یا اثبات Backend نیست.
