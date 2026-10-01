# قرارداد تحویل بین مراحل

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- handover-id / request-id / from-stage / to-stage / فرستنده/گیرنده: {{...}}
- baseline-id و مسیر manifest این بسته: {{...}}؛ digest نهایی این manifest فقط در approval و journal تحویل بیرون بسته ثبت می‌شود.
- parent baselines و approval referenceها: {{...}}
- مسیر receipt جدا: {{...}}؛ وضعیت جاری دریافت فقط در receipt و برد ثبت می‌شود و این سند مصوب تغییر نمی‌کند.

## خلاصه برای گیرنده

مسئله، outcome و scope همین نسخه: {{...}}. تغییر نسبت به نسخه قبلی: {{...}}. خارج scope: {{...}}.

## ترتیب مطالعه و محل حقیقت

| ترتیب | سند canonical و revision/hash | چرا بخواند؟ | IDهای مهم |
|---|---|---|---|
| 1 | {{...}} | {{...}} | {{...}} |

## تعهد و انتظارات

- محصول→QA: قواعد و UC/AC، حالت شکست/تکرار، داده/مجوز/عمر، dependency و موارد خارج scope؛ QA باید oracle و پوشش مستقل بسازد.
- QA→فنی: risk/scenario/coverage، معیار entry/exit، نیاز fixture/fault/clock و observable evidence؛ فنی test mapping و feasibility را مشخص کند.
- فنی→توسعه: impact-map و cross-module-flows، index بسته‌های change-spec/test-mapping و snapshotهای کامل، revisionId و مسیر مقصد و hash plan/فایل‌های snapshot برای انتشار T09، operation/DTO و error canonical، owner/layer/file، transaction/durability، composition، migration/runbook، dependency و task order و command evidence؛ developer فقط با G-T معتبر و اختیار صریح پیاده‌سازی همان scope اجرا کند.
- توسعه→review/دریافت: candidate، diff، review/evidence ماژول‌ها و کل درخواست، test reports ماژولی و integration/end-to-end، traceability، known limitation و وضعیت دقیق merge/deploy؛ گیرنده همان نسخه را باز کند.

فقط بند مرحلهٔ مربوط را با اطلاعات واقعی تکمیل کنید؛ بقیه را به‌عنوان راهنما حذف کنید.

این handover پیش از تأیید freeze می‌شود. digest manifest خودش، رأی نهایی، receipt و digest wrapper انتشار آینده داخل آن نیستند. نتیجهٔ T09 و digest نسخهٔ منتشرشدهٔ هر ماژول پس از G-T در journal تحویل T08 ثبت و به همان handover ارجاع می‌شوند؛ pointer جاری ماژول نیز با آن تطبیق داده می‌شود.

## وابستگی و موارد باز

| موضوع | owner | اثر/trigger | blocking یا خارج scope با دلیل | reference تصمیم |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## شرط دریافت

hashها منطبق، منابع قابل دسترسی، approval لازم موجود، مسئول مرحلهٔ بعد مشخص و blocker در scope صفر. برگشت باید finding، owner و node دقیق داشته باشد. این سند به‌تنهایی ارسال خارجی یا اعلام دریافت نیست.

## مرز تحویل به Backend

Backend معرفی‌شده در project/backend.json با مسیر ../BackendName برای agent product-workflow فقط خواندنی است. طراحی این بسته داخل workflow نوشته شده؛ آماده‌سازی Spec/Plan/Task، آزمون و اجرا در Backend به گیرندهٔ مستقل با قرارداد و اختیار همان محیط تحویل می‌شود. T08 در این scope HOLD است و این handover هیچ اختیار نوشتن Backend به تحویل‌دهنده نمی‌دهد.
