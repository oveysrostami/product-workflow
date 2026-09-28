# نگاشت QA ماژول OTP

IMPACT-ID: DEMO-IMP-OTP؛ target: module/otp. همهٔ ردیف‌ها planned/not-run هستند. oracle در [QA](../../../qa.md) تک‌مرجع است؛ candidate در [change-spec](change-spec.md).

| QA-ID | scope | محل سنجش پیشنهادی | oracle/evidence موردنیاز | وضعیت |
|---|---|---|---|---|
| DEMO-QA-01/02 | module | mapping و receipt tests | همان شناسه بدون raw code؛ conflict intent متفاوت و بدون اثر تازه | planned |
| DEMO-QA-03/04 | integration | PostgreSQL با barrier/fault و مرز response | یک اثر واقعی و عدم افشای مجدد پس از commit/قطع response | planned |
| DEMO-QA-05 | integration | Application و receipt با permission جاری | revoke با replay bypass نمی‌شود | planned |
| DEMO-QA-06 | module/integration | response/receipt/diagnostic boundaries | absence داده حساس در همه مسیرهای مورد ادعا | planned |

نام کلاس و مسیر suite نهایی، محیط و taskها در pilot واقعی تعیین می‌شوند؛ این نگاشت آموزشی G-T-ready نیست. در صورت اضافه‌شدن consumer محصولی واقعی، QA مشترک با همان ID در test-mapping هر دو target لینک و evidence end-to-end مستقل ثبت خواهد شد.
