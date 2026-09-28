# ارتباط، پیام، provider و کار پایدار

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

برای هر edge یک قرارداد مستقل بنویسید. edge یا event صرفاً برای استفاده از امکانات boilerplate ساخته نمی‌شود.

## EDGE-ID

- consumer/provider owner و business reason، recipe انتخاب‌شده: {{...}}
- contract/version/audience، public symbol/schema، local port و ACL: {{...}}
- data/input/output/error mapping، freshness و حدود: {{...}}
- trust/actor/scope/permission delegation و auth مجدد provider: {{...}}
- sync call خارج Work، deadline/budget/cancel، partial/unknown result: {{...}}
- call/event/recovery graph و sequence این edge: {{...}}

## پیام یا job، اگر لازم

| قرارداد | مقدار تصمیم‌شده و منبع |
|---|---|
| meaning: fact/command/result و زمان قطعیت | {{...}} |
| envelope identity/version/audience/causation و داده ممنوع | {{...}} |
| Outbox atomicity و subscriber obligations | {{...}} |
| Inbox dedup و ACK بعد commit | {{...}} |
| retry/deadline/backoff/horizon، lease/fencing/checkpoint | {{...}} |
| duplicate/late/out-of-order/unknown-version/quarantine | {{...}} |
| retention، mixed-version rollout و replay compatibility | {{...}} |
| compensation/manual action owner و authorization | {{...}} |

## provider خارجی

| failure | classification | اقدام retry/reconcile/quarantine/repair | identity حفظ‌شده | evidence |
|---|---|---|---|---|
| {{connect/TLS/timeout/cancel/429/5xx/invalid-response/unknown}} | {{...}} | {{...}} | {{...}} | {{...}} |

provider credentials فقط secret reference؛ request/response bounds، نتیجه نامعلوم و عدم تکرار اثر صرفاً برای تکمیل log، fallback مجاز طبق محصول و raw payload privacy: {{...}}. برای ObservedHttpClient، manifest نسخه‌دار integration و env/testهای policy Backend ثبت شود.

## schedule و عملیات

owner/role، startup-fixed enabled/timing/bounds، overlap/catch-up، off بدون لغو اثر قبلاً پذیرفته‌شده، shutdown/recovery identity، monitoring و metric labels محدود: {{...}}. worker/scheduler قابلیت غایب باید task داشته باشد.

## تست‌ها

crash قبل/بعد commit، duplicate/lost ACK، late reply، expired lease، provider outcome unknown، replay/restore و consumer compatibility؛ برای هرکدام QA-ID، test path و real-store evidence لازم: {{...}}.
