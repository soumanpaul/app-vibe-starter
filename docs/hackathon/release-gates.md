# Full V1 release gates — separate from the 90-minute demo

**Full V1: BLOCKED. Target verification: PENDING.** A successful [focused phone smoke](preflight.md) supports only the paths actually observed. It does not authorize T9, publication, distribution or a release claim. Source successes remain historical evidence and must not be transferred to this distinct application ID without target validation.

Authority: [evaluation protocol](../quality/evaluation.md), [archived source state](../../.starter/archive/state.md), [source T8 report](../quality/reports/t8-release-evaluation.md) and [raw source quality results](../quality/reports/t8-quality-results.json). Their source-local artifact paths are not promised target artifacts.

## Inherited blockers

The source iPhone fixed dataset retrieved/isolation-checked 20/20, but only **14/20 answers validated**, below the 16/20 semantic threshold even before human review. Absent evidence produced **three refusals, one validation failure and one irrelevant sourced answer**. Quiz generation yielded **0/10 valid complete sets**. Valid citation structure alone did not establish relevance. A separate smaller run's three successful quizzes do not supersede those failures.

The sustained run was **stopped by the user** at its last completed checkpoint of 9m52s; it did not complete 15 minutes. Thermal state reached serious; sampled resident memory was not an OS-measured true peak. **Do not automatically restart this stopped benchmark**, including as part of hackathon scripts or final verification. Resumption needs explicit authorization. Human review, fresh disconnected flow, network-attempt inspection, broader accessibility and Android physical runtime remain unresolved. Failed network capture is not zero-network evidence.

## Gate ledger

All target results below start **PENDING**. Coordinator records target evidence and inherited defects independently. Resolve measured quality failures with bounded changes and affected-case reruns without weakening validators or inventing answer keys; reserve the complete protocol for separately authorized evaluation/release work.

| Gate | Required acceptance evidence |
|---|---|
| Provenance and native build | Target revision/snapshot, exact lockfile and model identity from preflight, runtime/privacy patch, prompt/retrieval/OCR versions; actual phone/OS/ABI/RAM/storage and valid distinct-ID signed artifact. Native inference/OCR/PDF must work on each claimed platform. Source Android compilation alone is insufficient. |
| Deterministic correctness | Relevant typecheck/lint/tests plus scoring of correct/wrong/skipped/invalid questions, idempotent submission, source IDs/quotes, notebook filtering, token bounds and cancellation. No model grading or model-written SQL. |
| Migration/data integrity | Explicit migrations preserve data; rollback/failure does not reset it. History/attempt evidence is immutable across source edits; interrupted jobs recover. Verify with synthetic fixtures, never destructive tests on user data. |
| Retrieval/isolation | Fixed corpus: 20 answerable, 5 absent-evidence, 5 injection cases, 10 quiz requests across two subjects with distractors and same-topic different notebooks. Recall@5 at least 18/20; 100% selected notebook/source/revision isolation. |
| Answer quality | 100% valid published citation IDs/quotes; human-reviewed supported/correct answers at least 16/20. All five absent-evidence cases avoid invented sourced answers. Keep validation failures distinct from successful refusal. |
| Injection/privacy | All five injection cases preserve task boundaries, with no tool/network actions. Treat notes/output as untrusted. Inspect native diagnostics for content leaks and preserve log patches, backup exclusions and permission handling. |
| Quiz quality | At least 9/10 requests yield valid sets within one repair; 100% displayed items validated. At least 90% reviewed items unambiguous, correct and source-supported; 100% deterministic/idempotent grading. No curated fallback presented as generation. |
| Fresh disconnected operation | Explicitly install/download/verify first; disable Wi-Fi and cellular, cold-launch standalone without Metro. Fresh image/PDF import and OCR/review, new answer, quiz/submission, revision/history and relaunch all work. Observe attempted network traffic as well as connectivity; failed cloud calls are failures. |
| Durability/recovery | Force-close preserves history/completed attempts; interruption/background and repeated taps recover without duplicate or corrupt writes. Cover missing model, interrupted download/hash mismatch/low storage, denied camera, blank/rotated/large image, locked/scanned/corrupt PDF, malformed/truncated output, missing original and source removal during generation with authorized synthetic cases. |
| Physical performance | Separately authorized protocol: 3 cold loads, 10 short responses, 3 three-question quizzes and 15-minute study sequence. Record median/worst, peak-memory method, battery/power, thermal, crashes and cancellation. Targets: load ≤15s, first token ≤10s, answer ≤45s, quiz ≤90s, cancellation feedback ≤1s, no OOM/crash. Sampling limitations must remain explicit. Stopped sustained run remains stopped until authorized. |
| UX/accessibility | Compare actual screens to assigned docs/UX references; verify small/large text, keyboard, VoiceOver/Android screen reader as claimed, Reduce Motion, focus/reachability and failure/recovery states on claimed devices. Mockups, browser tests and visual approval alone do not pass native accessibility. |
| Human/support review | Independent human grounding/pedagogical review; fluent language-specific datasets/review before additional language claims. Document unsupported inputs/devices and exact scope. Tiny regression datasets do not prove curriculum-wide accuracy or mastery. |
| Release handoff | Complete target evidence ledger, resolved blockers and reviewed limitations; inspect privacy/signing/distribution readiness. Coordinator requires explicit user authorization for publication/distribution. Personal development signing is not distribution acceptance. |

## Evidence and decision rules

For each gate retain date, target code/config identity, device, exact command and exit status, dataset/model/runtime parameters, expected versus actual results, raw artifacts and reviewer. Use the [benchmark template](../engineering/templates/benchmark.md) for actual authorized runs. Keep private content out of diagnostics. Missing evidence is pending; failed execution or failed assertions are failures; report skipped checks explicitly. Re-run passing checks only when relevant changes invalidate them.

All native work and device access remain under A's single lease:

```text
python3 scripts/hackathon.py native-run --owner A -- <cmd>
```

No parallel builds/device use or automatic stale-lock eviction. Coordinator resolves test targeting before execution: source tests hardcode `org.gurukul.t0`, source test target is `GurukulT7UITests`, and newly generated workspace/scheme names must be discovered. Report zero executed tests as no evidence, never a passing smoke.

At hackathon handoff use the preflight evidence template and a bounded demo decision. Full-release handoff additionally lists every gate's PASS/FAIL/PENDING/BLOCKED status with evidence and remaining owner/action. Full V1 stays blocked while quality failures or mandatory acceptance gaps remain, regardless of demo appearance or source build successes. No automatic sustained evaluation, source checkout edits, data deletion, app uninstall or publication follows from completing these documents.
