# قرارداد تحویل بین مراحل

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- handover-id / request-id / from-stage / to-stage / فرستنده/گیرنده: {{...}}
- baseline-id و manifest path/digest: {{...}}
- parent baselines و approval referenceها: {{...}}
- وضعیت: {{ready-for-receipt / accepted / returned}}؛ receipt جدا: {{...}}

## خلاصه برای گیرنده

مسئله، outcome و scope همین نسخه: {{...}}. تغییر نسبت به نسخه قبلی: {{...}}. خارج scope: {{...}}.

## ترتیب مطالعه و محل حقیقت

| ترتیب | سند canonical و revision/hash | چرا بخواند؟ | IDهای مهم |
|---|---|---|---|
| 1 | {{...}} | {{...}} | {{...}} |

## تعهد و انتظارات

- محصول→QA: قواعد و UC/AC، حالت شکست/تکرار، داده/مجوز/عمر، dependency و موارد خارج scope؛ QA باید oracle و پوشش مستقل بسازد.
- QA→فنی: risk/scenario/coverage، معیار entry/exit، نیاز fixture/fault/clock و observable evidence؛ فنی test mapping و feasibility را مشخص کند.
- فنی→توسعه: impact-map و cross-module-flows، index بسته‌های change-spec/test-mapping ماژول‌ها، operation/DTO و error canonical، owner/layer/file، transaction/durability، composition، migration/runbook، dependency و task order و command evidence؛ developer فقط با G-T معتبر و اختیار صریح پیاده‌سازی همان scope اجرا کند.
- توسعه→review/دریافت: candidate، diff، review/evidence ماژول‌ها و کل درخواست، test reports ماژولی و integration/end-to-end، traceability، known limitation و وضعیت دقیق merge/deploy؛ گیرنده همان نسخه را باز کند.

فقط بند مرحلهٔ مربوط را با اطلاعات واقعی تکمیل کنید؛ بقیه را به‌عنوان راهنما حذف کنید.

## وابستگی و موارد باز

| موضوع | owner | اثر/trigger | blocking یا خارج scope با دلیل | reference تصمیم |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## شرط دریافت

hashها منطبق، منابع قابل دسترسی، approval لازم موجود، مسئول مرحلهٔ بعد مشخص و blocker در scope صفر. برگشت باید finding، owner و node دقیق داشته باشد. این سند به‌تنهایی ارسال خارجی یا اعلام دریافت نیست.
