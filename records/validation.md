# گزارش بررسی نسخهٔ ۱٫۸

تاریخ: ۲۰۲۶-۰۹-۲۸. محدودهٔ محصول، QA و فنی تا انتشار مستندات ماژول‌های درگیر و آمادگی پیاده‌سازی بررسی شد. این گزارش بررسی قرارداد و قالب‌های workflow است؛ اجرای پروندهٔ واقعی یا اثبات Backend نیست. تصویب انسانی کل نسخه pending است.

## نتیجهٔ بررسی مسیر

[چرخهٔ مستندسازی](../docs/11-documentation-cycle.md) ترتیب دریافت، پرسش‌وپاسخ، نگارش، review، رأی انسان و handover را برای هر سه تیم مشخص می‌کند. مصاحبهٔ محصول حفظ شد؛ Q07/Q08 برای QA و T10/T11 برای فنی افزوده شدند. پاسخ جزئی، ادامه پس از وقفه، کفایت اطلاعات بدون سؤال ساختگی و پایان مصاحبه با موارد باز مسیر مشخص دارند. پاسخ مصاحبه جای G-Q/G-T نیست.

برگشت QA به محصول و فنی به محصول/QA از مرحلهٔ تحلیل، گفت‌وگو و review به تیم مالک متصل است. C01 فقط اثر و اصلاحیه را در فایل کنترلی ثبت می‌کند؛ به‌روزرسانی impact-map با فنی می‌ماند. تغییر upstream به review/approval و دریافت مجدد نسخهٔ لازم متصل است.

handover پیش از gate freeze می‌شود؛ P08/Q06/T08 فرمان نگارش اسناد مصوب ندارند. digest manifest خودش و نتیجهٔ انتشار آینده در handover قرار نمی‌گیرند؛ این اطلاعات در approval/receipt/journal خارج manifest ثبت می‌شوند. تأیید G-T پیش از T09/T08 هنوز آمادگی تحویل نیست؛ تمام ماژول‌های درگیر باید منتشر و readback شوند.

## بررسی ساختاری و regression

```sh
python3 scripts/render_workflows.py --check
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

کارت‌های تولیدشده با graph منطبق و validator بدون خطا است. مجموعه ۸۰ Markdown، ۶۳ node در ۸ workflow، ۳۸ مسیر تمرینی و ۹۱ منبع ثابت دارد؛ آمار دقیق در [checks](checks.json) ثبت شده است. ۱۱ مسیر تازهٔ [تمرین تیم‌ها](../examples/team-entry.md) شامل پاسخ جزئی QA/فنی، توقف مصاحبه، برگشت به محصول/QA، انتشار چند ماژول و تغییر base هستند. validator اتصال edgeهای این مسیرها را می‌سنجد؛ ثبت واقعی پاسخ انسان و صحت معنایی تصمیم همچنان با review بررسی می‌شود.

هر ۱۲ آزمون موجود [regression](../scripts/test_validate.py) پاس شد: پنج آزمون جدایی وضعیت برد از طراحی و هفت آزمون انتشار دقیق snapshot مصوب، retry، حفظ تاریخچه، رد approvalِ pending، bytes تغییرکرده، base منقضی، مقصد symlink و ادعای پیاده‌سازی بدون revision. fixtureها فقط در کپی موقت ساخته شدند؛ هیچ کارت، approval، receipt یا ماژول واقعی ایجاد نشده است.

## Mermaid

همهٔ ۱۵ نمودار فعلی با Mermaid CLI 12.0.0، Node 22.22.0 و Google Chrome headless دوباره parse و به SVG رندر شدند. [شاهد رندر](mermaid-evidence.json) hash متن نمودارها و خروجی واقعی را نگه می‌دارد. بازرسی بصری تک‌تک نمودارها ادعا نمی‌شود؛ dependency پروژه تغییر نکرد.

## تاریخچه، scope و حدود بررسی

نسخهٔ دقیق ۱٫۷ پیش از تغییر در [آرشیو](history/workflow-kit-v1.7.zip) و [رکورد hash](history/workflow-kit-v1.7.json) حفظ شد. hash آرشیو، manifest، approvalِ pending و تمام artifacts منطبق‌اند. نسخهٔ ۱٫۸ manifest و approvalِ pending مستقل دارد؛ خواستهٔ کاربر در [ثبت طراحی](design-review.md) مرجع اختیار اصلاح است.

diff نسبت به آرشیو ۱٫۷ با writeScope نگهداری workflow تطبیق داده شد؛ git diff --check بدون خطا بود. برد واقعی با نسخهٔ آرشیوی یکسان است و تعداد کارت/ماژول واقعی صفر است. فایل Backend تغییر نکرد و پیاده‌سازی، merge یا deploy انجام نشد. این بررسی self-review است؛ independent review یا تأیید انسانی جعل نشده است.
