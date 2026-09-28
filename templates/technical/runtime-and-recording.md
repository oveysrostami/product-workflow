# اجرا، امنیت، ثبت و عملیات

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

## ترکیب deployment

| host / environment / role | ownerهای فعال | capability و وضعیت موجود | config/env non-secret | default/on/off و restart scope | prerequisite/owner |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

project-profile جدید از تصمیم انسانی؛ init dry-run و review پیش از apply. datasource/migration/worker در core host مفروض نیستند. authentication mode/claim mapping/revoke latency/no-fallback و public ingress: {{...}}. tenancy فقط اگر محصول خواسته و طراحی دارد.

## trust و دسترسی

| entry/operation | actor/context source | action/resource permission | ownership check | denial/non-disclosure | QA |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## recording policy

| target | required audit یا diagnostic/logbook | actor/time source | allowlist/redacted/omitted | transaction/after-commit | retention/access | off/failure behavior |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

required audit availability قبل اثر و append محلی؛ diagnostic failure نتیجه business را عوض نمی‌کند. model changelog با ModelChangePolicy، tracked/untracked fields و after-commit؛ منبع authoritative history در صورت نیاز جدا. secret/PAT/OTP/raw PII و payloadهای حساس ممنوع.

## health، performance و recovery

سیگنال‌ها/thresholdها/owner/اقدام، absence/stale monitoring، bounded labels/queues، readiness/liveness/role unavailable و feature-off evidence: {{...}}. SLO و p95 فقط با workload/resource/threshold مصوب و measurement plan.

runbookهای startup/config invalid، dependency failure، audit unavailable، reconcile/restore، deploy/rollback و operator authority: {{...}}. test suite و expected evidence برای enabled/disabled واقعی هر قابلیت: {{...}}.
