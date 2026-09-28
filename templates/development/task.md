# بستهٔ کار توسعه‌دهندهٔ AI

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

- TASK-ID / request / slice / assigned agent: {{...}}
- targetType / targetId / IMPACT-ID / مسئول فنی: {{...}}
- change-spec و test-mapping این target / EDGE/FLOW مشترک: {{...}}
- مسیر packet: {{development/modules/slug/tasks/id.md یا development/cross-module-tasks/id.md}}
- input baselines P/Q/T و digest / approval / implementation authorization: {{...}}
- checkout/base revision و dirty/diff snapshot: {{...}}
- prerequisite tasks و status: {{...}}
- تیم فعال / مسیرهای مجاز متعلق به همین تیم / مرجع انتساب: {{...}}

اسناد محصول، QA و فنی ورودی فقط خواندنی‌اند؛ حتی قرارگرفتن یک مسیر در این task مجوز ویرایش فایل متعلق به تیم دیگر نیست. توسعه برای نقص طراحی/سناریو اصلاحیه می‌دهد و evidence خودش را ثبت می‌کند.

## ورودی لازم به ترتیب

{{AGENTS/handbook/owner docs، rule/UC/AC/QA، TECH operation و backend workflow}}.

## کار و مرز

{{تغییر دقیق در هر owner/layer/file، public contract/data/API و non-goal}}. فایل‌های خارج اختیار: {{...}}. componentهایی که لازم نیستند: {{...}}.

## ترتیب و evidence

| گام | خروجی | command/test | شرط پایان | نتیجه واقعی/report |
|---|---|---|---|---|
| preflight | {{...}} | {{...}} | {{...}} | {{not-run}} |
| domain/application | {{...}} | {{...}} | {{...}} | {{not-run}} |
| adapter/storage | {{...}} | {{...}} | {{...}} | {{not-run}} |
| entrypoint/composition | {{...}} | {{...}} | {{...}} | {{not-run}} |
| verify/review packet | {{...}} | {{...}} | {{...}} | {{not-run}} |

## توقف و ادامه

ابهام رفتار → C01، نقص طرح → T04، محیط غایب → blocked همان node، fail → لایه مالک، input stale → impact. checkpoint، output paths و nextNode: {{...}}. success stub، mock-only durability و waiver عمومی ممنوع.


## پایان محلی و پایان درخواست

نتیجهٔ task و ماژول: {{...}}؛ evidence integration/end-to-end لازم و مسئول اجرای آن: {{...}}. task مشترک فقط allowed paths مشخص دارد؛ برای target بدون تغییر کد، کار به سنجش سازگاری محدود است. local ready، تأیید کل request یا مجوز merge/deploy نیست.
