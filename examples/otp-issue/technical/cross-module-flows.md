# مرزهای مشترک مثال OTP

در این نسخهٔ **آموزشی** جریان بین دو owner محصولی ندارد؛ تنها caller fixture و ماژول OTP حضور دارند. public boundary replay باید سنجیده شود، ولی fixture به owner داخلی ساختگی تبدیل نمی‌شود.

توالی caller → Application → Work → PostgreSQL در [candidate ماژول](modules/otp/change-spec.md) آمده است. DEMO-QA-03 و 04 به real-store integration و DEMO-QA-05 به authorization/replay نیاز دارند. اجرای end-to-end فرایند محصول مصرف‌کننده خارج این مثال است؛ برای pilot واقعی scope و oracle آن باید از قرارداد مصرف‌کننده تعیین شود.

یک مثال چندماژولیِ مستقل برای نمایش direct/dependent/compatibility-only در [نمونهٔ نقشهٔ اثر](../../module-impact.md) آمده است؛ آن نمونه نیاز جدید OTP تعریف نمی‌کند.
