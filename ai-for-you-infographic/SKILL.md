# AI For You  -  Infographic Generator Skill

Generate infographics for an AI For You post using NotebookLM.

Every post has THREE infographics:
- **Cover infographic**  -  landscape (14:10), editorial illustration + newsletter title only, Substack thumbnail
- **Mid-article infographic**  -  square (1:1, 1080x1080px), IMAGE-FORWARD illustrated scene with stat overlay, goes inside the newsletter
- **Download/share infographic**  -  portrait (full layout), all rows, goes at the end of the newsletter

## When This Skill Activates

**Explicit:**
- `/ai-for-you-infographic [post number]`  -  generates ALL THREE (cover + mid + download)
- `/ai-for-you-infographic [post number] cover`  -  generates Substack cover only
- `/ai-for-you-infographic [post number] mid`  -  generates mid-article square only
- `/ai-for-you-infographic [post number] download`  -  generates download/share portrait only
- `/ai-for-you-infographic [post number] threads`  -  generates threads-specific infographic only

**Intent detection:** Recognize requests like:
- "Generate the infographics for post 1043"
- "Make the cover infographic for post 1043"
- "Create all three infographics for the latest AI For You post"
- "Generate just the square infographic for post 1031"
- "Make the threads infographic for post 1043"

---

## Autonomy Rules

Run the full workflow with no confirmation. Auto-detect the most recent draft if no post number is given. Generation takes 5-15 min per infographic — fire all generate commands before waiting on any, then wait and download each. Update tracking when all are done. For threads mode, use the threads platform file as the primary source (not the main draft), use the dedicated threads notebook, generate a single portrait infographic at 1080x1350, and register in the asset DB with type='infographic-threads'.

---

## Cover Infographic Rules

The cover is the Substack thumbnail — the first thing readers see in the feed. These rules are non-negotiable:

**Dimensions:** 1456x1048px (14:10 landscape). NotebookLM always outputs a tall portrait. Post-processing crops the illustration from the bottom of that portrait and overlays the title text using PIL — do not rely on NotebookLM to place the title.

**Visual style — gold standard:**
- Premium editorial vector illustration. NOT photorealistic. NOT flat/minimal. Cinematic, warm, aspirational — like a still from an award-winning animated feature.
- Scene: African American woman with collarbone length, full, voluminous spiral curls (big natural hair energy) and glasses, seated at a sleek modern desk with a laptop and steaming mug.
- Framed by floor-to-ceiling windows with a city skyline at golden hour/dusk glowing behind her.
- Color palette: WARM and REGAL. Deep amber, burnt gold, warm pink, magenta, dusty rose, rich rose-gold, soft purple — the full regal sunset spectrum from golden-hour amber through warm pinks and magentas up to dusty rose and violet. NOT cool purple. NOT flat lavender. NOT dark navy.
- Window light creates a gorgeous backlit glow. Foreground is warm dark neutrals (desk, chair, room shadow). Small plant visible to one side.
- Reference: `/Users/kmalcolm/claude/iamkaymalcolm/posts/1043-switching-to-claude/infographic/1043-1183-switching-to-claude-infographic-cover-2026-05-22.png`

**Text:** The newsletter title is overlaid via PIL post-processing (STEP 6c). Do NOT ask NotebookLM to render the title — the NotebookLM prompt is pure illustration only.

**Post-processing (cover only — see STEP 6c):**
1. Download portrait to `/tmp/cover-raw-[POST_NUMBER].png`
2. Remove NotebookLM logo
3. Find where the illustration begins: scan top-to-bottom in 60px bands; crop 1048px from the first band where mean HSV saturation ≥ 0.50 (illustration is richly colored; text sections are near-grayscale). No backup band — start exactly at the threshold.
4. Center-crop to 1456px wide
5. Add a dark gradient overlay: fully opaque (alpha 255) for first 35px, fades to 0 by y=380 — kills any text bleed from NotebookLM's infographic content
6. Overlay the newsletter title as bold white PIL text at top-left (64px, 48px), 82pt, with a 3px drop shadow
7. Save final to post infographic folder

---

## Workflow

### STEP 0  -  Identify the target draft and mode

- If a post number is given, find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/` and locate the draft file inside it (matching `[POST_NUMBER]-*-newsletter-*.md` or `[POST_NUMBER]-*-draft-*.md`).
- If no argument, use the most recently modified draft across all post folders.
- Note the full post folder path as `POST_FOLDER` (e.g. `1043-switching-to-claude`) — needed for output paths.
- Check for a `cover`, `mid`, `download`, or `threads` argument to determine mode. Default (no argument) = ALL THREE (cover + mid + download).
- Read the full draft file.

---

### STEP 1  -  Extract infographic briefs

**For the cover**, pull from the draft file header:
- Newsletter title (used as the only text on the cover, overlaid via PIL)

**For the mid-article infographic**, find `### MID-ARTICLE INFOGRAPHIC` in the draft and pull:
- The stat, quote, or insight that is the visual focus
- Supporting subtext line(s)
- Visual suggestion for the scene

**For the download/share infographic**, find `### END INFOGRAPHIC` (preferred), `### Download/Share Infographic`, or `## 3g. INFOGRAPHIC BRIEF` and pull:
- Title
- Subtitle
- All row content verbatim (labels, teaser text, what-you-get lines, CTAs)
- Bottom stat
- Whether FULL CONTENT or TEASE

Also note from the file header: post number, topic/slug.

---

### STEP 2  -  Read the visual brand guide

Read the VISUAL BRAND section of `/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md`

Pull the AI For You infographic design system section. This gets passed to NotebookLM as design direction.

---

### STEP 3  -  Get or create per-type notebooks (one set per post, ever)

Each post gets exactly THREE dedicated notebooks — one per infographic type — stored in `.notebooks.json` in the post's infographic folder. Notebooks are never recreated if they already exist for a post.

**Check for existing notebooks first:**

```python
import json
from pathlib import Path

infographic_dir = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic")
infographic_dir.mkdir(exist_ok=True)
notebooks_file = infographic_dir / ".notebooks.json"

if notebooks_file.exists():
    nb = json.loads(notebooks_file.read_text())
    NB_COVER    = nb.get("cover")
    NB_MID      = nb.get("mid")
    NB_DOWNLOAD = nb.get("download")
    NB_THREADS  = nb.get("threads")
    print(f"Reusing notebooks: cover={NB_COVER} mid={NB_MID} download={NB_DOWNLOAD}")
    # Sources already loaded — skip STEP 4
```

**If `.notebooks.json` does not exist**, create the three notebooks and save IDs:

```bash
# Run all three creates in parallel
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli create "AI For You #[POST_NUMBER] - Cover" --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli create "AI For You #[POST_NUMBER] - Mid" --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli create "AI For You #[POST_NUMBER] - Download" --json &
wait
```

Save the three IDs to `.notebooks.json`:

```python
import json
from pathlib import Path

notebooks_file = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/.notebooks.json")
nb = {"cover": "[NB_COVER_ID]", "mid": "[NB_MID_ID]", "download": "[NB_DOWNLOAD_ID]"}
notebooks_file.write_text(json.dumps(nb, indent=2))
print(f"Saved notebook IDs: {nb}")
```

For **threads mode**: add a fourth key `"threads"` to `.notebooks.json` using the same pattern. Create it on first threads run, reuse on all subsequent threads runs for that post.

---

### STEP 4  -  Add sources and wait

**Skip this step entirely if `.notebooks.json` already existed** — sources were loaded on the first run.

If notebooks were just created, add both sources to all three in parallel:

```bash
DRAFT="[draft file path]"
BRAND="/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md"

/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$DRAFT" -n [NB_COVER] --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$BRAND"  -n [NB_COVER] --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$DRAFT" -n [NB_MID] --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$BRAND"  -n [NB_MID] --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$DRAFT" -n [NB_DOWNLOAD] --json &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add "$BRAND"  -n [NB_DOWNLOAD] --json &
wait
```

Wait for all six sources in parallel:

```bash
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_COVER_1]   -n [NB_COVER]    --timeout 120 &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_COVER_2]   -n [NB_COVER]    --timeout 120 &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_MID_1]     -n [NB_MID]      --timeout 120 &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_MID_2]     -n [NB_MID]      --timeout 120 &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_DOWNLOAD_1] -n [NB_DOWNLOAD] --timeout 120 &
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_DOWNLOAD_2] -n [NB_DOWNLOAD] --timeout 120 &
wait
```

If any source returns "not found", re-add it to that notebook and wait again before proceeding.

---

### STEP 5  -  Generate infographic(s)

**Always use Python 3.12:**
`/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli`

Fire ALL generate commands before waiting on any — they run in parallel inside NotebookLM. Each goes to its own dedicated notebook.

---

**STEP 5a  -  Cover (if mode is ALL or cover):**

The cover prompt asks for a pure illustration only — no text. The title is overlaid by PIL in post-processing (STEP 6c).

```
MOVIE POSTER LAYOUT. Pure full-bleed editorial illustration. Absolutely no text, no titles, no badges, no overlays, no series names, no handles — nothing. The illustration is the entire deliverable.

ILLUSTRATION STYLE:
- Premium editorial vector illustration. NOT photorealistic. NOT flat/minimal.
- Cinematic, warm, aspirational — like a still from an award-winning animated feature.
- Same visual energy as a high-end magazine cover.

COLOR PALETTE — WARM AND REGAL:
- Background sky: deep amber, burnt gold, warm pink, magenta, dusty rose, rich rose-gold, soft purple — the full regal sunset spectrum. WARM pinks and roses. NOT cool purple. NOT flat lavender. NOT dark navy.
- City skyline backlit with this warm regal light, glowing in the distance.
- Foreground: dark warm neutrals (desk, chair, room shadow) contrasting with the glowing window light.

SCENE:
- African American woman with collarbone-length, full, voluminous spiral curls and glasses.
- Seated at a sleek modern desk with a laptop and a steaming mug. Relaxed and confident.
- Framed by large floor-to-ceiling windows filled with the warm regal city-at-dusk glow.
- The window light creates a gorgeous backlit effect — warm amber and pink streaming in around her.
- Small plant visible to one side. Visible from approximately waist up, centered in the frame.
- The illustration occupies the full frame. The upper portion of the frame is open sky — no obstructions above her head.

DO NOT INCLUDE: any text, any title, any series badge, any handle, any subtitle, any stat, any CTA, any post number. Pure illustration only.
```

Run against the cover notebook:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation portrait --detail detailed --style professional "[instructions]" -n [NB_COVER] --json
```

Note artifact ID as `ARTIFACT_COVER`.

---

**STEP 5b  -  Mid-article square (if mode is ALL or mid):**

```
INSTAGRAM PHOTO WITH TEXT OVERLAY. This is a lifestyle illustration with two lines of text overlaid at the bottom — nothing more. Think: beautiful Instagram post where someone typed a quote over their photo.

THIS IS A PHOTO, NOT A LAYOUT. No columns, no rows, no headers, no sections, no bullet points, no problem/solution framing, no infographic structure of any kind.

THE ILLUSTRATION (fills 80% of the frame):
- African American woman with collarbone-length, full, voluminous spiral curls and glasses.
- At a clean modern desk with laptop open and coffee nearby. Calm, settled, focused energy.
- Premium editorial illustration — warm ambers, champagne, blush, golden hour tones.
- [VISUAL SUGGESTION FROM BRIEF]
- Her face is fully visible. She is the clear subject of the image.

TEXT OVERLAY (the only text — placed at the bottom of the illustration):
- Series badge top-left corner: AI FOR YOU | AI Work Bestie (small, gold #F4A261, pill shape)
- Main quote/stat, large bold white text centered at bottom: [STAT OR INSIGHT FROM BRIEF]
- One supporting line below in smaller white text: [SUPPORTING LINE FROM BRIEF]
- Handle bottom-right corner, very small: @iamkaymalcolm

THAT IS ALL. No other text. No sections. No rows. No headers. No additional layout elements.
```

Run against the mid notebook:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation portrait --detail detailed --style professional "[instructions]" -n [NB_MID] --json
```

Note artifact ID as `ARTIFACT_MID`.

---

**STEP 5c  -  Download/share portrait (if mode is ALL or download):**

Use explicit section numbering with "do not omit" on every row — this is what ensures all rows appear.

```
TALL PORTRAIT RESOURCE GUIDE INFOGRAPHIC. Must contain all sections listed below. Do not omit any section.

LAYOUT FROM TOP TO BOTTOM — ALL SECTIONS REQUIRED:

SECTION 1 — ILLUSTRATED HEADER (top 30% of image, do not omit):
African American woman with collarbone-length, full, voluminous spiral curls and glasses, at a modern desk with laptop and steaming mug, floor-to-ceiling windows with warm amber/gold/magenta city-at-dusk glow behind her. Premium editorial illustration, warm cinematic palette.
Series badge overlaid top-left: AI FOR YOU | AI Work Bestie (bold caps, gold #F4A261). NO post number.

SECTION 2 — TITLE (below the header, do not omit):
Large bold text, deep plum (#2D1B2E) or near-black (#1A1A1A).
[TITLE FROM BRIEF]

SECTION 3 — SUBTITLE (directly below title, do not omit):
Smaller text, deep plum.
[SUBTITLE FROM BRIEF]

[For each row from the brief, create a numbered section. Example for 3 rows:]

SECTION 4 — ROW 1 (full row, do not omit):
Row label in gold: [LABEL]
Time estimate: [TIME]
Teaser line: [TEASER TEXT]
Result line: [WHAT YOU GET]
Newsletter pointer with envelope icon: [CTA LINE]

SECTION 5 — ROW 2 (full row, do not omit):
Row label in gold: [LABEL]
Time estimate: [TIME]
Teaser line: [TEASER TEXT]
Result line: [WHAT YOU GET]
Newsletter pointer with envelope icon: [CTA LINE]

SECTION 6 — ROW 3 (full row, do not omit):
Row label in gold: [LABEL]
Time estimate: [TIME]
Teaser line: [TEASER TEXT]
Result line: [WHAT YOU GET]
Newsletter pointer with envelope icon: [CTA LINE]

SECTION [N+3] — BOTTOM STAT BAR (must appear at the very bottom, do not omit):
[BOTTOM STAT FROM BRIEF]

DESIGN: Champagne/blush background (#F0E2C8) for text sections. Gold/amber (#F4A261) row labels. Thin rose-gold dividers between rows (30% opacity). NO CTA bar after the stat. NO numbered emoji (1 2 3 in boxes). Emoji allowed: envelope icon for newsletter CTAs, clock icon for time estimates.
If any additional illustrated human figure appears beyond the header, she is an African American woman with collarbone-length, full, voluminous spiral curls and glasses.
```

Run against the download notebook:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation portrait --detail detailed --style professional "[instructions]" -n [NB_DOWNLOAD] --json
```

Note artifact ID as `ARTIFACT_DOWNLOAD`.

---

### STEP 5t  -  Generate threads infographic (threads mode only)

**Only run this step when mode is `threads`.**

Instead of the three standard types, generate a **Threads infographic** at **1080x1350px (4:5 portrait)**.

**Source file:** Find the threads platform file in the post folder matching `[POST_NUMBER]-*-threads-*.md`. Use this as the primary content source — NOT the main draft.

Instructions for the threads infographic:
```
Create a visually stunning, scroll-stopping portrait infographic (1080x1350px, 4:5 aspect ratio) optimized for the Threads feed on mobile. This infographic pairs with a Threads post and should feel like the post and the infographic are a visual duo — same energy, same vibe, same moment.

DESIGN:
- Format: Portrait 4:5, 1080x1350px
- Background: Soft feminine palette — choose one: blush pink (#F7CAD0), warm lavender (#E8D5F5), champagne (#F0E2C8), soft blush-to-champagne gradient, or light gold (#FDF3DC). NO dark backgrounds. NO dark navy. NO black backgrounds.
- Series badge top-left: "AI FOR YOU | AI Work Bestie" in bold caps, gold/amber accent (#F4A261). NO post number in the badge.
- Typography: Strong visual hierarchy. Bold condensed headline (Anton or Druk-style) for the main insight. Clean regular weight body copy. Premium feel — not a template.
- Color accents: Gold/amber (#F4A261) for labels or highlights. Deep plum (#2D1B2E) or near-black (#1A1A1A) for title and body text.
- Feature the single most shareable, screenshot-worthy insight from the Threads post — the thing a corporate woman would screenshot and send to her work group chat.
- Visual should feel like it was designed to live on a phone screen. Scroll-stopping on mobile.
- If any illustrated human figure appears, she is an African American woman with collarbone-length, full, voluminous spiral curls and glasses.
- Attribution: @iamkaymalcolm — bottom corner, small. No CTA text.
- Soft and feminine. Premium. Save-worthy. No clip art. No generic templates.
- NO em dashes anywhere. Replace any em dash with a hyphen ( - ).
- NO call-to-actions of any kind — no "Comment AI", "Drop WORD in the comments", "DM me", etc. Strip any such language entirely. Do not replace with alternative CTAs.

CONTENT (from threads source):
[Pull the most shareable insight, stat, or hook from the threads post — the thing someone would screenshot]
[Supporting detail or framing, 1-2 lines max]

Series badge: AI FOR YOU | AI Work Bestie
Bottom: @iamkaymalcolm
```

Run against the threads notebook:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation portrait --detail detailed --style professional "[instructions]" -n [NB_THREADS] --json
```

Note artifact ID as `ARTIFACT_THREADS`.

---

### STEP 5d  -  Register infographics in asset DB and determine filenames

Before downloading, register the infographic asset(s) in the DB to get their IDs and canonical filenames.

Derive `SHORT_NAME` from the draft topic slug (e.g. topic "Switching to Claude" → `switching-to-claude`). Use today's date as `DATE` (YYYY-MM-DD format).

**For threads mode**, run only the threads registration block:

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name = "[SHORT_NAME]"
post_number = "[POST_NUMBER]"

con = get_connection()
cur = con.cursor()

cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
post_id = post_row[0] if post_row else None

threads_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_id)
    VALUES ('infographic-threads','ai-for-you',:1,:2,
            'draft',:3,:4,:5)
    RETURNING id INTO :new_id""",
    [short_name + "-infographic-threads",
     f"Threads portrait infographic for post {post_number}",
     today, today, post_id, threads_var])
threads_id = int(threads_var.getvalue()[0])
cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'threads','pending')", (threads_id,))

cur.execute("SELECT a.id FROM assets a WHERE a.type='draft' AND a.post_id=:1", (post_id,))
draft_row = cur.fetchone()
if draft_row:
    cur.execute("INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'infographic-for')", (draft_row[0], threads_id))

con.commit()
con.close()
print(f"THREADS_ID={threads_id}")
```

Note the ID as `THREADS_ID`. Build the canonical filename:
- Threads: `[POST_NUMBER]-[SHORT_NAME]-infographic-threads-[DATE].png`

**For all/cover/mid/download modes**, run this registration block (include only the types being generated):

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name = "[SHORT_NAME]"
post_number = "[POST_NUMBER]"

con = get_connection()
cur = con.cursor()

cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
post_id = post_row[0] if post_row else None

# Register cover infographic
cover_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_id)
    VALUES ('infographic-cover','ai-for-you',:1,:2,
            'draft',:3,:4,:5)
    RETURNING id INTO :new_id""",
    [short_name + "-infographic-cover",
     f"Substack thumbnail cover infographic for post {post_number}",
     today, today, post_id, cover_var])
cover_id = int(cover_var.getvalue()[0])
cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'substack-newsletter','pending')", (cover_id,))

# Register mid-article infographic
mid_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_id)
    VALUES ('infographic-mid','ai-for-you',:1,:2,
            'draft',:3,:4,:5)
    RETURNING id INTO :new_id""",
    [short_name + "-infographic-mid",
     f"Mid-article square infographic for post {post_number}",
     today, today, post_id, mid_var])
mid_id = int(mid_var.getvalue()[0])
cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'substack-newsletter','pending')", (mid_id,))

# Register download/share infographic
dl_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_id)
    VALUES ('infographic-download','ai-for-you',:1,:2,
            'draft',:3,:4,:5)
    RETURNING id INTO :new_id""",
    [short_name + "-infographic",
     f"Download/share portrait infographic for post {post_number}",
     today, today, post_id, dl_var])
dl_id = int(dl_var.getvalue()[0])
for platform in ['substack-newsletter', 'instagram']:
    cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,:2,'pending')", (dl_id, platform))

# Link all to the parent draft asset
cur.execute("SELECT a.id FROM assets a WHERE a.type='draft' AND a.post_id=:1", (post_id,))
draft_row = cur.fetchone()
if draft_row:
    for asset_id in [cover_id, mid_id, dl_id]:
        cur.execute("INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'infographic-for')", (draft_row[0], asset_id))

con.commit()
con.close()
print(f"COVER_ID={cover_id}  MID_ID={mid_id}  DL_ID={dl_id}")
```

Note the IDs. Build canonical filenames:
- Cover: `[POST_NUMBER]-[SHORT_NAME]-infographic-cover-[DATE].png`
- Mid: `[POST_NUMBER]-[SHORT_NAME]-infographic-mid-[DATE].png`
- Download: `[POST_NUMBER]-[SHORT_NAME]-infographic-[DATE].png`

---

### STEP 6  -  Wait and download

Wait for each artifact, then download. Run waits in parallel. Each artifact waits against its own notebook.

**Cover (download to /tmp first — needs special post-processing):**
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ARTIFACT_COVER] -n [NB_COVER] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic /tmp/cover-raw-[POST_NUMBER].png -a [ARTIFACT_COVER] -n [NB_COVER]
```

**QUALITY GATE — Cover (run immediately after cover download, before STEP 6c):**

Display `/tmp/cover-raw-[POST_NUMBER].png` inline. Then ask Kay:

> "Cover raw portrait downloaded. Check: (1) Is the character an illustrated Black woman with curly hair and glasses, face clearly visible? (2) Is the palette warm — ambers, golds, pinks, sunset colors? If yes, I'll proceed to post-processing. If no, I'll regenerate."

If regeneration is needed, re-run the STEP 5a generate command against `[NB_COVER]` with the same prompt, wait for the new artifact, and download it again before proceeding to STEP 6c. Do NOT proceed to STEP 6c until Kay approves the raw portrait.

---

**Mid-article (download to /tmp first — needs special post-processing):**
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ARTIFACT_MID] -n [NB_MID] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic /tmp/mid-raw-[POST_NUMBER].png -a [ARTIFACT_MID] -n [NB_MID]
```

**QUALITY GATE — Mid (run immediately after mid download, before STEP 7a):**

Display `/tmp/mid-raw-[POST_NUMBER].png` inline. Then ask Kay:

> "Mid raw portrait downloaded. Check: (1) Is this an illustrated scene with a single character (photo-style, not a multi-row layout)? (2) Is the stat/quote text visible at the bottom? If yes, I'll crop to square. If no (wrong content type or missing text), I'll regenerate."

If regeneration is needed, re-run the STEP 5b generate command against `[NB_MID]` with the same prompt, wait for the new artifact, and download it again before proceeding to STEP 7a. Do NOT proceed to STEP 7a until Kay approves the raw portrait.

**Download/share portrait:**
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ARTIFACT_DOWNLOAD] -n [NB_DOWNLOAD] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic /Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/[POST_NUMBER]-[SHORT_NAME]-infographic-[DATE].png -a [ARTIFACT_DOWNLOAD] -n [NB_DOWNLOAD]
```

**Threads portrait (threads mode):**
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ARTIFACT_THREADS] -n [NB_THREADS] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic /Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/[POST_NUMBER]-[SHORT_NAME]-infographic-threads-[DATE].png -a [ARTIFACT_THREADS] -n [NB_THREADS]
```

---

### POST-PROCESSING ROUTING — RUN THIS BEFORE STEPS 6c / 7 / 7a / 7b

Each infographic type has its own dedicated post-processing chain. Run ONLY the steps listed for the type(s) being generated. Do not apply STEP 7 to the mid — it will leave the mid as a portrait instead of a square.

| Type | Steps to run | Output size |
|------|-------------|-------------|
| Cover | STEP 6c | 1456x1048px landscape |
| Mid-article | STEP 7a ONLY | 1080x1080px square |
| Download/share | STEP 7, then STEP 7b | Portrait + footer bar |
| Threads | STEP 7 ONLY | Portrait |

**Critical:** The mid-article raw file (`/tmp/mid-raw-[POST_NUMBER].png`) is a portrait. STEP 7a is the only step that converts it to a 1080x1080 square and saves it to the post infographic folder. If STEP 7a is skipped, the mid never gets saved to its final destination.

---

### STEP 7  -  Remove NotebookLM branding and fix duplicate handles

**For download and threads only.** Do NOT run this step for the mid-article infographic — mid uses STEP 7a instead.

```bash
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image
import numpy as np

def remove_notebooklm_logo(arr):
    h, w = arr.shape[:2]
    scale = w / 1536
    logo_h = int(55 * scale)
    logo_w = int(300 * scale)
    sample_start = h - logo_h - 50
    sample_end   = h - logo_h
    for i in range(logo_h):
        source_y = sample_start + (i % (sample_end - sample_start))
        arr[h - logo_h + i, w - logo_w:w, :] = arr[source_y, w - logo_w:w, :]
    print(f"Removed NotebookLM logo ({logo_w}x{logo_h}px corner)")
    return arr

def remove_duplicate_handles(arr):
    h, w = arr.shape[:2]
    scan_y_start = int(h * 0.70)
    scan_x_start = int(w * 0.60)
    region = arr[scan_y_start:h, scan_x_start:w, :]
    bright_rows = np.where(region.max(axis=(1, 2)) > 230)[0]
    if len(bright_rows) == 0:
        print("Duplicate handle check: no bright rows found, skipping")
        return arr
    clusters = []
    cluster_start = bright_rows[0]
    prev = bright_rows[0]
    for r in bright_rows[1:]:
        if r - prev > 10:
            clusters.append((cluster_start, prev))
            cluster_start = r
        prev = r
    clusters.append((cluster_start, prev))
    if len(clusters) <= 1:
        print(f"Duplicate handle check: {len(clusters)} cluster, no duplicates")
        return arr
    print(f"Duplicate handle check: found {len(clusters)} clusters — painting over {len(clusters)-1} duplicate(s)")
    non_first_rows = np.concatenate([bright_rows[(bright_rows >= s) & (bright_rows <= e)] for s, e in clusters[1:]])
    region_nf = arr[scan_y_start + non_first_rows.min():scan_y_start + non_first_rows.max() + 1, scan_x_start:w, :]
    bright_cols = np.where(region_nf.max(axis=(0, 2)) > 230)[0]
    if len(bright_cols) == 0:
        print("Duplicate handle check: could not determine x range, skipping")
        return arr
    x1 = max(0, scan_x_start + bright_cols.min() - 10)
    x2 = min(w, scan_x_start + bright_cols.max() + 10)
    for cluster_start_r, cluster_end_r in clusters[1:]:
        abs_start = scan_y_start + cluster_start_r
        abs_end   = scan_y_start + cluster_end_r + 1
        gap_height = abs_start - (scan_y_start + clusters[clusters.index((cluster_start_r, cluster_end_r)) - 1][1] + 1)
        gap_height = max(gap_height, 5)
        sample_start = abs_start - gap_height
        for i in range(abs_start, min(abs_end, h)):
            src_y = sample_start + ((i - abs_start) % gap_height)
            arr[i, x1:x2, :] = arr[src_y, x1:x2, :]
    return arr

def postprocess(filepath):
    img = Image.open(filepath).convert("RGB")
    arr = np.array(img)
    arr = remove_notebooklm_logo(arr)
    arr = remove_duplicate_handles(arr)
    Image.fromarray(arr, "RGB").save(filepath)
    print(f"Saved: {filepath}")

postprocess("FILEPATH_HERE")
PYEOF
```

Replace `FILEPATH_HERE` with the actual file path. Run once per file.

---

### STEP 7a  -  Crop mid infographic to square (mid only)

**Run this only for the mid-article infographic**, using the raw portrait downloaded to `/tmp`.

NotebookLM generates a tall portrait where the illustration occupies most of the height and the text sits at the very bottom. Because the portrait is too tall to fit face + text in a 1080px square without losing one or the other, we crop to show the face/character clearly, then overlay the stat text and badge ourselves using PIL. This gives reliable text placement regardless of where NotebookLM places it.

**Pass the text values from STEP 1:** `main_text` (the stat/insight), `sub_text` (the supporting line).

```bash
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def remove_notebooklm_logo(arr):
    h, w = arr.shape[:2]
    scale = w / 1536
    logo_h = int(55 * scale)
    logo_w = int(300 * scale)
    sample_start = h - logo_h - 50
    sample_end   = h - logo_h
    for i in range(logo_h):
        source_y = sample_start + (i % (sample_end - sample_start))
        arr[h - logo_h + i, w - logo_w:w, :] = arr[source_y, w - logo_w:w, :]
    return arr

def crop_mid_to_square(raw_path, output_path,
                        main_text, sub_text,
                        badge="AI FOR YOU  |  AI Work Bestie",
                        handle="@iamkaymalcolm"):
    img = Image.open(raw_path).convert("RGB")
    arr = np.array(img)
    arr = remove_notebooklm_logo(arr)
    img = Image.fromarray(arr, "RGB")
    w, h = img.size
    print(f"Raw mid size: {w}x{h}")

    # Crop face/character region (0.22 to 0.87) — stops above NotebookLM's text band.
    # We add text ourselves so we don't need to reach the bottom of the portrait.
    crop_y_start = int(h * 0.22)
    crop_y_end   = int(h * 0.87)
    crop = img.crop((0, crop_y_start, w, crop_y_end))

    # Resize to 1080px wide, center-crop to 1080px tall
    new_w = 1080
    new_h = int(crop.size[1] * (1080 / w))
    resized = crop.resize((new_w, new_h), Image.LANCZOS)
    top = max(0, (new_h - 1080) // 2)
    canvas = resized.crop((0, top, 1080, top + 1080)).convert("RGBA")

    # Dark gradient band at bottom 38% — text sits on this
    overlay = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    band_top = int(1080 * 0.62)
    for y in range(band_top, 1080):
        alpha = int(220 * min(1.0, (y - band_top) / (1080 * 0.12)))
        draw_ov.line([(0, y), (1080, y)], fill=(15, 5, 10, alpha))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    def load_font(size, bold=False):
        paths = ["/System/Library/Fonts/SFNS.ttf",
                 "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
                 else "/System/Library/Fonts/Supplemental/Arial.ttf"]
        for p in paths:
            try: return ImageFont.truetype(p, size)
            except: pass
        return ImageFont.load_default()

    GOLD  = (244, 162, 97)
    WHITE = (255, 255, 255)

    # Badge top-left
    badge_font = load_font(22, bold=True)
    draw.text((20, 20), badge, font=badge_font, fill=GOLD)

    # Main stat — large bold, word-wrapped to 1000px
    main_font   = load_font(48, bold=True)
    sub_font    = load_font(26)
    handle_font = load_font(20)

    words = main_text.split()
    lines, line = [], []
    for word in words:
        test = " ".join(line + [word])
        if draw.textlength(test, font=main_font) > 1000:
            if line: lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line: lines.append(" ".join(line))

    line_h = main_font.size + 8
    total_h = len(lines) * line_h + 12 + sub_font.size + 30
    text_y = 1080 - total_h - 36

    for i, ln in enumerate(lines):
        y = text_y + i * line_h
        draw.text((34, y + 2), ln, font=main_font, fill=(0, 0, 0, 120))
        draw.text((32, y),     ln, font=main_font, fill=WHITE)

    sub_y = text_y + len(lines) * line_h + 12
    draw.text((34, sub_y + 1), sub_text, font=sub_font, fill=(0, 0, 0, 100))
    draw.text((32, sub_y),     sub_text, font=sub_font, fill=(220, 220, 220))

    # Handle bottom-right
    handle_w = draw.textlength(handle, font=handle_font)
    draw.text((1080 - handle_w - 20, 1080 - handle_font.size - 14),
              handle, font=handle_font, fill=(180, 180, 180))

    canvas.convert("RGB").save(output_path)
    print(f"Mid square saved: {output_path} (1080x1080px)")

crop_mid_to_square(
    "/tmp/mid-raw-[POST_NUMBER].png",
    "OUTPUT_PATH_HERE",
    main_text="[STAT OR INSIGHT FROM BRIEF]",
    sub_text="[SUPPORTING LINE FROM BRIEF]"
)
PYEOF
```

Replace `[POST_NUMBER]`, `OUTPUT_PATH_HERE`, and the two text values from STEP 1 before running.

---

### STEP 7b  -  Add branded footer bar (download only)

**Run this only for the download/share infographic** — after STEP 7 post-processing. Do NOT run for mid, cover, or threads.

```bash
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image, ImageDraw, ImageFont

def add_branded_footer(filepath):
    img = Image.open(filepath).convert("RGB")
    w, h = img.size

    FOOTER_H   = 130
    FOOTER_BG  = (29, 8, 22)       # deep plum — matches stat bar
    WHITE      = (255, 255, 255)
    GOLD       = (244, 162, 97)    # #F4A261
    GRAY       = (160, 140, 150)   # separator
    S          = w / 1536          # scale factor

    FONT_HANDLE = int(32 * S)
    FONT_TEXT   = int(28 * S)
    RIGHT_MARGIN = int(48 * S)
    MAX_X = w - RIGHT_MARGIN

    def load_fonts(fh, ft):
        try:
            return (ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", fh),
                    ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", ft))
        except:
            return (ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", fh),
                    ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", ft))

    f_bold, f_reg = load_fonts(FONT_HANDLE, FONT_TEXT)

    def measure(fb, fr):
        ICON = int(30 * S)
        x = int(48*S) + ICON + int(14*S) + ICON + int(18*S)
        tmp = ImageDraw.Draw(Image.new("RGB", (w, 1)))
        for text, font in [
            ("@iamkaymalcolm", fb), ("|", fr),
            ("iamkaymalcolm.substack.com", fr), ("|", fr),
            ("LinkedIn Top Voice", fb), ("|", fr),
            ("AI & Data Leader, Fortune 100", fr),
        ]:
            x = tmp.textbbox((x, 0), text, font=font, anchor="lm")[2] + int(32*S)
        return x

    total = measure(f_bold, f_reg)
    if total > MAX_X:
        factor = MAX_X / total
        f_bold, f_reg = load_fonts(int(FONT_HANDLE * factor), int(FONT_TEXT * factor))

    new_img = Image.new("RGB", (w, h + FOOTER_H), FOOTER_BG)
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    CY = h + FOOTER_H // 2

    ICON = int(30 * S)
    IX = int(48 * S)
    IY = CY - ICON // 2

    # IG icon: rounded square + inner circle + dot
    draw.rounded_rectangle([IX, IY, IX+ICON, IY+ICON],
        radius=int(8*S), outline=WHITE, width=max(2, int(2.5*S)))
    inn = int(7*S)
    draw.ellipse([IX+inn, IY+inn, IX+ICON-inn, IY+ICON-inn],
        outline=WHITE, width=max(2, int(2*S)))
    dr = max(2, int(3*S))
    draw.ellipse([IX+ICON-int(10*S)-dr, IY+int(8*S)-dr,
                  IX+ICON-int(10*S)+dr, IY+int(8*S)+dr], fill=WHITE)

    # TikTok icon: music-note "d" shape
    TX = IX + ICON + int(14*S)
    ico = ICON
    sw  = max(3, int(5*S))
    nh_w = int(ico*0.62); nh_h = int(ico*0.48)
    draw.ellipse([TX, IY+ico-nh_h, TX+nh_w, IY+ico], fill=WHITE)
    st_x = TX + nh_w - sw
    draw.rectangle([st_x, IY, st_x+sw, IY+ico-nh_h//2], fill=WHITE)
    fw = int(ico*0.38); fh2 = int(ico*0.22)
    draw.rectangle([st_x+sw, IY, st_x+sw+fw, IY+fh2], fill=WHITE)
    draw.ellipse([st_x+sw+fw-fh2//2, IY, st_x+sw+fw+fh2//2, IY+fh2], fill=WHITE)

    x = TX + ICON + int(18*S)
    SEP = int(32*S)

    def write(x, text, fill, font):
        draw.text((x, CY), text, fill=fill, font=font, anchor="lm")
        return draw.textbbox((x, CY), text, font=font, anchor="lm")[2] + SEP

    x = write(x, "@iamkaymalcolm",               WHITE, f_bold)
    x = write(x, "|",                             GRAY,  f_reg)
    x = write(x, "iamkaymalcolm.substack.com",    WHITE, f_reg)
    x = write(x, "|",                             GRAY,  f_reg)
    x = write(x, "LinkedIn Top Voice",            GOLD,  f_bold)
    x = write(x, "|",                             GRAY,  f_reg)
    draw.text((x, CY), "AI & Data Leader, Fortune 100", fill=WHITE, font=f_reg, anchor="lm")

    new_img.save(filepath)
    print(f"Footer added: {filepath}")

add_branded_footer("FILEPATH_HERE")
PYEOF
```

Replace `FILEPATH_HERE` with the download infographic path.

---

### STEP 6c  -  Cover post-processing (cover only)

NotebookLM puts the illustration scene in the bottom half of the portrait. This step: removes the logo from the raw file, crops the illustration from the bottom, adds a gradient overlay, and overlays the title text using PIL.

```bash
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def remove_notebooklm_logo(arr):
    h, w = arr.shape[:2]
    scale = w / 1536
    logo_h = int(55 * scale)
    logo_w = int(300 * scale)
    sample_start = h - logo_h - 50
    sample_end   = h - logo_h
    for i in range(logo_h):
        source_y = sample_start + (i % (sample_end - sample_start))
        arr[h - logo_h + i, w - logo_w:w, :] = arr[source_y, w - logo_w:w, :]
    print(f"Logo removed ({logo_w}x{logo_h}px)")
    return arr

def build_cover(portrait_path, output_path, title):
    portrait = Image.open(portrait_path).convert("RGB")
    arr = np.array(portrait)
    arr = remove_notebooklm_logo(arr)
    portrait = Image.fromarray(arr, "RGB")
    pw, ph = portrait.size
    print(f"Portrait: {pw}x{ph}")

    # Find where the illustration begins by scanning top-to-bottom in 60px bands.
    # Text sections are near-grayscale (HSV saturation ~0.39-0.49).
    # The illustration jumps to 0.50+ saturation (warm ambers, golds, pinks).
    # Crop 1048px from exactly the threshold band — no backup.
    def mean_saturation(patch):
        r, g, b = patch[:,:,0]/255.0, patch[:,:,1]/255.0, patch[:,:,2]/255.0
        cmax = np.maximum(np.maximum(r, g), b)
        cmin = np.minimum(np.minimum(r, g), b)
        delta = cmax - cmin
        sat = np.where(cmax > 0.001, delta / cmax, 0.0)
        return float(np.mean(sat))

    arr_check = np.array(portrait)
    band, threshold = 60, 0.50
    y1 = ph - 1048  # fallback: bottom
    for scan_y in range(0, ph - 1048, band):
        if mean_saturation(arr_check[scan_y:scan_y+band]) >= threshold:
            y1 = scan_y
            print(f"Illustration top at y={y1} (sat threshold {threshold} crossed)")
            break
    else:
        print(f"Threshold not crossed — using fallback bottom crop at y={y1}")

    scene = portrait.crop((0, y1, pw, y1 + 1048))
    # Center horizontally to 1456px
    x1 = max(0, (pw - 1456) // 2)
    scene = scene.crop((x1, 0, x1 + 1456, 1048))

    # Gradient: fully opaque first 35px (kills any text bleed from NotebookLM content),
    # then fades to 0 by y=380. Title sits on the dark band.
    overlay = Image.new("RGBA", (1456, 1048), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    solid_end, fade_end = 35, 380
    for y in range(solid_end):
        draw_ov.line([(0, y), (1456, y)], fill=(20, 5, 15, 255))
    for y in range(solid_end, fade_end):
        alpha = int(255 * (1 - (y - solid_end) / (fade_end - solid_end)))
        draw_ov.line([(0, y), (1456, y)], fill=(20, 5, 15, alpha))
    scene = Image.alpha_composite(scene.convert("RGBA"), overlay).convert("RGB")

    # Overlay title text
    draw = ImageDraw.Draw(scene)
    font_size = 82
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", font_size)
    except:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)

    x, y = 64, 48
    # Drop shadow
    draw.multiline_text((x+3, y+3), title, font=font, fill=(0, 0, 0, 140), spacing=14)
    # White text
    draw.multiline_text((x, y), title, font=font, fill=(255, 255, 255), spacing=14)

    scene.save(output_path)
    print(f"Cover saved: {output_path} (1456x1048px)")

build_cover(
    "/tmp/cover-raw-[POST_NUMBER].png",
    "/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/[POST_NUMBER]-[SHORT_NAME]-infographic-cover-[DATE].png",
    "[NEWSLETTER TITLE]"
)
PYEOF
```

Replace `[POST_NUMBER]`, `[POST_FOLDER]`, `[SHORT_NAME]`, `[DATE]`, and `[NEWSLETTER TITLE]` before running. The title should match what was extracted from the draft in STEP 1. Use `\n` for line breaks if the title is long.

---

### STEP 8  -  Update tracking files

**Asset DB  -  update file paths:**

```python
import oracledb, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = "[DATE]"
INFOG = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic")

cover_file = "[POST_NUMBER]-[SHORT_NAME]-infographic-cover-[DATE].png"
mid_file   = "[POST_NUMBER]-[SHORT_NAME]-infographic-mid-[DATE].png"
dl_file    = "[POST_NUMBER]-[SHORT_NAME]-infographic-[DATE].png"

con = get_connection()
cur = con.cursor()
cur.execute("UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3", (str(INFOG / cover_file), today, [COVER_ID]))
cur.execute("UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3", (str(INFOG / mid_file), today, [MID_ID]))
cur.execute("UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3", (str(INFOG / dl_file), today, [DL_ID]))
con.commit()
con.close()
```

**Upload to Drive and record in assets_images:**

On the first run, use INSERT. On a regeneration run (assets_images rows already exist), use UPDATE instead — catch `ORA-00001` unique constraint violations and switch to UPDATE automatically:

```python
import subprocess, json, os, sys
from pathlib import Path
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
import oracledb

ROOT = "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"
post_folder = "[POST_FOLDER]"
INFOG = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic")

files = [
    ([COVER_ID], str(INFOG / "[POST_NUMBER]-[SHORT_NAME]-infographic-cover-[DATE].png")),
    ([MID_ID],   str(INFOG / "[POST_NUMBER]-[SHORT_NAME]-infographic-mid-[DATE].png")),
    ([DL_ID],    str(INFOG / "[POST_NUMBER]-[SHORT_NAME]-infographic-[DATE].png")),
]

subprocess.run(["rclone", "mkdir", f"gdrive:AI LinkedIn 2026/{post_folder}/infographic", "--drive-root-folder-id", ROOT], check=True)
for _, fp in files:
    subprocess.run(["rclone", "copy", fp, f"gdrive:AI LinkedIn 2026/{post_folder}/infographic", "--drive-root-folder-id", ROOT], check=True)

r = subprocess.run(["rclone", "lsjson", f"gdrive:AI LinkedIn 2026/{post_folder}", "--drive-root-folder-id", ROOT, "--dirs-only"],
                   capture_output=True, text=True, check=True)
folder_id = next(e["ID"] for e in json.loads(r.stdout) if e["Name"] == "infographic")

con = get_connection()
cur = con.cursor()
for asset_id, fp in files:
    gdrive_path = f"AI LinkedIn 2026/{post_folder}/infographic/{os.path.basename(fp)}"
    try:
        cur.execute("INSERT INTO assets_images (asset_id, gdrive_path, gdrive_folder_id, uploaded_at) VALUES (:1,:2,:3,CURRENT_TIMESTAMP)",
                    (asset_id, gdrive_path, folder_id))
    except oracledb.IntegrityError:
        cur.execute("UPDATE assets_images SET gdrive_path=:1, gdrive_folder_id=:2, uploaded_at=CURRENT_TIMESTAMP WHERE asset_id=:3",
                    (gdrive_path, folder_id, asset_id))
con.commit()
con.close()
print(f"Drive: infographic folder {folder_id}")
```

Then refresh the registry:
```
/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

---

### STEP 8b  -  Sync brief to Drive

Find the brief for this post, mark infographic checklist items complete, and push the updated brief to Bay's Drive:

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import subprocess
from pathlib import Path

post_folder = "[POST_FOLDER]"
post_number = "[POST_NUMBER]"
ROOT = "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"

brief_files = sorted(Path(f"/Users/kmalcolm/claude/iamkaymalcolm/posts/{post_folder}").glob(f"{post_number}-*-brief-*.md"))
if not brief_files:
    print("No brief found for this post - skipping brief sync")
else:
    brief_path = brief_files[-1]
    text = brief_path.read_text()
    text = text.replace("- [ ] Mid-article infographic", "- [x] Mid-article infographic")
    text = text.replace("- [ ] Download/share infographic", "- [x] Download/share infographic")
    brief_path.write_text(text)
    subprocess.run(["rclone", "copy", str(brief_path), f"gdrive:AI LinkedIn 2026/{post_folder}",
                    "--drive-root-folder-id", ROOT], check=True)
    print(f"Brief updated and synced to Drive: {brief_path.name}")
PYEOF
```

---

### STEP 9  -  Report back

Tell the user:
- Which infographic(s) were generated
- All file paths
- Whether notebooks were reused or newly created
- Show all images inline
- Confirm cover is 1456x1048px landscape

---

## Output File Naming

| Type | Filename pattern | Destination platform |
|------|-----------------|---------------------|
| Substack cover | `[POST_NUMBER]-[SHORT_NAME]-infographic-cover-[DATE].png` | substack-newsletter |
| Mid-article square | `[POST_NUMBER]-[SHORT_NAME]-infographic-mid-[DATE].png` | substack-newsletter |
| Download/share portrait | `[POST_NUMBER]-[SHORT_NAME]-infographic-[DATE].png` | substack-newsletter, instagram |
| Threads portrait | `[POST_NUMBER]-[SHORT_NAME]-infographic-threads-[DATE].png` | threads |

All save to: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/`

Create the `infographic/` subdirectory if it does not exist. Never save to a top-level infographic folder. Never save to content-drafts. Never save to the strategy folder.

---

## Content Rules

- **No em dashes anywhere.** Not in titles, subtitles, row labels, teaser text, bottom stats, or CTA bars. Replace with a hyphen ( - ). Zero exceptions.

- **No call-to-actions of any kind.** Infographics are standalone static assets. No CTA bars, no comment prompts, no "DM me", no "Link in bio", no "Subscribe", no ManyChat triggers. Strip any text containing "Comment [KEYWORD]", "Drop [WORD] in the comments", "Comment for", "DM me", or any action request. The `@iamkaymalcolm` handle is the only attribution allowed, and it appears as a small passive tag on mid/download/threads only — never on the cover.

---

## NotebookLM CLI Notes

- Always use: `/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli`
- Never use the bare `notebooklm` command (runs on Python 3.9, will fail)
- NotebookLM always outputs portrait regardless of instructions. Cover and mid have dedicated post-processing that handles the conversion — do not try to force landscape or square via the prompt.
- Each infographic type has its own dedicated notebook. Notebook IDs are stored in `[POST_FOLDER]/infographic/.notebooks.json` and reused on every subsequent run for that post.
- If `--orientation square` is not supported, use `--orientation portrait` — the mid post-processing handles the square conversion regardless.
- If auth fails: `notebooklm login` to re-authenticate
- Rate limiting: if generation fails, wait 5-10 min and retry once
