# AI For You — Gemini Green Screen Prompts Skill

Generate Gemini image prompts for green screen overlay assets used in AI For You B-roll videos. All images key out to neon green (#00FF00) for background removal in Descript or CapCut.

## When This Skill Activates

**Explicit:**
- `/ai-for-you-gemini [post number]` — generates 5 Gemini prompts for the post
- `/ai-for-you-gemini` — uses the most recently modified post folder

**Intent detection:** Recognize requests like:
- "Generate Gemini prompts for post 1041"
- "Create green screen images for the B-roll video"
- "Make Gemini image prompts for this post"
- "Generate the green screen overlays"

---

## Autonomy Rules

Run the full workflow automatically with no confirmation. Auto-detect the most recent post folder if no post number is given.

---

## People Representation Rules (Non-Negotiable)

These rules apply to **every prompt that includes a human figure**. No exceptions.

**Ethnicity:** Black, Hispanic, or Asian only. Never white. Rotate across the set so the full batch is diverse — not all one group.

**Gender:** Predominantly women. In a set of 5 images, 4 should feature women and 1 a man (or 3 women, 1 man, 1 no-person scene). Never more than 1-2 men in a 5-image set.

**Style — CRITICAL:**
- **Most images (3-4 of 5) must be photorealistic.** Use explicit style direction: "photorealistic," "real photograph style," "DSLR photo quality," "shot on camera." These look like real people, real faces, real lighting.
- **1-2 images may be illustrated/vector** — only when the concept genuinely suits an abstract or graphic treatment (e.g., a burst of icons, a symbolic scene with no face needed). Never default to vector. Only use it when it serves the concept better than a photo.
- Never describe a person as "illustrated," "cartoon," "vector," or "flat art" unless the image is intentionally in the 1-2 allowed illustrated slots.

**Photorealistic prompt construction:**
When writing a prompt for a realistic person, specify:
1. The ethnicity explicitly (e.g., "a Black woman," "a Latina woman," "an Asian man")
2. Relevant appearance detail that grounds the scene (e.g., "in a blazer," "natural curly hair," "business casual")
3. A photorealistic style tag: "photorealistic, real photograph, shot on camera, DSLR quality"
4. Lighting note: "natural window light," "soft studio lighting," "warm office lighting"
5. Expression or action that matches the scene concept

---

## Workflow

### STEP 0 — Identify the target post

- If a post number is given, find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/`
- If no argument, use the most recently modified post folder.
- Read the main draft file (matching `[POST_NUMBER]-*-draft-*.md`) OR the instagram-tiktok file (matching `[POST_NUMBER]-*-instagram-tiktok-*.md`) which contains the B-roll direction.
- Note the `POST_FOLDER` path and `POST_NUMBER`.

---

### STEP 1 — Extract B-roll scenes

Read the B-roll direction and identify 5 key moments that would benefit from a visual overlay. These should map to:
- The pain/problem scene (what life looks like before AI)
- The tool/action scene (what using AI looks like)
- The result/transformation scene (what life looks like after)
- Two supporting scenes tied to specific tips or points in the reel

Note each scene concept as a one-line description before writing the prompts.

---

### STEP 2 — Write 5 Gemini image prompts

For each scene, write one prompt. Follow all rules below.

**Universal prompt rules (every image):**
- Solid flat #00FF00 neon green background — no shadows, no gradients, no texture
- No text, no labels, no words, no logos anywhere in the image
- Square aspect ratio
- Clean, focused composition — one clear subject, no visual clutter

**People rules (see full detail above):**
- Black, Hispanic, or Asian — never white
- Majority women (4:1 or 3:2 ratio across the set)
- 3-4 prompts must be photorealistic; 1-2 may be illustrated/vector

**Prompt format:**
Write each prompt as a single paragraph. Include:
1. Scene concept and action (what is happening)
2. Person description: ethnicity, gender, relevant appearance, expression
3. Style: photorealistic OR illustrated (per the rules above)
4. Lighting (for photorealistic prompts)
5. The universal background/format line: "No text or labels anywhere in the image. Solid flat #00FF00 neon green background, no shadows, no gradients. Square aspect ratio."

**Label each prompt clearly:**
```
**Image [N] — [Scene name]**
[prompt paragraph]
```

---

### STEP 3 — Register in the asset DB

Before saving the file, register the asset to get the canonical ID and filename.

Derive `SHORT_NAME` from the post folder slug (e.g. folder `1041-ai-skills-why-use-them-work` → `ai-skills-why-use-them-work`). Use today's date as `DATE` (YYYY-MM-DD).

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
post_number = "[POST_NUMBER]"
short_name  = "[SHORT_NAME]"  # derived from post folder slug

con = get_connection()
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# Check if gemini-prompts asset already registered for this post (idempotent)
cur.execute(
    "SELECT id FROM assets WHERE type='gemini-prompts' AND post_number=:1", (post_number,)
)
existing = cur.fetchone()

if existing:
    asset_id = existing[0]
    print(f"Already registered as asset {asset_id}")
else:
    cur.execute("""
        INSERT INTO assets (type, pipeline, short_name, description, status,
                            created_date, updated_date, file_path, post_number)
        VALUES ('gemini-prompts','ai-for-you',:1,:2,'ready',:3,:4,:5,:6)""",
        (short_name + "-gemini-prompts",
         f"Gemini green screen image prompts for post {post_number}",
         today, today, '', post_number))
    asset_id = cur.lastrowid
    cur.execute(
        "INSERT INTO destinations (asset_id, platform, status) VALUES (:1,'production','pending')",
        (asset_id,)
    )
    # Link to parent draft asset
    cur.execute(
        "SELECT id FROM assets WHERE type='draft' AND post_number=:1", (post_number,)
    )
    draft_row = cur.fetchone()
    if draft_row:
        cur.execute(
            "INSERT INTO asset_links (from_id, to_id, relationship) VALUES (:1,:2,'gemini-prompts-for')",
            (draft_row[0], asset_id)
        )
    con.commit()
    print(f"Registered as asset {asset_id}")

con.close()
```

Note the ID as `ASSET_ID`. Build the canonical filename:
`[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-gemini-prompts-[DATE].md`

---

### STEP 4 — Save the output file

Save to the post folder (same directory as the instagram-tiktok and other platform files):
`/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-gemini-prompts-[DATE].md`

**File header:**
```
# [POST_NUMBER] — [Topic] — Gemini Green Screen Prompts

5 images for green screen overlay. Remove background in Descript or CapCut by keying out the neon green (#00FF00).

---
```

Then the 5 prompts, separated by `---`.

After saving, update the file_path in the DB:

```python
import oracledb, sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
con = get_connection()
cur = con.cursor()
cur.execute(
    "UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3",
    ("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[ASSET_ID]-[SHORT_NAME]-gemini-prompts-[DATE].md",
     "[DATE]", [ASSET_ID])
)
con.commit()
con.close()
```

Then refresh the registry:
```
/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

---

### STEP 5 — Report back

Tell the user:
- File path (full canonical name with asset ID)
- Asset ID registered in DB
- The 5 scene names chosen and which style (photo vs. illustrated) each uses
- The ethnicity/gender distribution across the set (confirm diversity rules were met)

---

## Quality Check

Before saving, confirm:
- [ ] 3-4 prompts are photorealistic (style tag present)
- [ ] 1-2 prompts may be illustrated — only if concept warrants it
- [ ] No white people anywhere in the set
- [ ] At least 3-4 women across the 5 images
- [ ] Ethnicities vary across the set (not all one group)
- [ ] Every prompt ends with the universal background line
- [ ] No text, labels, or gradients specified
- [ ] Every prompt maps to a B-roll scene in the direction

If any check fails, fix before saving.
