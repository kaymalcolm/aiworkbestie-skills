# AI For You — LinkedIn Document Skill

Generate a polished, branded LinkedIn document (PDF carousel) for an AI For You post.

**Two modes:**
- `generate` — creates 4-5 square slides (1080x1080px), removes branding, composites headshots at fixed positions. No PDF.
- `pdf` — compiles all `*linkedin-doc*` PNGs in the infographic folder into a final PDF.

---

## When This Skill Activates

**Explicit:**
- `/content-kit-linkedin-doc [post number]` — runs generate mode
- `/content-kit-linkedin-doc [post number] generate` — generate mode
- `/content-kit-linkedin-doc [post number] pdf` — pdf mode

**Intent detection:**
- "Make the LinkedIn document for post 1031"
- "Generate LinkedIn doc slides for post 004"
- "Convert the LinkedIn doc slides to PDF"
- "Build the LinkedIn carousel PDF for post 1031"

---

## Autonomy Rules

Run the full workflow with no confirmation. Auto-detect the most recent draft if no post number given. Slides take 5-10 min per image to generate — fire all generates before waiting on any.

---

## MODE 1: GENERATE

### STEP 0 — Identify the target draft

- Find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/`
- Find the draft file inside it matching `[POST_NUMBER]-*-draft-*.md`
- Also check for a `### LINKEDIN DOCUMENT BRIEF` section in the draft — use it if present. Otherwise derive from the draft's prompts/moves/carousel sections.
- Note `POST_FOLDER` (e.g. `1031-where-to-start-with-ai`), `POST_NUMBER`, `SHORT_NAME` (topic slug from folder name).

---

### STEP 1 — Extract LinkedIn doc brief from draft

Read the full draft. Pull:

1. **Hook / cover headline** — the pain point framing (not the solution). Look at the hook options or the carousel slide 1 headline. Use the one that is most scroll-stopping as a standalone LinkedIn document cover.
2. **Featured prompt (Slide 2)** — the single most copy-pasteable, highest-value prompt from the draft. Usually the one with the most detailed instructions or the one featured in Move 02 / the carousel detail slide. Extract verbatim prompt text, the move label, and the time estimate.
3. **Teaser list (Slide 3)** — the remaining moves/prompts (everything NOT featured in Slide 2). For each: Move number, title (bold label), one-sentence description.
4. **CTA slide content (Slide 4)** — the newsletter subscribe CTA. Always:
   - Headline: "Get all [N] prompts + the full reference guide."
   - Subscribe copy: "Subscribe to AI For You — my newsletter, right here on LinkedIn."
   - Body: "Access the complete toolkit featuring [list the 2-3 tools from the draft]."
   - CTA bar text: "AI For You Newsletter — Subscribe on LinkedIn"

Confirm total slide count (always 4 for posts with 4 prompts where 1 is featured, or 5 if there are enough prompts to feature 2).

---

### STEP 2 — Create NotebookLM notebook

```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli create "AI For You #[POST_NUMBER] — LinkedIn Document" --json
```

Note the notebook ID as `NB_ID`.

---

### STEP 3 — Add sources and wait

Run both adds in parallel:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add [DRAFT_FILE_PATH] -n [NB_ID] --json
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source add /Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md -n [NB_ID] --json
```

Wait for both in parallel:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_1] -n [NB_ID] --timeout 120
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli source wait [SRC_2] -n [NB_ID] --timeout 120
```

---

### STEP 4 — Generate all slides

**Always use:** `/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli`
**Always use `--orientation square`** for all slides (1080x1080).

Fire all generate commands before waiting on any — they run in parallel inside NotebookLM.

---

#### Slide 1 — Cover

```
Create a square (1080x1080px) cover slide for an AI For You LinkedIn document. This is the first slide of a multi-slide document carousel and must stop the scroll.

DESIGN:
- Background: Champagne (#F0E2C8) or soft blush-to-champagne gradient. NO dark backgrounds.
- Top-left badge: "AI FOR YOU | AI Work Bestie" — bold caps, gold/amber (#F4A261). Small, not oversized.
- Top-right: "1 of [TOTAL_SLIDES]" — small, muted text, same plum or gray tone as body.
- Large bold hook headline: deep plum (#2D1B2E) or near-black (#1A1A1A). This is the ONLY prominent element.
- CRITICAL — HEADSHOT RESERVED ZONE: Leave a completely blank circular area (200px diameter) in the lower-right corner of the slide, centered at approximately (860px from left, 820px from top). NO text, NO graphics, NO decorative elements may overlap or enter this zone. The zone boundary is a circle with radius 100px centered at (860, 820). Leave it empty — a headshot will be composited there.
- Bottom of slide: "@iamkaymalcolm" in very small muted text.
- NO em dashes anywhere. Use a hyphen ( - ) instead.
- NO headshot, NO circular photo, NO avatar. Leave the reserved zone completely blank.
- Soft, feminine, premium. Not a template. Not clip art.

CONTENT:
Hook headline: [HOOK FROM DRAFT — pain point framing, not the solution]
Slide count: 1 of [TOTAL_SLIDES]
Bottom handle: @iamkaymalcolm
```

Run:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation square --detail detailed --style professional "[SLIDE_1_PROMPT]" -n [NB_ID] --json
```

Note artifact ID as `ART_COVER`.

---

#### Slide 2 — Featured Prompt

```
Create a square (1080x1080px) content slide for an AI For You LinkedIn document. This slide shows the single most copy-pasteable prompt from the series — the one readers will screenshot.

DESIGN:
- Background: Same champagne/blush palette as the cover. Warm, soft, feminine. NO dark backgrounds.
- Top-left badge: "AI FOR YOU | AI Work Bestie" — small, bold caps, gold/amber (#F4A261).
- Top-right: "[N] of [TOTAL_SLIDES]" — small, muted.
- Move label line: gold/amber (#F4A261), bold — "[MOVE LABEL] — [MOVE TITLE]. | [TIME ESTIMATE]"
- Subheadline below move label: short descriptive line (1 line max).
- Prompt block: the full verbatim prompt text in a slightly lighter-weight font, inside a soft rounded rectangle or card (cream/light background, subtle shadow). Left-aligned. Readable at mobile size.
- Bottom CTA line: "Copy this. Open Claude or ChatGPT. Paste." — bold, centered.
- Bottom handle: "@iamkaymalcolm" — very small, muted.
- NO em dashes. NO headshot. NO circular photo anywhere.

CONTENT:
Move label: [MOVE_LABEL — e.g. "Move 02 - Any Meeting. Any Document."]
Time estimate: [e.g. "5 min"]
Subheadline: [one-line descriptor]
Prompt text (verbatim):
[FULL PROMPT TEXT — copy-pasteable]
Bottom CTA: "Copy this. Open Claude or ChatGPT. Paste."
```

Run:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation square --detail detailed --style professional "[SLIDE_2_PROMPT]" -n [NB_ID] --json
```

Note artifact ID as `ART_CONTENT`.

---

#### Slide 3 — Teaser (remaining moves)

```
Create a square (1080x1080px) teaser slide for an AI For You LinkedIn document. This slide previews the remaining prompts from the series (the ones NOT shown in the previous detailed slide).

DESIGN:
- Background: Blush pink (#F7CAD0) or warm lavender (#E8D5F5). Different enough from cover to signal a new section, but still in brand palette.
- Top-left badge: "AI FOR YOU | AI Work Bestie" — small, bold caps, gold/amber (#F4A261).
- Top-right: "[N] of [TOTAL_SLIDES]" — small, muted.
- Large bold headline: "[N] more inside the newsletter." — deep plum or near-black, very large, fills the upper half.
- For each remaining move, a horizontal row with:
  - Move label: "[MOVE X]" in gold/amber, bold
  - Move title on next line: bold, deep plum
  - One-sentence description: regular weight, smaller
  - Thin divider line between rows (rose gold or plum, 30% opacity)
  - Optional: a simple geometric icon or illustration (right side of each row) — keep it minimal and feminine. An illustrated folder, envelope, or circuit motif. If any illustrated human figure appears, she is an African American woman with collarbone-length curly natural hair and glasses.
- Bottom: "Last slide →" in small muted text + "@iamkaymalcolm"
- NO em dashes. NO headshot. NO numbered emoji (1️⃣ 2️⃣). Use plain move labels.

CONTENT:
Headline: "[N] more inside the newsletter."
[For each remaining move:]
Move [N]
[Title]
[One-sentence description]
```

Run:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation square --detail detailed --style professional "[SLIDE_3_PROMPT]" -n [NB_ID] --json
```

Note artifact ID as `ART_TEASER`.

---

#### Slide 4 — CTA (always last slide)

```
Create a square (1080x1080px) CTA slide for an AI For You LinkedIn document. This is the final slide — it drives newsletter subscriptions.

DESIGN:
- Background: Champagne (#F0E2C8) or blush-to-champagne gradient — matches the cover.
- Top-left badge: "AI FOR YOU | AI Work Bestie" — small, gold/amber (#F4A261).
- Top-right: "[TOTAL_SLIDES] of [TOTAL_SLIDES]" — small, muted.
- Large bold CTA headline in deep plum (#2D1B2E): "Get all [N] prompts + the full reference guide."
- Subscribe body copy below: "Subscribe to AI For You — my newsletter, right here on LinkedIn."
- Access line: "Access the complete toolkit featuring [tool list]."
- CRITICAL — HEADSHOT RESERVED ZONE: Leave a completely blank circular area (220px diameter) centered at approximately (810px from left, 430px from top). NO text, NO graphics, NO decorative elements may enter this zone. The zone boundary is a circle with radius 110px centered at (810, 430). Leave it completely empty — a headshot will be composited there.
- CRITICAL — NAME AREA: Directly below the reserved zone (approximately y=560 to y=640), place this text in a left-aligned or centered block:
  "Kay Malcolm"  — bold, deep plum or near-black, larger weight
  "VP @ Oracle | LinkedIn Learning Instructor specializing in AI Agents and Agentic Memory" — regular weight, smaller
  "Views are my own" — italic, smallest weight
  "Professional insights delivered from a personal perspective based on 20 years in enterprise technology" — very small, muted
- Bottom bar: Full-width bar with "AI For You Newsletter — Subscribe on LinkedIn" in contrasting text (white or plum on gold/amber, OR white on deep plum fill).
- Bottom handle: "@iamkaymalcolm" — very small, below bar.
- NO em dashes. NO headshot, NO circular photo, NO avatar. Leave the reserved zone blank.

CONTENT:
Headline: "Get all [N] prompts + the full reference guide."
Subscribe copy: "Subscribe to AI For You — my newsletter, right here on LinkedIn."
Access line: "Access the complete toolkit featuring [tool names from draft]."
Name: Kay Malcolm
Title: VP @ Oracle | LinkedIn Learning Instructor specializing in AI Agents and Agentic Memory
Disclaimer: Views are my own
Footer text: Professional insights delivered from a personal perspective based on 20 years in enterprise technology
CTA bar: "AI For You Newsletter — Subscribe on LinkedIn"
```

Run:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli generate infographic --orientation square --detail detailed --style professional "[SLIDE_4_PROMPT]" -n [NB_ID] --json
```

Note artifact ID as `ART_CTA`.

---

### STEP 5 — Register in asset DB and determine filenames

Before downloading, register a single `linkedin-doc-slides` asset for this post to get the asset ID.

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name = "[SHORT_NAME]"  # derived from folder slug
post_number = "[POST_NUMBER]"
total_slides = [TOTAL_SLIDES]  # e.g. 4

con = get_connection()
cur = con.cursor()

asset_var = cur.var(oracledb.NUMBER)
cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_number)
    VALUES ('linkedin-doc-slides','content-kit',:1,:2,
            'in-progress',:3,:4,:5)
    RETURNING id INTO :new_id""",
    [short_name + "-linkedin-doc-slides",
     f"LinkedIn document slides ({total_slides} slides) for post {post_number}",
     today, today, post_number, asset_var])
asset_id = int(asset_var.getvalue())
cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'linkedin','pending')", (asset_id,))

cur.execute("SELECT id FROM assets WHERE type='draft' AND post_number=:1", (post_number,))
draft_row = cur.fetchone()
if draft_row:
    cur.execute("INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'linkedin-doc-for')", (draft_row[0], asset_id))

con.commit()
con.close()
print(f"ASSET_ID={asset_id}")
```

Note as `ASSET_ID`. Build canonical filenames (zero-padded slide numbers):
- Cover:   `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-slide01-[DATE].png`
- Content: `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-slide02-[DATE].png`
- Teaser:  `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-slide03-[DATE].png`
- CTA:     `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-slide04-[DATE].png`

Save destination: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/`
Create the folder if it doesn't exist.

---

### STEP 6 — Wait and download all slides

Wait in parallel, then download each:

```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ART_COVER] -n [NB_ID] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ART_CONTENT] -n [NB_ID] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ART_TEASER] -n [NB_ID] --timeout 600
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli artifact wait [ART_CTA] -n [NB_ID] --timeout 600
```

Then download each once its wait completes:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic [COVER_PATH] -a [ART_COVER] -n [NB_ID]
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic [CONTENT_PATH] -a [ART_CONTENT] -n [NB_ID]
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic [TEASER_PATH] -a [ART_TEASER] -n [NB_ID]
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli download infographic [CTA_PATH] -a [ART_CTA] -n [NB_ID]
```

---

### STEP 7 — Remove NotebookLM branding and resize all slides to 1080x1080

NotebookLM generates at its own native resolution (typically 2048x2048 for square). After removing the logo, resize every slide to exactly 1080x1080px. This is the canonical LinkedIn document size and ensures the fixed headshot pixel coordinates in STEP 8 are always correct.

Run this block once for all 4 slides (replace paths with actual file paths):

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image
import numpy as np

TARGET_SIZE = (1080, 1080)

def clean_slide(filepath):
    img = Image.open(filepath).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Remove NotebookLM logo: ~55px tall x ~300px wide at 1536px reference width
    scale = w / 1536
    logo_h = int(55 * scale)
    logo_w = int(300 * scale)
    sample_start = h - logo_h - 50
    sample_end   = h - logo_h
    for i in range(logo_h):
        source_y = sample_start + (i % (sample_end - sample_start))
        arr[h - logo_h + i, w - logo_w:w, :] = arr[source_y, w - logo_w:w, :]

    # Resize to 1080x1080
    result = Image.fromarray(arr, "RGB").resize(TARGET_SIZE, Image.LANCZOS)
    result.save(filepath, quality=95)
    print(f"Cleaned + resized to 1080x1080: {filepath}")

clean_slide("[COVER_PATH]")
clean_slide("[CONTENT_PATH]")
clean_slide("[TEASER_PATH]")
clean_slide("[CTA_PATH]")
PYEOF
```

---

### STEP 8 — Composite Kay's headshot at fixed positions

**Run this Python script after all slides are downloaded and branding is removed.**

Headshot positions are hardcoded for 1080x1080 canvases. These are exact — do NOT adjust based on slide content.

- **Cover slide**: headshot circle center at **(960, 960)**, diameter **180px**
- **CTA slide**: headshot circle center at **(900, 525)**, diameter **190px**
- Content and Teaser slides: **no headshot**

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image, ImageDraw, ImageOps
import numpy as np

HEADSHOT_PATH = "/Users/kmalcolm/Documents/headshots/chosen-headshots/5M1A8962.JPG"
COVER_PATH   = "[COVER_PATH]"
CTA_PATH     = "[CTA_PATH]"

def load_headshot(diameter):
    """Load, EXIF-correct, center-crop, resize, and circularize the headshot."""
    hs = Image.open(HEADSHOT_PATH)
    hs = ImageOps.exif_transpose(hs)  # CRITICAL: raw file is 6720x4480 landscape, EXIF rotates to portrait
    hs = hs.convert("RGBA")
    w, h = hs.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top  = (h - min_dim) // 2
    # Crop top-biased: portrait shots have face in upper portion
    # Pull the crop up by 15% so the face is centered rather than the chest
    top = max(0, top - int(min_dim * 0.15))
    top = min(top, h - min_dim)
    hs = hs.crop((left, top, left + min_dim, top + min_dim))
    hs = hs.resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new('L', (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter - 1, diameter - 1], fill=255)
    hs.putalpha(mask)
    return hs

def composite_headshot(slide_path, center_x, center_y, diameter):
    """Composite circular headshot with gold ring onto a slide at exact fixed coordinates."""
    slide = Image.open(slide_path).convert("RGBA")
    w, h = slide.size

    # Gold ring: #F4A261, ring_width = 7% of diameter
    ring_w = max(6, int(diameter * 0.07))
    ring_size = diameter + ring_w * 2
    ring = Image.new('RGBA', (ring_size, ring_size), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse([0, 0, ring_size - 1, ring_size - 1], fill=(244, 162, 97, 255))  # gold #F4A261
    ring_draw.ellipse([ring_w, ring_w, ring_size - ring_w - 1, ring_size - ring_w - 1], fill=(0, 0, 0, 0))

    hs = load_headshot(diameter)

    # Paste ring first (behind headshot)
    ring_x = center_x - ring_size // 2
    ring_y = center_y - ring_size // 2
    slide.paste(ring, (ring_x, ring_y), ring)

    # Paste headshot centered at (center_x, center_y)
    hs_x = center_x - diameter // 2
    hs_y = center_y - diameter // 2
    slide.paste(hs, (hs_x, hs_y), hs)

    slide.convert("RGB").save(slide_path, quality=95)
    print(f"Headshot composited at ({center_x}, {center_y}) d={diameter}px → {slide_path}")

# Cover: lower-right corner — pixel-sampled clear zone (880-1080, 860-1080)
composite_headshot(COVER_PATH, center_x=960, center_y=960, diameter=180)

# CTA: right column mid — pixel-sampled clear zone (740-1060, 400-650)
composite_headshot(CTA_PATH, center_x=900, center_y=525, diameter=190)
PYEOF
```

---

### STEP 9 — Update asset DB, upload to Drive, and export registry

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import oracledb, datetime, subprocess, json, os, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
post_folder = "[POST_FOLDER]"
post_number = "[POST_NUMBER]"
asset_id    = [ASSET_ID]
cover_path  = "[COVER_PATH]"   # use the cover path as the representative file

# Update asset DB file_path and status
con = get_connection()
cur = con.cursor()
cur.execute("UPDATE assets SET file_path=:1, status='ready', updated_date=:2 WHERE id=:3",
    (cover_path, today, asset_id))
con.commit()
con.close()

# Upload all slide PNGs to Drive
ROOT = "1ZISATI9hlcdRK0dpWBRoLcUWR1Wn19oe"
infog_dir = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic")
slide_files = sorted(infog_dir.glob("*linkedin-doc-slide*.png"))

subprocess.run(["rclone", "mkdir", f"gdrive:posts/{post_folder}/infographic",
                "--drive-root-folder-id", ROOT], check=True)
for fp in slide_files:
    subprocess.run(["rclone", "copy", str(fp), f"gdrive:posts/{post_folder}/infographic",
                    "--drive-root-folder-id", ROOT], check=True)

# Get infographic subfolder Drive ID
r = subprocess.run(["rclone", "lsjson", f"gdrive:posts/{post_folder}",
                    "--drive-root-folder-id", ROOT, "--dirs-only"],
                   capture_output=True, text=True, check=True)
folder_id = next(e["ID"] for e in json.loads(r.stdout) if e["Name"] == "infographic")

# INSERT into assets_images (cover path as representative gdrive_path for this asset)
gdrive_path = f"posts/{post_folder}/infographic/{os.path.basename(cover_path)}"
con = get_connection()
cur = con.cursor()
cur.execute("INSERT INTO assets_images (asset_id, gdrive_path, gdrive_folder_id, uploaded_at) "
            "VALUES (:1,:2,:3,CURRENT_TIMESTAMP)",
            (asset_id, gdrive_path, folder_id))
con.commit()
con.close()
print(f"Drive: {len(slide_files)} slides → infographic folder {folder_id}")
PYEOF

/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

---

### STEP 10 — Report

Tell the user:
- Total slides generated and file paths
- Notebook ID for reference
- Show all 4 slides inline
- Confirm headshot was composited on cover and CTA at fixed positions
- Remind them to run Mode 2 (pdf) when ready: `/content-kit-linkedin-doc [POST_NUMBER] pdf`

---

## MODE 2: PDF

### STEP P0 — Find the post folder and all slide PNGs

- Find: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/infographic/`
- Glob for all files matching `*linkedin-doc-slide*.png` in that folder (NOT in archive/).
- Sort by filename (slide01, slide02... are zero-padded so lexicographic sort = slide order).
- Confirm slide count and list them to yourself before proceeding.

---

### STEP P1 — Compile to PDF

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
from PIL import Image
from pathlib import Path
import glob, re

infographic_dir = Path("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic")
output_pdf = infographic_dir / "[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-[DATE].pdf"

# Find and sort slide files
slide_files = sorted(
    [f for f in infographic_dir.glob("*linkedin-doc-slide*.png")],
    key=lambda p: re.search(r'slide(\d+)', p.name).group(1) if re.search(r'slide(\d+)', p.name) else p.name
)

if not slide_files:
    raise FileNotFoundError("No *linkedin-doc-slide*.png files found")

print(f"Found {len(slide_files)} slides:")
for f in slide_files:
    print(f"  {f.name}")

images = [Image.open(f).convert("RGB") for f in slide_files]
first = images[0]
rest  = images[1:]
first.save(output_pdf, save_all=True, append_images=rest)
print(f"PDF saved: {output_pdf}  ({len(images)} pages)")
PYEOF
```

---

### STEP P2 — Register PDF in asset DB

Look up the existing `linkedin-doc-slides` asset for this post. Create a new sibling asset for the PDF:

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
short_name   = "[SHORT_NAME]"
post_number  = "[POST_NUMBER]"
pdf_path     = "[OUTPUT_PDF_PATH]"

con = get_connection()
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

cur.execute("""
    INSERT INTO assets (type, pipeline, short_name, description, status,
                        created_date, updated_date, post_number, file_path)
    VALUES ('linkedin-doc-pdf','content-kit',:1,:2,
            'ready',:3,:4,:5,:6)""",
    (short_name + "-linkedin-doc",
     f"LinkedIn document PDF for post {post_number}",
     today, today, post_number, pdf_path))
pdf_id = cur.lastrowid
cur.execute("INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'linkedin','pending')", (pdf_id,))

cur.execute("SELECT id FROM assets WHERE type='draft' AND post_number=:1", (post_number,))
draft_row = cur.fetchone()
if draft_row:
    cur.execute("INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'linkedin-doc-for')", (draft_row[0], pdf_id))

con.commit()
con.close()
print(f"PDF_ASSET_ID={pdf_id}")
PYEOF

/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

---

### STEP P3 — Report

Tell the user:
- PDF path
- Total pages (slides)
- Asset ID
- Upload instructions: LinkedIn → Start a post → Document → select PDF → Add a title for the document (use the hook headline)

---

## File Naming Convention

| File | Pattern |
|------|---------|
| Slide PNGs | `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-slide[NN]-[DATE].png` |
| PDF | `[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-linkedin-doc-[DATE].pdf` |

- Slide numbers are zero-padded two digits: `slide01`, `slide02`, `slide03`, `slide04`
- All save to: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/infographic/`
- Never save to archive/, strategy/, or content-drafts/

---

## Design Spec Summary (1080x1080)

| Element | Value |
|---------|-------|
| Canvas | 1080 x 1080 px, square |
| Background | Champagne #F0E2C8, blush #F7CAD0, lavender #E8D5F5, or blush-to-champagne gradient. Vary. No dark. |
| Badge | "AI FOR YOU \| AI Work Bestie" — bold caps, gold/amber #F4A261, top-left |
| Title | Deep plum #2D1B2E or near-black #1A1A1A |
| Accent | Gold/amber #F4A261 |
| Dividers | Rose gold or soft plum, 30% opacity |
| Bottom bar | Deep plum or gold/amber fill |
| Handle | @iamkaymalcolm — small, muted, bottom-right |
| Em dashes | NEVER. Replace with hyphen ( - ) always. |
| Headshot | Composited programmatically — NOT by NotebookLM |
| Cover headshot center | (960, 960) px, diameter 180 px — lower-right clear zone |
| CTA headshot center | (900, 525) px, diameter 190 px — right-column mid clear zone |
| Ring color | Gold #F4A261, width = 7% of diameter |

---

## NotebookLM CLI Notes

- Always use: `/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli`
- Never use bare `notebooklm` command (runs Python 3.9, will fail)
- `--orientation square` for all slides
- If auth fails: `notebooklm login`
- Rate limiting: if generation fails, wait 5-10 min and retry once
