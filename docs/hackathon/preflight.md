# 90-minute hackathon preflight and phone handoff

Preparation only. No installs, downloads, builds or device checks were performed for this document. Every target-app result is **pending**, including capabilities that passed in the source. Read [target instructions](../../AGENTS.md), [archived source state](../../.starter/archive/state.md) and [full release gates](release-gates.md). Copied state and `.local/` evidence paths describe the source; they are not evidence that artifacts exist or work here.

## Before starting the clock

- Coordinator chooses reuse-baseline or fresh-implementation mode, records allowed reuse and the actual target root, and supplies `docs/hackathon/README.md`, `ownership.json`, `lanes.md` and `scripts/hackathon.py`. Those orchestration files were absent at this inspection; their implementation and validation remain coordinator prerequisites. Do not bypass a missing lease helper to build.
- Coordinator alone bootstraps the active app and owns package installs, root config, lockfiles, shared contracts and integrated checks. Other lanes develop only their assigned files. This preparation owns only this document and `release-gates.md`; coordinator consolidates state and status.
- Use **Node 22.23.3**, with source evidence on npm **10.9.0**. Check `node --version` and `npm --version`; the old source-host Node 22.12.0 was insufficient. Do not assume its ignored local toolchain exists here. Use an explicitly provisioned toolchain without changing global configuration.
- Preserve the reference `package-lock.json`; coordinator uses `npm ci` after active-root bootstrap, never an incidental `npm install` that changes dependency resolution. The postinstall invokes `scripts/private-llama.mjs`; retain and verify the native privacy patch. Lockfile or lifecycle failure is a blocker to resolve, not a reason to skip it.
- Reference pins: Expo **57.0.26 (SDK 57)**, React Native **0.86.3**, React **19.2.3**, llama.rn **0.9.1**. Inspect [package](../../.starter/reference-app/package.json), [app config](../../.starter/reference-app/app.json) and [native reference](../../.starter/native-reference/Podfile). This requires a custom native development build or standalone native build. `npm start` selects Expo Go; Expo Go cannot establish local inference, custom OCR/PDF, or offline acceptance. `npm run start:dev` requires a compatible installed development app.
- Select one primary physical phone early. Prepare synthetic printed-English notes, one local image and one image-only PDF. No live student records or access to the source app's container.

### iOS first-device prerequisites

Full Xcode with compatible iPhone SDK/device support, accepted license/first-launch setup, CocoaPods, paired and trusted unlocked iPhone, Developer Mode and a valid signing team/profile are needed. Source evidence used Xcode 27.0 (27A266a); it does not prove this target toolchain. Command Line Tools alone are insufficient. Inspect `xcode-select -p`, `xcodebuild -version` and `pod --version`; any setup/download is an explicit coordinator action. Do not change global Xcode selection as incidental preparation.

Coordinator selects a **new, distinct bundle/application ID** before generation, signing, installation or testing. Never install this target as `org.gurukul.t0`, which could replace the user's source app. Update app config, generated settings, test host and test-runner identifiers consistently within ownership. Do not reuse source provisioning blindly; check target signing and expiry, keeping credentials out of logs.

Do not assume the generated `.xcworkspace`, scheme, product or target name. Discover the actual workspace after generation, then have A inspect its schemes/targets under the lease. Reference Podfile names `GurukulT0`, but that is not a promised target name here. Source UI test target is **`GurukulT7UITests`**. Source `tests/ios/T7UITests.swift` hardcodes `XCUIApplication(bundleIdentifier: "org.gurukul.t0")`, and `scripts/ios-t7-tests.rb` hardcodes the associated test bundle identifier. Coordinator must adapt target test orchestration with A before invocation; copied commands could otherwise test the source app or execute no tests. Preserve native privacy/backup protections when generating the target.

### Optional Android prerequisites

Only select Android for the timebox if tooling and a physical phone are ready. Source setup used **JDK 17**, Android SDK/build-tools **36/36.0.0**, ARM64 and minimum API 24; verify actual generated Gradle/NDK requirements rather than installing a guessed NDK. Inspect `java -version`, `adb version`, configured `JAVA_HOME`/`ANDROID_HOME`, installed SDK packages and NDK `source.properties`. A checks the selected device with `adb devices -l` under the lease; enable USB debugging and authorize the host. Source Android compilation passed, but physical Android runtime remains unverified. Missing Android tools/device does not authorize a parallel Android build while iOS runs; mark Android pending/out of demo scope.

### Disk and explicit downloads

Run read-only capacity checks from the target root before installing and again before building:

```sh
df -h . "$HOME"
du -sh .starter assets
```

After those directories actually exist, inspect `du -sh node_modules ios/Pods android .local`. Record phone free storage separately. Reserve space for dependencies, Pods/Gradle intermediates, build artifacts, model staging and the installed model; 1.117 GB free alone is insufficient. Source Android tooling/build consumed about 20 GiB, and source iOS work encountered low-disk failures: these are planning evidence, not measured target requirements. Coordinator records available space and a headroom decision. Stop if capacity is inadequate. **No deletion, cache purge, clean prebuild, uninstall, database reset or replacement of user files without confirmation.**

Dependency/toolchain/app installation and teacher download are explicit online steps, completed before disconnected checks. Coordinator records each chosen download and destination. Never silently fetch a model on launch or send study content over the network. Download through the explicit teacher flow, or disclose an authorized staged synthetic-demo setup; source files are not automatically available to this new app sandbox.

Exact teacher identity from [reference manifest](../../.starter/reference-app/src/t0/model.json):

| Field | Required identity |
|---|---|
| Model / repository | Qwen2.5-1.5B-Instruct / Qwen/Qwen2.5-1.5B-Instruct-GGUF |
| Revision | `91cad51170dc346986eccefdc2dd33a9da36ead9` |
| Artifact / quantization | `qwen2.5-1.5b-instruct-q4_k_m.gguf` / Q4_K_M |
| Size | **1,117,320,736 bytes**, approximately **1.117 GB** decimal (1.041 GiB) |
| SHA-256 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| License / runtime | Apache-2.0 / `llama.rn@0.9.1` |

Use the manifest's pinned download/license URLs; no unpinned replacement or illustrative Qwen3 model size. Record byte/hash verification for the actual target artifact. A host hash does not establish successful phone installation, load or inference.

## Single native lease

All native generation, Pods, builds, install/launch, simulator/phone automation and device inspection are serialized through **owner A**. Coordinator owns installs; coordinate their timing with A and the lease whenever native tooling is involved. Other lanes request checks from A instead of running their own commands.

```text
python3 scripts/hackathon.py native-run --owner A -- <cmd>
```

Replace `<cmd>` with the reviewed command and discovered target paths/IDs; this is syntax, not a runnable placeholder. No parallel builds, separate-platform build, competing device session or unleased IDE build. Wait for completion before another operation. Do not background heavy work to release the lease early. The lease is a coordination convention; check for already-running external work. Never automatically evict a stale lock: coordinator/A first establish whether its process is still active. Missing/broken helper means native work waits for coordinator repair.

## Timebox and prioritized phone smoke

Prerequisites should be ready before kickoff; cold tooling installs may exhaust 90 minutes. Checkpoints are **10/30/55/70/90 minutes**: coordinator confirms scope/contracts at 10, integration risks at 30, integration candidate at 55 and phone readiness at 70. At 70 stop expanding scope. If a signed target build or verified model is unavailable, record the blocker and demonstrate only verified functionality; do not manufacture a complete flow.

Minutes **70–90** are a focused smoke, not the sustained T8 benchmark. A holds exclusive device access and records actual elapsed time; stop at the timebox and mark remaining steps pending.

| Priority / window | Focused check and evidence |
|---|---|
| P0, 70–73 | Confirm target bundle ID, artifact/signing, device/OS and actual model readiness. For offline evidence use embedded production JS with no Metro dependency; disable Wi-Fi and cellular, record state and cold relaunch. A dev-client-only result is explicitly limited. |
| P0, 73–77 | Traverse introduction/local profile/teacher to Home. Create a uniquely named synthetic notebook; paste and review/save fresh English text in the chosen destination. Check persistence and actual readiness/error states. |
| P0, 77–81 | Ask one fresh source-backed question; inspect quote/source/revision and saved history. Exercise an absent-evidence question if time allows. Retain validation failure or irrelevant output as failure, never relax validation. |
| P0, 81–85 | Request a live three-question quiz. If valid, answer correct/wrong/skipped, verify deterministic score and source review, then duplicate-submit protection. If generation fails, show it and mark downstream checks pending. Do not substitute curated questions. |
| P0, 85–88 | Force-close/reopen; inspect saved history/attempt and original evidence. Exercise one bounded cancel/background recovery path if time allows. Capture actual screens against the applicable docs/UX reference. |
| P1, remaining time | Fresh offline image/PDF OCR with review/save; source-revision change and immutable old history; keyboard/large text/accessibility; separate labeled Buddy flow. Record each omitted path pending. File picker/permission or native failures remain visible. |
| 88–90 | Coordinator consolidates exact pass/fail/pending evidence, limitations, unresolved defects and demo decision. No last-minute sustained run or publishing. |

Wireless-off success alone does not establish zero network attempts. Record network observation separately; inability to capture attempts is pending, not pass. A successful small quiz does not cancel the inherited ten-request quality failure.

## Truthful demo disclosure

State reuse/fresh mode and what existed before the hackathon. Name the actual phone, build and verified model; disclose preinstallation/staging and prepared synthetic notes. Label extractive Summary/Explain as selected-source excerpts and quizzes as bounded source-sentence practice where applicable. Buddy is separate general-knowledge local chat, not notebook-grounded fallback. Show failures honestly; recordings or saved results must be explicitly labeled if separately authorized.

Do not claim full V1, broad teaching reliability, conceptual quiz quality, mastery/diagnosis, Bengali OCR, arbitrary handwriting, universal phone support or complete offline/network acceptance. **Target evidence is pending until captured; full V1 remains blocked by inherited T8 quality failures.** The user-stopped sustained benchmark must not automatically resume. See [release gates](release-gates.md) for the separate acceptance protocol.

## Final evidence template (coordinator fills with actual results)

```text
Date/time / coordinator / A:
Mode and reused baseline provenance / target revision or snapshot:
Actual target root / bundle or application ID:
Node/npm / lockfile identity / install result:
Platform tools / discovered workspace, scheme, test target:
Artifact path, configuration, signing/expiry / embedded JS or Metro dependency:
Phone model / OS / RAM / free storage; host free storage:
Model ID / revision / quantization / bytes / SHA-256 / license / runtime:
Download or staging method, explicit authorization / phone verification:
Lease command(s) / exact test command(s), counts and exit codes:
Each smoke row: PASS | FAIL | PENDING | BLOCKED + actual observation:
Wireless state / network-attempt observation (separate results):
UX reference / screenshot paths and comparison / accessibility pending:
Logs and raw result paths (target evidence, no private content):
Failures, omitted checks, data-preservation observations:
Demo decision and disclosures:
Full V1: BLOCKED; inherited T8 failures and remaining release gates:
Next bounded action / owner; sustained benchmark remains stopped:
```
