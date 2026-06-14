# AI For You  -  Story Generator Skill

Generate 3 Instagram Story frames for an AI For You post using NotebookLM. Stories are designed to start conversations, trigger DM flows, and amplify posts  -  not just drive link clicks.

## When This Skill Activates

**Explicit:**
- `/ai-for-you-story [post number]`  -  generates all 3 stories

**Intent detection:** Recognize requests like:
- "Generate the stories for post 002"
- "Make the Instagram stories for the latest AI For You post"
- "Create stories for 001"

---

## Autonomy Rules

Run the full workflow with no confirmation. All 3 stories go into the same NotebookLM notebook. Fire all 3 generate commands before waiting on any  -  they run in parallel. Wait and download each as it completes. Show every image inline as it downloads.

---

## Visual Style  -  Warm Regal Editorial Illustration

Stories use the same gold-standard editorial illustration style as the cover infographic — NOT flat pastel backgrounds. The illustrated scene IS the background.

**Reference:** `/Users/kmalcolm/claude/iamkaymalcolm/posts/1043-switching-to-claude/infographic/1043-1183-switching-to-claude-infographic-cover-2026-05-22.png`

```
ILLUSTRATION STYLE:
  Premium editorial vector illustration. NOT photorealistic. NOT flat/minimal.
  Cinematic, warm, aspirational — like a still from an award-winning animated feature.
  Same visual energy as a high-end magazine cover.

SCENE (used as background on all stories):
  An African American woman with collarbone length, full, voluminous spiral curls (collarbone length, big natural hair energy) and glasses. At a sleek modern desk with a laptop and steaming mug.
  Framed by floor-to-ceiling windows with a city skyline glowing at golden hour / dusk.
  Small plant visible to one side.

COLOR PALETTE — WARM AND REGAL:
  Sky: deep amber, burnt gold, warm pink, magenta, dusty rose, rich rose-gold, soft purple
       — the full regal sunset spectrum. NOT cool purple. NOT flat lavender. NOT dark navy.
  Foreground: dark warm neutrals (desk, chair, room shadow) against the glowing window light.
  Window light: gorgeous backlit glow — warm amber and pink streaming in around the character.

TEXT COLORS:
  Primary overlay:  White (#FFFFFF)  -  always on the illustrated background
  Accent:           Gold/amber (#F4A261)  -  series badge, callout lines, attribution
  Dark panels:      When a text block needs extra contrast, use a semi-transparent
                    dark warm overlay (deep plum at 60% opacity) behind the text only.

Series badge: "AI FOR YOU | AI Work Bestie"  -  ALL CAPS, gold/amber (#F4A261), small, top-left
Handle: @iamkaymalcolm  -  bottom corner, small, white
Link sticker: Soft rounded pill button, gold/amber fill or white fill
```

**Vary the mood across the 3 stories** — one can lean golden/amber-warm, one more pink/magenta, one more dusty rose/plum. Same scene, different atmospheric lighting emphasis. No flat color backgrounds on any of the 3.

---

## Workflow

### STEP 0  -  Identify the target post

- Find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/` and locate the draft file inside it (matching `[POST_NUMBER]-*-draft-*.md`). Note the full post folder name as `POST_FOLDER` (e.g. `1031-where-to-start-with-ai`) and derive `SHORT_NAME` from it (e.g. `where-to-start-with-ai`).
- Also find the brief: `posts/[POST_FOLDER]/ai-for-you-[POST_NUMBER]-brief.md` (if it exists)
- Read both files. The draft has the full newsletter content and hook. The brief has the distilled production notes and content angles.

---

### STEP 1  -  Extract story content

From the draft and brief, pull:
- **The main hook** (non-negotiable line from the post)
- **The core stat or bold claim** (e.g. "4 in 5 people want to use AI at work")
- **The use cases or list items** (the numbered/bulleted things the post teaches)
- **A strong pull quote** from the newsletter body  -  one sentence that would stop a scroll
- **The CTA keyword** (usually "Comment AI") and what it delivers
- **The newsletter title** (for the link sticker label)

---

### STEP 2  -  Get or create the stories notebook (one per post, ever)

Check `stories/.notebooks.json` first. If the notebook already exists for this post, reuse it and skip STEP 3 entirely.

```python
import json, subprocess
from pathlib import Path

stories_dir = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/stories")
stories_dir.mkdir(exist_ok=True)
notebooks_file = stories_dir / ".notebooks.json"

if notebooks_file.exists():
    nb = json.loads(notebooks_file.read_text())
    notebook_id = nb["stories"]
    print(f"Reusing stories notebook: {notebook_id}")
    # Sources already loaded — skip STEP 3
else:
    # Create notebook
    result = subprocess.run(
        ["/opt/homebrew/bin/python3.12", "-m", "notebooklm.notebooklm_cli",
         "create", "AI For You #[POST_NUMBER] - [Topic] Stories", "--json"],
        capture_output=True, text=True, check=True
    )
    import json as _json
    notebook_id = _json.loads(result.stdout)["notebook"]["id"]
    notebooks_file.write_text(json.dumps({"stories": notebook_id}, indent=2))
    print(f"Created stories notebook: {notebook_id}")
```

---

### STEP 3  -  Add sources and wait

**Skip this step entirely if `.notebooks.json` already existed** — sources were loaded on the first run.

If the notebook was just created, add the draft file and brief (if it exists). Run adds in parallel, wait in parallel.

```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add [draft file path] -n [notebook_id] --json
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add [brief file path] -n [notebook_id] --json  # if exists
```

Wait:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [source_id] -n [notebook_id] --timeout 120
```

If any source returns "not found", re-add it and wait again before proceeding.

---

### STEP 4  -  Choose 3 story types and generate

**Randomly select 3 from the 5 types below** (no repeats). Use Python's `random.sample(["poll","stat-card","countdown","question","pull-quote"], 3)` to pick. Record which types were chosen as `TYPE_1`, `TYPE_2`, `TYPE_3`.

**Kay illustration assignment:**
- Story 1 (`TYPE_1`) gets Kay's picture
- Story 2 (`TYPE_2`) does NOT get Kay's picture
- Story 3 (`TYPE_3`) gets Kay's picture

For each type, use the template below. If the story is assigned Kay's picture, merge in the **Kay variant block** for that type (described in each template).

---

#### Story Type: Poll

**Base prompt:**
```
Create an Instagram Story frame for the AI For You series. Cinematic, warm, editorial — NOT a flat color background.

FORMAT: Portrait 9:16, 1080x1920px.

BACKGROUND SCENE:
Premium editorial vector illustration filling the full frame. A warm regal cityscape at golden
hour / dusk visible through floor-to-ceiling windows. The scene glows with deep amber, burnt gold,
warm pink, and magenta — the full regal sunset palette. Dark warm neutrals in the foreground
(desk, chair). The illustrated scene IS the background; no flat color.

DESIGN RULES:
- Series badge top-left: "AI FOR YOU | AI Work Bestie"  -  tiny, gold/amber (#F4A261)
- Handle bottom-right: @iamkaymalcolm  -  small, white
- Question text: large, centered, white — placed in the middle of the frame over a subtle
  semi-transparent dark warm overlay so it reads clearly against the scene
- Poll widget below question: two rounded pill options side by side, white fill with dark text
- NO link sticker on this one  -  the poll IS the CTA.
- Cinematic, personal energy. Feels like a question from someone who actually knows you.
- The scene sets a mood; the question is the message.

CONTENT:
Question (large, centered, white): "[MAIN HOOK OR CURIOSITY QUESTION — max 7 words per line, 2 lines max, fragment or punchy phrase, no em dashes]"
Poll option 1: "Yes, daily"
Poll option 2: "I keep saying I will"
```

**Kay variant addition** (merge into DESIGN RULES when this story gets Kay):
```
- FEATURE KAY: The African American woman with collarbone length, full, voluminous spiral curls (collarbone length, big natural hair energy) and glasses is prominently visible in the scene — seated at her desk, holding her mug,
  looking directly at the viewer as if she's asking them the question personally. She occupies
  the lower 50% of the frame. The question text and poll widget sit above her in the upper half,
  over a subtle dark overlay for readability. Her direct gaze makes the poll feel personal, not generic.
```

---

#### Story Type: Stat Card

**Base prompt:**
```
Create an Instagram Story frame for the AI For You series. Bold, punchy — one stat, cinematic scene.

FORMAT: Portrait 9:16, 1080x1920px.

BACKGROUND SCENE:
Premium editorial vector illustration filling the full frame. Lean into the deeper end of the
regal palette for this one — rich magentas, warm dusty rose, deep amber fading into soft plum
at the top. City skyline glowing at dusk through floor-to-ceiling windows. Dark warm foreground.
The scene creates drama; the stat owns the moment.

DESIGN RULES:
- Series badge top-left: "AI FOR YOU | AI Work Bestie"  -  tiny, gold/amber (#F4A261)
- Handle bottom-right: @iamkaymalcolm  -  small, white
- Stat text: large, bold, white — centered in the frame, takes up 50-60% of the canvas.
  Use a subtle semi-transparent dark warm panel behind the stat if needed for contrast.
- One supporting line below in smaller weight, white or soft gold
- Link sticker at bottom: soft rounded pill, gold/amber fill
- Minimal. The stat IS the message. The scene is the mood.

CONTENT:
Stat (large, bold, white): "[CORE STAT OR BOLD CLAIM FROM THE POST]"
Supporting line (small, white): "[ONE SHORT LINE — max 7 words, fragment only, adds context or tension]"
Link sticker: "I wrote you a starting point →"
```

**Kay variant addition** (merge into DESIGN RULES when this story gets Kay):
```
- FEATURE KAY: The African American woman with collarbone length, full, voluminous spiral curls (collarbone length, big natural hair energy) and glasses is seated at her desk in the lower portion of the frame, visible from
  waist up. She looks confident and composed — not posed, just real. The stat text occupies
  the upper half of the frame, commanding attention above her. Her presence makes the stat
  feel personal, not abstract. Use the warm amber-gold end of the regal palette so she reads
  clearly against the glowing background.
```

---

#### Story Type: Countdown

**Base prompt:**
```
Create an Instagram Story frame for the AI For You series. Tappable list energy — like someone
is about to tell you something good, set against a gorgeous cinematic scene.

FORMAT: Portrait 9:16, 1080x1920px.

BACKGROUND SCENE:
Premium editorial vector illustration filling the full frame. Lean toward the warmer, lighter
end of the regal palette — warm champagne-gold, soft amber, hints of dusty rose. City glowing
softly through the windows. The scene feels inviting and abundant, like opportunity is right
outside that window.

DESIGN RULES:
- Series badge top-left: "AI FOR YOU | AI Work Bestie"  -  tiny, gold/amber (#F4A261)
- Handle bottom-right: @iamkaymalcolm  -  small, white
- ONE text element only: the teaser line, large, bold, white — over a subtle dark warm panel for contrast
- No lists or bullets on this frame. If there are multiple use cases, pick the single most surprising one. The list lives in the newsletter, not the story frame.
- Link sticker at bottom: soft rounded pill, gold/amber fill
- Feels like a teaser, not a full reveal. One hook sparks more curiosity than four bullet points.

CONTENT:
Text overlay (large, bold, white): "[SINGLE MOST SURPRISING USE CASE OR TEASER — max 7 words, fragment only]"
Link sticker: "Read it here"
```

**Kay variant addition** (merge into DESIGN RULES when this story gets Kay):
```
- FEATURE KAY: The African American woman with collarbone length, full, voluminous spiral curls (collarbone length, big natural hair energy) no glasses is visible in the lower portion of the frame, seated at her desk, leaning
  slightly forward — warm and conspiratorial, like she's about to let you in on something. The
  lead line and list occupy the upper two-thirds of the frame above and around her. Her presence
  gives the list a personal, insider feel — these aren't just tips, they're what she actually uses.
```

---

#### Story Type: Question

**Base prompt:**
```
Create an Instagram Story frame for the AI For You series. Intimate, direct — a question that
hits, set against a cinematic editorial scene.

FORMAT: Portrait 9:16, 1080x1920px.

BACKGROUND SCENE:
Premium editorial vector illustration filling the full frame. Lean into the deeper, moodier end
of the regal palette — warm magenta fading into dusty rose and deep amber. City at dusk, glowing
through floor-to-ceiling windows. Dark warm foreground. The mood is reflective and direct.

DESIGN RULES:
- Series badge top-left: "AI FOR YOU | AI Work Bestie"  -  tiny, gold/amber (#F4A261)
- Handle bottom-right: @iamkaymalcolm  -  small, white
- ONE text element: the question, large, centered, bold, white — placed in the upper-middle of the frame over a subtle dark warm panel for contrast.
- No stacked list on this frame. The question is the only text element. If there are items to tease, they live in the newsletter.
- Link sticker at the very bottom: rounded pill, gold/amber fill
- Quiet and confident. The question alone is the hook.

CONTENT:
Main question (large, white): "[STRONG QUESTION FROM THE POST — max 7 words per line, 2 lines max, no em dashes]"
Link sticker: "Get the prompts →"
```

**Kay variant addition** (merge into DESIGN RULES when this story gets Kay):
```
- FEATURE KAY: The African American woman with medium length, full, voluminous spiral curls (collarbone length, big natural hair energy) and glasses is centered in the upper portion of the frame, looking directly at the
  viewer. The question is hers and she means it — her expression is direct, warm, not posed.
  She is visible from the shoulders up against the glowing city background. The stacked list
  and closing line sit below her with generous breathing room. Her direct gaze makes the
  question feel personal, not rhetorical.
```

---

#### Story Type: Pull Quote

**Base prompt:**
```
Create an Instagram Story frame for the AI For You series. Magazine editorial cover energy —
one sentence, one breathtaking scene.

FORMAT: Portrait 9:16, 1080x1920px.

BACKGROUND SCENE:
Premium editorial vector illustration filling the full frame. This is the most cinematic of the
three stories — the full gold-standard scene: warm amber, gold, rich pink, magenta, and dusty
rose in the sky. City skyline glowing through floor-to-ceiling windows. Dark warm foreground.
A soft gradient overlay darkens the lower third of the frame so the quote reads cleanly.
This should feel like a magazine cover.

DESIGN RULES:
- Series badge top-left: "AI FOR YOU | AI Work Bestie"  -  tiny, gold/amber (#F4A261)
- Handle bottom-right: @iamkaymalcolm  -  small, white
- Pull quote: large, bold, white — placed in the lower third of the frame over the dark overlay.
  Max 2 lines. Max 7 words per line. The ONE sentence that would stop a scroll. Fragment or punchy phrase preferred. Quotation marks optional.
  Let the quote breathe — generous spacing above and below.
- Attribution below: small, gold/amber  -  "AI For You"
- Link sticker below attribution: soft rounded pill, white or gold fill
- Minimal. The quote IS the message. The scene is the world it lives in.
- No bullet points. No lists. Just the quote and the scene.

CONTENT:
Pull quote (large, white): "[MOST POWERFUL SINGLE SENTENCE FROM THE NEWSLETTER BODY  -  the one
that is true, sharp, and makes someone feel seen]"
Attribution (small, gold): "AI For You"
Link sticker: "Read the full issue →"
```

**Kay variant addition** (merge into DESIGN RULES when this story gets Kay):
```
- FEATURE KAY: The African American woman with collarbone legnth, full, voluminous spiral curls (big natural hair energy) occupies the upper 50-60% of the frame — seated at her desk, relaxed and
  real, not posed. She is the editorial subject. The warm regal cityscape glows behind her through
  the windows. A soft dark gradient overlay covers the lower 40% of the frame; the pull quote sits
  there, overlaid on the darkened scene. Her presence above makes the quote feel like it came from
  someone who means it. This is a magazine editorial cover — a real person with something to say.
```

---

Fire all 3 as portrait (adapt prompts with Kay variant where applicable):
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation portrait --detail detailed --style professional "[story instructions]" -n [notebook_id] --json
```

Note all 3 artifact IDs: `ARTIFACT_S1` through `ARTIFACT_S3`.

---

### STEP 5  -  Wait and download

Before downloading, register all 3 story assets in the DB to get their IDs and canonical filenames. Use the actual `TYPE_1`, `TYPE_2`, `TYPE_3` labels chosen in STEP 4.

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name = "[SHORT_NAME]"
post_number = "[POST_NUMBER]"

# Replace these with the actual types chosen in STEP 4
chosen_labels = ["[TYPE_1]", "[TYPE_2]", "[TYPE_3]"]

con = get_connection()
cur = con.cursor()

story_ids = []
for n, label in enumerate(chosen_labels, start=1):
    id_var = cur.var(oracledb.NUMBER)
    cur.execute("""
        INSERT INTO assets (type, pipeline, short_name, description, status,
                            created_date, updated_date, post_number)
        VALUES ('story','ai-for-you',:1,:2,'draft',:3,:4,:5)
        RETURNING id INTO :new_id""",
        [f"{short_name}-story-{n:02d}",
         f"Story {n:02d} ({label}) for post {post_number}",
         today, today, post_number, id_var])
    last_id = int(id_var.getvalue())
    story_ids.append(last_id)
    cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'instagram','pending')", (last_id,))

con.commit()
con.close()
print("  ".join(f"S{i+1}_ID={sid}" for i, sid in enumerate(story_ids)))
```

Note the 3 IDs. Build canonical filenames as `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-story-0[N]-[DATE].png`.

Wait for all 3 in parallel, then download each as it completes. Show the image inline immediately after each download  -  don't wait for all 3 to finish before showing any.

```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ARTIFACT_Sn] -n [notebook_id] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic /Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/stories/[POST_NUMBER]-[S_ID]-[SHORT_NAME]-story-0[N]-[DATE].png -a [ARTIFACT_Sn] -n [notebook_id]
```

Output file naming (labels reflect actual types chosen):
| Story | Filename |
|-------|----------|
| Story 1  -  [TYPE_1] (with Kay) | `[POST_NUMBER]-[S1_ID]-[SHORT_NAME]-story-01-[DATE].png` |
| Story 2  -  [TYPE_2] | `[POST_NUMBER]-[S2_ID]-[SHORT_NAME]-story-02-[DATE].png` |
| Story 3  -  [TYPE_3] (with Kay) | `[POST_NUMBER]-[S3_ID]-[SHORT_NAME]-story-03-[DATE].png` |

All save to: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/stories/`

Create the `stories/` subdirectory if it does not exist. After all 3 are downloaded, update the DB file paths:

```python
import oracledb, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
STORIES = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/stories")
today = "[DATE]"

con = get_connection()
cur = con.cursor()
for n, sid in enumerate([S1_ID, S2_ID, S3_ID], start=1):
    fname = f"[POST_NUMBER]-{sid}-[SHORT_NAME]-story-{n:02d}-{today}.png"
    cur.execute("UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3",
        (str(STORIES / fname), today, sid))
con.commit()
con.close()
```

Then refresh: `/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md`

---

### STEP 6  -  Remove NotebookLM branding

After each file downloads, immediately strip the NotebookLM badge from the bottom. Run once per file as it completes (don't wait for all 3).

NotebookLM adds branding in two forms:
1. A full white/light strip at the very bottom (large, ~119px)
2. Small watermark text in the bottom-right corner blending into the background (small, ~45px)

The script handles both: it scans for a light strip first, then always applies a minimum 45px crop to catch the small text watermark regardless.

```bash
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image
import numpy as np

def remove_notebooklm_badge(filepath):
    img = Image.open(filepath)
    arr = np.array(img.convert("RGB"))
    h, w = arr.shape[:2]

    # Pass 1: scan from bottom upward while rows are light (catches full white strip)
    badge_start = h
    for y in range(h - 1, max(h - 120, 0), -1):
        if np.mean(arr[y]) > 180:
            badge_start = y
        else:
            break

    # Pass 2: always crop at least 45px to catch the small text watermark
    # that blends into the background and isn't detected by brightness scan
    MIN_CROP = 45
    crop_to = min(badge_start, h - MIN_CROP)

    img.crop((0, 0, w, crop_to)).save(filepath)
    print(f"Cropped to {crop_to}px (removed {h - crop_to}px) from {filepath}")

remove_notebooklm_badge("FILEPATH_HERE")
PYEOF
```

Replace `FILEPATH_HERE` with the actual file path before running.

---

### STEP 7  -  Upload to Google Drive and record in assets_images

After branding is removed from all 3, upload each file to Google Drive using rclone into the structured post folder, then INSERT into `assets_images`.

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import subprocess, json, os, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

ROOT = "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"
post_folder = "[POST_FOLDER]"   # e.g. "1031-where-to-start-with-ai"
story_files = [
    ("[S1_FILE_PATH]", [S1_ID]),
    ("[S2_FILE_PATH]", [S2_ID]),
    ("[S3_FILE_PATH]", [S3_ID]),
]

# Create stories folder (idempotent)
subprocess.run(["rclone", "mkdir", f"gdrive:AI LinkedIn 2026/{post_folder}/stories",
                "--drive-root-folder-id", ROOT], check=True)

# Upload all 3
for fp, _ in story_files:
    subprocess.run(["rclone", "copy", fp, f"gdrive:AI LinkedIn 2026/{post_folder}/stories",
                    "--drive-root-folder-id", ROOT], check=True)

# Get stories subfolder Drive ID
r = subprocess.run(["rclone", "lsjson", f"gdrive:AI LinkedIn 2026/{post_folder}",
                    "--drive-root-folder-id", ROOT, "--dirs-only"],
                   capture_output=True, text=True, check=True)
folder_id = next(e["ID"] for e in json.loads(r.stdout) if e["Name"] == "stories")

# INSERT into assets_images for each story (UPDATE on regen)
import oracledb as _odb
con = get_connection()
cur = con.cursor()
for fp, asset_id in story_files:
    gdrive_path = f"AI LinkedIn 2026/{post_folder}/stories/{os.path.basename(fp)}"
    try:
        cur.execute("INSERT INTO assets_images (asset_id, gdrive_path, gdrive_folder_id, uploaded_at) "
                    "VALUES (:1,:2,:3,CURRENT_TIMESTAMP)",
                    (asset_id, gdrive_path, folder_id))
    except _odb.IntegrityError:
        cur.execute("UPDATE assets_images SET gdrive_path=:1, gdrive_folder_id=:2, uploaded_at=CURRENT_TIMESTAMP "
                    "WHERE asset_id=:3",
                    (gdrive_path, folder_id, asset_id))
con.commit()
con.close()
print(f"Uploaded 3 stories to Drive: stories folder {folder_id}")
PYEOF
```

If rclone is not installed: `brew install rclone`. If `gdrive:` remote is not configured, stop and show the user rclone config setup instructions from the gdrive-upload skill.

---

### STEP 7b  -  Sync brief to Drive

Find the brief for this post, mark the stories checklist item complete, and push the updated brief to Bay's Drive:

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
    text = text.replace("- [ ] Instagram Stories generated", "- [x] Instagram Stories generated")
    brief_path.write_text(text)
    subprocess.run(["rclone", "copy", str(brief_path), f"gdrive:AI LinkedIn 2026/{post_folder}",
                    "--drive-root-folder-id", ROOT], check=True)
    print(f"Brief updated and synced to Drive: {brief_path.name}")
PYEOF
```

---

### STEP 8  -  Update tracking files

**`/Users/kmalcolm/claude/iamkaymalcolm/todo.md`**
- Add to COMPLETED: `- [x] Stories for post [NNN] generated (3 frames: [TYPE_1] w/Kay, [TYPE_2], [TYPE_3] w/Kay)`

---

### STEP 9  -  Report back

- Show all 3 images inline
- List all file paths
- Notebook ID and whether it was reused or newly created
- Brief note on which story type each one is, and which ones feature Kay
- Confirm branding removed from each (px cropped, or "no badge detected")
- Confirm all 3 uploaded to Google Drive (Bay's folder) under `posts/[POST_FOLDER]/stories/` — report the dynamically resolved subfolder ID

---

## Story Text Rules (Enforced — Every Frame)

Stories are visual. Text overlays are minimal. These apply to every frame, every type:

- **Max 7 words per text overlay line**
- **Max 2 lines of text per frame** (handle and link sticker do not count)
- **Fragments and punchy phrases only** — not full sentences. "3 prompts I use daily" not "Here are the three prompts I use every single day."
- **No bullets or lists on any frame.** Multiple points = multiple frames. This skill generates 3 frames — plan accordingly. Pick the single best hook per frame.
- **No em dashes anywhere on story frames.** Hyphen, period, or rewrite.
- **One text element per frame.** The visual carries emotion; the text carries the hook. Not both.

Stories are Instagram only. Do not generate story content for any other platform.

---

## Voice Rules

- **No em dashes anywhere.** Not in story prompts, not in text overlays, not in link sticker labels, not in question text. Use a hyphen ( - ), a period, semi colon, colon or comma or rewrite the line. ZERO exceptions.
- **Anti-AI writing standards apply to all text overlay content.** Poll questions, pull quotes, stat card lines, and CTA text must pass the same four tests as all other Kay Malcolm content: originality, human, tone, pattern. Any line that reads like it came from a template  -  a brand account, a generic motivational post, a perfectly balanced sentence  -  rewrite it before passing it to NotebookLM. Pull quotes come verbatim from the draft (which was already graded). Poll questions and story-specific lines are new copy and must be graded before use.

---

## NotebookLM CLI Notes

- Always use: `/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli`
- Never use the bare `notebooklm` command (runs on Python 3.9, will fail)
- If auth fails: `notebooklm login` to re-authenticate
- Rate limiting: if generation fails, wait 5-10 min and retry once
