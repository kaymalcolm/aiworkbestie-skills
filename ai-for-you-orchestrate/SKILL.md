# AI For You — Full Pipeline Orchestrator

Run the complete AI For You content pipeline end-to-end, wiring all phases together with correct dependency ordering and Phase 4 parallelism. Phases 1-3 run sequentially with two pause points for review. Phase 4 (infographic + story) spawns as parallel background agents.

## When This Skill Activates

**Explicit:**
- `/ai-for-you-orchestrate "[topic]"` — start from Phase 1 (full pipeline)
- `/ai-for-you-orchestrate [research file path]` — start from Phase 2 (newsletter onward)
- `/ai-for-you-orchestrate [newsletter file path]` — start from Phase 3 (social content onward)

**Intent detection:** Recognize requests like:
- "Run the full pipeline on [topic]"
- "Orchestrate the full content run for post [number]"
- "Run everything from the research file"
- "Start the pipeline from the newsletter file"

---

## Pipeline Map

```
Phase 1:  /ai-for-you-research   → research file
          ↓ PAUSE 1 — reel + hooks review
Phase 2:  /ai-for-you-newsletter → newsletter file   [auto-advance]
Phase 3:  /ai-for-you            → social content package
          ↓ PAUSE 2 — B-roll direction review (inside Phase 3)
Phase 4:  ┌─ /ai-for-you-infographic  [parallel agents]
          └─ /ai-for-you-story
          ↓ [wait for both agents to complete]
          /ai-for-you-brief      → production brief (auto-generated)
          ↓ PAUSE 3 — infographic review before Substack publish
Phase 5:  /ai-for-you-substack-publish → brief updated with Substack URL
          /ai-for-you-manychat
```

---

## Autonomy Rules

- Run each phase fully before pausing. Do not interrupt a phase mid-execution.
- At pause points: display the output clearly, then stop and wait. Do not advance until the user types "continue" (or any affirmative).
- After a pause, resume exactly where the pipeline left off — do not re-run completed phases.
- Phase 4 agents run in parallel. Do not wait for one before spawning the other.

---

## Workflow

### STEP O-0 — Determine starting phase

Inspect the input:

| Input type | Starting phase |
|---|---|
| Plain topic string (e.g., "AI prompts for meetings") | Phase 1 |
| Path to a research file (`*-research-*.md`) | Phase 2 |
| Path to a newsletter file (`*-newsletter-*.md`) | Phase 3 |
| Post number only (e.g., `1043`) | Locate the newsletter file first; if found → Phase 3. If only research file found → Phase 2. |

Announce the starting phase in one line before proceeding: "Starting pipeline at Phase [N] — [reason]."

---

### STEP O-1 — Phase 1: Research (skip if starting at Phase 2 or 3)

Invoke the `/ai-for-you-research` skill with the provided topic. Run it to completion. The skill saves the research file and reports back the file path, proposed slug, keyword candidate, B-roll direction, and hook options.

Capture from the output:
- `RESEARCH_FILE_PATH`
- `PROPOSED_POST_NUMBER`
- `SLUG`
- `CANDIDATE_KEYWORD`

---

### PAUSE 1 — Review hooks and reel before newsletter

After Phase 1 completes (or if starting at Phase 2, read the research file to extract this content), display:

```
═══════════════════════════════════════════════
PAUSE 1 — REVIEW BEFORE PHASE 2 (NEWSLETTER)
═══════════════════════════════════════════════

Post: [POST_NUMBER] | Slug: [SLUG] | Keyword candidate: [KEYWORD]

── HOOK OPTIONS ──────────────────────────────
[Hook Option 1]

[Hook Option 2]

[Hook Option 3]

── B-ROLL DIRECTION ──────────────────────────
On-screen text hook: [verbatim]

[Clip-by-clip B-roll direction and text overlay script verbatim]

End card: [verbatim]

═══════════════════════════════════════════════
Review the hooks and B-roll direction above. Edit the research file if you want changes.
Type **continue** to generate the newsletter (Phase 2).
```

Wait. Do not proceed to Phase 2 until the user types "continue" or an equivalent affirmative.

---

### STEP O-2 — Phase 2: Newsletter (skip if starting at Phase 3)

Invoke the `/ai-for-you-newsletter` skill with the research file path. Run it to completion. The skill registers the keyword, creates the post record, generates the newsletter, and saves the newsletter file.

Capture from the output:
- `NEWSLETTER_FILE_PATH`
- `POST_NUMBER` (confirmed)
- `SLUG` (confirmed)
- `COMMENT_KEYWORD` (registered)

Report in one line: "Phase 2 complete — newsletter saved at [path]. Advancing to Phase 3."

---

### STEP O-3 — Phase 3: Social Content

Invoke the `/ai-for-you` skill with the newsletter file path. The skill handles:
- Carrying forward the B-roll direction and on-screen text hook from the research file
- Displaying them for review (**this is PAUSE 2** — built into Phase 3's newsletter file mode)
- Generating all social content (carousel, captions, YouTube, Threads, Twitter, LinkedIn caption, infographic briefs)
- Running the brand grader on all content
- Saving all platform files
- Registering assets in the DB

Wait for Phase 3 to complete fully before proceeding to Phase 4.

Capture from the Phase 3 output:
- `POST_FOLDER` — the post folder path (`/posts/[POST_NUMBER]-[SLUG]/`)
- `POST_NUMBER` (confirmed)

---

### STEP O-4 — Phase 4: Parallel Visual Assets

After Phase 3 is confirmed complete, spawn two background agents simultaneously using the Agent tool with `run_in_background: true`.

**Agent A — Infographic:**
```
Prompt: "Read and execute the skill at /Users/kmalcolm/.claude/skills/ai-for-you-infographic/SKILL.md.
Generate ALL THREE infographics (cover + mid + download) for post number [POST_NUMBER].
The post folder is [POST_FOLDER].
Run the full skill workflow end-to-end. Register completed infographics in the asset DB.
Report back: which infographics were generated and saved, file paths, and any errors."
```
Use `subagent_type: "general-purpose"`.

**Agent B — Stories:**
```
Prompt: "Read and execute the skill at /Users/kmalcolm/.claude/skills/ai-for-you-story/SKILL.md.
Generate all 3 Instagram Story frames for post number [POST_NUMBER].
The post folder is [POST_FOLDER].
Run the full skill workflow end-to-end. Register completed stories in the asset DB.
Report back: which stories were generated and saved, file paths, and any errors."
```
Use `subagent_type: "general-purpose"`.

Tell the user:
```
Phase 4 running in parallel —
  [Agent A] Generating 3 infographics (cover + mid + download)
  [Agent B] Generating 3 Instagram Stories

You'll be notified when both complete. You can work in the session while they run.
```

Wait for both agents to report back before proceeding.

---

### STEP O-5 — Phase 4 completion report

When both Phase 4 agents complete, consolidate their reports and tell the user:

```
Phase 4 complete.

Infographics:
  [list files generated or errors]

Stories:
  [list files generated or errors]
```

If either agent reported an error, note it clearly and suggest running that skill manually.

---

### STEP O-5.5 — Auto-generate production brief

Immediately after Phase 4 completes (both agents done), invoke `/ai-for-you-brief [POST_NUMBER]`. Run it to completion. The skill registers the brief in the DB, saves the file, and uploads to Drive.

Tell the user one line: "Brief generated: [BRIEF_FILE_PATH]"

---

### PAUSE 3 — Infographic review before Substack publish

After the brief is generated, display all infographic and story images inline for review, then pause:

```
═══════════════════════════════════════════════
PAUSE 3 — REVIEW INFOGRAPHICS BEFORE PUBLISHING
═══════════════════════════════════════════════

Review the infographics and stories above before Substack publishes.

  Cover:    [COVER_FILE_PATH]
  Mid:      [MID_FILE_PATH]
  Download: [DOWNLOAD_FILE_PATH]
  Stories:  [STORY_01_PATH] | [STORY_02_PATH] | [STORY_03_PATH]

If anything needs to be regenerated, run the individual skill now.
Type **continue** when ready to move to Phase 5.
═══════════════════════════════════════════════
```

Wait. Do not advance to Phase 5 until the user types "continue" or an equivalent affirmative.

---

### STEP O-6 — Phase 5 offer

After the user approves the infographics:

```
Pipeline through Phase 4 is complete for post [POST_NUMBER].

Ready for Phase 5:
  → Publish to Substack:  /ai-for-you-substack-publish [NEWSLETTER_FILE_PATH]
  → Set up ManyChat:      /ai-for-you-manychat [POST_NUMBER]

Run them in order — ManyChat config depends on the published Substack URL.

After Substack publishes, run /ai-for-you-brief [POST_NUMBER] again to update
the brief with the live Substack URL.
```

Do not run Phase 5 automatically. Stop here.

---

## Error Handling

**Phase fails mid-run:** Report which phase failed and the error. Do not attempt to re-run the phase automatically. Tell the user to fix the issue and re-invoke the orchestrator with the appropriate starting file (research or newsletter) to resume from the correct phase.

**Agent A or B fails:** Note the failure in the Phase 4 report. The failed asset can be generated manually with its skill. Do not block Phase 5 on a Phase 4 failure.

**Pause not acknowledged after a long wait:** Do not auto-advance. The pipeline stays paused until the user explicitly continues.

---

## State Tracking

At each phase boundary, echo the confirmed values so the user always knows where the pipeline stands:

```
✓ Phase 1 complete — research: [RESEARCH_FILE_PATH]
✓ Phase 2 complete — newsletter: [NEWSLETTER_FILE_PATH] | keyword: [KEYWORD]
✓ Phase 3 complete — post folder: [POST_FOLDER]
⟳ Phase 4 in progress — infographic agent + story agent running
✓ Phase 4 complete
✓ Brief generated — [BRIEF_FILE_PATH]
⏸ PAUSE 3 — awaiting infographic review
✓ Phase 5 ready
```

Use `✓` for complete, `⟳` for in-progress, `✗` for failed.
