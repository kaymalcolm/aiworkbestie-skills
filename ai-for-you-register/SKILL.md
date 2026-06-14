# AI For You — Register Skill

Register a completed AI For You draft in the asset database and add it to the post queue. Called automatically by `/ai-for-you` after files are saved, or run manually if registration was skipped or needs to be re-run.

## When This Skill Activates

**Explicit:** User types `/ai-for-you-register [post_number]`

**Called by:** `/ai-for-you` after STEP 5 (file save complete)

**Intent detection:** Recognize requests like:
- "Register post 1043 in the database"
- "Run the DB registration for post 1043"
- "The draft is saved — register it"
- "Re-run registration for post 1031"

---

## Autonomy Rules

Run all steps automatically. No confirmation needed. If the post is already registered (idempotent check), report and stop — do not create duplicates.

Requires:
- `post_number` (e.g. `1043`)
- A saved draft folder at `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/`

If the draft folder is missing, report the expected path and stop.

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

## STEP 1 — Find the draft files

List the post folder:
```bash
ls /Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/
```

Identify the primary platform files by name pattern:
- B-roll direction: `[POST_NUMBER]-*-instagram-tiktok-*.md` (contains B-roll direction + captions)
- Threads: `[POST_NUMBER]-*-threads-*.md`
- Twitter: `[POST_NUMBER]-*-twitter-*.md`
- YouTube Short: `[POST_NUMBER]-*-youtube-short-*.md`
- Newsletter: `[POST_NUMBER]-newsletter-*-*.md`
- LinkedIn doc (optional): `[POST_NUMBER]-*-linkedin-*.md`

Extract from the folder and file names:
- `SHORT_NAME` / `slug` (from `[POST_NUMBER]-[slug]-script-*.md`)
- `DATE` (from filename date suffix)
- `POST_FOLDER` (full folder name, e.g. `1043-switching-to-claude`)

Read the script file and the newsletter file in full. You will extract content from them for the DB inserts. Also read the instagram and tiktok caption files if they exist.

After reading both files, load the newsletter file content into a Python variable using the bash command below — do NOT inline the newsletter text as a string literal in the Python script, as it will be truncated. The file path is the one found in STEP 1.

```bash
NEWSLETTER_FILE="/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-newsletter-[SHORT_NAME]-[DATE].md"
```

---

## STEP 2 — Register draft in asset DB

```python
import oracledb, datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
post_number = "[POST_NUMBER]"
short_name  = "[slug — e.g. switching-to-claude]"
description = "Draft: [topic] (post [POST_NUMBER])"

# Read newsletter file content — never inline as a string literal
with open("[FULL_NEWSLETTER_FILE_PATH]", "r") as f:
    newsletter_content = f.read()

# Extract Substack Note section (between ## SUBSTACK NOTE and ## LINKEDIN NEWSLETTER)
_note_start   = newsletter_content.find("## SUBSTACK NOTE")
_linkedin_start = newsletter_content.find("## LINKEDIN NEWSLETTER")
substack_note = newsletter_content[_note_start:_linkedin_start].strip() \
                    .replace("## SUBSTACK NOTE", "").strip().rstrip("-").strip()

PLATFORMS = [
    "instagram-tiktok", "youtube-short",
    "twitter", "threads", "substack-newsletter", "substack-note", "linkedin-newsletter",
]

con = get_connection()
cur = con.cursor()

# Check if draft already registered
cur.execute("""
    SELECT p.id, a.id
    FROM posts p
    LEFT JOIN assets a ON a.post_id = p.id AND a.type = 'script'
    WHERE p.post_number = :1""", (post_number,))
existing_row = cur.fetchone()
if existing_row and existing_row[1]:
    post_id = existing_row[0]
    asset_id = existing_row[1]
    print(f"Draft for post {post_number} already registered as asset {asset_id} — updating newsletter caption")
    # Always re-sync newsletter captions from file (file content may have changed)
    for _platform, _content in [("substack-newsletter", newsletter_content),
                                  ("substack-note", substack_note)]:
        cur.execute("SELECT id FROM post_captions WHERE asset_id=:1 AND platform=:2",
                    [asset_id, _platform])
        if cur.fetchone():
            cur.execute("UPDATE post_captions SET caption=:1 WHERE asset_id=:2 AND platform=:3",
                        [_content, asset_id, _platform])
        else:
            cur.execute("INSERT INTO post_captions (asset_id, platform, caption) VALUES (:1,:2,:3)",
                        [asset_id, _platform, _content])
    con.commit()
    con.close()
    print(f"ASSET_ID={asset_id}")
    # Stop here — all other tables are correct
    import sys; sys.exit(0)
else:
    # 1. INSERT posts row (or reuse if it exists without an instagram-tiktok asset)
    if existing_row:
        post_id = existing_row[0]
    else:
        post_id_var = cur.var(oracledb.NUMBER)
        cur.execute("""
            INSERT INTO posts (post_number, slug, topic, status)
            VALUES (:1,:2,:3,'active')
            RETURNING id INTO :4""",
            (post_number, short_name, description, post_id_var))
        post_id = int(post_id_var.getvalue()[0])

    # 2. INSERT draft asset
    new_id_var = cur.var(oracledb.NUMBER)
    cur.execute("""
        INSERT INTO assets (type, pipeline, short_name, description, status,
                            created_date, updated_date, post_id)
        VALUES ('script','ai-for-you',:1,:2,'draft',:3,:4,:5)
        RETURNING id INTO :6""",
        (short_name, description, today, today, post_id, new_id_var))
    asset_id = int(new_id_var.getvalue()[0])

    # 3. INSERT destinations — one per platform
    for platform in PLATFORMS:
        cur.execute(
            "INSERT INTO destinations (asset_id, platform, status) VALUES (:1,:2,'pending')",
            (asset_id, platform))

    # 4. INSERT post_scripts — extract from the instagram-tiktok file
    # reel_script      = ## B-ROLL DIRECTION section body (on-screen text hook + clip-by-clip direction + end card)
    # reel_ending_*    = platform-specific end card text from ## END CARD DIRECTION block
    reel_script           = """[FULL B-ROLL DIRECTION — verbatim from ## B-ROLL DIRECTION section in instagram-tiktok file]"""
    reel_ending_instagram = "[IG end card text — from END CARD DIRECTION in instagram-tiktok file]"
    reel_ending_tiktok    = "[TikTok end card text — from END CARD DIRECTION in instagram-tiktok file]"
    reel_ending_linkedin  = None  # LinkedIn is carousel only, no video end card

    cur.execute("""
        INSERT INTO post_scripts
            (asset_id, reel_script, reel_ending_instagram, reel_ending_tiktok,
             reel_ending_linkedin, youtube_long)
        VALUES (:1,:2,:3,:4,:5,:6)""",
        (asset_id, reel_script,
         reel_ending_instagram, reel_ending_tiktok, reel_ending_linkedin,
         None))

    # 5. INSERT post_slides — extract each carousel slide from ## CAROUSEL section in script file
    # Slides may be in table format (| Slide | Headline | Body |) or ### Slide N — LABEL / **Headline:** / **Body:** format
    slides = [
        (1, "[Slide 1 headline — hook text]",    "[Slide 1 body]"),
        (2, "[Slide 2 headline]",                "[Slide 2 body]"),
        # ... continue for all generated slides (7-9 slides)
        # Last slide: CTA slide with named-promise keyword CTA
    ]
    for slide_num, headline, body in slides:
        cur.execute(
            "INSERT INTO post_slides (asset_id, slide_number, headline, body) VALUES (:1,:2,:3,:4)",
            (asset_id, slide_num, headline, body))

    # 6. INSERT post_captions — extract verbatim from each platform file
    # Threads: combine all 3 posts separated by ---POST BREAK--- delimiter
    captions = [
        ("instagram",
         "[Full Instagram caption from ## CAPTION section in *-instagram-*.md, or None if file absent]",
         "[Instagram hashtags from ## HASHTAGS section in *-instagram-*.md, or None if file absent]"),
        ("tiktok",
         "[Full TikTok caption from ## CAPTION section in *-tiktok-*.md, or None if file absent]",
         "[TikTok hashtags from ## HASHTAGS section in *-tiktok-*.md, or None if file absent]"),
        ("twitter",
         "[Full Twitter/X thread — all tweets verbatim from ## THREAD section in *-twitter-*.md, separated by ---TWEET BREAK--- delimiters]",
         None),
        ("threads",
         "[Threads post 1]\n\n---POST BREAK---\n\n[Threads post 2]\n\n---POST BREAK---\n\n[Threads post 3]",
         None),
        ("youtube-short",
         "[YouTube Short description with tags]",
         None),
        ("substack-newsletter",
         newsletter_content,  # full file — never inline
         None),
        ("substack-note",
         substack_note,       # extracted from ## SUBSTACK NOTE section
         None),
        ("linkedin-newsletter",
         "[LinkedIn newsletter ending line directing to LinkedIn newsletter]",
         None),
    ]
    for platform, caption, hashtags in captions:
        cur.execute(
            "INSERT INTO post_captions (asset_id, platform, caption, hashtags) VALUES (:1,:2,:3,:4)",
            (asset_id, platform, caption, hashtags))

    # 7. INSERT post_keywords — extract from ## KEYWORDS section in script file
    cur.execute("""
        INSERT INTO post_keywords (asset_id, comment_keyword, pinned_comment, manychat_notes)
        VALUES (:1,:2,:3,:4)""",
        (asset_id,
         "[COMMENT_KEYWORD]",
         "[Pinned comment text, or None if this post does not use a pinned comment]",
         None))

    # 8. INSERT post_production — reel + carousel always; no companion
    cur.execute("""
        INSERT INTO post_production (asset_id, has_reel, has_companion, has_carousel)
        VALUES (:1, 1, 0, 1)""",
        (asset_id,))

    con.commit()
    print(f"Registered draft as asset {asset_id} with {len(PLATFORMS)} destinations and all content tables")

con.close()
print(f"ASSET_ID={asset_id}")
```

---

## STEP 3 — Update file_path in DB

```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
import datetime
today = datetime.date.today().isoformat()
con = get_connection()
cur = con.cursor()
cur.execute(
    "UPDATE assets SET file_path=:1, updated_date=:2 WHERE id=:3",
    ("/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-[SHORT_NAME]-script-[DATE].md",
     today, asset_id))
con.commit()
con.close()
```

Then refresh the registry:
```
/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

---

## STEP 4 — Add to post queue

```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
con = get_connection()
cur = con.cursor()
cur.execute("""
    UPDATE posts
    SET queue_order = (SELECT NVL(MAX(queue_order),0)+1 FROM posts WHERE queue_order IS NOT NULL)
    WHERE id = :1""",
    (post_id,))
con.commit()
con.close()
```

To view the current queue at any time:
```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
con = get_connection()
cur = con.cursor()
cur.execute("SELECT queue_order, post_number, slug FROM posts WHERE queue_order IS NOT NULL ORDER BY queue_order")
for row in cur.fetchall():
    print(row)
con.close()
```

---

## STEP 5 — Confirm

Tell the user:
- Asset ID assigned
- Number of destinations registered
- File path recorded in DB
- Queue position

One line per item. No trailing summary.
