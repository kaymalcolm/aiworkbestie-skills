# AI For You — Substack Publish Skill

Publish an AI For You newsletter to Substack as a draft, with infographics uploaded to Substack's CDN. Reads from the `## SUBSTACK EDITION` section of the newsletter file.

## When This Skill Activates

**Explicit:** `/content-kit-substack-publish [post number]` or `/content-kit-substack-publish [path to newsletter file]`

**Legacy alias:** `/content-kit-substack` also activates this skill.

**Intent detection:** Recognize requests like:
- "Post the 1031 newsletter to Substack"
- "Publish the Substack draft for post 003"
- "Submit the newsletter as a Substack draft"

---

## Critical Background: Why Image Upload Must Happen Before add_image

The `mcp__substack__substack_add_image` tool accepts a `url` parameter. Passing a local file path does NOT work - Substack stores it as an `assetError` node, which displays as "IMAGE NOT FOUND" in the editor. The fix is to upload the image to Substack's CDN first using the `upload_image()` method from the substack Python client, then pass the resulting S3 URL to `substack_add_image`.

---

---

## Platform Detection

Before any file operations, detect the base directory:

```bash
python3 -c "import platform; print('/Users/kmalcolm/claude/iamkaymalcolm' if platform.system() == 'Darwin' else '/home/opc/iamkaymalcolm')"
```

- **Mac (Darwin):** `BASE_DIR = /Users/kmalcolm/claude/iamkaymalcolm`
- **OCI (Linux):** `BASE_DIR = /home/opc/iamkaymalcolm`

Use `BASE_DIR` for every file path in this skill.

---

## Autonomy Rules

**Before running anything**, ask the user which actions to perform:

> "Which of these do you want to publish?
> 1. Newsletter draft (Substack editor draft)
> 2. Substack note (public, posts immediately)
> 3. Both"

Wait for the answer. Run only the steps the user selects. If they say "both", run all steps. If they say "newsletter only" or "1", skip STEP 5. If they say "note only" or "2", skip STEPs 1–4 (still parse the newsletter for note text, then just post the note).

Only stop (without asking) if the newsletter file cannot be found.

---

## Workflow

### STEP 0 - Identify the target

- If a post number is given (e.g. `1031`), find the post folder: `{BASE_DIR}/posts/[POST_NUMBER]-*/`
- Find the newsletter file inside: match `[POST_NUMBER]-*newsletter*.md` or `[POST_NUMBER]-newsletter-*.md`
- Note the post folder path and the SHORT_NAME (slug from the folder name, e.g. `where-to-start-with-ai`)

**Look up infographics from the asset DB** — do NOT glob the filesystem. Query Oracle to get the latest registered infographic assets for this post that have a Google Drive record (i.e., are in `assets_images`). This guarantees we use the most recently generated file that is also backed up to Drive.

```python
import sys
sys.path.insert(0, "{BASE_DIR}/assets")
from oracle_db import get_connection

post_number = "[POST_NUMBER]"

con = get_connection()
cur = con.cursor()

# Latest mid infographic with a Drive record
# Must join through posts table — assets.post_id is an internal sequential ID, not the post number
cur.execute("""
    SELECT a.file_path, ai.gdrive_path
    FROM assets a
    JOIN assets_images ai ON ai.asset_id = a.id
    JOIN posts p ON p.id = a.post_id
    WHERE a.type = 'infographic-mid'
      AND a.pipeline = 'content-kit'
      AND p.post_number = :1
      AND a.file_path IS NOT NULL
    ORDER BY a.id DESC
    FETCH FIRST 1 ROWS ONLY
""", (post_number,))
mid_row = cur.fetchone()

# Latest download infographic with a Drive record
cur.execute("""
    SELECT a.file_path, ai.gdrive_path
    FROM assets a
    JOIN assets_images ai ON ai.asset_id = a.id
    JOIN posts p ON p.id = a.post_id
    WHERE a.type = 'infographic-download'
      AND a.pipeline = 'content-kit'
      AND p.post_number = :1
      AND a.file_path IS NOT NULL
    ORDER BY a.id DESC
    FETCH FIRST 1 ROWS ONLY
""", (post_number,))
dl_row = cur.fetchone()

con.close()

mid_path = mid_row[0] if mid_row else None
dl_path  = dl_row[0]  if dl_row  else None
print(f"IMAGE 1 (mid):      {mid_path}")
print(f"IMAGE 2 (download): {dl_path}")
```

If neither query returns a row, stop and tell the user no infographics with Drive records were found for this post — they may need to run `/content-kit-infographic [POST_NUMBER]` first. Use `mid_path` as IMAGE_1_PATH and `dl_path` as IMAGE_2_PATH in STEP 1.

---

### STEP 1 - Upload infographics to Substack CDN

Before creating the draft, upload both images to get real CDN URLs. Use this shell command:

```bash
source /Users/kmalcolm/.claude/.substackrc && /Users/kmalcolm/.claude/substack-mcp/venv/bin/python3 -c "
import os, sys
sys.path.insert(0, '/Users/kmalcolm/.claude/substack-mcp')
from substack_client import SubstackClient
client = SubstackClient(os.getenv('SUBSTACK_SID'), os.getenv('SUBSTACK_PUBLICATION'))
r1 = client.upload_image('IMAGE_1_PATH')
r2 = client.upload_image('IMAGE_2_PATH')
print(r1['url'])
print(r2['url'])
"
```

Store the two URLs as CDN_URL_1 and CDN_URL_2.

If either image file does not exist: skip it, set the URL to None, and continue. Note the missing image in the final report.

If the upload command fails entirely: stop and tell the user the credentials may need refreshing at `/Users/kmalcolm/.claude/.substackrc`.

---

### STEP 2 - Parse the newsletter file

Read the newsletter markdown file. If the file contains a `## SUBSTACK EDITION` section, read only that section (ignore everything outside it). Otherwise fall back to reading the full file.

Extract from the Substack Edition:

**Title:** Find the line `**Title:**` and strip the prefix. This is the email subject line.

**Subtitle:** Find the line `**Subtitle:**` and strip the prefix.

**Content segments:** Split the body at the two infographic placeholder markers. The markers look like:
- `**[INFOGRAPHIC` or `*Image:` or a line referencing an infographic file

Identify:
- `INTRO`: all content before the first infographic marker (everything from the byline through the intro text, up to but not including the infographic marker)
- `MAIN_CONTENT`: all content between the two infographic markers (all four moves with their code blocks)
- `CLOSING`: all content after the second infographic marker (closing text, sign-off, footer)

Within MAIN_CONTENT, identify code blocks (fenced with ``` in the markdown). These will be sent separately via `substack_add_code_block`. Extract each code block's text and the prose sections between them.

---

### STEP 3 - Build the draft in sequence

Build the Substack draft in this exact order to position images correctly:

**3a. Create the draft:**
Call `mcp__substack__substack_create_draft` with:
- title = Title from STEP 2
- subtitle = Subtitle from STEP 2
- body = INTRO text (plain prose, no code blocks)

Note the returned `draft_id`.

**3b. Add the first infographic (mid article):**
Call `mcp__substack__substack_add_image` with:
- draft_id = the draft ID
- url = CDN_URL_1
- alt = "AI For You - where to start with AI"

Skip this call if CDN_URL_1 is None.

**3c. Add MAIN_CONTENT (moves 1-4):**
For each section in MAIN_CONTENT, in order:
- If it is a prose paragraph: call `mcp__substack__substack_append_to_draft` with add_timestamp=false
- If it is a code block: call `mcp__substack__substack_add_code_block` with the code content

**3d. Add the second infographic (full reference guide):**
Call `mcp__substack__substack_add_image` with:
- draft_id = the draft ID
- url = CDN_URL_2
- alt = "AI For You - full reference guide"
- caption = Extract the caption line from the newsletter if present (usually "All four prompts in one place. Save it to your phone."), otherwise leave blank

Skip this call if CDN_URL_2 is None.

**3e. Add CLOSING:**
Call `mcp__substack__substack_append_to_draft` with the closing content, add_timestamp=false.

---

### STEP 4 - Register the newsletter draft in the asset DB

After creating the draft, register it in the asset DB:

```python
import oracledb, datetime, sys
from pathlib import Path

sys.path.insert(0, "{BASE_DIR}/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
post_number = "POST_NUMBER"
short_name = "SHORT_NAME"
draft_id_substack = DRAFT_ID
edit_url = f"https://iamkaymalcolm.substack.com/publish/post/{draft_id_substack}"

con = get_connection()
cur = con.cursor()

cur.execute(
    "SELECT id FROM assets WHERE type='substack-draft' AND post_number=:1",
    (post_number,)
)
existing = cur.fetchone()

if not existing:
    asset_var = cur.var(oracledb.NUMBER)
    cur.execute("""
        INSERT INTO assets (type, pipeline, short_name, description, status,
                            created_date, updated_date, file_path, post_number)
        VALUES ('substack-draft','content-kit',:1,:2,'ready',:3,:4,:5,:6)
        RETURNING id INTO :new_id""",
        [short_name + "-substack-draft",
         f"Substack draft for post {post_number}",
         today, today, edit_url, post_number, asset_var])
    asset_id = int(asset_var.getvalue())
    con.commit()
    print(f"Registered substack-draft as asset {asset_id}")
else:
    print(f"Already registered as asset {existing[0]}")

con.close()
```

Then refresh the registry:
```bash
/opt/homebrew/bin/python3.12 {BASE_DIR}/assets/manage-assets.py export-md
```

---

### STEP 5 - Post a Substack note

After the newsletter draft is created, write and post a short Substack note teasing it.

**Draft the note text** from the newsletter content:
- Use the Title and Subtitle (from STEP 2) as the hook
- Pull 1–2 concrete takeaways from INTRO or MAIN_CONTENT
- Keep it conversational and direct — Kay's voice, not marketing copy
- Target ~200 characters; hard max 400

Do not include a link (the draft isn't published yet — no live URL exists).

Call `mcp__substack__substack_post_note` with the drafted text.

---

### STEP 6 - Report back

Tell the user:
- The newsletter draft edit URL (clickable)
- The Substack note text that was posted (if applicable)
- Which images were uploaded (both / just one / none) and their CDN URLs
- Asset DB IDs registered

One short paragraph.

---

## Rules

- No confirmation prompts during the workflow
- Never pass a local file path as the `url` to `substack_add_image` - always upload first
- If parsing the newsletter structure is ambiguous, err on the side of putting content in the right order rather than failing
- Do not modify the newsletter file - it is read-only
