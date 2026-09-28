# مالکیت، context و Domain

> قالب است؛ `{{...}}` را با تصمیم و شاهد واقعیِ غیرحساس جایگزین کنید. وجود این فایل به معنی approval یا اجرای تست نیست.

## module و context

| owner | مسئولیت/زبان | داده و invariant متعلق | خارج scope | actor/permission | public exports |
|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای هر رابطه upstream/downstream، published language/ACL/customer-supplier و دلیل تعیین کنید. سه نمودار واقعی مستقل: dependencyهای source، synchronous calls و durable event/process/recovery. label هر edge contract/version/owner را نشان دهد؛ وجود cycle و ambient transaction بررسی شود.

## aggregate و مدل خالص

| aggregate/value/entity | identity/scope | invariant فوری | creation در برابر restore | transition/rejection | concurrent action | repository/read-store |
|---|---|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

برای هر aggregate توضیح مستقل boundary consistency، bounded load/save، child membership، equality/immutability، external references و version بنویسید. اگر query بدون aggregate است دلیل و bounded criteria/read-store را مشخص کنید.

## lifecycle و proof

stateDiagram/flowchart واقعی با failure بدون partial mutation، factory در برابر restore و modelVersion ناشناخته اضافه شود. time/ID/facts ورودی resolved هستند؛ domain IO/config/framework ندارد. domain fact خصوصی از integration event مستقل است.

| invariant / Backend rule | behavior source | pure test | failure/no-partial-mutation assert | QA-ID |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## محل کد و قرارداد

{{contracts/runtime/domain/application/infrastructure/presentation، package، POM، imports مجاز و forbidden، host wiring}}. معیار review مالکیت قبل از SQL/controller است.
