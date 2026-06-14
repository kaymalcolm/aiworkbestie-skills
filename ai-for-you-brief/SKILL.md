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

- If a post number or file path is given, find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/` and locate the draft file inside it (matching `[POST_NUMBER]-*-draft-*.md`). Note the full post folder path as `POST_FOLDER` (e.g. `1031-where-to-start-with-ai`).
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

**3a — Insert the asset row first to get the auto-incremented ID:**

```python
import oracledb, datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name  = "[SHORT_NAME]"   # derived from post folder slug
post_number = "[POST_NUMBER]"

con = get_connection()
cur = con.cursor()

cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
post_id = post_row[0] if post_row else None

# INSERT brief asset — capture generated ID via RETURNING
new_id_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_id)
    VALUES ('brief','ai-for-you',:1,:2,'draft',:3,:4,:5)
    RETURNING id INTO :6""",
    (short_name + "-brief",
     f"Production brief for post {post_number}",
     today, today, post_id, new_id_var))
brief_id = int(new_id_var.getvalue()[0])

# Link to the parent draft asset
cur.execute("SELECT a.id FROM assets a WHERE a.type='draft' AND a.post_id=:1", (post_id,))
draft_row = cur.fetchone()
if draft_row:
    cur.execute(
        "INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'brief-for')",
        (draft_row[0], brief_id))

con.commit()
con.close()
print(f"BRIEF_ID={brief_id}")
```

Note the ID as `BRIEF_ID`. Build the canonical filename:
`[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md`

**3b — Save the brief to:**
`/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md`

---

### STEP 4  -  Update tracking files

**4a — Update file_path in the DB now that the file is saved:**

```python
import sys, datetime
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
file_path = "/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md"

con = get_connection()
cur = con.cursor()
cur.execute(
    "UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3",
    (file_path, today, brief_id))
con.commit()
con.close()
```

**4b — Refresh the registry:**
```
/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

No separate queue update is needed — the queue view auto-detects brief presence via JOIN on `post_id`.

---

### STEP 5  -  Upload brief to Google Drive

Upload the saved brief to the iamkaymalcolm posts folder alongside the other post assets:

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import subprocess
brief_path = "/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md"
post_folder = "[POST_FOLDER]"
subprocess.run(["rclone", "copy", brief_path,
                f"gdrive:AI LinkedIn 2026/{post_folder}",
                "--drive-root-folder-id", "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"], check=True)
print(f"Brief uploaded to Drive: AI LinkedIn 2026/{post_folder}/[POST_NUMBER]-[SHORT_NAME]-brief-[DATE].md")
PYEOF
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
3. **B-roll directions are specific.** Reference the shot bank from `general-strategy.md`. Name the shot type, the mood, what's in frame. Don't say "lifestyle footage"  -  say "Kay walking away from desk, coffee in hand, bag over shoulder  -  living her life, not looking at a screen."
4. **Canva specs are always included for carousel posts (FORMAT 1).** Exact dimensions, font guidance, color values. No guessing.
5. **ManyChat setup is flagged every time** there's a comment keyword CTA  -  it must be live before the post goes up, not after.
6. **The pinned comment timing is non-negotiable.** If the post uses an incomplete list close, the pinned comment must go up within 5 minutes of the post going live. Flag this explicitly.
7. **No strategy context in the brief.** The social media manager does not need to know why decisions were made. She needs to know what to do. Keep strategy out of this document entirely.
