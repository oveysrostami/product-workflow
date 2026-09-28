# گزارش اجرای QA و تست

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- run-id / candidate revision / dirty و diff digest / baselines P-Q-T: {{...}}
- executor / environment fingerprint غیرحساس / زمان اجرا: {{...}}
- ابزار و نسخه / command دقیق / محدودیت دسترسی: {{...}}

| QA-ID / test | command یا روش دستی | expected | actual امن | pass/fail/blocked/not-run | evidence path/hash | defect |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## صحت شواهد

- suite count / tests / failure / error / skip: {{...}}
- skippedها و اینکه required بوده‌اند: {{...}}
- fixture و database/provider واقعی یا fake: {{...}}
- reportها از همین run و همین revision هستند؟ {{شاهد timestamp/manifest/hash}}
- به علت تغییر candidate کدام شواهد stale شده‌اند؟ {{...}}
- cleanup و اثرات باقی‌مانده: {{...}}

## حکم QA

{{accept / reject / blocked}} با reference تصمیم انسانی. بحرانی‌های باقی‌مانده، پوشش، flakyها و residual owner/موعد: {{...}}. command موفق بدون test discovery کافی نیست؛ planned یا not-run هرگز pass گزارش نشود.


## نتایج ماژولی و سرتاسری

برای هر evidence، targetType/targetId و scope module/integration/end-to-end ثبت شود. گزارش مشترک یک candidate یکسان برای تمام targetها دارد؛ پاس‌بودن جداگانهٔ suiteهای ماژول به‌تنهایی نتیجهٔ مشترک نیست. failure مشترک با EDGE/FLOW و owner پیگیری به تمام targetهای متأثر متصل شود.
