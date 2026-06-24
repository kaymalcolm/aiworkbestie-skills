# Broll Searcher — Coder Agent Skill

Spawn a senior Python engineer agent that reads the `.collab/` folder, determines whether to run in **fix mode** (apply test-analysis bugs and risks) or **build mode** (implement from planner spec), then makes precise, high-quality edits to the Python files and database. Writes a detailed change log to `.collab/`.

## When This Skill Activates

**Explicit:** User types `/broll-code`

**With arguments:**
- `/broll-code fix` — force fix mode (apply test-analysis findings only)
- `/broll-code build` — force build mode (implement from spec)
- `/broll-code fix+build` — apply fixes first, then build to spec

**Intent detection:** Recognize requests like:
- "Apply the broll fixes"
- "Code up the broll changes"
- "Fix the bugs in broll searcher"
- "Build from the spec"
- "Go fix the Python files for broll"
- "Apply everything from the test analysis"

---

## Autonomy Rules

Run the full workflow with no confirmation. Edit Python files directly. Run SQL via SQLcl MCP if DB changes are needed. Write a change log when done. Never skip a BUG fix in favor of a WARN.

---

## Paths

| Item | Path |
|---|---|
| App root | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/` |
| Collab dir | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/` |
| Test analysis | `.collab/test-analysis-2026-06-18.md` (most recent) |
| Spec file | `.collab/spec-YYYY-MM-DD.md` (most recent, if present) |
| Change log output | `.collab/changes-YYYY-MM-DD.md` |

---

## Mode Selection Logic

Before spawning the agent, check `.collab/` for the most recent spec and test-analysis files:

```
list files in .collab/ → identify:
  - most recent test-analysis-*.md
  - most recent spec-*.md (may not exist yet)
```

Mode rules:
- **Fix mode**: always runs. Test-analysis findings are always applied.
- **Build mode**: runs only if a spec file exists in `.collab/`. If no spec exists, skip build mode and note it in the report.
- Default (no argument): fix mode if only test-analysis present; fix+build if spec also present.

---

## Workflow

### STEP 1 — Identify collab files

List `.collab/` and identify the most recent test-analysis and spec files. Note their names for the agent.

### STEP 2 — Spawn the coder agent

Use the Agent tool with the following prompt, substituting the actual filenames found in STEP 1. Wait for its result.

```
You are a senior Python engineer specializing in FastAPI, Oracle ADB 23ai, and production API quality. Your job is to apply fixes and improvements to the Broll Searcher application — a B-roll video search service.

You produce A+ quality code: correct error handling, precise types, no silent failures, clean interfaces, no dead code, no premature abstraction. You do not add features that weren't asked for. You do not leave half-finished work.

---

## PHASE 1 — READ EVERYTHING FIRST

Read every source file before touching anything.

**Source files to read** (all in /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/):
db.py, smugmug_client.py, embedder.py, video_utils.py, video_describer.py, ingestion.py, search.py, scheduler.py, main.py, routes.py, requirements.txt, .env

**Collab files to read** (in .collab/):
- [TEST_ANALYSIS_FILENAME] — read every finding, severity, and recommended fix
- [SPEC_FILENAME if present] — read every section; this is the authoritative contract if present

Do not make any edits until you have read all files.

---

## PHASE 2 — FIX MODE: Apply all BUG and RISK findings

Work through the test analysis in priority order. For each [BUG] and [RISK] finding:

1. Re-read the relevant file at the exact lines cited
2. Confirm you understand what the current code does and why it's wrong
3. Apply the fix using the Edit tool (surgical edits only — do not rewrite surrounding code)
4. If the fix requires a new helper function, add it near the function it serves
5. If the fix requires a new import, add it at the top of the file with the existing imports
6. After each edit, verify the change is syntactically correct by re-reading the affected lines

### Required fixes (apply all of these):

**FIX-1: db.py — ORA- error detection**
After parsing the JSON output in `_run_sqlcl`, scan stdout for `ORA-\d{5}` patterns and raise RuntimeError with the Oracle error line. This must run BEFORE the JSON parse attempt so that ORA- errors in a statement that produced no rows are still caught. Add `import re` if not present.

The scan must:
- Check every line of proc.stdout
- Raise on the FIRST ORA- line found
- Include the full line content in the error message
- NOT raise on lines where "ORA-" appears in a column value or comment (check that the line starts with whitespace + "ORA-" or matches `r'^\s*ORA-\d{5}'`)

**FIX-2: db.py — password not exposed in process args or error messages**
The subprocess call `[_SQLCL_BIN, "-nolog", f"{_USER}/{_PASSWORD}@{_DSN}"]` puts the password in the process argument vector, visible in `ps aux`. 

Fix: pass credentials via stdin instead of command line:
```python
proc = subprocess.run(
    [_SQLCL_BIN, "-nolog", "-S", "/nolog"],
    input=f"CONNECT {_USER}/{_PASSWORD}@{_DSN}\n" + script,
    ...
)
```
Alternatively, if `-nolog` with inline connect string is the only reliable SQLcl pattern for this wallet setup, at minimum ensure error messages use a redacted form:
```python
raise RuntimeError(f"SQLcl error (user={_USER}@{_DSN}): {proc.stderr.strip()}")
# NEVER include _PASSWORD in any log or error message
```
Choose whichever approach works for the existing wallet/TNS_ADMIN setup. Add a comment explaining the security decision.

**FIX-3: db.py — add sql_str edge case (empty string)**
`sql_str("")` currently returns `"''"` which inserts an empty string into Oracle. This is semantically different from NULL. Add a note in the docstring: "Use sql_str(None) to insert NULL; sql_str('') inserts empty string — make sure that's the intent."

**FIX-4: ingestion.py — EXIF date format normalization**
Replace the `taken_raw` / `taken_expr` block (lines that set `taken_raw` and `taken_expr`) with:

```python
taken_raw = (img_data.get("DateTimeOriginal") or img_data.get("Date", ""))[:19]
if taken_raw:
    # EXIF format uses colons as date separators: "2024:05:15 14:30:00"
    # Normalize to ISO 8601: "2024-05-15 14:30:00"
    if len(taken_raw) >= 10 and taken_raw[4] == ":" and taken_raw[7] == ":":
        taken_raw = taken_raw[:4] + "-" + taken_raw[5:7] + "-" + taken_raw[8:]
    fmt = "'YYYY-MM-DD\"T\"HH24:MI:SS'" if "T" in taken_raw else "'YYYY-MM-DD HH24:MI:SS'"
    taken_expr = f"TO_TIMESTAMP('{taken_raw}', {fmt})"
else:
    taken_expr = "NULL"
```

**FIX-5: ingestion.py — guard empty frames after extract_keyframes**
Immediately after the `try/except` block for `extract_keyframes`, add:

```python
if not frames:
    print(f"  No frames extracted for {smugmug_id} (video may be < {10}s), skipping.")
    return False
```

This must come before the `describe_video_keyframes` call and the CLIP embedding loop.

**FIX-6: ingestion.py — guard re-SELECT after INSERT**
After `rows = run_sql(f"SELECT id FROM media_items WHERE smugmug_id = ...")` (the one AFTER the INSERT), add:

```python
if not rows:
    raise RuntimeError(
        f"INSERT appeared to succeed but re-SELECT returned no row for smugmug_id={smugmug_id}. "
        f"Likely a silent ORA- error — check db.py ORA- detection."
    )
```

**FIX-7: ingestion.py — concurrent sync guard**
At the start of `run_full_sync`, before the INSERT into sync_log, add a check:

```python
running = run_sql("SELECT id FROM sync_log WHERE status = 'running' AND ROWNUM = 1")
if running:
    raise RuntimeError("A sync is already in progress. Aborting to prevent concurrent ingestion.")
```

**FIX-8: video_utils.py — improve error on curl failure**
In `extract_keyframes`, wrap the `subprocess.run(["curl", ...])` call to catch `subprocess.CalledProcessError` and re-raise with the URL and status code:

```python
try:
    subprocess.run(["curl", "-L", "-o", video_path, "--max-time", "300", video_url],
                   check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    raise RuntimeError(
        f"curl failed (exit {e.returncode}) downloading video: {video_url}"
    ) from e
```

**FIX-9: video_describer.py — guard empty frames**
At the top of `describe_video_keyframes`:

```python
if not frames:
    return ""
```

**FIX-10: video_describer.py — add retries and configurable model**
1. In `_get_client()`, initialize with `max_retries=3`:
```python
_client = anthropic.Anthropic(max_retries=3)
```
2. Make the model configurable via env var:
```python
import os
_MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
```
Then use `model=_MODEL` in the `messages.create` call.

**FIX-11: search.py — Oracle Text CTX operator sanitization**
Add a new function `_sanitize_ctx_query` and use it in `text_search`:

```python
import re

_CTX_RESERVED = re.compile(r'[${?}~%!;,()\[\]\\^]')

def _sanitize_ctx_query(q: str) -> str:
    """Strip Oracle Text reserved operator characters to prevent ORA-29902."""
    return _CTX_RESERVED.sub(' ', q).strip() or q
```

In `text_search`, change `escape(query_text)` to `escape(_sanitize_ctx_query(query_text))`.

**FIX-12: routes.py — concurrent sync guard via HTTP 409**
Replace the `trigger_sync` endpoint body:

```python
@router.post("/ingest/sync")
async def trigger_sync(request: Request, background_tasks: BackgroundTasks):
    rows = run_sql("SELECT id FROM sync_log WHERE status = 'running' AND ROWNUM = 1")
    if rows:
        raise HTTPException(status_code=409, detail="A sync is already running. Check /ingest/status.")
    pipeline = request.app.state.pipeline
    background_tasks.add_task(pipeline.run_full_sync)
    return {"status": "sync started", "message": "Check /ingest/status for progress"}
```

**FIX-13: routes.py — VECTOR column deserialization**
In `find_more_like_this`, replace the vector parsing:

```python
raw = rows[0].get("visual_embedding")
if raw is None:
    raise HTTPException(status_code=404, detail="Media item has no visual embedding yet")
# Oracle returns VECTOR as a string — may be JSON array "[0.1, ...]" or other format
try:
    stored_vector = json.loads(raw) if isinstance(raw, str) else list(raw)
    if not isinstance(stored_vector, list) or len(stored_vector) != 768:
        raise ValueError(f"Unexpected vector shape: {type(stored_vector)}, len={len(stored_vector) if hasattr(stored_vector, '__len__') else 'N/A'}")
except (json.JSONDecodeError, ValueError, TypeError) as e:
    raise HTTPException(status_code=500, detail=f"Could not parse stored embedding: {e}")
```

**FIX-14: main.py — ALL_INDEXES in health check**
Replace the health check SQL:

```python
rows = run_sql(
    "SELECT STATUS FROM ALL_INDEXES "
    "WHERE INDEX_NAME = 'IDX_MI_VISUAL' AND TABLE_OWNER = 'BROLL'"
)
```

**FIX-15: scheduler.py — validate timezone at startup**
Replace the scheduler timezone handling:

```python
import pytz

def start_scheduler(pipeline):
    tz_name = os.environ.get("APP_TIMEZONE", "America/New_York")
    try:
        timezone = pytz.timezone(tz_name)
    except Exception:
        print(f"WARNING: Unknown timezone '{tz_name}', falling back to UTC. "
              f"Set APP_TIMEZONE to a valid tz database name.")
        timezone = pytz.UTC
    scheduler = BackgroundScheduler(timezone=timezone)
    ...
```

Also add `pytz` to requirements.txt if it's not already there.

**FIX-16: .env — add missing Oracle variables**
The .env file is missing ORACLE_USER, ORACLE_PASSWORD, ORACLE_WALLET_DIR, ORACLE_DSN, and CLAUDE_MODEL. Add them:

```
ORACLE_DSN=kmalcolm_tp
ORACLE_USER=broll
ORACLE_PASSWORD=<your_broll_schema_password>
ORACLE_WALLET_DIR=/Users/kmalcolm/oracle/wallet
CLAUDE_MODEL=claude-haiku-4-5-20251001
```

Keep all existing values. Only add the missing ones. Do not touch ANTHROPIC_API_KEY or SmugMug credentials.

---

## PHASE 3 — BUILD MODE (only if a spec file was provided)

If a spec file exists in .collab/, read Section 10 ("Changes Required from Test Analysis") and Section 3 ("Module Contracts"). For each contract in the spec that is NOT already satisfied by the FIX-* changes above, implement it.

Priorities for build mode:
1. Any startup validation requirements from Section 9 of the spec
2. Any interface contract changes from Section 5 that aren't covered by fixes
3. Any error handling policy requirements from Section 6
4. Security mitigations from Section 7 that aren't covered by fixes

Do NOT implement new features that aren't in the spec or test analysis. Do NOT refactor working code. Do NOT add abstraction layers. Fix what's broken and build what's specified.

---

## PHASE 4 — VERIFY YOUR CHANGES

After all edits are complete:

1. Re-read each modified file from top to bottom
2. Check that all imports are correct (no missing imports from new functions)
3. Check that all function signatures match what callers expect
4. Check that no previously working code path was broken
5. Verify the .env has all required variables (no module will try to read a var that isn't defined)

For any change that involves Oracle SQL:
- Read the exact SQL string you produced
- Mentally run it against the schema: does it reference real column names, correct table names, correct Oracle syntax?
- Check for unclosed quotes, missing commas, mismatched parentheses

---

## PHASE 5 — WRITE CHANGE LOG

Write a detailed change log to:
/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/changes-2026-06-18.md

Format:
```markdown
# Broll Searcher — Change Log
**Date:** [today]
**Mode:** [Fix / Build / Fix+Build]
**Source:** test-analysis-YYYY-MM-DD.md [+ spec-YYYY-MM-DD.md if used]

## Changes Applied

### FIX-N: [short title]
**File:** filename.py
**Lines changed:** [line range]
**What changed:** [one sentence]
**Why:** [the original bug or risk]
**Verification:** [how to confirm it works]

---
[repeat for each change]

## Files Modified
- db.py
- ingestion.py
- [etc.]

## Files NOT Modified (and why)
- [any file that had findings but required no code change]

## Database Changes Required
[Any SQL that must be run against Oracle ADB before deployment. Include exact statements.]

## Open Items
[Any finding that could NOT be fixed in code — e.g., requires env var changes by the user, requires a DB migration that needs ADMIN access, etc.]
```

After writing the change log, confirm the path and byte count.
```

---

### STEP 3 — Report to user

After the agent completes, report:

```
Broll Searcher code changes applied.

Change log: /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/changes-YYYY-MM-DD.md

Files modified:
[list from agent]

[paste the ## Open Items section from the change log]
```

If the agent did not write the change log, write it yourself from the agent's output before reporting.
