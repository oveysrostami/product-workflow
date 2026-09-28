# گزارش باگ و regression

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- BUG/DEF-ID / request و originNode / reporter / status: {{reported / reproduced / investigating / fixed-awaiting-QA / verified / inconclusive / closed-as-designed}}
- ماژول‌ها و اثر / environment و candidate / زمان امن: {{...}}
- قرارداد baseline و RULE/UC/AC یا QA-ID: {{...}}

## مشاهده و انتظار

Actual: {{آنچه مشاهده شده و evidence امن}}.
Expected: {{معنی دقیق قاعده با source؛ نه حدس AI}}.

بازتولید گام‌به‌گام با fixture ساختگی: {{...}}. نرخ تکرار/شرایط و وضعیت not-reproduced اگر مربوط: {{...}}. scope اثر و شدت در برابر priority: {{...}}.

## سناریوی regression

{{Given/When/Then/Must-not و محل ثبت در QA scenarios}}.

## investigation و رفع

| فرض/یافته | fact یا hypothesis | شاهد source→failure | اثر data/consumer | تصمیم fix یا ادامه |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

approval گزارش خارجی توسط همان درخواست‌کننده: {{reference}}؛ دریافت فنی: {{receipt}}؛ fix plan/TECH/task: {{...}}؛ code revision: {{...}}؛ retest/regression evidence و QA verification: {{...}}.

گزارش تأییدشده «آماده بررسی فنی» است. technical acknowledgment پایان مرحله محصولی باگ است؛ تنها retest معتبر می‌تواند fixed را به verified تبدیل کند.
