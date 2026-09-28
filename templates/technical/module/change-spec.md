# تغییرات یک ماژول در این درخواست

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. این سند به‌تنهایی approval یا evidence اجرا نیست.

- request / IMPACT-ID / targetType و targetId / module-slug: {{...}}
- مسئول فنی / نوع اثر / نیاز به تغییر کد و دلیل: {{...}}
- baseline فعلی Backend و baseline محصول/QA: {{...}}

## قبل و بعد

{{رفتار یا قرارداد موجود، تغییر موردنیاز همین درخواست، non-goal و source RULE/AC/QA}}. برای compatibility-only، «کد تغییر نمی‌کند» با تحلیل اثر و آزمون لازم نوشته شود؛ قالب طراحی کامل را بی‌دلیل تکثیر نکنید.

## delta و محل حقیقت

| TECH-ID | موضوع تغییر | وضع قبلی → طرح جدید | قاعده/سناریو | سند canonical Backend با revision/hash/section | فایل/لایه متأثر |
|---|---|---|---|---|---|
| {{...}} | {{domain/usecase/DTO/data/migration/security/event/config}} | {{...}} | {{...}} | {{...}} | {{...}} |

جزئیات کامل operation/DTO/data/delivery در اسناد canonical همان owner تکمیل می‌شود؛ این پرونده delta و دلیل و ارجاع را نگه می‌دارد. یک clause دو نسخه editable ندارد. اگر draft موقت اینجا تولید شد، T06 انتقال/انتخاب مرجع را پیش از freeze قطعی کند.

## وابستگی و consumerها

EDGE/FLOWهای مشترک، producer/consumerهای متأثر، compatibility و migration/rollout prerequisites: {{...}}. import runtime یا SQL خصوصی owner دیگر مجاز نیست.

## اجرا و تست

TASK-IDها و مسیر بسته‌های `development/modules/<slug>/tasks/`، ترتیب داخل slice، test-mapping همین target و evidence موردنیاز: {{...}}. task مشترک host/integration یک مسئول مشخص و allowed paths دارد.

## review ماژول

یافته‌ها، reference reviewer مستقل، رأی مسئول فنی روی manifest درخواست و blockerهای باقی‌مانده: {{...}}. local ready به معنی G-T/G-D کل درخواست نیست.
