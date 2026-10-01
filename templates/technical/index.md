# بستهٔ طراحی فنی

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- request / Tech lead / P-Q baseline و digest: {{...}}
- اتصال project/backend.json و digest / BackendName / مسیر ../BackendName و resolve واقعی / access=read-only / مسیر AGENTS و قواعد هدف: {{...}}
- Backend revision، adopted edition/profile، local decisions: {{...}}
- setup recorded-state / مسیر و digest record و plan منتخب / محدودیت مشاهده و نتیجهٔ preflight خارجی فقط اگر evidence واقعی وجود دارد؛ در این workflow اجرا نمی‌شود: {{...}}
- baseline معماری: مسیر و digest AGENTS/قواعد/تصمیم‌های محلی و setup، source revision و dirty/diff؛ مقادیر secret/environment کپی نشوند: {{...}}
- تصمیم‌های ثابت setup، انتخاب‌های بازِ مجاز و تعارض‌های نیازمند تغییر baseline با owner/مرجع: {{...}}
- workflow اصلی Backend و workflowهای وابسته: {{...}}
- discovery commandها و نتیجه واقعی doctor/explain: {{...}}
- گفت‌وگوی فنی: technical/interview.md با پاسخ‌های T10/T11 یا دلیل کفایت اطلاعات؛ انتخاب‌های باز و صاحب اختیار: {{...}}

این اطلاعات در T02 توسط تیم فنی در `technical/index.md` همین پرونده ثبت می‌شوند؛ `request.md` محصول فقط خواندنی است.

[قرارداد چارچوب setup](../../docs/15-setup-bound-architecture.md) و [setup پروژه](../../docs/16-project-setup.md) برای T02 تا تحویل لازم‌اند. معماری و طرح درخواست داخل همین workflow نوشته می‌شوند؛ Backend فقط خواندنی است و هیچ ابزار آن اجرا نمی‌شود. تصمیم‌های ثبت‌شدهٔ setup دوباره سؤال آزاد نمی‌شوند. طرح مصوب، آزمون واقعی موجود، activation SDD و اختیار اجرای مستقل گیرنده جدا ثبت شوند؛ آماده‌سازی آزمون آینده در Backend توسط agent این workflow انجام نمی‌شود.

## بسته‌های ماژولی و جریان مشترک

- [قالب impact-map](impact-map.md) → `technical/impact-map.md`؛ فهرست کامل targetها و نوع اثر.
- [قالب cross-module-flows](cross-module-flows.md) → `technical/cross-module-flows.md`؛ قراردادهای مشترک و oracle سرتاسری.
- [قالب change-spec](module/change-spec.md) و [test-mapping](module/test-mapping.md) → `technical/modules/<module-slug>/` برای هر ماژول متأثر؛ host/platform در `technical/components/<component-id>/` در صورت نیاز.

| targetType / targetId | IMPACT-ID و نوع اثر | مسئول فنی | change-spec | test-mapping | review ماژول / blocker |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## انتخاب setup و فعال‌بودن قابلیت

| capability | موجود در source / انتخاب setup / config معلوم / verified-runtime / unknown | مسیر و hash شاهد | revision/environment شاهد، اگر موجود | override/محدودیت | gap و مالک اقدام مستقل Backend |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

وجود implementation یا state=completed setup به‌تنهایی فعال/verified بودن قابلیت را اثبات نمی‌کند. raw environment، credential و payload به این سند کپی نشوند.

## مرجع canonical

| TECH-ID | موضوع | snapshot نامزد و مسیر انتشار در modules/ | base revision/hash | قواعد و revision Backend | rule/QA مرتبط |
|---|---|---|---|---|---|
| {{TECH-01}} | {{...}} | {{modules/owner/docs/...}} | {{...}} | {{...}} | {{...}} |

در زمان freeze دو فایل editable مرجع برای یک تصمیم وجود نداشته باشد. قالب‌های Backend شامل module-spec، context-map، domain-model، use-case-spec، dto-contract، communication-contract، recording-policy، acceptance-record و ADR در مخزن کدِ هدف، در صورت وجود و پس از معرفی مسیر/revision در این index، بررسی می‌شوند. [قالب‌های فنی همین مجموعه](../README.md) تمام بخش‌های لازم طراحی و تحویل workflow را دارند؛ AGENTS و قواعد هدف هنگام کار روی همان کد نیز رعایت می‌شوند.

هر ماژول snapshot کامل در `technical/modules/<slug>/snapshot/` دارد؛ snapshot-plan و تمام فایل‌ها در manifest T freeze می‌شوند. بعد از G-T، T09 نسخهٔ مصوب را در modules/ منتشر می‌کند. [قرارداد کتابخانه](../../docs/10-module-library.md) و [قالب snapshot](../modules/README.md) مبنا هستند.

## قابلیت لازم در برابر موجود

| capability | نیاز RULE/QA | implemented/optional/reference/unavailable | شاهد source/test | gap و task | اثر بر gate |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## تصمیم‌ها و ریسک‌ها

{{ADRها و alternatives با دلیل، اثر compatibility، انتخاب‌های انسانی لازم، موارد برگشتی به محصول و testability QA}}.

## نقشهٔ اسناد

ابتدا impact-map و بستهٔ هر ماژول را بسازید. قالب‌های module-and-domain، operation برای تک‌تک عملیات، data-and-migration، communication-and-delivery، runtime-and-recording و implementation-plan را طبق applicability تکمیل یا به سند canonical لینک کنید. N/A و دلیل در index بماند.
