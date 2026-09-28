# اثر تغییر و ابطال نسخه

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- change-id / request-id / originNode / resumeNode: {{...}}
- گزارش‌دهنده، مرجع، نوع تغییر و دلیل: {{...}}
- baseline فعلی و desired behavior: {{...}}

| ID/فایل | اثر مستقیم | dependent IDs | re-review/retest لازم | unaffected با دلیل |
|---|---|---|---|---|
| {{RULE/QA/TECH/TASK}} | {{...}} | {{...}} | {{...}} | {{...}} |

## تصمیم scope

{{تغییر/رفع ابهام/رد درخواست، مرجع انسان و owner}}. وضعیت ادغام به گفته درخواست‌کننده و مقصد سند: {{...}}.

## وضعیت پایین‌دست

| approval/evidence | baseline قبلی | valid/stale | چرا؟ | owner و node تجدید |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

کار مستقل مجاز به ادامه: {{...}}؛ کار وابسته متوقف: {{...}}؛ revision تازه و history: {{...}}. reject تغییر مجوز نادیده‌گرفتن gap واقعی scope قبلی نیست.

## اثر ماژولی و قرارداد مشترک

IMPACT-IDهای قدیم/جدید، targetهای اضافه/حذف‌شده، EDGE/FLOWهای تغییرکرده، producer و consumerها و QAهای module/integration/end-to-end متأثر: {{...}}. دلایل unaffected بودن سایر targetها و اثر بر reviewهای محلی و gate کل: {{...}}. تنها سنجش provider برای تغییر public contract کافی نیست.
