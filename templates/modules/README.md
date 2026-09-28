# {{module-name}} — وضعیت کامل ماژول

> قالب نامزد snapshot است؛ تمام محتوا پیش از G-T تکمیل می‌شود. طرح کامل ماژول را بنویسید؛ delta درخواست به‌تنهایی کافی نیست.

- moduleId / bounded context / مسئول فنی و مرجع انتصاب: {{...}}
- revisionId / نسخهٔ پیشین و digest / درخواست مبنا: {{...}}
- baseline محصول و QA / منشأ RULE و AC و QA: {{...}}
- Backend repository و revision بررسی‌شده: {{...}}
- وضعیت اجرای مشاهده‌شده، evidence و محدودیت: {{...}}
- موضوع این نسخه: آخرین طرح تأییدشده پس از انتشار T09؛ اجرای کد مستقل است.

## مسئولیت، زبان و مرز

{{هدف ماژول، قابلیت‌ها، non-goal، vocabulary/ubiquitous language، مالک تصمیم و داده؛ شرحی مستقل از درخواست‌ها}}.

## رفتار محصول و پذیرش

| RULE / UC / AC | رفتار و نتیجهٔ کامل جاری | بازیگر/مجوز | خطا و اثر ممنوع | منشأ تصمیم مصوب |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

{{شرح مستقل همهٔ عملیات از دید محصول؛ قواعد گذشتهٔ بدون تغییر نیز نوشته شوند. داده/زمان/مرز/تکرار/رقابت/حریم خصوصی و پذیرش‌های مرتبط کامل باشند؛ پیوند منبع جای شرح نیست}}.

## مدل دامنه و lifecycle

{{aggregate root، entity، value object، invariant، factory/restore، version و state transition؛ یا N/A با دلیل و مالک. نمودار واقعی مدل و گذار، failure بدون partial mutation؛ IO/framework وارد Domain/Application نشود}}.

## context map و قراردادهای عمومی

| upstream/downstream | قرارداد/version | مالک تصمیم و داده | port/ACL/event | compatibility و recovery |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

{{source dependency، call و event/recovery graphهای واقعی؛ فقط public contracts owner دیگر، بدون foreign runtime/SQL/transaction. بخش‌های ماژولِ طرف ارتباط تا حد لازم اینجا توضیح داده شوند}}.

## عملیات، DTO و دسترسی

{{هر عملیات: input/presence/null/bounds، trusted context، authorization/resource scope، sequence، output/error و observable evidence، read/mutation، duplicate/same intent/conflict/concurrency/unknown؛ transport و API audience در صورت ارتباط. برای تفصیل فایل داخلی همین snapshot لینک شود}}.

## داده، transaction و delivery

{{schema و ownership، mapper/JPA، commit boundary و Work، version/receipt/replay auth، audit اتمی، Outbox/Inbox و provider/network خارج transaction؛ privacy/retention، retry/deadline/reconcile، migration/mixed-version و recovery. موضوع نامرتبط دلیل دارد}}.

## runtime و composition

{{module/contracts/runtime/POM، host wiring، role/config و feature-off، startup validation، recording/observability و dependencyهای واقعی؛ قابلیت implemented/reference/optional/unavailable جدا باشد}}.

## آزمون و شواهد

| RULE/AC/QA یا قاعدهٔ Backend | invariant/عملیات | module/integration/end-to-end | oracle و روش سنجش | fixture/suite | وضعیت اجرای مشاهده‌شده و evidence |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

{{پوشش کل رفتار جاری ماژول، ریسک و limitations؛ not-run طراحی با pass اجرا اشتباه نشود. oracle مصوب QA با منشأ حفظ شود}}.

## وضعیت پیاده‌سازی و اختلاف با طرح

{{در revision بررسی‌شده چه چیزی implemented/partial/unavailable/unknown است؛ تغییرهای این طرح که هنوز اجرا نشده‌اند و evidence لازم. برای وضعیت پس از انتشار طرح، implementation همان ماژول با designRevision/digest بررسی شود}}.

## تاریخچه و ترتیب مطالعه

{{نسخه و تغییر تجمعی با منشأ درخواست؛ شناسه و digest نسخهٔ قبلی و لینک سندهای داخلی مکمل همین snapshot، تصمیم‌ها و محدودیت‌های باقیماندهٔ غیرمسدودکننده. خواننده بدون مطالعهٔ پرونده‌های قدیمی بتواند ماژول را بررسی کند}}.
