# داده، ذخیره‌سازی و migration

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

## مالکیت و persistence

owner/schema/runtime principal/migrator reference و host composition: {{...}}. credentials خام ممنوع‌اند. JPA entity در Infrastructure از domain مستقل است. Hibernate/JPA پیش‌فرض؛ native/JDBC استثنا به evidence و reason نیاز دارد.

ER واقعی schema با تمام entityهای داده و رابطه‌های owner-local، فیلدهای مهم، PK/unique/version و indexهای لازم ارائه شود. foreign owner reference، FK/join خصوصی ایجاد نمی‌کند.

| dataset/entity | دلیل و owner | fields/constraints | mapping Domain↔JPA | دسترسی/grants | retention و clock آغاز | purge/hold/replay اثر |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## اتمی‌بودن و شکست

Work participants، lock/version order و bounds، physical transaction، receipt/audit/Outbox، connection/statement deadline و confirmed/unknown outcome: {{...}}. provider و foreign call بیرون write transaction. test fault پس از هر write و اثبات rollback/commit واقعی: {{...}}.

## evolution

| مرحله | تغییر افزایشی | نسخه قدیم/جدید | migration/backfill actor | checkpoint/budget | rollback یا roll-forward | evidence |
|---|---|---|---|---|---|---|
| expand | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| backfill | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| contract | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

migration file/version/registration، عدم ویرایش baseline اعمال‌شده، migrate role جدا و serving schema validate بدون DDL: {{...}}. restore backup به‌همراه پیام/receipt/provider effects reconciliation و owner تصمیم: {{...}}. «DB backup داریم» به‌تنهایی recovery plan نیست.

## پذیرش واقعی

PostgreSQL واقعی برای constraints، concurrency، rollback همه participantها، denied foreign schema/DDL، grantهای runtime/migrate، old/new overlap و recovery. suite/test/QA mapping و داده ساختگی: {{...}}.
