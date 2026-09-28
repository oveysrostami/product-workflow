# طرح انتشار اختیاری

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- request / G-D / artifact revision/hash / target: {{...}}
- Release owner / Operator / authorization reference با actions و limits: {{...}}

## ترتیب اعمال قابل review

| action | اثر دقیق و مقصد | prerequisite | evidence موفقیت/readback | recovery | صاحب اختیار |
|---|---|---|---|---|---|
| {{merge/migrate/deploy/flag}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## سازگاری و داده

expand/backfill/contract، old/new consumers/workers، drain، retention/replay، backup و restore reconciliation: {{...}}. rollback binary داده/اثر provider را لزوماً برنمی‌گرداند.

## gate و خروج

verify full و policy release جاری، current-run ledger/report/JAR/SBOM، candidate freshness، migration grants و actual sink/provider acceptance: {{...}}. smoke و monitoring thresholds، زمان مشاهده موردنیاز و owner: {{...}}.

## failure

rollback/roll-forward/reconcile در حدود اختیار، trigger توقف، unknown effect و readback، incident handover و receipt عملیات: {{...}}. نبود اختیار یا prerequisite به blocked می‌رود.
