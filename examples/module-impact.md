# مثال آموزشی نقشهٔ اثر چندماژولی

این مثال کاملاً فرضی است و هیچ نیاز محصول یا تغییر Backend را تصویب نمی‌کند. فرض آموزش: قرارداد پاسخ یک owner تغییر می‌کند؛ یک consumer نیازمند تطبیق mapper است و consumer دیگری طبق تحلیل اولیه با همان کد سازگار می‌ماند ولی باید تست شود. نام‌ها برچسب آموزشی‌اند.

| IMPACT-ID | module | نوع اثر | تغییر کد؟ | تغییر/بررسی | سناریو |
|---|---|---|---|---|---|
| DEMO-IMP-01 | source-owner | direct | بله، فقط در فرض آموزش | تولید قرارداد جدید و سازگاری نسخه قبل | DEMO-QA-PROVIDER |
| DEMO-IMP-02 | consumer-owner | dependent | بله، فقط در فرض آموزش | mapper ورودی و ترجمه failure | DEMO-QA-CONSUMER و DEMO-QA-FLOW |
| DEMO-IMP-03 | observer-owner | compatibility-only | خیر طبق فرض؛ نیازمند اثبات | اجرای regression قرارداد فعلی | DEMO-QA-OBSERVER و DEMO-QA-FLOW |

ساختار مورد انتظار درخواست:

```text
technical/
  impact-map.md
  cross-module-flows.md
  implementation-plan.md
  modules/source-owner/change-spec.md
  modules/source-owner/test-mapping.md
  modules/consumer-owner/change-spec.md
  modules/consumer-owner/test-mapping.md
  modules/observer-owner/change-spec.md
  modules/observer-owner/test-mapping.md
  handover.md
development/
  modules/source-owner/tasks/DEMO-TASK-PROVIDER.md
  modules/consumer-owner/tasks/DEMO-TASK-MAPPER.md
  modules/observer-owner/tasks/DEMO-TASK-COMPATIBILITY.md
  cross-module-tasks/DEMO-TASK-FLOW.md
```

DEMO-TASK-COMPATIBILITY کار بررسی و آزمون است و تولید کد اجباری ندارد. DEMO-QA-FLOW یک سناریوی مشترک با oracle واحد در QA است؛ test-mapping همه targetهای مربوط به همان ID لینک می‌دهند. task مشترک یک مسئول integration و allowed paths معین دارد.

ترتیب آموزشی: توافق و review قرارداد provider/consumer، taskهای محلی طبق dependency، آزمون compatibility، سپس اجرای جریان مشترک روی candidate واحد. T06 و V01 هر سه بسته و کل جریان را می‌سنجند؛ سه local pass جای DEMO-QA-FLOW را نمی‌گیرد. اگر قرارداد provider بعداً تغییر کند C01 اثر آن بر هر دو consumer را دوباره بررسی می‌کند.

برای ساخت پروندهٔ واقعی از [impact-map](../templates/technical/impact-map.md)، [change-spec](../templates/technical/module/change-spec.md) و [test-mapping](../templates/technical/module/test-mapping.md) استفاده شود. هیچ approval یا evidence اجرا برای این مثال وجود ندارد.
