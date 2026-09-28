# مثال آموزشی: تکرار درخواست صدور OTP

این مثال از [قرارداد محصول OTP](../../../product-doc/modules/otp/00-product-contract.md) و [پذیرش‌ها](../../../product-doc/modules/otp/tests/product-acceptance-scenarios.md) استفاده می‌کند. scope نمایش، تفاوت لایه‌های مستندات برای P-09 و OTP-04/05/16 است؛ **طرح کامل یا مجوز پیاده‌سازی OTP نیست**. سایر محدودیت‌های واقعی OTP مانند مجوز، سهمیه و عدم نگهداری کد همچنان لازم‌اند و این مثال آن‌ها را لغو نمی‌کند.

| سند | چیزی که نشان می‌دهد |
|---|---|
| [محصول](product.md) | معنای یک‌بار نمایش کد و تکرار همان درخواست |
| [QA](qa.md) | oracle مستقل و failure case بدون تصمیم SQL |
| [فنی](technical/index.md) | impact-map و بستهٔ ماژولی OTP، همراه candidate و test-mapping |
| [تحویل](handover.md) | بسته قابل انتقال با status صادقانه |
| [مسیرهای تمرینی](walkthroughs.md) | happy path، پاسخ جزئی، برگشت و باگ |

هیچ approval انسانی، تست pass یا Backend implementation برای این مثال ادعا نشده است. نقش‌های انسانی نام‌گذاری سازمانی نشده‌اند. اجرای pilot واقعی از I01 و انتصاب نقش‌ها شروع می‌شود.
