# Broll Searcher — Planner Agent Skill

Spawn a senior software architect agent that reads the entire codebase and BUILD_GUIDE, absorbs the test analysis, and produces an exhaustive engineering spec: exact function signatures, module contracts, error taxonomy, data-flow diagrams, Oracle-specific invariants, performance budgets, and security threat model. Output goes to `.collab/spec-YYYY-MM-DD.md`.

## When This Skill Activates

**Explicit:** User types `/broll-plan`

**Intent detection:** Recognize requests like:
- "Write the spec for broll searcher"
- "Plan out the broll code in detail"
- "Deep spec on the broll project"
- "Write the engineering spec before we code"
- "Run the planner agent"

---

## Autonomy Rules

Spawn the agent immediately. No confirmation. Write the spec file and report the path when done.

---

## Paths

| Item | Path |
|---|---|
| App root | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/` |
| Build guide | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/BUILD_GUIDE.md` |
| Collab dir | `/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/` |
| Output filename | `spec-YYYY-MM-DD.md` (use today's date) |

---

## Workflow

### STEP 1 — Spawn the planner agent

Use the Agent tool with the following prompt verbatim. Wait for its result before reporting to the user.

```
You are a principal software architect with deep expertise in Python, FastAPI, Oracle Autonomous Database 23ai (HNSW vector search, Oracle Text CTX indexing), HuggingFace CLIP embeddings, and production API design. Your job is to produce an exhaustive engineering specification for the Broll Searcher application — a B-roll video search tool backed by SmugMug, Claude Vision, CLIP, and Oracle ADB.

This spec will be used by a coder agent to implement fixes and new features. It must be precise enough that an A+ engineer could implement from it without referring to the BUILD_GUIDE.

---

## PHASE 1 — READ EVERYTHING FIRST

Read every file below before writing a single line of spec. Do not skip any.

**Python source files** (in /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/):
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
- requirements.txt

**Reference documents:**
- BUILD_GUIDE.md (full file — all 10 sections + architecture review)
- .collab/test-analysis-2026-06-18.md (the test analysis — all bugs and risks must be addressed in the spec)

Read the test analysis carefully. Every [BUG] and [RISK] finding must be reflected in this spec either as a fixed contract or as an explicit design decision.

---

## PHASE 2 — WRITE THE SPEC

The spec has the following required sections. Write them all. Do not summarize — be exhaustive.

---

### Section 1: Architecture and Data Flow

Write an ASCII diagram showing:
- All modules and their relationships (arrows for function calls / data passed)
- The two runtime phases: STARTUP and REQUEST
- The ingestion pipeline step-by-step with the data types flowing between steps
- The Oracle schema tables and indexes involved in each operation

Then write 2-3 paragraphs of prose explaining the key architectural decisions:
- Why SQLcl subprocess instead of python-oracledb
- Why CLIP visual embedding on media_items (not a separate table) as the primary search vector
- Why Oracle Text CTX instead of CLIP text embedding at query time
- Why one worker, one process, no async DB access

---

### Section 2: Environment and Configuration Contract

For each environment variable the app depends on, write:
- Variable name
- Which module reads it
- When it's read (import time / startup / per-request)
- Required vs optional, and the default if optional
- Validation that must happen (format check, non-empty check, etc.)
- What breaks if it's missing or wrong (specific error, silent failure, etc.)

Cover ALL variables: ORACLE_DSN, ORACLE_USER, ORACLE_PASSWORD, ORACLE_WALLET_DIR, SQLCL_BIN, SMUGMUG_API_KEY, SMUGMUG_API_SECRET, SMUGMUG_ACCESS_TOKEN, SMUGMUG_ACCESS_TOKEN_SECRET, SMUGMUG_GALLERY_KEYS, APP_TIMEZONE, ANTHROPIC_API_KEY, CLAUDE_MODEL (new — should be added).

At the end of this section, write the required .env file template with every variable, a comment on each line, and correct defaults.

---

### Section 3: Module Contracts

For EACH Python file, write:

**Module header:**
- Single-sentence purpose
- What it owns (data, connections, state)
- What it must NOT do (cross-module boundaries, e.g. db.py must not import from ingestion.py)
- Dependencies (what it imports and why)

**For EACH function in the module:**

```
### function_name(param: Type, ...) -> ReturnType

**Purpose:** One sentence.

**Preconditions:**
- List every assumption that must be true when this function is called
- Include env vars that must be set, objects that must be initialized, etc.

**Postconditions:**
- What is guaranteed to be true after a successful return
- What side effects occurred (DB rows inserted, files written, etc.)

**Parameters:**
- param_name (Type): what it is, valid range, edge values that must be handled

**Returns:**
- Exact type and shape, including what an empty result looks like vs None vs raises

**Raises:**
- ExceptionType: exactly when, what message format to use
- List every exception that can propagate from this function (including from callees)

**Edge cases:**
- Enumerate every non-obvious input or state that must be handled explicitly
- For each: what happens, and whether the spec requires it to raise, skip, or return a sentinel

**Performance budget:**
- Expected wall-clock time for the normal case
- What the maximum acceptable time is before something is wrong

**Security notes:**
- If the function handles user input, document the exact escaping strategy
- If it calls external services, document what can leak in error messages
```

Write this level of detail for every function in: db.py, smugmug_client.py, embedder.py, video_utils.py, video_describer.py, ingestion.py, search.py, scheduler.py, main.py, routes.py.

Do not abbreviate. If a module has 8 functions, write all 8.

---

### Section 4: Oracle Database Contract

Write the authoritative spec for all Oracle interactions.

**Schema DDL** — write the exact CREATE TABLE and CREATE INDEX statements that should be used, with inline comments on every column explaining its purpose, constraints, and edge values. Include the sequence for sync_log ID retrieval that fixes the sync_id race condition.

**SQL patterns** — for each query type used by the app, write:
- The exact SQL template (with parameter placeholders named clearly)
- Which index it uses and how to verify (EXPLAIN PLAN output expected)
- What the result shape is (columns returned, their types, how SQLcl serializes them)
- What an empty result looks like vs an Oracle error
- Any Oracle-specific gotchas for this query type

Cover: INSERT with RETURNING, visual_search HNSW FETCH APPROXIMATE, text_search CONTAINS, sync_log insert+retrieve, keyframe_vectors insert, USER_INDEXES / ALL_INDEXES health check.

**VECTOR column serialization** — document exactly how Oracle 23ai serializes a VECTOR(768, FLOAT32) column when returned via SQLcl JSON format. Is it a JSON array `[0.1, ...]`? A string? A dict? Write the correct deserializer for `find_more_like_this` in routes.py.

**Oracle Text lifecycle** — document the exact sequence for:
1. Initial bulk load (NOPOPULATE → ingest → SYNC_INDEX → rebuild with ON COMMIT)
2. Nightly incremental (ON COMMIT fires automatically per row commit)
3. Manual re-sync if needed (CTX_DDL.SYNC_INDEX)
4. How to verify CTX index health

**Error taxonomy** — list every ORA- error code the app can encounter, what caused it, and whether the app should retry, skip the item, or abort:
- ORA-00001: unique constraint violation
- ORA-01861: literal does not match format string
- ORA-29902: Oracle Text operator error
- ORA-04031: out of shared memory (HNSW index growth)
- Any others relevant to this app

---

### Section 5: Inter-Module Interface Contracts

For each module boundary (A calls B), write:
- What A passes to B (exact types)
- What A expects B to return or raise
- What B is NOT allowed to do (e.g., B must not close a connection A needs)
- What A must do if B raises (retry, skip, abort, log and continue)

Cover all edges:
- main.py → embedder.py (CLIP load, embed_image)
- main.py → smugmug_client.py (init, get_target_albums)
- main.py → ingestion.py (run_full_sync called as background task)
- ingestion.py → db.py (run_sql, run_dml, sql_str, vec_literal)
- ingestion.py → video_utils.py (extract_keyframes)
- ingestion.py → video_describer.py (describe_video_keyframes)
- ingestion.py → embedder.py (embed_image)
- ingestion.py → smugmug_client.py (get_target_albums, get_album_images, get_image_urls)
- routes.py → search.py (visual_search, text_search)
- routes.py → embedder.py (embed_image, embed_image_from_url)
- routes.py → db.py (run_sql for find_more_like_this and sync_status)
- scheduler.py → ingestion.py (run_full_sync on cron)

---

### Section 6: Error Handling Strategy

Write the definitive error handling policy for the application. This is not per-function — it is the overall philosophy that all modules must follow.

Cover:
1. **Error taxonomy**: infrastructure errors (DB down, SQLcl not found) vs data errors (bad date format, empty video) vs external service errors (SmugMug 4xx, Anthropic rate limit)
2. **Per-item fault isolation**: what the ingestion pipeline must do when one video fails (log and continue; never abort the batch for a single item failure)
3. **Startup fatal errors**: which errors must crash the app at startup (missing required env var, CLIP model load failure, scheduler timezone error) vs which can be deferred
4. **Request-time errors**: what HTTP status codes and error body shapes the API must return for each error type
5. **Silent failure policy**: enumerate the cases where the current code silently succeeds with wrong data (ORA- in stdout, empty description, missing embedding) and the spec requirement to make these loud
6. **Logging strategy**: what must be logged (level, format, what fields) for each error type so that someone reading `journalctl -u broll-searcher` can diagnose a failed ingestion without a debugger

---

### Section 7: Security Threat Model

Write a threat model specific to this app. For each threat:
- Threat: what an attacker or misconfiguration could do
- Attack surface: which endpoint or code path
- Current status: protected / unprotected / partially protected
- Required mitigation: exact code change needed

Cover:
1. SQL injection via text search query (Oracle CTX operators, single quotes)
2. SQL injection via album_key filter parameter
3. Arbitrary file write via /search/image (malformed image, path traversal)
4. Secret leakage in error messages (password in subprocess args, API key in stack trace)
5. Unauthenticated /ingest/sync triggering expensive operations
6. SSRF via /search/url (user-supplied URL fetched by the server)
7. Large file upload DoS via /search/image
8. Concurrent sync DoS (flooding /ingest/sync)

---

### Section 8: Performance Budget

Write the expected timing for each operation and the maximum acceptable latency:

| Operation | Expected (normal) | Max acceptable | Bottleneck | Mitigation if exceeded |
|---|---|---|---|---|
| CLIP model load at startup | 10-30s | 60s | Disk I/O, first download | Pre-cache model weights |
| Single video keyframe extract | 30-120s | 300s | Download + FFmpeg | Configurable interval_sec |
| Claude Vision description | 2-5s | 30s | Anthropic API latency | max_retries=3, timeout |
| CLIP embed one frame | 0.5-2s CPU | 10s | CPU inference | Batch frames (see note) |
| CLIP embed all frames (avg) | 5-20s | 60s | CPU inference | Already sequential, fine |
| Oracle INSERT (one row) | 0.5-1s | 5s | SQLcl subprocess overhead | Accept; can't reduce |
| Per-video ingestion total | 60-180s | 300s | Download + CLIP | Monitor; skip stuck items |
| Text search query | 0.2-0.5s | 2s | Oracle CTX scan | CTX index must be synced |
| Visual search query | 0.3-1s | 3s | HNSW + SQLcl overhead | HNSW TARGET ACCURACY 95 |
| /health endpoint | 0.5s | 2s | SQLcl subprocess | Accept |

Add a note on full-library ingestion time: for N videos at 120s each, total wall-clock time is N*2 minutes. For 100 videos that is ~3.3 hours. Nightly incremental syncs will be much faster (only new/changed videos).

---

### Section 9: Startup Sequence and Lifespan Contract

Write the exact sequence that must happen during FastAPI lifespan startup, with the requirement for each step:

1. load_dotenv() — must run before any os.environ reads
2. Validate required env vars — fail fast with clear error if any are missing (list which ones are required)
3. CLIPEmbedder() — blocking; must complete before app accepts requests
4. Validate APP_TIMEZONE — must validate before creating scheduler
5. SmugMugClient init — non-blocking; no network call at init time
6. IngestionPipeline init — non-blocking
7. start_scheduler() — starts background thread; must not block
8. app.state assignments — embedder and pipeline stored for route access
9. FastAPI starts accepting requests

For each step, write: what happens if it fails, and whether that failure should crash the app or degrade gracefully.

---

### Section 10: Changes Required from Test Analysis

This section translates every [BUG] and [RISK] finding from the test analysis into a concrete spec requirement. For each finding:

**Finding:** [paste the original severity + title]
**Root cause:** One sentence.
**Spec requirement:** The exact code change required, written as a contract ("Function X MUST do Y when Z").
**Verification:** How to confirm the fix worked (unit test, manual test, SQL query, etc.).

Cover all 6 BUGs and all findings marked as RISK. Do not cover WARNs unless they affect correctness.

---

## PHASE 3 — WRITE THE FILE

Write the complete spec to:
/Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/spec-2026-06-18.md

This will be a long document. Do not abbreviate. Do not skip sections. Write every function signature, every contract, every edge case. The goal is a document an A+ engineer can implement from without ambiguity.

After writing, confirm the file path and byte count.
```

---

### STEP 2 — Report to user

After the agent completes:

```
Broll Searcher engineering spec complete.

Spec: /Users/kmalcolm/claude/iamkaymalcolm/apps/broll-searcher/.collab/spec-YYYY-MM-DD.md
Size: [byte count]

Sections written:
1. Architecture and Data Flow
2. Environment and Configuration Contract
3. Module Contracts ([N] functions specified)
4. Oracle Database Contract
5. Inter-Module Interface Contracts
6. Error Handling Strategy
7. Security Threat Model
8. Performance Budget
9. Startup Sequence
10. Changes Required from Test Analysis ([N] findings addressed)

Run /broll-code to apply the findings and build to spec.
```
