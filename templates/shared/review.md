# گزارش بازبینی

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- review-id / مرحله / reviewer و نقش: {{...}}
- نویسنده و شاهد استقلال reviewer: {{...}}
- input baseline/digest / code revision یا diff digest: {{...}}
- scope و معیار review: {{...}}

برای مستندات محصول/QA/فنی، ابتدا گزارش subagent در P05/Q04/T06 و سپس رأی reviewer انسانی در P12/Q09/T12 طبق قرارداد ثبت می‌شوند. هر رکورد review-id جدا دارد و بیرون manifest محتوای تیم به همان bytes متصل است؛ رد/اصلاح، رکورد قبلی را بازنویسی نمی‌کند.

## گزارش subagent

- agent-id / مرجع مأموریت / writer-id و دلیل استقلال: {{...}}
- فهرست کامل فایل/بخش‌های مطالعه‌شده و digest/revision: {{...}}
- دامنهٔ ناقص/دسترس‌ناپذیر و علت: {{...}}
- مرجع نسخهٔ اصلاحی و review قبلی در صورت تکرار: {{...}}

| finding | severity | محل دقیق/ID | شاهد منبع | اثر/سناریوی شکست | اصلاح پیشنهادی | owner/node | وضعیت و evidence رفع |
|---|---|---|---|---|---|---|---|
| {{F-01}} | {{blocking/major/minor}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## رأی و پوشش

{{ready / rework / blocked}}؛ تصمیم انسانی لازم یا محدودیت استقلال با علت: {{...}}. حوزه‌های واقعاً بررسی‌شده: {{...}}. حوزهٔ بررسی‌نشده و علت: {{...}}. blockerهای باقیمانده: {{...}}.

برای code review، POM/import/SQL و call/event/recovery graph، authorization، durability، compatibility و evidence freshness جدا نام برده شوند. نتیجه «یافته‌ای نبود» به معنی تست اجراشده یا تأیید انسان نیست.

## رکورد جداگانهٔ رأی reviewer انسانی اسناد

در رکورد انسانی جدا و append-only ثبت شود:

- review-id / node انسانی / identity / نقش و مرجع انتصاب: {{...}}
- نسخه و digest بستهٔ بررسی‌شده: {{...}}
- review-id، مسیر و digest گزارش subagent مرتبط: {{...}}
- تصمیم واقعی accepted یا rework / متن و مرجع پیام / زمان واقعی یا null: {{...}}
- یافته‌های انسانی و مقصد اصلاح یا معیار تأیید: {{...}}
- ثبت‌کنندهٔ کنترل Coordinator است؛ executor تصمیم Human؛ decisionReference در journal همین پاسخ واقعی است.

تا دریافت رأی واقعی، waiting-human با resumeNode همان node انسانی است؛ placeholder، معرفی reviewer، پاسخ interview یا رأی subagent رأی انسانی نیست. این تأیید، approval نهایی gate نیست.


## سطح review

reviewScope: {{module / request}}؛ targetType/targetId یا targetهای مشارکت‌کننده: {{...}}؛ IMPACT/EDGE/FLOW: {{...}}.

در review درخواست، نتیجهٔ review تک‌تک ماژول‌های متأثر، compatibility قراردادها، ترتیب dependency و evidence integration/end-to-end بررسی می‌شود. اگر یک فرد مسئول چند ماژول است، انتساب و رأی هر scope صریح ثبت شود. blocker مشترک باید در هر دو سمت edge دیده شود.
