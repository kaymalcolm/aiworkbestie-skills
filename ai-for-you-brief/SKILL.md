# AI For You  -  Production Brief Skill

Generate a clean, actionable 1-page handoff document for the social media manager from a completed AI For You draft.

## When This Skill Activates

**Explicit:** User types `/ai-for-you-brief` or `/ai-for-you-brief [post number or file path]`

**Intent detection:** Recognize requests like:
- "Create a brief for post 003"
- "Generate the social media manager handoff for the latest post"
- "Make a production brief for [post]"

---

## Autonomy Rules

Run the full workflow with no confirmation. Auto-detect the target file if no argument is given (use the most recently modified `ai-for-you-0*.md` in content-drafts). Save the brief and report the file path.

---

## Workflow

### STEP 0  -  Identify the target draft

- If a post number or file path is given, find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/` and locate the draft file inside it by matching `[POST_NUMBER]-*-instagram-*.md` first. If that doesn't exist, fall back to any `[POST_NUMBER]-*.md` that is not a brief, script, or platform-specific file (twitter, threads, tiktok, youtube). Note the full post folder path as `POST_FOLDER` (e.g. `1031-where-to-start-with-ai`).
- If no argument, find the most recently modified draft across all post folders.
- Read the full draft file.
- Also read `/Users/kmalcolm/claude/iamkaymalcolm/strategy/general-strategy.md` for the b-roll shot bank and platform rules.

---

### STEP 1  -  Extract everything needed for execution

From the draft file, pull:

- Post number and topic
- Format (FORMAT 1 value post / FORMAT 2 take post)
- On-screen text hook (verbatim)
- B-roll direction (verbatim  -  all clips and text overlays)
- End card direction (verbatim)
- All carousel slide text (verbatim)
- All captions per platform (verbatim, ready to paste), including share_trigger line
- Hashtags per platform
- Comment keyword and named-promise CTA (e.g., "Comment STACK and I'll DM you the exact 4-tool list")
- Pinned comment text (if incomplete list close format)
- Posting order
- Infographic status: check whether infographic files exist in `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/` (matching `[POST_NUMBER]-*-infographic-mid-*.png` and `[POST_NUMBER]-*-infographic-*.png`). Note which are done and which still need to be generated.

---

### STEP 2  -  Generate the production brief

Write the brief in this exact structure. Keep it tight. This is a working doc, not a strategy doc  -  every line should be something the social media manager can act on directly.

---

```
# AI For You  -  Production Brief
**Topic:** [topic]
**Format:** [FORMAT 1  -  Value Post / FORMAT 2  -  Take Post]
**Draft file:** [file path]
**Brief generated:** [date]

---

## 🎬 REEL DIRECTION

**Format:** [FORMAT 1  -  Value Post (multi-clip B-roll) / FORMAT 2  -  Take Post (single lifestyle clip)]

**On-screen text hook (first clip, first 2 sec):**
"[exact hook text — verbatim from draft]"

**B-roll shot list:**

**Shot 1 | 0-Xs**
Footage: [specific clip description]
Text: [exact text on screen]
Sub: [exact sub-text]
Notes: [pull from library / new shot needed]

[continue for all shots in the same block format]

**End card direction:**
[exact end card text and layout — verbatim from draft]

**B-roll sourcing notes:** [which shots Kay likely has in her existing lifestyle library, any new shots needed]

---

## 📱 CAROUSEL SPECS

**Canva dimensions:** 1080 x 1080px (square) or 1080 x 1350px (portrait  -  recommended for feed)
**Font:** Bold condensed sans-serif for headlines (Anton or similar), regular weight for body
**Background:** Dark navy or near-black (#0D1117)
**Text color:** White primary, gold/amber accent for series badge
**Series badge:** "AI FOR YOU | AI Work Bestie"  -  top-left corner, gold/amber

**Slides:**

**Slide 1 — HOOK (biggest text)**
Headline: [exact text]
Body: [exact text]

**Slide 2**
Headline: [exact text]
Body: [exact text]

[continue for all slides in the same block format — add a label like "— CTA" or "— HOOK" only when the slide has a functional role worth flagging]

[If reel only / no carousel: "No carousel for this post."]

---

## 📋 CAPTIONS  -  READY TO PASTE

### Instagram
[full caption verbatim  -  paste directly]

**Hashtags:**
[hashtags]

**Comment keyword:** [keyword]  -  set up ManyChat trigger before posting

---

### TikTok
[full TikTok caption verbatim]

**Hashtags:**
[hashtags]

---

### Twitter / X
[full Twitter post verbatim]

---

### Threads
**Post 1:**
[text]

**Post 2:**
[text]

**Post 3 (if applicable):**
[text]

---

## 📌 COMMENT SETUP

[IF incomplete list close / pinned comment:]
**Pin this comment IMMEDIATELY after the reel goes live  -  within 5 minutes:**

"[exact pinned comment text]"

[IF comment keyword CTA:]
**ManyChat keyword:** [KEYWORD]
**Auto-DM should send:** [link to newsletter / prompts / breakdown]
**Set up before posting.**

[IF no pinned comment needed:]
"No pinned comment for this post. Respond to first 10 comments within the first hour."

---

## 🗓️ POSTING SCHEDULE

**Day 1**
- [Platform] - [Action]

**Day 2**
- [Platform] - [Action]

[continue for all days]

**First comment pinned:** [yes/no  -  and when]

---

## ✅ PRE-POST CHECKLIST

- [ ] ManyChat keyword set up and tested (primary post keyword)
- [ ] B-roll clips sourced from library (or new shots captured)
- [ ] Video edited with text overlays and end card
- [ ] Carousel designed in Canva and exported (FORMAT 1 posts)
- [ ] All captions copied into scheduling tool or native app
- [ ] Bio link is active (iamkaymalcolm.substack.com)
- [ ] Pinned comment text saved and ready to paste immediately after posting
- [ ] Mid-article infographic generated and embedded in newsletter (posts/[POST_FOLDER]/infographic/[POST_NUMBER]-...-infographic-mid-[DATE].png)
- [ ] Download/share infographic generated and embedded in newsletter (posts/[POST_FOLDER]/infographic/[POST_NUMBER]-...-infographic-[DATE].png)
- [ ] Instagram Stories generated and uploaded to Drive (posts/[POST_FOLDER]/stories/)
- [ ] Substack Note ready to post to Notes feed (separate from the newsletter issue)
- [ ] Newsletter title and subtitle set in Substack before publishing
```

---

### STEP 3  -  Register in DB and save the brief

Derive `SHORT_NAME` from the post folder slug (e.g. folder `1031-where-to-start-with-ai` → `where-to-start-with-ai`). Use today's date as `DATE` (YYYY-MM-DD format).

**3a — Connect and insert via MCP SQLcl:**

```
1. Call mcp__sqlcl__connect with connection_name: "26ai"

2. Call mcp__sqlcl__sql_run:
   SELECT id FROM posts WHERE post_number = '[POST_NUMBER]'
   → capture result as POST_ID

3. Call mcp__sqlcl__sql_run:
   INSERT INTO assets (type, pipeline, short_name, description, status,
                       created_date, updated_date, post_id, file_path)
   VALUES ('brief', 'ai-for-you', '[SHORT_NAME]-brief',
           'Production brief for post [POST_NUMBER]', 'draft',
           DATE '[TODAY]', DATE '[TODAY]', [POST_ID],
           '/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[TODAY].md')

4. Call mcp__sqlcl__sql_run:
   SELECT id FROM assets
   WHERE short_name = '[SHORT_NAME]-brief' AND post_id = [POST_ID]
   ORDER BY id DESC FETCH FIRST 1 ROW ONLY
   → capture result as BRIEF_ID
```

Build the canonical filename:
`[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md`

**3b — Save the brief to:**
`/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md`

---

### STEP 4  -  (No additional tracking steps needed)

`file_path` was included in the INSERT in Step 3a. The queue view auto-detects brief presence via JOIN on `post_id` — no registry refresh needed.

---

### STEP 5  -  Upload brief to Google Drive

Upload the saved brief to the iamkaymalcolm posts folder alongside the other post assets:

```bash
rclone copy "[BRIEF_FILE_PATH]" "gdrive:AI LinkedIn 2026/[POST_FOLDER]" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"
```

---

### STEP 6  -  Report back

Tell the user:
- The brief file path
- How many sections it has
- Whether a pinned comment is needed (and when to post it)

One short paragraph. That's it. They can read the brief.

---

## Rules for Writing the Brief

1. **No em dashes anywhere in the brief.** If any em dash appears in verbatim content pulled from the draft, replace it with a hyphen ( - ) before writing it into the brief. Zero exceptions.
2. **Every caption is verbatim from the draft.** Do not rewrite, shorten, or improve. The draft is approved content. The brief is execution, not editing.
3. **B-roll directions are specific.** Reference the shot bank from `general-strategy.md`. Name the shot type, the mood, what's in frame. Don't say "lifestyle footage"  -  say "Kay walking away from desk, coffee in hand, bag over shoulder  -  living her life, not looking at a screen." For FORMAT 1 posts with more than 3 shots, default to an alternating Lifestyle / Screen Capture pattern. Never run more than 2 screen captures back-to-back. If the draft's shot list violates this, rewrite it before including it in the brief. Document the final pattern in the sourcing notes line (e.g., "Pattern: Lifestyle / SC / Lifestyle / SC / Lifestyle / Lifestyle").
4. **Canva specs are always included for carousel posts (FORMAT 1).** Exact dimensions, font guidance, color values. No guessing.
5. **ManyChat setup is flagged every time** there's a comment keyword CTA  -  it must be live before the post goes up, not after.
6. **The pinned comment timing is non-negotiable.** If the post uses an incomplete list close, the pinned comment must go up within 5 minutes of the post going live. Flag this explicitly.
7. **No strategy context in the brief.** The social media manager does not need to know why decisions were made. She needs to know what to do. Keep strategy out of this document entirely.
8. **The B-roll checklist item must be specific.** Do not write "B-roll clips sourced from library (or new shots captured)." Write out which shot numbers are library pulls and which require new recording, derived directly from the shot list. Example: "B-roll: shots 1, 3, 5, 6 from library; shot 2 = screen capture of long conversation scroll; shot 4 = screen capture of PDF-to-markdown conversion."
