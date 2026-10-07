# Shared interface contract — lanes A–H

Prepared 2026-10-06 from `.starter/reference-app/` actual exports. This is a contract freeze for parallel implementation, not a claim that providers have delivered a runnable app. Paths below are target-root paths; the inspected seed is the same path under `.starter/reference-app/`. Do not edit that snapshot or the source GURUKUL checkout.

## Authority, mode and ownership

Read target `AGENTS.md` first. The coordinator explicitly selects reuse or fresh mode and records that decision before integration. Existing reference code and copied reports must never be presented as newly written or newly verified work. At preparation time `docs/hackathon/README.md`, `ownership.json` and `lanes.md` were not present; their creation belongs to other owners. The allocation below records this task's required split. The coordinator must reconcile those artifacts with this contract before kickoff; absence is not permission for overlapping edits.

| Lane | Exclusive implementation scope | Consumes / provides |
| --- | --- | --- |
| A native/model | `modules/`, generated `ios/` and `android/`, `src/t0/`, model domain/lifecycle, `src/services/native-slot.ts`, `src/adapters/model/native.ts`, privacy patch script | Native bridge, verified model lifecycle and global runtime slot for C/D/E/G/H |
| B data | ALL `src/db/`, ALL `src/adapters/sqlite/`, `src/services/foundation.ts`, `src/adapters/storage-native.ts` | Every repository, migrations, recovery, cleanup and foundation; other lanes request changes, never write SQL adapters |
| C imports/library | `src/domain/imports.ts`, import manager, `src/adapters/imports/`, camera/sheet helpers, `src/features/notebooks/` | Reviewed immutable sources; consumes A bridge, B imports/storage, D notebook Study |
| D Study | `src/domain/study.ts`, study manager, `src/adapters/model/study.ts`, Study UI except `QuizPanel.tsx` | Evidence/validation, shared `StudyRuntime` and `loadGroundedRuntime`, notebook Study/history |
| E quiz | `src/domain/quiz.ts`, quiz manager, `src/adapters/model/quiz.ts`, `src/features/study/QuizPanel.tsx` | Generated validated quizzes and attempt UI; consumes D evidence/runtime, B quizzes |
| F progress | `src/domain/progress.ts`, `src/features/progress/` | Derived review/history and repeat entry; consumes B progress/quizzes, E QuizPanel |
| G Buddy | `src/domain/buddy.ts`, buddy manager, `src/adapters/model/buddy.ts`, `src/features/buddy/` | Separate general-chat UI/policy; consumes D runtime and B Buddy repository |
| H shell/profile | `app/`, onboarding/settings/shared UI, `src/domain/profile.ts`, `src/domain/experience.ts` | Navigation, local profile/session/splash, shared components and safe user-facing errors |
| Coordinator | Root `App.tsx`/`index.ts`, package/config/lockfiles, bootstrap/build/test orchestration, shared contracts, global state/plans | Integration decisions, config locks, mode and native build lease |

Feature tests follow their lane; shared test orchestration remains coordinator-owned. Diagnostic cross-feature files and any unlisted path require an explicit ownership assignment before edits. A does not edit package locks/Expo config; H does not edit foundation/profile SQL; E owns QuizPanel despite its `study/` directory. B owns storage-native despite its native calls. Domain type owners and B coordinate together when validators are imported by repositories.

Freeze exported names, module paths, parameter order, persisted states, prop shapes and validation semantics below. Do not create replacement facades such as `StorageService`, `RetrievalService`, `submitAttempt`, or a `src/contracts/` API just because old architecture sketches mention logical services. Request a contract change with affected producers/consumers and coordinator acknowledgement before changing an interface.

## Fresh-mode artifact and report handshake

The reference snapshot is a read-only specification, not a runtime dependency. Fresh target modules must not import `.starter/reference-app`, silently copy whole implementations, or use a production mock to make a dependent lane appear complete. Reuse mode must explicitly disclose reused code.

1. Provider publishes its exact owned artifact paths and exports in `docs/hackathon/status/<lane>.md`. Include mode, delivered versus pending exports, parameter/prop compatibility, migration needs, dependency requests, exact commands/results and remaining native/UI gates. The status path is a reporting protocol, not an existing TypeScript API.
2. Consumer reads the provider's report AND actual target artifacts. Record accepted exports or a concrete mismatch. A file existing, an announced plan, or a frozen signature is not delivery or verification.
3. Until a provider exists, continue independent domain/UI work and tests within ownership. Test doubles implementing the seed ports belong only in tests. Do not add ambient declarations, fake production repositories, canned successful AI replies, import aliases to the seed, or placeholder native success to pass integration. Report blocked integrated typecheck/route wiring honestly.
4. Provider and consumer coordinate ready artifacts without editing each other's files. Coordinator resolves freeze changes and shared configuration. H wires real features only after their target dependencies exist; explicit unavailable/loading/error states are allowed, simulated readiness is not.
5. At coordinator checkpoints (10/30/55/70/90 minutes), reports distinguish authored artifacts, accepted contracts, host checks, actual device evidence and unresolved blockers. No provider is assumed finished by elapsed time. Coordinator alone consolidates global state.

Important dependencies: B foundation imports validators from C/D/E/F/G/H and A's manifest; B cannot claim a runnable foundation from SQL files alone. D provides the shared runtime loaded by E and G. B's storage-native imports D/E/G managers and C's file URI helper. H composes all lanes. Coordinate those artifacts without introducing runtime mocks or moving B's SQL into features.

## Database and foundation: B's frozen boundary

Actual exports from `src/db/types.ts`:

```ts
type SqlValue = string | number | null;
interface SqlExecutor {
  execAsync(sql: string): Promise<void>;
  runAsync(sql: string, ...params: SqlValue[]): Promise<{ changes: number; lastInsertRowId: number }>;
  getFirstAsync<Result>(sql: string, ...params: SqlValue[]): Promise<Result | null>;
  getAllAsync<Result>(sql: string, ...params: SqlValue[]): Promise<Result[]>;
}
interface Database extends SqlExecutor {
  withExclusiveTransactionAsync(work: (transaction: SqlExecutor) => Promise<void>): Promise<void>;
}
interface Migration {
  version: number;
  apply(transaction: SqlExecutor): Promise<void>;
}
```

`initializeFoundation(database: Database)` in `src/services/foundation.ts` awaits `migrate`, then imports/study/quizzes/Buddy recovery in that order, then reads profile/notebooks/session. Its returned keys are exactly `repository`, `profile`, `notebooks`, `session`, `buddy`, `models`, `imports`, `study`, `quizzes`, `progress`, `storage`. `Foundation = Awaited<ReturnType<typeof initializeFoundation>>` is exported; consumers use it or indexed access such as `Foundation['progress']`, not a separately invented interface.

`getFoundation()` in `src/adapters/sqlite/open.ts` caches initialization, resets its opening promise on failure, and refreshes profile/notebooks on subsequent calls. It does **not** refresh the cached `session` field; H must update its local foundation after successful `saveSession` or explicitly read `repository.readSession()`. Reopening is not a reset/reseed operation.

The actual app database is `gurukul.db`, unrelated to `~/codex/test.db`. Main connection enables WAL/foreign keys. Exclusive writes open a separate connection, enable foreign keys before `BEGIN IMMEDIATE`, then commit/rollback and close. Preserve `finalizeUnusedStatementsBeforeClosing: false` from the seed adapter. Do not substitute Expo's transaction defaults without equivalent connection/foreign-key evidence.

### Ordered migration ledger

B exclusively owns migration files and registration in `migrate(database: Database, migrations: readonly Migration[] = ...)`. Other lanes provide requirements and fixtures; they do not reserve their own migration numbers or run feature DDL. Freeze 1–10 in order:

| Version/file under `src/db/migrations/` | Export | Responsibility |
| --- | --- | --- |
| `001-foundation.ts` | `foundationMigration` | Profile, notebooks and labeled synthetic baseline; migrator owns `schema_migrations` ledger |
| `002-model-installations.ts` | `modelMigration` | Pinned installation provenance/checkpoints |
| `003-imports.ts` | `importsMigration` | Originals/jobs/drafts/revisions/pages/chunks/FTS |
| `004-study.ts` | `studyMigration` | Study turns and immutable evidence snapshots |
| `005-quizzes.ts` | `quizMigration` | Quiz/item/attempt/response tables and immutability guards |
| `006-progress.ts` | `progressMigration` | `progress_flags`, `quiz_repeats`, completion index |
| `007-cleanup.ts` | `cleanupMigration` | Durable `file_cleanup` queue |
| `008-local-session.ts` | `localSessionMigration` | Singleton welcome/teacher/active; existing profiles become active |
| `009-buddy.ts` | `buddyMigration` | Separate Buddy chats/turns and active-turn protection |
| `010-profile-avatar.ts` | `profileAvatarMigration` | Nullable constrained boy/girl avatar; no default assignment |

Versions and applied ledger must be contiguous; unknown/future/gapped versions throw exported `DatabaseVersionError`. Pending migrations and ledger entries run transactionally. Conflicting unversioned tables fail rather than being overwritten. No database deletion, silent reset, downgrade, renumbering or table overwrite. Any additional migration requires B plus coordinator agreement after 10, with preservation/rollback evidence.

### Repository exports and callable signatures

These are methods returned by factories, not individually exported functions. Async methods return promises; inferred return shapes remain defined by the named source files. Do not invent named repository types where the seed has none.

`repository.ts`: `createRepository(database: SqlExecutor)`; exported `FoundationRepository`, `Notebook = { id: string; title: string; createdAt: string }`, `SessionStage = 'welcome' | 'teacher' | 'active'`.

- `readProfile(): Promise<Profile | null>`, `saveProfile(input: ProfileInput): Promise<Profile>`.
- `readSession(): Promise<SessionStage>`, `saveSession(stage: SessionStage): Promise<void>`.
- `listNotebooks(): Promise<Notebook[]>`; notebook creation is `imports.createNotebook`, not this repository.

`models.ts`: `createModelRepository(database: SqlExecutor, manifest: ModelManifest)` returns `pendingRemoval(name: string): Promise<boolean>`, `read(): Promise<Installation | null>`, `save(record: Installation): Promise<void>`. Reads match manifest ID/revision/hash/bytes; a matching row alone is not native verification.

`imports.ts`: `createImportRepository(database: Database)`; exported `ImportRepository`.

- `source(id: string)`, `job(id: string)`, `pages(jobId: string)`, `latestJob(documentId: string)` return Source, ImportJob, DraftPage array and ImportJob respectively; missing required records throw.
- `transition(jobId: string, status: ImportStatus, code: string | null = null)`, `recover()`, `createNotebook(id: string, title: string)`, `list(notebookId: string)`.
- `create(input: { id: string; jobId: string; revisionId: string; notebookId: string; title: string; kind: SourceKind; filename: string })`.
- `inspected(jobId: string, info: SourceInfo)` returns duplicate ID or null; `addPage(jobId: string, page: DraftPage)`, `saveDraft(jobId: string, pageNumber: number, text: string)`, `publish(jobId: string)`.
- `revise(documentId: string, jobId: string, revisionId: string)`, `select(documentId: string, selected: boolean)`, `search(notebookId: string, query: string)`; search rows contain `document_id`, `title`, `page_number`, `text`, `revision_id`.

`study.ts`: `createStudyRepository(database: Database)`; exported `StudyRepository`, `StudyTurn`.

- `recover()`, `sections(notebook: string): Promise<Evidence[]>`, `retrieve(notebook: string, question: string, section?: string): Promise<Evidence[]>`.
- `begin(input: { id: string; notebook: string; action: StudyAction; question: string; model: string; prompt: string })`.
- `evidence(id: string, evidence: Evidence[], tokens: number)`, `finish(id: string, result: StudyResult)`, `stop(id: string, status: 'cancelled' | 'failed', error: string)`, `history(notebook: string): Promise<StudyTurn[]>`.

`quizzes.ts`: `createQuizRepository(database: Database)`; exported `QuizRepository`, `QuizRow`, `Attempt`, `ItemRow`, `ResponseRow`.

- `recover()`, `begin(input: { id: string; notebook: string; count: 3 | 5; evidence: Evidence[]; model: string; prompt: string })`, `fail(id: string, status: 'failed' | 'cancelled', error: string)`.
- `publish(id: string, items: { id: string; item: QuizItem }[])`, `list(notebook: string): Promise<QuizRow[]>`.
- `detail(id: string)` returns `{ quiz, items, attempt, responses }`, with nullable attempt and raw `item_json`/`evidence_json` snapshots.
- `start(quizId: string, attemptId: string): Promise<Attempt>`, `select(attemptId: string, itemId: string, selected: number | null, excluded = false)`, `submit(attemptId: string): Promise<Attempt>`.

`progress.ts`: `createProgressRepository(database: Database)` returns `read()` (the result of `deriveProgress`), `flag(attemptId: string, itemId: string, flagged: boolean)`, `repeat(parentId: string, quizId: string, attemptId: string): Promise<string>`. There is no exported `ProgressRepository` alias; use `Foundation['progress']` or `ReturnType<typeof createProgressRepository>`.

`buddy.ts`: `createBuddyRepository(database: Database)`; exported `BuddyRepository`, `BuddyChat`, `BuddyTurn`. Methods: `recover()`, `chats(): Promise<BuddyChat[]>`, `turns(chat: string): Promise<BuddyTurn[]>`, `begin(chat: string, id: string, question: string, model: string)`, `context(id: string, tokens: number, omitted: number)`, `finish(id: string, text: string)`, `stop(id: string, status: 'failed' | 'cancelled', error: string)`, `remove(chat: string)`. `finish` receives serialized model JSON for validation, not arbitrary display text. Removal requires explicit UI confirmation and refuses an active turn.

`storage.ts`: `createStorageRepository(database: Database)`; exported `RemovalTarget = { kind: 'source' | 'notebook'; id: string }`, `ownedFile(name: string)`.

- `preview(target: RemovalTarget)` returns `{ token, sources, turns, quizzes, attempts }`.
- `remove(target: RemovalTarget, confirmedToken: string)` recomputes the plan transactionally and rejects changed confirmation (`CHANGED`).
- `removeModel(id: string, filename: string | null, partial: string | null)`, `pending()` returning filename/attempts/error_code rows, `cleanup(removeFile: (filename: string) => Promise<void>)`.

Removal includes affected duplicate sources, generated snapshots and repeat descendants; metadata deletion and filesystem deletion are separate. Queue filenames before committing metadata deletion; retry failed cleanup visibly. Never delete arbitrary paths, notes during model removal, or Buddy chats during notebook removal. This is not forensic erasure. `storage-native.ts` exports `withIdleStudy<Result>(foundation: Foundation, work: () => Promise<Result>)`, `availableStorage()`, `cleanupFiles(foundation: Foundation)`, `retryCleanup(foundation: Foundation)`. UI confirmation and native-idle guards are required around destructive calls; the SQL storage idle check alone does not cover Buddy/model activity.

## Domain records, validation and provenance

Keep the actual casing: profile/Notebook use camelCase; stored Source, StudyTurn, BuddyTurn and quiz rows use snake_case; Evidence uses camelCase. JSON snapshots are not safe merely because a DB column is a string.

| Owner/module | Existing types and states |
| --- | --- |
| H `domain/profile.ts` | `Language = 'en' | 'hi' | 'bn'`; `ProfileAvatar = 'boy' | 'girl'`; `ProfileInput = { nickname: string; language: Language; avatar?: ProfileAvatar }`; `Profile = ProfileInput & { id: string; createdAt: string; updatedAt: string }`; `validateProfile(input)` |
| A `domain/model.ts` | `ModelManifest` fields: id/revision/filename/sha256/bytes/license/licenseUrl/runtime/url. `Installation` has status, nullable filename/partial, received. Persisted status: absent/downloading/verifying/paused/failed/ready. `ModelState` adds phase/busy/message; phase also allows checking/loading/loaded/generating/unloading |
| C `domain/imports.ts` | `SourceKind = 'txt' | 'pdf' | 'jpg' | 'png'`; `ExtractionMethod = 'text' | 'pdf-text' | 'pdf-ocr' | 'image-ocr'`; `ImportStatus = 'copying' | 'extracting' | 'review' | 'indexing' | 'ready' | 'failed' | 'cancelled' | 'interrupted' | 'duplicate'`; exported Source/ImportJob/DraftPage/SourceInfo/ImportFailure |
| D `domain/study.ts` | `StudyAction = 'ask' | 'explain' | 'summary'`; `Evidence = { chunkId: string; documentId: string; revisionId: string; pageNumber: number; title: string; text: string; start: number; end: number }`; `Citation = { chunkId: string; quote: string }`; `StudyResult = { status: 'answer' | 'insufficient_evidence'; answer: string; citations: Citation[] }` |
| B Study rows | `StudyTurn.status`: generating/complete/insufficient/cancelled/interrupted/failed; evidence_json/result_json/coverage/model_version/prompt_version/prompt_tokens/error/created_at plus ID/notebook/action/question |
| E `domain/quiz.ts` | `QuizItem = { prompt: string; options: string[]; correctIndex: number; explanation: string; topicId: string; citations: Citation[] }`; type alone does not enforce four options or valid key. QuizRow/Attempt status are typed as string; DB guards and services enforce their state machine |
| B Buddy rows | BuddyChat has id/title/created_at/updated_at. BuddyTurn has chat_id/question/nullable answer, generating/complete/failed/cancelled/interrupted, error/model_version/prompt_version/prompt_tokens/omitted_turns/created_at |
| F `domain/progress.ts` | `ProgressRow`, `PracticeResponse`, `deriveProgress(rows: ProgressRow[])`, `practiceSummary(data: ReturnType<typeof deriveProgress>)`; use inferred derived shapes, no invented mastery entity |

C publishes only reviewed text through transactional `publish`: complete ordered pages, immutable revision/page/chunk IDs and offsets, active revision pointer and FTS updated together. `DraftPage` contains `page_number`, `raw_text`, `reviewed_text`, `extraction_method`, nullable `preview_name`; `SourceInfo` contains sha256/bytes/pages. Limits are 20 MiB input, 1 MiB text bytes, ten pages, 4096 per image dimension, 20,000 text characters per page. Latin/printed English baseline; preferred language does not promise Bengali OCR or translation. Existing derived page/chunk IDs and section topic IDs are deliberate exceptions to UUID entity IDs.

D retrieves only selected documents/current revisions in the requested notebook, including direct-section lookup. Up to 16 lexical candidates / 100 selectable sections; section argument is a chunk ID. Snapshot all Evidence fields before generation; edits never rewrite old evidence. `validateStudy(text: string, evidence: Evidence[]): StudyResult` enforces exact schema, known citations, exact quotes, bounded text, and answer equal to normalized joined quotes. Summary requires an explicit section and says section-only. Empty retrieval persists `insufficient`, not a Buddy answer. Revalidate history before rendering; failed/truncated/late output is not an answer. Structural grounding does not prove relevance.

E uses `topicFor(evidence)` → `section:<chunkId>`, `quizSchemaFor`, `validateQuiz(value: unknown, evidence: Evidence[], previous: QuizItem[] = [])`, `parseQuiz(text: string, evidence: Evidence[], previous: QuizItem[])`, and `gradeQuiz(items: { id: string; item: unknown; evidence: Evidence[]; excluded?: boolean }[], selections: Record<string, number | null>)`. Publish the whole requested 3/5-item set only after transactional revalidation. Source-sentence completion requires one `____`, four unique options, model-emitted key 0–3, known topic/citations, exact supporting explanation and reconstruction of the quote with the keyed option. Never invent keys or replace failed generation with curated questions. One regeneration per item; strict validation survives both attempts.

Submission is deterministic and idempotent under an exclusive transaction. One attempt per quiz; `start` resumes it. Skipped scorable items count wrong; invalid/excluded items do not count; zero scorable yields null score. Preserve raw correct/scorable counts and immutable responses. A repeated saved quiz is a new explicit repeat with provenance, not regeneration of old keys.

Provenance travels with evidence and model/prompt identity. Current manifest: Qwen2.5-1.5B-Instruct, Q4_K_M, revision `91cad51170dc346986eccefdc2dd33a9da36ead9`, 1,117,320,736 bytes, SHA-256 `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`, Apache-2.0, llama.rn 0.9.1. Keep `src/t0/model.json` URLs/license/evidence together; quantization and deviceEvidence are manifest JSON fields beyond the narrower ModelManifest type. `feasibility-model.json` is historical Qwen3, not the selected teacher. Prompt versions: `t4-extractive-v2`, `t5-mcq-v8-source-decoding`, `buddy-v1`.

## Native/runtime interfaces and serialization

A provides `nativeReaderAvailable` and `getReader()` from `src/t0/native.ts`. The optional DocumentReader bridge must fail truthfully when absent. Its production methods are `verifyModel(name: string, bytes: number, hash: string): Promise<string>`, `modelDirectory(): Promise<string>`, `setDownloadAwake(active: boolean): Promise<void>`, `newId(): string`, `inspectSource(name: string, kind: string): Promise<{ sha256: string; bytes: number; pages: number }>`, `sourcePage(name: string, kind: string, page: number): Promise<{ text: string; method: ExtractionMethod; preview: string | null }>`, `promoteModel(partial: string, filename: string): Promise<void>`, `imageText(name: string): Promise<string>`, `pdfText(name: string): Promise<string>`, and `memory()` returning Android pssKb/nativeHeapBytes OR iOS residentBytes. These memory measures are not interchangeable or true peak measurements. Optional smoke flags/device/report methods remain diagnostic-only.

A's `ModelManager(manifest: ModelManifest, ports: ModelPorts)` exposes snapshot/subscribe/check/download/load/answer/cancel/unload/setForeground/removeInstallation. `ModelPorts` names are read/save/exists/freeBytes/uniqueName/download/verify/promote/load; `download(name, progress, signal)` is cancellable and `load(path)` returns `LocalContext` (answer/stop/release). `getModelManager(repository: Pick<ModelPorts, 'read' | 'save'> & { pendingRemoval?(name: string): Promise<boolean> })` and `modelNativeAvailable` are exported by `adapters/model/native.ts`.

Verification precedes every native load. Preserve pinned HTTPS download, full byte/hash checks, disk allowance `requiredModelStorage(bytes) = bytes * 2 + 1 GiB`, unique staging/final filenames, non-overwriting promotion and crash reconciliation. Retry is a disclosed restart, not verified range resume. Ready in SQLite does not mean verified/loaded; unload does not delete an installation.

C's `ImportManager(repository: ImportRepository, ports: ImportPorts)` exposes `start(input: { notebookId: string; title: string; kind: SourceKind; uri?: string; text?: string })`, `retry(jobId: string)`, snapshot/subscribe/cancel/setForeground. ImportPorts: `id()`, `copy(input: { uri?: string; text?: string }, filename: string): Promise<void>`, `inspect(filename: string, kind: SourceKind): Promise<SourceInfo>`, `page(filename: string, kind: SourceKind, number: number): Promise<Omit<DraftPage, 'page_number' | 'reviewed_text'>>`, `claim(): () => void`. Native adapter exports `importNativeAvailable`, `importId()`, `sourceUri(name: string)`, `getImportManager(repository: ImportRepository)`, `pickSource()`, `captureSource()`.

D exports the shared runtime contract from `services/study-manager.ts`:

```ts
interface StudyRuntime {
  count(messages: ChatMessage[]): Promise<number>;
  generate(messages: ChatMessage[], schema?: object): Promise<{ text: string; truncated: boolean }>;
  stop(): Promise<void>;
  release(): Promise<void>;
}
```

`ChatMessage` is exported by `domain/study.ts` with role system/user/assistant and content string. `StudyManager(repository: StudyRepository, ports: { id(): string; model: string; load(): Promise<StudyRuntime> })` exposes `run(notebook: string, action: StudyAction, question: string, section?: string)` plus snapshot/subscribe/cancel/setForeground. `getStudyManager(foundation: Foundation)` and `loadGroundedRuntime(foundation: Foundation, schema: object = studySchema, observe?: (measurement: object) => void, candidate?: { manifest: ModelManifest; filename: string }): Promise<StudyRuntime>` live in D's model adapter. Candidate override requires the explicit native evaluation flag, not a product model-selection API.

E exports `QuizManager`, `getQuizManager(foundation: Foundation)`; `generate(notebook: string, count: 3 | 5, section?: string)` plus snapshot/subscribe/cancel/setForeground. Its constructor's `QuizPorts` is **not exported**: id/model/sections/load and optional diagnostic observeCandidate; consumers must not import it. G exports `BuddyManager(repository: BuddyRepository, ports: { id(): string; model: string; load(): Promise<StudyRuntime> })`, `run(chat: string, question: string)` and snapshot/subscribe/cancel/setForeground; adapter provides `getBuddyManager(foundation: Foundation)`.

Actual process serialization is `claimNativeSlot(): () => void` and `withNativeSlot<Result>(work: () => Promise<Result>): Promise<Result>`. It is a non-reentrant fail-busy lease, **not a queued scheduler**. Release is idempotent. Model retained contexts, OCR/import, Study, Quiz, Buddy, cleanup and diagnostics must share this one slot; no lane-local replacement. D's loader unloads the idle ModelManager, claims, verifies and loads, then retains the slot until context release. E/G call that loader; they must not double-claim around it. Surface busy and require teacher unload before conflicting diagnostics. Keep busy until native work settles; Stop/background requests cancellation, discards late output and releases resources after completion. Do not promise immediate native cancellation or parallel inference/OCR. A native release failure must remain visible as a blocker, not be papered over with a fresh slot.

The seed uses real formatted-chat token counts, 1450 prompt / 400 output / 198 reserve in a 2048 context, CPU two threads, GPU zero, seed 42, temperature zero, thinking disabled. Quiz requests stop at 30 seconds; Buddy at 60 seconds; timers request cancellation, not guaranteed hard termination.

## H–B profile, logout, splash and feature wiring

H validates/saves through `foundation.repository`; B preserves the singleton profile ID/createdAt. Omitted avatar preserves the existing avatar via SQL COALESCE; null clearing is not an advertised ProfileInput operation. Empty-name UI may choose Student, but `validateProfile` itself rejects empty/control-containing/>60-code-point nicknames. Avatar is a decorative key, not inferred gender or account identity.

Cold launch shows `IntroductionPage = 'book' | 'robot'` using `IntroductionScreen({ page, next, back })`; introduction state is in H memory, not a new migration. Book → robot → persisted workspace gate. `WelcomeScreen({ initial?: ProfileInput, save(input: ProfileInput): Promise<void> })` saves profile then session teacher. `TeacherSetup({ foundation, finish(): Promise<void>, back(): Promise<void> })` verifies/reuses an installed teacher; explicit Continue or Explore first sets active. No implicit redownload. Existing profiles migrating to active still see the two-screen cold-launch introduction.

Logout Cancel changes nothing. Confirmed logout checks import/model busy, then `withIdleStudy` (Study/Quiz/Buddy plus shared native slot), persists welcome, updates H state and resets introduction to book. Failure must not claim logout succeeded. No profile/history/model/source deletion; local logout is neither authentication, privacy lock nor cloud restore. Preserve data across restart, and do not replace the user's source app through the old bundle ID.

Actual UI integration points:

| Consumer → provider | Frozen call/props |
| --- | --- |
| H → C | `LibraryScreen({ foundation, viewportHeight?: number, onNavigate?(): void })` |
| C → D | `NotebookStudy({ foundation, notebook: string, historyOnly: boolean, viewportHeight?: number })` |
| D/F → E | `QuizPanel({ foundation, notebook: string, section?: string, close(): void, initialQuiz?: string, repeatPractice?: boolean })` |
| H → F | `ProgressScreen({ foundation, onNavigate?: () => void })` |
| H → G | `BuddyScreen({ foundation, height: number, navigate(route: 'notebooks' | 'progress'): void })` |

`app/routes.ts` exports `mainRoutes`, `MainRoute`, `Route = MainRoute | 'diagnostics'`, `routeLabels`. Existing main routes: notebooks/buddy/study/progress/settings; visible tabs exclude study, and notebooks is labeled Home. `StudyScreen()` is the generic entry, not a replacement for notebook-scoped Study. H owns navigation and shared UI signatures; consumers request changes to `src/features/shared/` rather than cloning them. Use existing `docs/UX/README.md` and numbered references (especially Study 04, Quiz 05, Progress 06, Home 09/10, History 11, teacher 12, Settings 13, profile 14, splash 15/splash folder, Buddy 15/16). No new artwork is authorized by this contract task.

Study → Quiz carries notebook and optional section chunk ID; E gets sections through `foundation.study.sections`, not independent retrieval. Quiz → Progress flows only through committed B attempt/response snapshots. F's `read()` derives history/topics from retained records; latest-ten valid responses per topic, fewer than three means limited evidence, unrounded accuracy <70% with at least three means priority. Wrong evidence remains reviewable beyond that window. Flags affect derived review, not historical grades. Repeats use `progress.repeat(parentId, quizId, attemptId)` then E's `initialQuiz`/`repeatPractice`; saved-material review/repeat needs no model. Never label repeated practice as independent mastery, diagnosis or exam prediction.

Buddy uses separate chats/turns and `buddySchema`/`validateBuddy`/`validateBuddyQuestion`; it is explicitly general local model knowledge, not note-grounded evidence. It shares the runtime mechanics, not Study retrieval/citations or Progress scoring. Context uses only the same chat's newest contiguous completed pairs within budget, records omitted turns, excludes failed/interrupted turns, and preserves older history. JSON `{answer}` is bounded/validated and rendered as plain text; no SQL/tool execution. Notebook deletion does not delete Buddy history; Study failure must never silently route to Buddy. G owns chat introduction/history and confirmed chat removal.

## Generated native projects, privacy and build coordination

There are two different leases: the JS slot above serializes app work; the coordinator's native/build lease serializes install/prebuild/Pods/Gradle/Xcode and shared build resources. A uses the coordinated native lease; nobody starts a second build to work around a busy slot. Record owner/operation/start/artifacts/release in orchestration reports; use the coordinator's `scripts/hackathon.py` lease when delivered, do not assume it already exists or silently evict stale locks.

Generated native directories are A-owned implementation artifacts. Root app config, dependency pins, package lock, identity and build orchestration are coordinator-owned. `.starter/native-reference/` supplies historical Podfile/lock/properties and Android properties, not a generated app that has already passed a new build. No concurrent install/prebuild, `--clean` reset, wholesale native replacement, package upgrades or lock rewrites. Preserve native patches and recheck generated settings after any authorized regeneration. New bundle/application IDs must be coordinator-selected and distinct from seed `org.gurukul.t0`. Expo Go is UI preview only; native capability checks must disable unavailable AI/OCR/PDF.

Privacy preservation requirements tied to actual seed artifacts:

- `scripts/private-llama.mjs` targets exactly llama.rn 0.9.1 and fails on unexpected source; `npm run native:privacy` is explicit, not proof it ran. It forces source builds on iOS/Android, suppresses llama/ggml/common/JNI/iOS log and token callback paths, removes exception detail from the Android wait error, and skips Android OpenCL/Hexagon targets. Preserve verification via the script's `--check`; a precompiled binary bypassing patched source is not compliant evidence. Runtime patch provenance in historical reports is `gurukul-private-log-v1`.
- Expo config has Android `allowBackup: false`; A/coordinator must inspect the generated manifest and actual build, including platform transfer behavior, rather than infer complete backup exclusion from JSON. Native Android files use `context.filesDir`, not `noBackupFilesDir`.
- iOS `LocalDocuments.modelDirectory()` sets Documents `isExcludedFromBackup`; promotion and SourceDocuments extraction/preview paths also set exclusions. SQLite's default location/sidecars and exclusions must be verified in the new native app, especially before first teacher/import use. Do not infer every fresh profile/database file is already excluded simply because model promotion sets an attribute later.
- Preserve app-private sources/model filenames, native path/signature/hash checks and one-page-at-a-time bounded extraction. iOS uses Vision/PDFKit, Android bundled Latin ML Kit/PdfRenderer. Permissions are explicit camera-only as needed; no microphone/photos upload or study-content network path. App-private storage is not an encryption claim.
- Logs/reports contain operation/status/timing/byte counts/model/prompt identity, not notes, contact details, prompts, tokens or answers. Synthetic opt-in diagnostics remain separate. Native report-writing methods are not general content export. No analytics, cloud inference/OCR, login/backend requirement or silent network fallback. Network is only explicit model download and installation; failed cloud attempts still violate the boundary.

## Evidence and known limits

Source inspection establishes this contract, not executable target delivery. `docs/architecture/system.md`, `data.md`, `ai.md`, `docs/engineering/t3-imports.md` and ADR-002 explain invariants, but contain historical/proposed sections: actual seed exports and migrations take precedence over illustrative services/entities. Preserve recorded limitations when implementing their interfaces.

Historical `docs/quality/reports/t8-release-evaluation.md`: 14/20 answer cases succeeded, six failed validation; absent-evidence testing included an irrelevant sourced answer; 0/10 complete quiz sets passed the wider dataset despite earlier small-pack success. Latest copied state also records the real Study Ask “What do roots absorb?” validation failure. Do not weaken validators or claim broad AI quality because a source-exact summary or short Buddy recall passed.

The sustained run was user-stopped at about 9m52s, not a passed 15-minute gate. BPF capture lacked permission; Instruments export failed (`Document Missing Template Error`, exit 133). Neither proves zero network attempts. Fresh disconnected new-model OCR/answer/quiz/revision/history, broad accessibility/VoiceOver/large text and Android runtime remain pending. Historical iPhone Release successes and Android compilation are not fresh-starter evidence or support for all devices. Do not resume the stopped T8 run, build, download models or launch implementation workers as part of preparing this document.

Each delivered UI report records its UX reference, checked interactions, actual screenshot comparison when available and pending native/accessibility gates. Host unit tests/typecheck can establish signatures and deterministic logic; test doubles remain tests only and do not prove native behavior. Run focused owned checks once when implementation is authorized; coordinator runs integrated checks. This documentation-only preparation requires text/interface review, not a build, database operation, benchmark, implementation or separate status/state edit.
