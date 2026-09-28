# بستهٔ فنی آموزشی درخواست replay

وضعیت: draft آموزشی؛ نه G-T و نه مجوز پیاده‌سازی صادر شده است.

- [نقشهٔ اثر](impact-map.md): چرا OTP در این مثال target مستقیم است.
- [جریان مشترک](cross-module-flows.md): مرز caller fixture و نبود consumer محصولیِ نام‌گذاری‌شده.
- [شرح تغییر OTP](modules/otp/change-spec.md) و [نگاشت تست](modules/otp/test-mapping.md): بستهٔ ماژولی نمونه.

برنامهٔ آموزشی: تعریف input/output امن و receipt، مسیر authorization، persistence atomic و replay، سپس سنجش از مرز عمومی با fixture. در pilot واقعی taskها زیر development/modules/otp/tasks قرار می‌گیرند؛ تا تکمیل تمام قراردادها و تأیید G-T هیچ task اجرایی فعال نیست. این نمونه پوشش کامل ماژول OTP نیست.
