# گزارش بازبینی

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- review-id / مرحله / reviewer و نقش: {{...}}
- نویسنده و شاهد استقلال reviewer: {{...}}
- input baseline/digest / code revision یا diff digest: {{...}}
- scope و معیار review: {{...}}

| finding | severity | محل دقیق/ID | شاهد منبع | اثر/سناریوی شکست | اصلاح پیشنهادی | owner/node | وضعیت و evidence رفع |
|---|---|---|---|---|---|---|---|
| {{F-01}} | {{blocking/major/minor}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## رأی و پوشش

{{ready / rework / need-human / محدودیت استقلال}}. حوزه‌های واقعاً بررسی‌شده: {{...}}. حوزهٔ بررسی‌نشده و علت: {{...}}. blockerهای باقیمانده: {{...}}.

برای code review، POM/import/SQL و call/event/recovery graph، authorization، durability، compatibility و evidence freshness جدا نام برده شوند. نتیجه «یافته‌ای نبود» به معنی تست اجراشده یا تأیید انسان نیست.


## سطح review

reviewScope: {{module / request}}؛ targetType/targetId یا targetهای مشارکت‌کننده: {{...}}؛ IMPACT/EDGE/FLOW: {{...}}.

در review درخواست، نتیجهٔ review تک‌تک ماژول‌های متأثر، compatibility قراردادها، ترتیب dependency و evidence integration/end-to-end بررسی می‌شود. اگر یک فرد مسئول چند ماژول است، انتساب و رأی هر scope صریح ثبت شود. blocker مشترک باید در هر دو سمت edge دیده شود.
