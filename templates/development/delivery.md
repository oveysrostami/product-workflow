# تحویل نتیجه و پذیرش

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- request / candidate revision و artifact digest / baseline P-Q-T: {{...}}
- scope تمام‌شده و وضعیت دقیق: {{reviewed / ready-to-merge / merged / deployed؛ هرکدام با شاهد}}

## نتیجه

چه مسئله‌ای حل شد و رفتار پیش/پس چیست؟ {{...}}. مسیر کد/قرارداد مهم: {{...}}. scope خارج و محدودیت: {{...}}.

## evidence

| ادعا / AC / Backend rule | evidence path/hash | revision/run/environment | نتیجه/count/skip | محدودیت |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

review مستقل و findingهای بسته‌شده: {{...}}. رأی QA، Tech lead و درخواست‌کننده روی candidate: {{approval refs}}. testcase بدون اجرا صریح not-run می‌ماند؛ اگر لازم است G-D نمی‌گذرد.

## تحویل عملیاتی مرتبط

migration/compatibility، config و secret references، flags، observability، rollback/restore/reconcile، operator و runbook: {{...}}. اگر انتشار در scope نیست روشن ثبت کنید.

## باقی‌مانده و دریافت

| مورد | اثر | owner | trigger/موعد | blocking یا nonblocking و دلیل |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

manifest نهایی، گیرنده، receipt و next action: {{...}}. پایان پیاده‌سازی مساوی انتشار نیست.


## تحویل ماژول‌ها و نتیجهٔ مشترک

| targetType / targetId | IMPACT-ID و نوع اثر | task/review | evidence محلی | evidence مشترک QA/FLOW | رأی مسئول فنی و limitation |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

سپس تحقق outcome کل درخواست را با evidence integration/end-to-end مربوط و همان candidate توضیح دهید. نبود تغییر کد در target سازگاری-only با نبود اثر آزمون یکسان نیست.
