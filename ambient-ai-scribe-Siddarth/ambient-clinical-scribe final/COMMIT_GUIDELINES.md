# GitHub Workflow — Mandatory Rules (Infotact Evaluation)

**This is graded on process, not just final code.** A monolithic final-day
push, however clean the code is, is grounds for disqualification per the
program spec. Read this before you touch `git push`.

## 1. Kanban board (set up Week 1, Day 1)

- Repo → **Projects** tab → new board with columns **To Do / In Progress / Done**.
- Break the 4-week roadmap into individual **Issues**, e.g.:
  - `#1 Integrate Whisper ASR pipeline`
  - `#2 Add speaker turn diarization heuristic`
  - `#3 Prompt-engineer SOAP JSON synthesis`
  - `#4 Build ICD-10 vector DB + RAG search`
  - `#5 Human-in-the-loop dashboard (edit/approve/sign-off)`
  - `#6 EHR JSON export`
- Move issues across the board as you work — GitHub timestamps every
  transition, and that timeline is audited for a steady weekly cadence.

## 2. Commit frequency & semantic messages

- **3–5 commits per active development day.** One commit = one logical
  change (a UI fix and a prompt tuning change are two separate commits).
- Every commit message references the issue it addresses:
  ```
  feat: add pause-based speaker diarization to transcription.py (fixes #2)
  prompt-tuning: enforce lowercase SOAP JSON keys in system prompt (fixes #3)
  fix: wire CORS middleware for React dashboard dev server (fixes #5)
  ```
- Common prefixes: `feat:`, `fix:`, `prompt-tuning:`, `refactor:`, `docs:`,
  `test:`, `chore:`.

## 3. Branching — never commit directly to `main`

- One short-lived feature branch per issue: `feature/icd-rag-search`,
  `feature/soap-llm-synthesis`, `fix/cors-dashboard`.
- Open a **Pull Request** into `main` at the end of each week summarizing
  what shipped and why (architectural decisions, pivots, trade-offs).
- Squash or keep history as your team prefers, but `main` should only ever
  move forward via reviewed PRs.

## 4. Credentials & PHI

- No API keys in source. Everything sensitive goes through `.env`
  (`.env` is already gitignored here — never remove that line).
- `data.db` and `icd_db/` are also gitignored — don't force-add generated
  local data, and never push real patient audio/transcripts.

## Suggested Week-by-Week issue breakdown (matches the spec's roadmap)

- **Week 1** — Audio ingestion, Whisper integration, basic diarization, DB schema.
- **Week 2** — SOAP prompt engineering, Pydantic schema validation, fallback logic.
- **Week 3** — ICD-10 dataset prep, ChromaDB embedding + RAG search, integration with Assessment field.
- **Week 4** — Dashboard (edit/approve/sign-off), EHR JSON export, CORS/deployment fixes, final README + tests.
