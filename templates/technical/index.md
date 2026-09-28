# بستهٔ طراحی فنی

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- request / Tech lead / P-Q baseline و digest: {{...}}
- Backend revision، adopted edition/profile، local decisions: {{...}}
- workflow اصلی Backend و workflowهای وابسته: {{...}}
- discovery commandها و نتیجه واقعی doctor/explain: {{...}}

## بسته‌های ماژولی و جریان مشترک

- [قالب impact-map](impact-map.md) → `technical/impact-map.md`؛ فهرست کامل targetها و نوع اثر.
- [قالب cross-module-flows](cross-module-flows.md) → `technical/cross-module-flows.md`؛ قراردادهای مشترک و oracle سرتاسری.
- [قالب change-spec](module/change-spec.md) و [test-mapping](module/test-mapping.md) → `technical/modules/<module-slug>/` برای هر ماژول متأثر؛ host/platform در `technical/components/<component-id>/` در صورت نیاز.

| targetType / targetId | IMPACT-ID و نوع اثر | مسئول فنی | change-spec | test-mapping | review ماژول / blocker |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## مرجع canonical

| TECH-ID | موضوع | مسیر نهایی در Backend | revision/hash | draft در این پرونده یا canonical | rule/QA مرتبط |
|---|---|---|---|---|---|
| {{TECH-01}} | {{...}} | {{modules/owner/docs/...}} | {{...}} | {{...}} | {{...}} |

در زمان freeze دو فایل editable مرجع برای یک تصمیم وجود نداشته باشد. قالب‌های Backend شامل module-spec، context-map، domain-model، use-case-spec، dto-contract، communication-contract، recording-policy، acceptance-record و ADR در مخزن کدِ هدف، در صورت وجود و پس از معرفی مسیر/revision در این index، بررسی می‌شوند. [قالب‌های فنی همین مجموعه](../README.md) تمام بخش‌های لازم طراحی و تحویل workflow را دارند؛ AGENTS و قواعد هدف هنگام کار روی همان کد نیز رعایت می‌شوند.

## قابلیت لازم در برابر موجود

| capability | نیاز RULE/QA | implemented/optional/reference/unavailable | شاهد source/test | gap و task | اثر بر gate |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## تصمیم‌ها و ریسک‌ها

{{ADRها و alternatives با دلیل، اثر compatibility، انتخاب‌های انسانی لازم، موارد برگشتی به محصول و testability QA}}.

## نقشهٔ اسناد

ابتدا impact-map و بستهٔ هر ماژول را بسازید. قالب‌های module-and-domain، operation برای تک‌تک عملیات، data-and-migration، communication-and-delivery، runtime-and-recording و implementation-plan را طبق applicability تکمیل یا به سند canonical لینک کنید. N/A و دلیل در index بماند.
