# راهنمای ساخت پرونده از قالب‌ها

قالب‌ها قرارداد محتوا هستند، نه سند آمادهٔ تأیید. آن‌ها را فقط متناسب با applicability به پرونده کپی کنید و لینک‌های نسبی را برای محل جدید اصلاح کنید. هر placeholder با تصمیم واقعی یا N/A مستدل جایگزین شود؛ open item مؤثر به‌صراحت blocking بماند.

قواعد مصاحبه، routing، عمق اسناد و تأیید محصول در [راهنمای مستقل محصول](../docs/09-product-authoring.md) تعریف شده‌اند. برای شروع به مخزن نمونه نیاز نیست؛ ورودی فنی فقط هنگام کار روی مخزن کدِ هدف معرفی می‌شود.

## شروع دستی

1. ابتدا [تیم و پرونده را انتخاب کنید](../workflows/00-team-entry.md). فقط برای نیاز تازه `requests/<request-id>/` بسازید؛ request، tracking، decisions، applicability و traceability را از shared بردارید و یک کارت از board-card.json در requests/board.json اضافه کنید. انتخاب QA/فنی پروندهٔ موجود را ادامه می‌دهد.
2. مصاحبه اگر سؤال لازم است؛ impact اگر baseline تغییر می‌کند؛ review، manifest، approval و receipt به ازای هر تحویل. این‌ها تاریخچه append-only دارند.
3. برای محصول contract، عملیات/UC و acceptance را تکمیل کنید؛ flows/data متناسب. product handover از قالب کامل shared ساخته شود.
4. QA plan/scenarios/coverage را تکمیل و پس از approval تحویل فنی دهید. execution فقط پس از candidate پر می‌شود.
5. فنی ابتدا impact-map و cross-module-flows را می‌سازد؛ برای هر ماژول متأثر change-spec و test-mapping در `technical/modules/<slug>/` می‌گذارد. اسناد canonical Backend همراه index/hash مرجع طراحی کامل می‌مانند. قالب‌های module/domain، operation و data برای تکمیل همان اسناد canonical هستند.
6. توسعه taskهای هر ماژول را در `development/modules/<slug>/tasks/` و task مشترک با مسئول معلوم را در `development/cross-module-tasks/` می‌گیرد. review و QA هر دو سطح ماژول و کل درخواست را پوشش می‌دهند. release صرفاً در صورت scope انتشار.

## فهرست قالب‌ها

| مشترک | کاربرد |
|---|---|
| [کارت برد](shared/board-card.json) | وضعیت جاری، تیم، node، نسخه و ارجاع مدارک در board.json |
| [tracking](shared/tracking.md) | سابقهٔ جابه‌جایی و اصلاحیه‌ها؛ بدون وضعیت جاری موازی |
| [request](shared/request.md) | مسئله، stakeholder، نقش، scope و routing |
| [decisions](shared/decisions.md) | منشأ تصمیم و موارد باز |
| [interview](shared/interview.md) | متن batch و پاسخ، بدون تکرار سؤال |
| [applicability](shared/applicability.md) | مدارک لازم/نامرتبط با دلیل |
| [change-impact](shared/change-impact.md) | affected IDs و stale approval/evidence |
| [review](shared/review.md) | یافته با شاهد و مسیر اصلاح |
| [handover کامل](shared/handover.md) | قرارداد فرستنده/گیرنده و نسخه |
| [manifest](shared/manifest.json) | فایل/مخزن/revision/hash؛ بدون self-hash |
| [approval](shared/approval.json) | تصمیم انسان روی manifest مشخص |
| [receipt](shared/receipt.json) | اعلام دریافت واقعی، جدا از approval |
| [node-run](shared/node-run.json) | checkpoint هر node و ادامه پس از وقفه |
| [traceability](shared/traceability.csv) | ردیابی چندبه‌چند از rule تا evidence |

| مرحله | قالب‌ها |
|---|---|
| محصول | [contract](product/contract.md)، [flows/data](product/flows-and-data.md)، [operations/UC](product/operations-and-use-cases.md)، [acceptance](product/acceptance.md)، [handover](product/handover.md) |
| QA | [plan](qa/plan.md)، [scenarios](qa/scenarios.md)، [coverage](qa/coverage.md)، [execution](qa/execution.md)، [bug](qa/bug.md)، [handover](qa/handover.md) |
| فنی | [index](technical/index.md)، [impact-map](technical/impact-map.md)، [cross-module-flows](technical/cross-module-flows.md)، [change-spec ماژول](technical/module/change-spec.md)، [test-mapping ماژول](technical/module/test-mapping.md)، [module/domain](technical/module-and-domain.md)، [operation](technical/operation.md)، [data/migration](technical/data-and-migration.md)، [communication/delivery](technical/communication-and-delivery.md)، [runtime/recording](technical/runtime-and-recording.md)، [implementation plan](technical/implementation-plan.md)، [handover](technical/handover.md) |
| توسعه | [task](development/task.md)، [delivery](development/delivery.md)، [release](development/release.md)؛ review و execution از قالب مشترک و QA |

## تکمیل JSONهای ثبت

قالب‌ها عمداً pending و دارای placeholder هستند. approval تنها پس از پاسخ واقعی شامل decision با `role`، `identity`، `decision`، `reference`، `text` و `at` می‌شود؛ زمان نامعلوم null است. نقش G-P باید با درخواست‌کننده request یکسان باشد. برای رأی ماژولی، decision شامل reviewScope و targetType/targetId و مرجع انتصاب مسئول فنی نیز هست؛ رأی نهایی درخواست scope جدا دارد. تصمیم‌های G-T/G-D چندنقشی می‌توانند در یک فایل یا فایل‌های مستقل روی digest یکسان ثبت شوند؛ approved فقط پس از همه requiredRoles.

receipt شامل identity/role گیرنده، تصمیم accepted/returned، decisionReference، زمان واقعی و علت رد است. دریافت AI در D01 دریافت agent است؛ با دریافت انسانی QA/Tech اشتباه نشود.

manifest parentها را به digest immutable وصل می‌کند؛ approval و receipt جزو artifacts همان manifest نیستند. `openBlockers: []` فقط بعد بررسی واقعی خالی می‌ماند. JSON معتبر به‌تنهایی معنای workflow را validate نمی‌کند؛ gateها مسئول بررسی authority، scope و evidence‌اند.

در `traceability.csv` برای روابط چندبه‌چند چند ردیف بسازید؛ شناسه‌ها را با ویرگول در یک خانه انباشته نکنید. در طراحی status برابر planned و evidence خالی است. هنگام اجرا pass/fail/blocked/not-run و reference واقعی اضافه می‌شود.


در traceability جدید، IMPACT-ID و targetType/targetId و scenario_scope و relationship_id به ارتباط نیاز تا evidence اضافه شده‌اند. برای یک QA مشترک ردیف‌های target متفاوت با همان QA-ID بسازید. `node-run.workUnit` تعیین می‌کند اجرای T04 یا D03 مربوط به کدام ماژول و task است؛ attempt فقط retry همان واحد است.

## مالکیت هنگام تکمیل قالب‌ها

کپی و تکمیل محتوای هر تیم را همان تیم انجام می‌دهد؛ Coordinator فقط کنترل‌فایل‌های مشترک را ایجاد و به‌روز می‌کند. node-run شامل executor.team و writeScope است: allowedPaths پیش از اجرا، ownershipReference برای شاهد مالکیت و reviewedOutputPaths/outOfScopeChanges پس از بررسی diff ثبت می‌شوند. آرایهٔ خالی allowedPaths مجوز نوشتن نیست. [قرارداد مالکیت](../docs/08-team-file-ownership.md) بر محل خروجی هر قالب مقدم است.
