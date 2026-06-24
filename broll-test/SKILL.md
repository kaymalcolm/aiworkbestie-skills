# Broll Searcher — Test Analysis Skill

Spawn a code-review agent that reads every Python file in the broll-searcher app, walks the happy path and key edge cases, and writes a structured analysis report to `.collab/` in the project directory.

## When This Skill Activates

**Explicit:** User types `/broll-test`

**Intent detection:** Recognize requests like:
- "Test the broll searcher code"
- "Review the broll-searcher for edge cases"
- "Run the broll test agent"
- "Write the test analysis for broll"

---

## Autonomy Rules

Run the full workflow with no confirmation. Write the output file and report the path when done.

---

## Paths

| Item | Path |
|---|---|
| App root | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/` |
| Output dir | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/` |
| Output filename | `test-analysis-YYYY-MM-DD.md` (use today's date) |

---

## Workflow

### STEP 1 — Spawn the analysis agent

Use the Agent tool with the following prompt. Pass it verbatim — do not paraphrase or summarize. Spawn this as a foreground agent and wait for its result before proceeding.

```
You are a senior Python engineer doing a pre-deployment code review of a FastAPI + Oracle ADB application called Broll Searcher. Your job is to walk through every Python file, identify happy-path correctness and edge-case risks, and produce a structured analysis report.

The app lives at: /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/

## Files to read (read ALL of them before writing anything)

- db.py
- smugmug_client.py
- embedder.py
- video_utils.py
- video_describer.py
- ingestion.py
- search.py
- scheduler.py
- main.py
- routes.py

Also read the .env file to understand the environment variable names (values are secrets — note variable names only, never log actual values in your output).

## Analysis framework

For each file, evaluate:

### Happy path
Does the core flow work correctly end-to-end? Walk through what happens on a successful run:
- SmugMug API returns a video → keyframes extracted → Claude describes it → CLIP embeds it → row inserted → text search finds it
- Trace this through db.py, ingestion.py, video_utils.py, video_describer.py, embedder.py

### Edge cases to check

1. **db.py**
   - What happens if SQLcl is not on PATH?
   - What if the SQL returns no rows vs. an empty items array?
   - Does `sql_str()` correctly handle strings with single quotes?
   - Does `vec_literal()` produce valid Oracle VECTOR syntax for a 768-dim list?
   - What if `_run_sqlcl` timeout is hit (60s vs 120s — which is it)?

2. **smugmug_client.py**
   - What if a gallery key in SMUGMUG_GALLERY_KEYS doesn't exist in SmugMug?
   - What if `get_album_images` returns an album with 0 videos (all images)?
   - What if pagination never terminates (NextPage always present)?
   - What if `get_image_urls` returns a dict with none of the expected size keys (Th, S, L, XL, Original, Video)?
   - OAuth token expiry — SmugMug tokens are permanent until revoked, but what happens if auth fails mid-crawl?

3. **video_utils.py**
   - What if FFmpeg is not installed on the OCI instance?
   - What if `curl` download fails (private URL expired, SmugMug 403)?
   - What if the video has a duration shorter than `interval_sec` (10s) — 0 frames extracted?
   - What if `extract_keyframes` returns an empty list and `embed_video` is called — does it raise cleanly?
   - Temp dir cleanup: does the `with tempfile.TemporaryDirectory()` guarantee cleanup even if FFmpeg crashes?

4. **video_describer.py**
   - What if `frames` is an empty list?
   - What if Claude Vision returns an empty string?
   - What if the Anthropic API key is invalid or rate-limited?
   - Is the Anthropic client initialized lazily — what if `ANTHROPIC_API_KEY` is missing from env at import time vs. at first call?

5. **ingestion.py**
   - What if both `description` and `avg_vec` are None (both steps failed)? Is a row with all NULLs for those columns still inserted?
   - What if `original_url` is None — is it caught before calling `extract_keyframes`?
   - The `taken_raw[:19]` slice: what if SmugMug returns an EXIF-format date (`2024:05:15 14:30:00`) vs ISO 8601 (`2024-05-15T14:30:00`) — does the Oracle TO_TIMESTAMP format string handle both?
   - What if `run_dml` for the INSERT fails (duplicate key race condition, DB timeout)?
   - The `sql_str(description)` in the INSERT: what if description is >4000 chars (CLOB limit for inline literals in Oracle)?
   - What if the sync_log INSERT fails at the start — does the pipeline still run?

6. **search.py**
   - What if `visual_search` is called before any rows exist (empty table) — does Oracle return 0 rows cleanly or error on HNSW with empty index?
   - What if `text_search` is called before `CTX_DDL.SYNC_INDEX` has been run — does CONTAINS() return 0 rows or error?
   - What if `query_vector` is all zeros — is the cosine distance undefined?
   - SQL injection: `escape(query_text)` is used in CONTAINS() — is single-quote doubling sufficient for Oracle Text CONTAINS syntax, or does it need additional escaping for CTX operators like `$`, `?`, `{}`?

7. **main.py / routes.py**
   - What if CLIP model fails to load at startup — does the app crash entirely or handle gracefully?
   - What if `SMUGMUG_GALLERY_KEYS` is empty or not set — does `SmugMugClient` get `gallery_keys=None` correctly?
   - `/ingest/sync` fires a background task — if a sync is already running, does triggering again start a second concurrent sync? Is that safe?
   - `request.app.state.embedder` in routes — what if a route is called before lifespan completes (race at startup)?
   - The `/health` endpoint queries `USER_INDEXES` — does this work when the Oracle schema is `broll` (not the session user)?

8. **scheduler.py**
   - What if `APP_TIMEZONE` is set to an invalid timezone string?
   - What if `pipeline.run_full_sync` raises an exception — does APScheduler swallow it silently, or does it log/disable the job?

### Cross-cutting concerns

- **SQL injection surface:** List every place user input touches a SQL string and evaluate whether the escaping is sufficient.
- **Secret leakage:** Check for any place where env var values, tokens, or API keys could appear in logs, error messages, or API responses.
- **Concurrency:** The app runs with `--workers 1` in uvicorn. Are there any shared mutable state problems if a background ingestion task runs while a search request comes in?
- **Missing env var handling:** What happens if any required env var (ORACLE_PASSWORD, SMUGMUG_API_KEY, etc.) is missing — does the app crash at startup or at first use?

## Output format

Write a single markdown file with this structure:

---
# Broll Searcher — Test Analysis
**Date:** [today]
**Files reviewed:** db.py, smugmug_client.py, embedder.py, video_utils.py, video_describer.py, ingestion.py, search.py, scheduler.py, main.py, routes.py

## Happy Path — End-to-End Trace
[Walk the full ingestion flow step by step: SmugMug crawl → keyframe extraction → Claude Vision → CLIP embed → Oracle insert → Oracle Text search. Note where each module hands off to the next and whether the contracts between them are correct.]

## Findings

For each finding use this format:
**[SEVERITY] File:line-range — Short title**
> What the issue is, why it matters, and the recommended fix.

Severity levels:
- **[BUG]** — will fail or produce wrong results in a real run
- **[RISK]** — will fail under specific conditions (empty results, network error, etc.)
- **[WARN]** — degrades silently, produces confusing output, or is a maintenance hazard
- **[OK]** — explicitly confirmed as correct (use sparingly — only for things that look wrong but aren't)

## Edge Case Summary Table

| Scenario | File | Status | Notes |
|---|---|---|---|
| Empty gallery (0 videos) | smugmug_client.py | [PASS/FAIL/RISK] | ... |
| Video shorter than 10s (0 frames) | video_utils.py | ... | ... |
| Claude Vision rate limited | video_describer.py | ... | ... |
| ... | ... | ... | ... |

Fill in at least 15 scenarios covering the edge cases from the analysis above.

## Recommended Fixes (Priority Order)

List only BUG and RISK items, ranked by impact. For each, give the exact file, the line(s) to change, and the fix in a code block.

---

Write this report to a file. Do NOT return it as your response text — write it directly to disk at:
/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/test-analysis-[TODAY_DATE].md

After writing, confirm the file path and byte count.
```

---

### STEP 2 — Report to user

After the agent completes, report:

```
Broll Searcher test analysis complete.

Report: /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/test-analysis-[date].md

[paste the ## Recommended Fixes section from the agent's output here]
```

If the agent failed to write the file, read the report from the agent's response and write it to disk yourself before reporting.
