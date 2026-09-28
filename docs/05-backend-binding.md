# اتصال فرآیند به boilerplate موجود

این صفحه قرارداد داخلی اتصال به مخزن کد هدف و یک adapter نمونه برای ساختار بررسی‌شدهٔ Backend است. برای استفاده از workflow و قالب‌ها نیازی به checkout همسایه نیست. در شروع هر اجرای واقعی، revision و قواعد جاری دوباره خوانده می‌شوند. این صفحه راهنماست و authority موازی با `AGENTS.md` (AGENTS Backend) نمی‌سازد.

## انتخاب مخزن کد هدف

در T01/T02 مسیر checkout، repository، revision، دستور AGENTS و محل قواعد کدِ هدف در request/technical-index ثبت می‌شوند. محل نصب ثابت یا checkout همسایه فرض نمی‌شود. مسیرهای کد و commandهای زیر نسبت به همان checkout معرفی‌شده‌اند؛ در این پروژه اجرا نمی‌شوند. اگر ابزار یا قابلیت نمونه در هدف وجود ندارد، فنی معادل واقعی یا prerequisite را مشخص می‌کند؛ غیبت آن با نتیجهٔ ساختگی پوشانده نمی‌شود. طراحی اولیه می‌تواند با قالب‌های محلی آماده شود؛ تأیید انطباق با کد و اجرای تغییر نیاز به ورودی واقعی همان مخزن دارد.

## adapter نمونه و محدودهٔ کاربرد

`pom.xml` (reactor) پیش‌فرض شامل `platform/kernel`، `contracts`، `runtime`، `adapters-spring`، `testing` و `application-host` است. نمونه‌های Access/Tasks/Activity و fixtureهای DeliveryProbe/WorkflowProbe در profile جدا `reference-examples` هستند. Java 25، Spring Boot 4.1.1، wrapper Maven 3.9.11 و PostgreSQL 18 baseline نمونهٔ بررسی‌شده است، نه انتخاب الزامی هر پروژه؛ تصمیم ارتقا در scope این طراحی نیست.

هسته host محصول/IAM/datasource/worker آمادهٔ همهٔ نیازها نیست. `_doc/15-authority-and-traceability.md` (وضعیت authority و drift) بین implemented، optional، reference، acceptance-only و unavailable فرق می‌گذارد. scheduler/control-agent و operationهای CLIِ compose‌نشده را آماده معرفی نکنید. نیاز محصول به قابلیت غایب باید task واقعی با evidence داشته باشد.

## خروجی طراحی و مکان پیاده‌سازی

| موضوع | مرجع اختیاری در adapter نمونهٔ هدف | خروجی لازم فنی/توسعه |
|---|---|---|
| owner و context | `_doc/01-architecture.md` (معماری)، `_doc/02-module-workflow.md` (module workflow) | `modules/<owner>/docs/MODULE.md`، `CONTEXT_MAP.md`، vocabulary و responsibility |
| Domain | `_doc/03-domain.md` (Domain) | `DOMAIN_MODEL.md`؛ invariant، factory/restore، transition؛ Java خالص |
| Application و DTO | `_doc/04-application.md` (Application)، `_doc/05-dto-and-mapping.md` (DTO) | spec هر operation، typed execute input/result، failure، trusted context و ports |
| Persistence | `_doc/06-persistence.md` (Persistence) | schema owner، JPA entity جدا و mapper؛ Work/transaction، version، receipt، audit و migration |
| Ingress/API | `_doc/07-presentation.md` (Presentation)، `_doc/10-security.md` (Security) | owner-local presentation، OpenAPI گروه audience برای هر BFF یا internal و تست route/spec |
| ارتباط | `_doc/08-module-communication.md` (Communication) | public versioned contracts، Application port و Infrastructure ACL؛ call/event/recovery graph |
| پیام/job/provider | `_doc/09-events-and-workflows.md` (Delivery) | Outbox/Inbox، checkpoint، retry، unknown/reconcile، compensation و schedule off |
| ثبت و کنترل | `_doc/11-observability.md` (Observability) | required audit اتمی جدا از diagnostics، allowlist/redaction، bounded metrics و owner |
| کیفیت و شواهد | `_doc/12-verification-and-operations.md` (Verification)، `_doc/13-clean-code.md` (Clean code) | focused tests، suites واقعی، graph review، skip/limitation و acceptance record |
| policy و ابزار | `_doc/17-ai-agent-workflow.md` (Agent workflow) | catalog، work record، doctor/explain/scaffold/verify و policyهای جاری |

ساختار production جدید:

```text
modules/<owner>/contracts/src/main/java/com/amos/backend/<owner>/contracts/v1/
modules/<owner>/runtime/src/main/java/com/amos/backend/<owner>/
  domain/  application/  infrastructure/  presentation/
modules/<owner>/docs/
```

## قواعدی که باید در طراحی و review دیده شوند

- Domain/Application بدون Spring/JPA/Jackson/Servlet/Validation، IO یا ambient clock/config؛ time/ID ورودی resolved است. rejection نباید partial mutation بسازد.
- authorization داخل Application، actor/scope از ingress معتبر؛ scope جاری reference برابر `system.single` است، نیاز tenancy از آن استنتاج نمی‌شود.
- consumer فقط contracts عمومی provider را می‌شناسد؛ foreign runtime import، private SQL/join/FK و transaction مشترک ownerها ممنوع‌اند. host wiring-only است.
- persistence جدید Hibernate/JPA پیش‌فرض؛ native query در EntityManager با ضرورت اثبات‌شده؛ JDBC مستقیم آخرین استثنای مستدل با evidence اتصال همان transaction. نمونهٔ قدیمی مجوز استثنا نیست.
- business state، receipt و required audit/Outbox لازم یک commit محلی دارند. network/provider بیرون write transaction است. `@Async` یا listener after-commit تضمین delivery نیست.
- receipt replay نیازمند authorization جاری است؛ same key/different intent conflict. commit timeout نتیجهٔ `UNKNOWN` دارد تا شاهد معتبر خلافش؛ موفقیت یا rollback فرض نشود.
- audit availability پیش از اثر و append اتمی؛ diagnostic/model changelog post-commit جای audit authoritative نیست. raw code/token/PII وارد log، metric، trace، response error یا مستند نمی‌شود.
- migration افزایشی با role و credential جدا، بدون startup DDL serving؛ expand/backfill/contract، mixed version و restore/reconcile با evidence.
- dependency/POM، policy owner registration، explicit composition، contract exports، config validation و feature off behavior بخشی از تحویل است، نه کار پنهان بعدی.

## دستورها و زمان استفاده

تمام دستورهای زیر **از ریشهٔ Backend** اجرا می‌شوند؛ نوشتن آن‌ها در سند، اجرای این نوبت نیست.

```sh
./scripts/agent/doctor
./scripts/agent/workflow feature
./scripts/agent/explain modules/<owner>/docs modules/<owner>/runtime
./scripts/agent/scaffold-owner <owner> --classification product --dry-run
./scripts/agent/scaffold-owner <owner> --classification product --apply
./scripts/agent/scaffold-use-case <owner> <UpperCamelName> --dry-run
./scripts/agent/scaffold-use-case <owner> <UpperCamelName> --apply
python3 scripts/check-documentation.py
./mvnw -B validate
./mvnw -B spotless:check test
./scripts/agent/verify --changed
./scripts/agent/verify --full
```

`workflow` بر اساس نوع، یکی از `new-app/new-module/feature/edit/bug/integration/durable-workflow/data-change/review-release` است. scaffold فقط در scope نیاز و پس از review dry-run اجرا می‌شود؛ success stub تولید نمی‌کند. app تازه ابتدا profile تصمیم‌گرفتهٔ انسان را لازم دارد:

```sh
./scripts/agent/init-project --profile project-profile.json --dry-run
./scripts/agent/init-project --profile project-profile.json --output .env.project --apply
```

syntax را با ابزار جاری تطبیق دهید؛ بعضی نمونه‌های قدیمی `_agent-doc` شکل positional متفاوت دارند. profile فقط reference امن secret دارد؛ target host باید قابلیت منتخب را compose کند. apply این profile طبق workflow backend review انسان می‌خواهد.

## برنامهٔ evidence

| اثر | حداقل نوع اثبات |
|---|---|
| فقط مستندات Backend | checker مستندات و factual/link review |
| runtime | validate، formatter/unit و verify changed؛ suiteهای focused مطابق policy |
| DB/receipt/audit | PostgreSQL واقعی: rollback هر participant، concurrent version/key، replay reauthorization، grant denial و unknown commit |
| message/job/provider | real durable store، crash، duplicate/lost ACK، retry/deadline، late result و uncertainty/reconcile؛ mock فقط تست منطق |
| migration | schema/grant، old/new overlap، restart/backfill و recovery روی دادهٔ ساختگی |
| HTTP | authentication/authorization، presence/null/bounds/errors، audience OpenAPI و route coverage |
| performance claim | workload/hardware/threshold مصوب، نرخ واقعی، error count و p95؛ عدد نمونه baseline محصول نیست |
| release | verify full و شواهد current-run artifact/commit؛ prerequisiteهای واقعی sink/provider طبق policy جاری |

`scripts/ci/policy/verification.v1.json` (verification policy) و `_doc/12-verification-and-operations.md` (راهنمای اجرا) تعیین‌کننده‌اند. `verify --changed` جای PostgreSQL acceptance یا full release نیست. suite غیرفعال، صفر تست یا skip اجباری pass محسوب نمی‌شود. برای انتشار عمومی، requirements ویژهٔ Sentry و ledger provenance همان Backend نیز برقرارند؛ این مجموعه آن‌ها را سبک نمی‌کند.

برای هر اجرای تست: command، source revision و dirty/diff hash، environment غیرحساس، زمان، test/fail/error/skip count، report و digest را نگه دارید. گزارش قدیمی پس از تغییر کد current نیست. شواهد graphها و POM/import/SQL علاوه بر ArchUnit بررسی می‌شوند.

## اتصال بستهٔ ماژولی درخواست به کد

`technical/impact-map.md` نام ownerهای واقعی و caller/consumerهای متأثر را به شواهد checkout وصل می‌کند. `technical/modules/<owner>/change-spec.md` فقط delta و reference دقیق به `backend/modules/<owner>/docs/` است؛ تغییر قرارداد عمومی باید test-mapping producer و consumer و cross-module-flows را به‌روز کند. باگ/refactor هم impact-map دارند، حتی اگر فقط یک ردیف لازم باشد.

مسیر taskهای توسعه `development/modules/<owner>/tasks/<task-id>.md` است. migration و contract producer پیش‌نیاز task consumer هستند فقط وقتی dependency واقعی چنین اقتضا کند؛ ترتیب از graph مصوب تعیین می‌شود. تغییر مشترک host/platform با component target و task دارای مسئول مشخص ثبت می‌شود. gate هر ماژول و سپس candidate کل درخواست طبق همان verification policy بررسی می‌شوند.
