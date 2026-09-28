# handover آموزشی محصول به QA

- شناسه: DEMO-OTP-P-Q؛ scope: replay صدور مطابق DEMO-P01 تا DEMO-P06.
- فرستندهٔ نمونه: Product writer؛ گیرندهٔ لازم: QA owner که در pilot واقعی منصوب می‌شود.
- وضعیت: **draft، هنوز ready-for-receipt نیست**؛ approval و manifest تولیدی ندارد.
- ترتیب مطالعه: [محصول](product.md)، [پذیرش‌های محصول](acceptance.md)، سپس [QA آموزشی](qa.md).
- تعهد محصول: کد فقط پاسخ نخست؛ replay همان شناسه بدون کد و بدون اثر تازه؛ same key/different intent conflict؛ مجوز جاری و privacy برقرار.
- خارج دامنهٔ مثال: قرارداد کامل Verify/Cancel/config/cleanup، rollout و اتصال Account. نیازهای این عملیات برای یک نسخهٔ واقعی در همان پروندهٔ تازه تصمیم‌گیری می‌شوند.
- انتظار از QA: تحلیل independent oracle برای response lost، race، permission و leak؛ پوشش شش پذیرش محلی؛ scope افزودهٔ pilot فقط از قرارداد مصوب همان پرونده.
- انتظار از فنی بعد QA: DTO/receipt بدون raw code، Work اتمی و test mapping واقعی؛ فرض existence ماژول OTP ممنوع.
- موارد باز برای pilot: تعیین افراد gate، snapshot/approval قرارداد همان پرونده، حدود slice واقعی و محیط evidence؛ این‌ها blocker اجرای واقعی‌اند.
- شرط دریافت واقعی: manifest معتبر و G-P صریح و دسترسی QA؛ receipt pending تا پاسخ انسان. این مثال receipt ساختگی تولید نمی‌کند.
