# نقشهٔ اثر درخواست بر ماژول‌ها

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. این سند به‌تنهایی approval یا evidence اجرا نیست.

- request / baseline P-Q / source revision Backend / مسئول تحلیل: {{...}}
- مسئله و outcome درخواست، نه فقط فهرست فایل‌ها: {{...}}

## ماژول‌های متأثر

| IMPACT-ID | module-slug | اثر direct/dependent/compatibility-only | علت و شاهد caller/contract/data | حوزه رفتار/data/API/event/config/auth | code change لازم؟ | مسئول فنی | change-spec/test-mapping | QA-IDها |
|---|---|---|---|---|---|---|---|---|
| {{IMP-01}} | {{...}} | {{...}} | {{...}} | {{...}} | {{yes/no/open با دلیل}} | {{...}} | {{modules/slug/...}} | {{...}} |

برای هر ردیف، `modules/<module-slug>/change-spec.md` و `test-mapping.md` بسازید. ماژول فقط نیازمند سنجش سازگاری نیز این دو سند را کوتاه و مستدل دارد؛ برایش task تولید کد نسازید. status فعلی کد، requirement تازه ایجاد نمی‌کند.

## وابستگی‌ها

| EDGE-ID | provider → consumer | contract/version | نوع اثر روی مصرف‌کننده | پیش‌نیاز اجرا/rollout | FLOW/QA مشترک | owner |
|---|---|---|---|---|---|---|
| {{EDGE-01}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## host/platform و موارد بررسی‌شدهٔ بدون اثر

| targetType / targetId | متأثر یا unaffected | شاهد و دلیل | component packet یا دلیل نبود پوشه | owner |
|---|---|---|---|---|
| {{host/platform/module}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای host/platform متأثر، بسته در `components/<component-id>/` قرار می‌گیرد؛ از این دسته‌بندی owner کسب‌وکار ساختگی نسازید. اثر نامعلوم open item است، نه unaffected.

## جمع‌بندی دامنه

فهرست کامل targetهای وارد G-T، ریسک compatibility، بخش‌های مستقل قابل ادامه و موارد باز با owner: {{...}}. هر تغییر فهرست یا edge از C01 و بررسی stale شدن وابستگی‌ها عبور می‌کند.
