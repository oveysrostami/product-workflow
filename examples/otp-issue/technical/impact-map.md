# نقشهٔ اثر آموزشی replay

| IMPACT-ID | target | نوع اثر | شاهد و دامنه | تغییر کد | بسته |
|---|---|---|---|---|---|
| DEMO-IMP-OTP | module: otp | direct | DEMO-P02/P03/P04/P05 و DEMO-AC-01 تا DEMO-AC-04 در قرارداد/پذیرش محلی؛ معنای صدور و replay | فقط پیشنهاد برای pilot؛ پیاده‌سازی انجام نشده | [change-spec](modules/otp/change-spec.md)، [test-mapping](modules/otp/test-mapping.md) |

Caller این مثال یک fixture سرویس مجاز است و owner محصولی مستقلی معرفی نشده است. Account یا Notification از روی نام مثال به scope اضافه نمی‌شوند. در pilot واقعی T02 باید consumerهای واقعی را شناسایی کند و در صورت اثر dependent یا compatibility-only برایشان بسته بسازد. نبود اطلاعات consumer به معنی اثبات unaffected بودن آن نیست.

host/platform در این آموزش تغییر نمی‌کنند؛ مسیر عمومی و تنظیمات کامل در طرح pilot باز است. انتخاب این scope فقط محدودهٔ آموزش است، نه تأیید معماری یا کاهش الزامات واقعی OTP.
