# AI For You — Sync Skill

Pull the current DB state of one post's content and overwrite local `.md` files with the DB version. Operates at the item-type level — each item type (reel_script, instagram, newsletter, etc.) syncs to its own dedicated file. Gate is on `asset_item_status.status`, not `assets.status`.

## When This Skill Activates

**Explicit:** User types `/ai-for-you-sync [post_number]` — e.g. `/ai-for-you-sync 1039`

Also responds to `/ai-for-you-refresh [post_number]` (legacy alias).

**Intent detection:** Recognize requests like:
- "Sync post 1039 from the database"
- "Pull the latest DB content for post 1039 down to local"
- "Overwrite my local files for post 1039 with what's in ADB"
- "Refresh post 1039 from the database"

---

## Autonomy Rules

Run all steps automatically with no confirmation unless:
- The post_number is not found in the DB (ask once)
- No buckets qualify (all item_types DRAFT — report and stop)

---

## Connection

```
Helper : /Users/kmalcolm/claude/iamkaymalcolm/assets/oracle_db.py
Runtime: python3.12
```

Python preamble for all DB queries:
```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
```

---

## File Buckets

Each bucket maps one or more `item_type` values to a single local file. A bucket syncs if any of its item_types has `status IN ('EDITED', 'APPROVED')` in `asset_item_status`.

| Bucket | File scan pattern | item_types | DB sources |
|---|---|---|---|
| `script` | `-script-` in filename | reel_script, carousel | post_scripts, post_slides, post_keywords |
| `newsletter` | `newsletter` in filename | newsletter, substack_note, linkedin | post_captions (substack-newsletter, substack-note, linkedin-newsletter) |
| `instagram` | `-instagram-` (not `instagram-tiktok`) | instagram | post_captions platform='instagram' |
| `tiktok` | `-tiktok-` in filename | tiktok | post_captions platform='tiktok' |
| `threads` | `-threads-` in filename | threads | post_captions platform='threads' |
| `twitter` | `-twitter-` in filename | twitter | post_captions platform='twitter' |
| `youtube-short` | `-youtube-short-` in filename | youtube_short | post_captions platform='youtube-short' |
| `brief` | `-brief-` in filename | brief | post_scripts.brief |
| `gemini` | `-gemini-` in filename | gemini | post_scripts.gemini_prompts |
| `manychat` | `-manychat-` in filename | manychat | post_keywords |

---

## Workflow

### STEP 1 — Look up the script asset and item statuses

`post_number` is VARCHAR2 on the `posts` table — cast to string. Accept both the old type name and the new one:

```python
con = get_connection()
cur = con.cursor()

cur.execute("""
    SELECT a.id, a.type, a.short_name, a.status, a.file_path
    FROM assets a
    JOIN posts p ON p.id = a.post_id
    WHERE p.post_number = :pn
      AND a.pipeline = 'ai-for-you'
      AND a.type IN ('script', 'instagram-tiktok')
""", [str(post_number)])
row = cur.fetchone()

if not row:
    # tell user: No script asset found for post {post_number}. Stop.
    pass

asset = {"id": row[0], "type": row[1], "short_name": row[2],
         "status": row[3], "file_path": row[4]}

cur.execute("""
    SELECT item_type, status
    FROM asset_item_status
    WHERE asset_id = :1
""", [asset["id"]])
item_statuses = {r[0]: r[1] for r in cur.fetchall()}
# Missing item_types default to 'DRAFT'

con.close()
```

If no asset row: tell user "No script asset found for post {post_number} in the ai-for-you pipeline." Stop.

---

### STEP 2 — Determine which buckets to sync

```python
BUCKETS = {
    'script':        {'item_types': {'reel_script', 'carousel'}},
    'newsletter':    {'item_types': {'newsletter', 'substack_note', 'linkedin'}},
    'instagram':     {'item_types': {'instagram'}},
    'tiktok':        {'item_types': {'tiktok'}},
    'threads':       {'item_types': {'threads'}},
    'twitter':       {'item_types': {'twitter'}},
    'youtube-short': {'item_types': {'youtube_short'}},
    'brief':         {'item_types': {'brief'}},
    'gemini':        {'item_types': {'gemini'}},
    'manychat':      {'item_types': {'manychat'}},
}

APPROVED = {'EDITED', 'APPROVED'}

to_sync = []
skipped = []

for bucket_name, bucket in BUCKETS.items():
    qualifying = [t for t in bucket['item_types']
                  if item_statuses.get(t, 'DRAFT') in APPROVED]
    if qualifying:
        to_sync.append({'bucket': bucket_name, 'approved_types': qualifying})
    else:
        skipped.append({'bucket': bucket_name,
                        'statuses': {t: item_statuses.get(t, 'DRAFT')
                                     for t in bucket['item_types']}})
```

If `to_sync` is empty: report what was found and skipped, then stop.

---

### STEP 3 — Pull all DB content in one pass

Run all four queries once. NULL fields → empty string.

```python
con = get_connection()
cur = con.cursor()
asset_id = asset["id"]

# Scripts
cur.execute("""
    SELECT reel_script, companion_script, brief, gemini_prompts,
           youtube_long, youtube_short,
           reel_ending_instagram, reel_ending_tiktok, reel_ending_linkedin
    FROM post_scripts WHERE asset_id = :1
""", [asset_id])
sr = cur.fetchone()
scripts = {}
if sr:
    fields = ['reel_script','companion_script','brief','gemini_prompts',
              'youtube_long','youtube_short',
              'reel_ending_instagram','reel_ending_tiktok','reel_ending_linkedin']
    scripts = {f: (sr[i] or '') for i, f in enumerate(fields)}

# Slides
cur.execute("""
    SELECT slide_number, headline, body
    FROM post_slides WHERE asset_id = :1
    ORDER BY slide_number
""", [asset_id])
slides = [{"slide_number": r[0], "headline": r[1] or '', "body": r[2] or ''}
          for r in cur.fetchall()]

# Captions — keyed by platform
cur.execute("""
    SELECT platform, caption, hashtags
    FROM post_captions WHERE asset_id = :1
    ORDER BY platform
""", [asset_id])
captions = {r[0]: {"caption": r[1] or '', "hashtags": r[2] or ''}
            for r in cur.fetchall()}

# Keywords
cur.execute("""
    SELECT comment_keyword, pinned_comment, manychat_notes
    FROM post_keywords WHERE asset_id = :1
""", [asset_id])
kr = cur.fetchone()
keywords = {"comment_keyword": kr[0] or '', "pinned_comment": kr[1] or '',
            "manychat_notes": kr[2] or ''} if kr else {}

con.close()
```

---

### STEP 4 — Resolve local file path per bucket

Post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/{post_number}-{short_name}/`

For each bucket in `to_sync`, find the local file by scanning the post folder for `.md` files matching the bucket's pattern:

- `script`: filename contains `-script-`
- `newsletter`: filename contains `newsletter`
- `instagram`: filename contains `-instagram-` AND does NOT contain `instagram-tiktok`
- `tiktok`: filename contains `-tiktok-`
- `threads`: filename contains `-threads-`
- `twitter`: filename contains `-twitter-`
- `youtube-short`: filename contains `-youtube-short-`
- `brief`: filename contains `-brief-`
- `gemini`: filename contains `-gemini-`
- `manychat`: filename contains `-manychat-`

Use the first match. If no match, construct a new path:
```
{post_folder}/{post_number}-{short_name}-{bucket_name}-{today YYYY-MM-DD}.md
```
Create the post folder if it does not exist.

---

### STEP 5 — Build file content per bucket

Write only sections with non-empty content.

**`script` bucket:**
```
# AI For You — {short_name}

**Post:** {post_number}
**Asset ID:** {asset_id}
**Type:** script
**Status:** {asset status}
**Synced:** {today}

---

## B-ROLL DIRECTION

{scripts.reel_script}

**[Instagram ending]**
{scripts.reel_ending_instagram}

**[TikTok ending]**
{scripts.reel_ending_tiktok}

**[LinkedIn ending]**
{scripts.reel_ending_linkedin}

---

## CAROUSEL ({N} slides)

| Slide | Headline | Body |
|-------|----------|------|
| 1 | {headline} | {body} |
...

---

## KEYWORDS

**Comment keyword:** {keywords.comment_keyword}

**Pinned comment:**
{keywords.pinned_comment}

**ManyChat notes:**
{keywords.manychat_notes}
```
Omit any ending block whose value is empty. Omit CAROUSEL section if no slides. Omit KEYWORDS section if all keyword fields are empty.

**`newsletter` bucket:**
```
# AI For You — {short_name} — Newsletter

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## SUBSTACK NEWSLETTER

{captions['substack-newsletter'].caption}

---

## SUBSTACK NOTE

{captions['substack-note'].caption}

---

## LINKEDIN NEWSLETTER

{captions['linkedin-newsletter'].caption}
```
Omit any section whose caption is empty.

**`instagram` bucket:**
```
# AI For You — {short_name} — Instagram

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## CAPTION

{captions['instagram'].caption}

---

## HASHTAGS

{captions['instagram'].hashtags}
```
Omit HASHTAGS section if empty.

**`tiktok` bucket:**
```
# AI For You — {short_name} — TikTok

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## CAPTION

{captions['tiktok'].caption}

---

## HASHTAGS

{captions['tiktok'].hashtags}
```

**`threads` bucket:**
```
# AI For You — {short_name} — Threads

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## THREADS POSTS

{captions['threads'].caption}
```

**`twitter` bucket:**
```
# AI For You — {short_name} — Twitter/X

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## TWITTER/X POST

{captions['twitter'].caption}
```

**`youtube-short` bucket:**
```
# AI For You — {short_name} — YouTube Short

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## DESCRIPTION

{captions['youtube-short'].caption}

---

## TAGS

{captions['youtube-short'].hashtags}
```

**`brief` bucket:**
```
# AI For You — {short_name} — Brief

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## BRIEF

{scripts.brief}
```

**`gemini` bucket:**
```
# AI For You — {short_name} — Gemini Prompts

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## GEMINI PROMPTS

{scripts.gemini_prompts}
```

**`manychat` bucket:**
```
# AI For You — {short_name} — ManyChat

**Post:** {post_number}
**Asset ID:** {asset_id}
**Synced:** {today}

---

## KEYWORDS

**Comment keyword:** {keywords.comment_keyword}

**Pinned comment:**
{keywords.pinned_comment}

**ManyChat notes:**
{keywords.manychat_notes}
```

---

### STEP 6 — Delete old file and write new (per bucket)

For each bucket in `to_sync`:

If an existing file was found in Step 4:
- Delete it: `rm "{old_path}"`
- Write the new file to the SAME path.

If no file existed:
- Write to the constructed path.

---

### STEP 7 — Update `assets.file_path` in DB (script bucket only)

After writing, if the script bucket file path differs from `assets.file_path` (or `file_path` was NULL):
```python
con = get_connection()
cur = con.cursor()
cur.execute(
    "UPDATE assets SET file_path = :1 WHERE id = :2",
    [script_file_path, asset_id]
)
con.commit()
con.close()
```

Only update `file_path` for the script bucket. Other bucket files are not tracked in the assets table.

---

### STEP 8 — Report

```
Post {post_number} — {short_name}

Synced ({N}):
  ✓ {bucket}  [{approved item_types}]  → {file_path}

Skipped — no approved item_types ({N}):
  - {bucket}  [item_type: DRAFT, ...]

Errors:
  - {bucket}  {error message}
```
