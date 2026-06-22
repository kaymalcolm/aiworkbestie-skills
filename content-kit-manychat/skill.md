# AI For You — ManyChat Config Generator Skill

Generate ManyChat automation configs for both the post/comment flow and the story reply flow for an AI For You post. Saves two config files to the post folder and writes them to PostVault.

## When This Skill Activates

**Explicit:** `/content-kit-manychat [POST_NUMBER]`

**Intent detection:** Recognize requests like:
- "Generate the ManyChat config for post 1043"
- "Set up the ManyChat automation for the latest post"
- "Create the ManyChat flows for 1031"

---

## Autonomy Rules

Run the full workflow with no confirmation. If the keyword or Substack URL is missing, note it and generate the config with a clear placeholder — do not stop.

---

## Position in the Workflow

This skill runs AFTER `/content-kit-substack`. It needs:
- The comment keyword (registered in `post_keywords` during `/content-kit`)
- The Substack URL (registered in `destinations` or derivable from the slug after `/content-kit-substack` runs)

---

## Workflow

### STEP 0 — Read post data from DB

```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

post_number = "[POST_NUMBER]"

con = get_connection()
cur = con.cursor()

# Resolve post_number to post_id
cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
if not post_row:
    print("ERROR: No post found for post_number", post_number)
    exit(1)
post_id = post_row[0]

# Get keyword, post short_name, and asset_id
cur.execute("""
    SELECT a.id, a.short_name, pk.comment_keyword, pk.pinned_comment
    FROM assets a
    LEFT JOIN post_keywords pk ON pk.asset_id = a.id
    WHERE a.post_id = :1
      AND a.type = 'instagram-tiktok'
      AND a.pipeline = 'content-kit'
""", (post_id,))
row = cur.fetchone()

if not row:
    print("ERROR: No instagram-tiktok asset found for post", post_number)
    exit(1)

asset_id, short_name, keyword, pinned_comment = row
print(f"asset_id={asset_id}, short_name={short_name}, keyword={keyword}")

# Get Substack URL — try destinations first, then derive from short_name
cur.execute("""
    SELECT d.post_url, a.file_path
    FROM assets a
    LEFT JOIN destinations d ON d.asset_id = a.id AND d.platform = 'substack-newsletter'
    WHERE a.post_id = :1
      AND a.type = 'substack-draft'
      AND a.pipeline = 'content-kit'
    ORDER BY a.id DESC
    FETCH FIRST 1 ROWS ONLY
""", (post_id,))
sub_row = cur.fetchone()

if sub_row and sub_row[0]:
    substack_url = sub_row[0]  # live posted URL
elif sub_row and sub_row[1]:
    # file_path is the edit URL — convert to public URL using short_name
    substack_url = f"https://open.substack.com/pub/iamkaymalcolm/p/{short_name}"
else:
    substack_url = f"https://open.substack.com/pub/iamkaymalcolm/p/{short_name}"

print(f"substack_url={substack_url}")

# Get instagram caption to extract the named promise
cur.execute("""
    SELECT caption FROM post_captions
    WHERE asset_id = :1 AND platform = 'instagram'
""", (asset_id,))
cap_row = cur.fetchone()
instagram_caption = cap_row[0] if cap_row else ""

con.close()
```

### STEP 1 — Extract the named promise from the caption

Scan the instagram caption for the line matching: `Comment [KEYWORD] and I'll send you [THING]`

Extract the `[THING]` portion — this is what the audience was promised and what the DM should reference.

If the named promise cannot be found, derive it from the post topic (the `short_name`, converted to plain English). Example: `where-to-start-with-ai` → "where to start with AI at work."

Store as `NAMED_PROMISE`.

### STEP 2 — Generate keyword variants

From `KEYWORD` (e.g. `TOOLS`), generate:
- `KEYWORD_UPPER` = `TOOLS`
- `KEYWORD_LOWER` = `tools`
- `KEYWORD_TITLE` = `Tools`

ManyChat keyword triggers should include all three variants plus any 2-3 character partial matches that are unambiguous. Standard set: `[KEYWORD], [keyword], [Keyword]`

### STEP 3 — Generate the Post/Comment Automation config

Structure this as a readable reference document — every field shows exactly what to enter in ManyChat.

```
## POST / COMMENT AUTOMATION — [KEYWORD]

**Automation name:** [KEYWORD] - Posts

---

### TRIGGER
When someone comments on: any post or reel
And the comment contains: [KEYWORD_UPPER], [KEYWORD_LOWER], [KEYWORD_TITLE]

---

### ACTION 1 — Reply to comment under the post
(Rotated randomly — enter all three in ManyChat)

Reply 1: "Gotchu friend, sent you the link in your DMs"
Reply 2: "Let's get your [topic noun] together, check your DMs!"
Reply 3: "Check your DMs!"

---

### ACTION 2 — Opening DM (sent immediately)

Message:
  "Hey there friend, hope your day is going well :-)

  Click the [KEYWORD_UPPER] link below."

Button label: [KEYWORD_UPPER] (Click this)
Button URL: [SUBSTACK_URL]

---

### ACTION 3 — Follow gate DM (default: ON)

Message:
  "Nearly there! The link is especially for my followers ✨

  Right after you follow me, I'll send you the link so you can dive straight in! 🎉"

(ManyChat sends the final DM automatically once they follow)

---

### ACTION 4 — Final DM with link (sent after they follow)

Message:
  "Here you go! [NAMED_PROMISE]

  [KEYWORD_UPPER] (click me!)"

Button label: [KEYWORD_UPPER] (click me!)
Button URL: [SUBSTACK_URL]

---

### OTHER AUTOMATIONS

React to comment with: ❤️
```

### STEP 4 — Generate the Story Automation config

```
## STORY AUTOMATION — [KEYWORD]

**Automation name:** [KEYWORD] - Stories

---

### TRIGGER
When someone replies to: any story
And the reply contains: [KEYWORD_UPPER], [KEYWORD_LOWER], [KEYWORD_TITLE]

---

### ACTION 1 — DM (sent immediately)

Message:
  "Here you go! [NAMED_PROMISE]

  Click [KEYWORD_UPPER] to get it"

Button label: [KEYWORD_UPPER] (click me!)
Button URL: [SUBSTACK_URL]

---

### ACTION 2 — Follow-up DM (sent ~24 hours later)

Message:
  "Just want to make sure the link worked and you're fully taken care of! 🙏

  Do you have any questions? Either way let me know, I'm here to help ❤️"

---

### OTHER AUTOMATIONS

React to story reply with: ❤️
```

### STEP 5 — Save the config files

Identify the post folder:
`/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-[SHORT_NAME]/`

Save two files there:

**File 1:** `[POST_NUMBER]-manychat-post-[DATE].md`

Header:
```
# ManyChat — Post/Comment Automation — [KEYWORD]

**Post:** [POST_NUMBER] — [SHORT_NAME]
**Keyword:** [KEYWORD_UPPER]
**Substack URL:** [SUBSTACK_URL]
**Named promise:** [NAMED_PROMISE]
**Follow gate:** ON (default)
**Date generated:** [today]
```
Then the full post automation config from STEP 3.

**File 2:** `[POST_NUMBER]-manychat-story-[DATE].md`

Header:
```
# ManyChat — Story Automation — [KEYWORD]

**Post:** [POST_NUMBER] — [SHORT_NAME]
**Keyword:** [KEYWORD_UPPER]
**Substack URL:** [SUBSTACK_URL]
**Named promise:** [NAMED_PROMISE]
**Date generated:** [today]
```
Then the full story automation config from STEP 4.

### STEP 6 — Write configs to PostVault DB

Upsert `post_keywords` with both config fields (JSON type — pass Python dict or JSON string):

```python
import sys, datetime
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

today = datetime.date.today().isoformat()
post_config   = """[FULL POST CONFIG TEXT FROM STEP 3]"""
story_config  = """[FULL STORY CONFIG TEXT FROM STEP 4]"""

con = get_connection()
cur = con.cursor()
cur.execute(
    "SELECT id FROM post_keywords WHERE asset_id = :1",
    (asset_id,)
)
if cur.fetchone():
    cur.execute("""
        UPDATE post_keywords
        SET manychat_post_config = :1, manychat_story_config = :2
        WHERE asset_id = :3
    """, (post_config, story_config, asset_id))
else:
    cur.execute("""
        INSERT INTO post_keywords (asset_id, manychat_post_config, manychat_story_config)
        VALUES (:1, :2, :3)
    """, (asset_id, post_config, story_config))
con.commit()
con.close()
print(f"ManyChat configs written to DB for asset {asset_id}")
```

### STEP 7 — Refresh registry

```bash
/opt/homebrew/bin/python3.12 /Users/kmalcolm/claude/iamkaymalcolm/assets/manage-assets.py export-md
```

### STEP 8 — Report back

Tell the user:
- The two file paths saved
- The keyword used
- The Substack URL embedded (note if it's a placeholder)
- Confirm DB write succeeded

One short paragraph. No trailing summary.

---

## Notes

- The follow gate (ACTION 3 in the post flow) is always ON by default. If the user wants to turn it off for a specific post, they can edit the config file and the DB field directly in PostVault.
- If the Substack post hasn't been published yet, the URL will be `https://open.substack.com/pub/iamkaymalcolm/p/[short_name]` — update it in PostVault once the post goes live.
- ManyChat keyword matching is case-insensitive in the platform, but entering all three variants (`TOOLS`, `tools`, `Tools`) is belt-and-suspenders and matches Kay's current setup exactly.
