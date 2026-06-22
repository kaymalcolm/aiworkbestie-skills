# Skill Update Plan: content-kit-brief

Derived from the 1046 brief regeneration session (2026-06-15). Four concrete problems were exposed during execution. All changes are to `SKILL.md`.

---

## Change 1 — B-roll alternating pattern (Rule 3)

**Problem:** The skill says "B-roll directions are specific" but gives no structural rule. The 1046 brief had 4 consecutive screen captures before it was flagged and manually corrected.

**Change:** Add to Rule 3 in the Rules section:

> For FORMAT 1 posts with more than 3 shots, default to an alternating Lifestyle / Screen Capture pattern. Never run more than 2 screen captures back-to-back. If the draft's shot list violates this, rewrite it before including it in the brief. Document the final pattern in the sourcing notes line (e.g., "Pattern: Lifestyle / SC / Lifestyle / SC / Lifestyle / Lifestyle").

**Also add:** A new Rule 8:

> The B-roll checklist item must be specific. Do not write "B-roll clips sourced from library (or new shots captured)." Write out which shot numbers are library pulls and which require new recording, derived directly from the shot list. Example: "B-roll: shots 1, 3, 5, 6 from library; shot 2 = screen capture of long conversation scroll; shot 4 = screen capture of PDF-to-markdown conversion."

---

## Change 2 — DB registration: replace Python scripts with MCP SQLcl

**Problem:** Steps 3a and 4a use Python `oracledb` which requires `ORACLE_PASSWORD` as a shell env var. This var is not available in the Bash tool's environment, so both steps silently fail.

**Change:** Replace Steps 3a and 4a entirely with MCP SQLcl tool calls.

Connection name is `26ai`. Auto-commit is on, so no explicit COMMIT needed.

**New Step 3a — connect and insert (replaces the Python block):**

```
1. Call mcp__sqlcl__connect with connection_name: "26ai"
2. Call mcp__sqlcl__sql_run:
   SELECT id FROM posts WHERE post_number = '[POST_NUMBER]'
   → capture as POST_ID

3. Call mcp__sqlcl__sql_run:
   INSERT INTO assets (type, pipeline, short_name, description, status,
                       created_date, updated_date, post_id, file_path)
   VALUES ('brief', 'content-kit', '[SHORT_NAME]-brief',
           'Production brief for post [POST_NUMBER]', 'draft',
           DATE '[TODAY]', DATE '[TODAY]', [POST_ID],
           '/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[TODAY].md')

4. Call mcp__sqlcl__sql_run:
   SELECT id FROM assets
   WHERE short_name = '[SHORT_NAME]-brief' AND post_id = [POST_ID]
   ORDER BY id DESC FETCH FIRST 1 ROW ONLY
   → capture as BRIEF_ID
```

**Remove Step 4a entirely** — `file_path` is now included in the initial INSERT, so no UPDATE step is needed.

---

## Change 3 — Registry refresh: remove or mark optional

**Problem:** Step 4b runs `manage-assets.py export-md` which also fails with the same missing env var. The skill's own note already says "No separate queue update is needed — the queue view auto-detects brief presence via JOIN on post_id."

**Change:** Remove Step 4b. The skill's queue auto-detection covers it.

---

## Change 4 — Drive upload: replace Python subprocess with direct rclone

**Problem:** Step 5 wraps `rclone` in a Python subprocess. Unnecessary complexity. Direct Bash call works and is simpler.

**Change:** Replace the Python block in Step 5 with:

```bash
rclone copy "[BRIEF_FILE_PATH]" "gdrive:AI LinkedIn 2026/[POST_FOLDER]" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"
```

---

## Change 5 — Draft file detection pattern (Step 0)

**Problem:** Step 0 looks for `[POST_NUMBER]-*-draft-*.md` but post files are named like `1046-tokens-and-cost-instagram-2026-05-28.md` with no "draft" in the name. The auto-detect logic will find nothing.

**Change:** Update Step 0 to look for the instagram file as the primary source:

> Find the primary draft file by matching `[POST_NUMBER]-*-instagram-*.md` inside the post folder. If that doesn't exist, fall back to any `[POST_NUMBER]-*.md` that is not a brief, script, or platform-specific file (twitter, threads, tiktok, youtube).

---

## File summary

All 5 changes are to `/Users/kmalcolm/.claude/skills/content-kit-brief/SKILL.md`. No other files need updating.

**Estimated edit scope:**
- Step 0: ~3 lines changed
- Step 3a: entire Python block replaced (15 lines → 8 lines of MCP calls)
- Step 4a: deleted
- Step 4b: deleted
- Step 5: Python block replaced with 3-line rclone call
- Rules section: Rule 3 extended, Rule 8 added
