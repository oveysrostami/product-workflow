# گزارش بررسی نسخهٔ ۱٫۱۳

تاریخ: ۲۰۲۶-۱۰-۰۱. محدوده: skill setup اتصال Backend همسایه، مستندسازی فنی محلی و دسترسی فقط خواندنی Backend. انتخاب واقعی درخواست‌کننده در [تصمیم مرزبندی](technical-boundary-decision.md) است؛ تصویب سازمانی کل نسخه همچنان pending است.

## قرارداد و تغییر

[Setup پروژه](../docs/16-project-setup.md) project/backend.json را کنترل‌فایل عملیاتی و ../BackendName را تنها مسیر Backend معرفی می‌کند. AGENTS، skillها، قالب index/handover، مالکیت، gate، onboarding و graph به همین مرز متصل‌اند. اسناد canonical فنی در product-workflow هستند؛ Backend فقط خوانده می‌شود و هیچ command/module آن اجرا/import نمی‌شود. T08 برای skill مستندسازی HOLD است و recorder عبور مستقیم به D01 را رد می‌کند؛ کارت‌های توسعه/release اجرای مستقل آینده را توصیف می‌کنند.

helper فقط project/backend.json را ایجاد می‌کند؛ preview/inspect هیچ فایلی نمی‌نویسند. source/config/plan با runtime verified متفاوت‌اند. validator اتصال موجود و عدم ورود project/backend.json به manifest/inventory ثابت را بررسی می‌کند. این ابزارها sandbox همهٔ writeهای agent یا اثبات تصمیم/هویت انسانی نیستند. بازبینی مستقل subagent تغییر نگهداری انجام نشده؛ review دومرحله‌ای بسته‌های واقعی همچنان برقرار است.

## بررسی جاری

۹ آزمون setup در fixture موقت پاس شدند: مسیر همسایه مستقل از cwd، basename/traversal و پوشهٔ غایب، symlink، preview بدون تغییر، apply فقط کنترل‌فایل محلی، retry/عدم overwrite و حفظ منبع، عدم تغییر/اجرای کد Backend و عدم خروج secret، ثبت setup ناقص/منقضی و عدم ادعای runtime. ۲۹ آزمون skill workflow پاس شدند؛ regression تازه از تحویل T08 به اجرای مستقیم Backend جلوگیری می‌کند. دو آزمون validator برای اتصال mutable/read-only و جدایی آن از بستهٔ immutable اضافه شدند؛ هر ۱۴ آزمون مجموعه پاس شدند. مجموع سه suite برابر ۵۲ آزمون موفق است. validator بدون خطا، کارت‌های generated منطبق و git diff --check موفق بودند.

quick_validate روی هر دو skill موفق بود؛ از Python/PyYAML موجود در /private/tmp/product-workflow-skill-validation-20260929 استفاده شد و dependency نصب نشد. هر ۱۵ نمودار Mermaid با CLI موجود و Google Chrome headless parse و رندر شدند؛ گزارش واقعی و hashها در [شاهد](mermaid-evidence.json) هستند. بررسی بصری همهٔ SVGها ادعا نمی‌شود.

## نصب و مشاهدهٔ خواندنی

skill setup از منبع repository در ~/.codex/skills/product-workflow-setup نصب شد. قبل از sync skill قبلی، تمام فایل‌های نصب‌شده با HEAD تطبیق داشتند؛ تغییرات محلی overwrite نشدند و فقط فایل‌های تغییرکرده همگام شدند. preview روی Backend قبلاً معرفی‌شده backend-spring بدون apply و بدون اجرای کد آن انجام شد: ۱۳ منبع و ۵ ماژول موجود در source، setup record مشاهده‌نشده و runtime unknown؛ اتصال واقعی workflow ساخته نشد.

نسخهٔ دقیق ۱٫۱۲، manifest/approval و hash همهٔ ۱۴۰ artifact در [آرشیو](history/workflow-kit-v1.12.zip) و [رکورد](history/workflow-kit-v1.12.json) حفظ شدند. نسخهٔ ۱٫۱۳ approval pending مستقل دارد. اجرای واقعی setup یک پروژه، gate درخواست، activation SDD یا verification runtime Backend از این بررسی نتیجه نمی‌شود.
