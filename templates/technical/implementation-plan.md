# برنامهٔ slice و تست

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

## بسته‌های ماژولی و ترتیب بین آن‌ها

impact-map و cross-module-flows مرجع تقسیم‌اند. برای هر task، targetType/targetId، مسیر change-spec و test-mapping، dependency producer/consumer و مسئول مشخص کنید. taskهای ماژولی در `development/modules/<module-slug>/tasks/<task-id>.md` و کار مشترک host/integration در `development/cross-module-tasks/<task-id>.md` قرار می‌گیرند.

| slice | targetهای مشارکت‌کننده | پیش‌نیاز contract/migration/wiring | ترتیب taskها | QA integration/end-to-end | مسئول نتیجهٔ مشترک |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای target compatibility-only فقط task بررسی/آزمون متناسب بسازید. آمادگی ماژول‌های مستقل اجازهٔ عبور G-T یا G-D درخواستِ دارای dependency باز نیست.

## کوچک‌ترین slice قابل پذیرش

{{outcome مستقل و rule/UC/AC/QA مربوط؛ dependencyهای لازم}}. اولین slice را تا composition و evidence کامل کنید، سپس عملیات بعدی. interface/schema design پیش از implementation است.

| TASK-ID | TECH/QA/AC | owner/layer و فایل | کار دقیق | dependency | تعریف پایان و suite/evidence | ریسک/recovery |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

ترتیب پیش‌فرض: contracts → Domain → Application → Infrastructure → Presentation → composition/acceptance. برای query بدون Domain، N/A با دلیل. wiring/policy/docs/tests باید در scope همان task باشد؛ کار ضروری را به follow-up نامعلوم منتقل نکنید.

## verification mapping

| QA یا Backend rule | test path/suite | fixture/environment | command | assertهای لازم | report artifact | owner |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

از commands واقعی Backend و policy جاری استفاده شود. unit/fake، real PostgreSQL، contract/entrypoint، recovery و full release متناسب انتخاب شوند. prerequisite غایب و تأثیرش بر gate: {{...}}.

## آماده‌سازی اجرای AI

اختیار عمل/محدوده نوشتن، branch یا snapshot base، preserve changes، doctor/explain، scaffold dry-run، work record، ممنوعیت‌ها، reviewer مستقل و مسیر توقف: {{...}}.

## اختتام

شرط G-T: task بدون تصمیم محصول باز، QA testability پذیرفته، owner و فایل و evidence مشخص، capability gap در scope قابل اجرا، G-P/G-Q معتبر. برنامهٔ اجرا مجوز merge/deploy تولید نمی‌کند.
