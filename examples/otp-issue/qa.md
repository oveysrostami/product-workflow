# QA: بررسی مستقل replay صدور

وضعیت تمام سناریوها **planned / not-run** است. source: P-09/P-12 و OTP-04/05/16 در اسناد OTP؛ permission checks از P-02/P-10.

| ID | Given / When | Then و Must-not | مشاهدهٔ evidence |
|---|---|---|---|
| DEMO-QA-01 | سرویس مجاز، fixture مقصد و کاربرد؛ صدور موفق و سپس همان intent/key | همان challenge؛ raw code در response دوم absent؛ صدور و سهمیه اثر دوباره ندارد | response contract و state/count امن؛ secret در گزارش چاپ نشود |
| DEMO-QA-02 | key قبلی با مقصد یا کاربرد متفاوت | conflict؛ challenge تازه و تغییر قبلی رخ ندهد | error معنایی و absence of side effect |
| DEMO-QA-03 | commit صدور موفق، response پیش از رسیدن قطع، همان درخواست تکرار | فقط شناسه قبلی؛ هیچ بازیابی raw code و هیچ صدور دوباره | fault بعد commit قبل response و همان durable identity |
| DEMO-QA-04 | دو درخواست همان key/intent هم‌زمان با barrier | حداکثر یک صدور واقعی؛ کد خام حداکثر در یک پاسخ | state واقعی و دو outcome؛ جزئیات اولین برنده نیازمند طراحی/بازبینی |
| DEMO-QA-05 | پس از صدور، مجوز همان سرویس قطع؛ replay | عدم bypass authorization و عدم افشای کد | permission source فعلی و denied outcome |
| DEMO-QA-06 | sentinel ساختگی به‌جای secret در fixture؛ storage/log/trace/error بررسی | raw code در هیچ سابقه نباشد | assertion عدم وجود sentinel بدون چاپ آن |

شرح DEMO-QA-03: fixture سرویس و کاربرد مجاز و policy کافی؛ fault روی ارسال پاسخ پس از commit فعال می‌شود. caller همان key را حفظ می‌کند. بعد از برداشتن fault، همان درخواست دوباره اجرا می‌شود. observable oracle challenge یکسان و نبود فیلد کد در پاسخ replay است؛ provider ارسال پیام اصلاً مسئولیت OTP نیست. cleanup داده fixture بعد اجرا انجام شود. تصمیم فناوری fault injection با فنی است.

Q04 باید ruleهای باقیمانده OTP را برای pilot واقعی پوشش دهد؛ شش سناریوی این مثال پوشش کامل ماژول نیستند. اعداد سهمیه/زمان، مرز انقضا و دیگر عملیات از source خودشان می‌آیند؛ از این مثال رفتار تازه نتیجه نگیرید.
