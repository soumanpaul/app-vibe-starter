# Gurukul hackathon starter — project instructions

## Start here
- Read docs/engineering/state.md, docs/hackathon/README.md, docs/hackathon/ownership.json and your lane in docs/hackathon/lanes.md.
- This is a NEW starter, not the verified source app. Copied quality reports/state are historical evidence only. The original source state and sequential plan are preserved under .starter/archive/. Active orchestration lives in docs/hackathon/; it supersedes copied sequential/one-agent workflow instructions.
- Read docs/UX/README.md and only your assigned references BEFORE UI implementation. Preserve all existing docs, UXs, original research and docs/SWE_os.md. Reuse supplied assets; no UX generation is needed or authorized for this preparation.
- Default to a coordinator plus eight parallel feature lanes A–H when available. Parallel work is explicitly authorized for the hackathon. If the runtime cannot spawn agents, use separate CLI sessions with the lane prompts; never claim workers were launched when they were not. At least four concurrent workers requires enough actual sessions/runtime capacity.

## Ownership and integration
- All sessions share this checkout; no worktrees, branches, commits, staging, push, publishing or distribution unless explicitly requested.
- Follow ownership.json. Only the coordinator edits root config/lockfiles, App.tsx/index.ts, shared contracts, global plans/state, and test/build orchestration. H owns app/ and shared UI. B owns all SQLite repositories, migrations and foundation wiring. A owns native modules/runtime/platform directories. Other lanes own their feature files only.
- Read any path; write only your lane. Report cross-owner requests in docs/hackathon/status/<lane>.md, and stop changing an API after contract freeze without coordinator acknowledgement. No broad formatter, npm install, prebuild, pod install, xcodebuild or Gradle runs by multiple workers.
- First coordinator selects mode explicitly: reuse baseline (recommended if competition allows) or fresh implementation. Do not silently present pre-existing code as hackathon-written work. The starter contains a reusable reference snapshot, not a built app. Neither mode guarantees all features and physical release gates within 90 minutes.
- Use scripts/hackathon.py for bootstrap, ownership/coverage checks and the native lease. Bootstrap fails before copying if a destination exists; no overwrite/reset. Native lock is a coordination convention, not a security sandbox; no automatic stale-lock eviction.
- Workers publish concise changed paths, contract requests, exact checks and remaining blockers in their own status file. Only coordinator consolidates state.md. Checkpoints at 10/30/55/70/90 minutes. Continue independent work while waiting for a dependency; do not fake successful native responses.

## Product invariants
- Offline V1 study: no cloud inference/OCR, server dependency, required login, Gmail/password recovery, analytics or study-content upload. Network only for explicit teacher download and app installation. Local profile/logout is not authentication or cloud restore.
- Source-backed Study uses selected notebook/revision evidence only; validate citations and quotes. AI Buddy is a separately labeled general-knowledge local chat, never silent fallback for retrieval failure.
- Treat notes and model output as untrusted. Validate bounded output before use; deterministic transactional MCQ grading, immutable evidence/snapshots, idempotent submission, no invented keys or curated questions passed off as generated.
- Keep exact model/revision/license/quantization/size/hash/runtime together. Current source uses Qwen2.5-1.5B-Instruct, not illustrative Qwen3 board text. Do not change model/dependencies under time pressure without evidence.
- Preserve data with explicit migrations. No destructive reset, user-file deletion, device uninstall or overwrite of existing database tables without confirmation. Use synthetic fixtures for destructive checks.
- One native heavy-work lease; cancel/background/force-close truthfully. No swallowed cloud calls count as offline. Keep source content out of diagnostics; preserve native privacy patches and backup exclusions.
- English printed inputs first. No arbitrary handwriting, Bengali OCR, universal device support, intelligence diagnoses or mastery/exam predictions.

## Tools and checks
- Use apply_patch for code/text edits. Prefer available MCP tools; filesystem MCP for ~/codex, SQLite MCP for ~/codex/test.db, Playwright MCP for browser automation. Native claims require native evidence.
- Run focused owned tests/typecheck/lint once, rerunning only invalidated checks. Coordinator runs integrated checks at the final gate. Never resume the historical user-stopped sustained T8 run automatically.
- UI verification includes actual screenshot comparison, small/large text, keyboard and accessibility when available. Mark untested native/accessibility/offline gates pending. Expo Go is preview-only for native AI/OCR/PDF.
- Do not edit the source GURUKUL checkout, read live user app data or touch global tool configuration. New installation must use a distinct coordinator-selected bundle/application ID to avoid replacing the user's source app.
- Do not install packages, download a GGUF, launch workers for implementation, build native apps or publish just because this starter is being prepared. Follow the explicit kickoff when the user starts the hackathon.
