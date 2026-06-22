# Buffer Scheduler Skill

Schedule social media captions for an AI For You post to Buffer — Instagram, TikTok, LinkedIn, Twitter, Threads, and YouTube — in one command. Optionally also schedule Instagram and TikTok Stories with the infographic image attached.

## When This Skill Activates

**Explicit:** `/buffer [post_number]` or `/buffer [post_number] [ISO scheduled_at]`

**With Stories:** `/buffer [post_number] --stories` or "schedule 1031 with stories"

**Intent detection:** Recognize requests like:
- "Schedule post 1031 to Buffer"
- "Queue the social posts for 1031"
- "Push 1031 captions to Buffer for tomorrow at 9am"
- "Send the social copy to Buffer"
- "Schedule 1031 with Instagram Stories"

---

## Autonomy Rules

Run the full workflow with no confirmation prompts. Only stop if:
- The post folder cannot be found
- No Buffer channels are returned (auth issue)
- A specific platform file is missing — skip that platform and note it in the report

---

## Two Buffer Accounts

| Account name     | Covers                        |
|------------------|-------------------------------|
| `insta-buffer`   | Instagram, TikTok, LinkedIn   |
| `threads-buffer` | Twitter/X, Threads, YouTube   |

Credentials are already loaded into the MCP server via `.bufferrc`.

---

## Workflow

### STEP 1 — Discover channels

Call `buffer_list_channels` for both accounts in parallel. Store the full channel list for each.

From `insta-buffer` channels, identify (by `service` field):
- `instagram` → `INSTAGRAM_CHANNEL_ID`
- `tiktok` → `TIKTOK_CHANNEL_ID`
- `linkedin` → `LINKEDIN_CHANNEL_ID`

From `threads-buffer` channels, identify:
- `twitter` → `TWITTER_CHANNEL_ID`
- `threads` → `THREADS_CHANNEL_ID`
- `youtube` → `YOUTUBE_CHANNEL_ID`

If a platform has no matching channel, skip it and note it in the final report.

---

### STEP 2 — Locate the post folder and infographic

Find the post folder: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/`

Inside, identify these content files by glob pattern:
- `[POST_NUMBER]-*instagram-tiktok-*.md` → INSTAGRAM/TIKTOK file
- `[POST_NUMBER]-*threads-*.md` → THREADS file
- `[POST_NUMBER]-*twitter-*.md` → TWITTER file
- `[POST_NUMBER]-*linkedin-*.md` → LINKEDIN file
- `[POST_NUMBER]-*youtube-short-*.md` → YOUTUBE file (may not exist — skip if absent)

Inside the `infographic/` subfolder, locate:
- Full infographic: `[POST_NUMBER]-*infographic*.png` — the file that does NOT have `-mid` in the name → `INFOGRAPHIC_PATH`
- Mid infographic: `[POST_NUMBER]-*infographic-mid*.png` → `INFOGRAPHIC_MID_PATH`

Read all content files.

---

### STEP 3 — Upload infographic

Always upload the full infographic for attachment to Instagram and TikTok posts:

```
buffer_upload_image(file_path=INFOGRAPHIC_PATH)
```

Store the returned URL as `INFOGRAPHIC_URL`.

If the infographic file does not exist, set `INFOGRAPHIC_URL = None` and continue — posts will be text-only.

---

### STEP 4 — Extract captions

**Instagram caption:**
From the Instagram/TikTok file, find the `## INSTAGRAM CAPTION` section. Extract all text from that heading until you hit `**Hashtags:**` or `**Comment keyword:**` or `---` (whichever comes first). Then append the hashtags line (the `**Hashtags:**` value, stripping the bold label). Do NOT include the `**Comment keyword:**` line or any section after it.

Final format:
```
[body paragraphs]

[hashtags string]
```

**TikTok caption:**
From the Instagram/TikTok file, find the `## TIKTOK` section. Extract all text until the next `---` or `##`. If no separate TikTok section exists, use the Instagram caption.

**LinkedIn caption:**
From the LinkedIn file, find the `## LINKEDIN CAPTION` section. Extract all text from that heading until the next `---` or `##` heading or end of file.

**Threads caption:**
From the Threads file, find the `**[Opening post:]**` block. Extract ONLY the text of that block — the paragraphs that follow `**[Opening post:]**` until the first `---`. Do NOT include the carousel prompt block.

**Twitter caption:**
From the Twitter file, find the `## TWITTER / X` section. Extract all text from that heading until the next `---` or `##` heading or end of file.

**YouTube caption:**
From the YouTube Short file (if it exists), find the `## DESCRIPTION` or `## YOUTUBE` section and extract the caption text. If the file doesn't exist, skip YouTube entirely.

---

### STEP 5 — Build and schedule posts

Use `buffer_batch_create_posts` once per account (two calls total).

**`insta-buffer` batch** — Instagram, TikTok, LinkedIn:
```json
{
  "account": "insta-buffer",
  "posts": [
    {
      "text": "[instagram caption]",
      "profile_ids": ["[INSTAGRAM_CHANNEL_ID]"],
      "media_link": "[INFOGRAPHIC_URL or omit if null]",
      "scheduled_at": "[ISO_TIME_if_provided]"
    },
    {
      "text": "[tiktok caption]",
      "profile_ids": ["[TIKTOK_CHANNEL_ID]"],
      "media_link": "[INFOGRAPHIC_URL or omit if null]",
      "scheduled_at": "[ISO_TIME_if_provided]"
    },
    {
      "text": "[linkedin caption]",
      "profile_ids": ["[LINKEDIN_CHANNEL_ID]"],
      "scheduled_at": "[ISO_TIME_if_provided]"
    }
  ]
}
```

**`threads-buffer` batch** — Twitter, Threads, YouTube:
```json
{
  "account": "threads-buffer",
  "posts": [
    {
      "text": "[twitter caption]",
      "profile_ids": ["[TWITTER_CHANNEL_ID]"],
      "scheduled_at": "[ISO_TIME_if_provided]"
    },
    {
      "text": "[threads caption]",
      "profile_ids": ["[THREADS_CHANNEL_ID]"],
      "scheduled_at": "[ISO_TIME_if_provided]"
    },
    {
      "text": "[youtube caption]",
      "profile_ids": ["[YOUTUBE_CHANNEL_ID]"],
      "scheduled_at": "[ISO_TIME_if_provided]"
    }
  ]
}
```

If `scheduled_at` was not provided by the user, omit it entirely from the post objects — Buffer will add the post to the next open queue slot.

Omit `media_link` entirely if `INFOGRAPHIC_URL` is null — do not pass a null value.

---

### STEP 5b — Schedule Stories (only if `--stories` flag or user said "with stories")

After the regular posts are scheduled, schedule Story posts for Instagram and TikTok.

Stories require an image. If `INFOGRAPHIC_URL` is null, skip this step and note it.

Use `buffer_create_post` (single call per Story — batch doesn't mix post types cleanly):

**Instagram Story:**
```json
{
  "account": "insta-buffer",
  "text": "",
  "profile_ids": ["[INSTAGRAM_CHANNEL_ID]"],
  "media_link": "[INFOGRAPHIC_URL]",
  "post_type": "story",
  "scheduled_at": "[ISO_TIME_if_provided]"
}
```

**TikTok Story:**
```json
{
  "account": "insta-buffer",
  "text": "",
  "profile_ids": ["[TIKTOK_CHANNEL_ID]"],
  "media_link": "[INFOGRAPHIC_URL]",
  "post_type": "story",
  "scheduled_at": "[ISO_TIME_if_provided]"
}
```

Stories have no caption text — the image is the content. Use the same scheduled time as the regular posts, or omit if not specified.

---

### STEP 6 — Update destinations in the asset DB

For each platform successfully scheduled to Buffer, mark its `destinations` row as scheduled.

Platform name mapping (Buffer service → destinations.platform):

| Buffer service | destinations.platform |
|---|---|
| `instagram` | `instagram-tiktok` |
| `tiktok` | `instagram-tiktok` |
| `linkedin` | `linkedin-newsletter` |
| `twitter` | `twitter` |
| `threads` | `threads` |
| `youtube` | `youtube-short` |

Note: Instagram and TikTok share one `instagram-tiktok` destinations row — scheduling either marks it scheduled.

```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

# Build the list of destinations.platform values that were successfully scheduled
# Map from Buffer service names to destinations.platform names (see table above)
scheduled_platforms = []  # e.g. ["instagram-tiktok", "twitter", "threads", "youtube-short"]

con = get_connection()
cur = con.cursor()

# Find the draft asset for this post
cur.execute(
    "SELECT id FROM assets WHERE type='draft' AND pipeline='content-kit' AND post_number=:1",
    (POST_NUMBER,))
row = cur.fetchone()
if row:
    asset_id = row[0]
    for platform in scheduled_platforms:
        cur.execute(
            "UPDATE destinations SET status='scheduled' WHERE asset_id=:1 AND platform=:2",
            (asset_id, platform))
        if cur.rowcount == 0:
            print(f"No destinations row for post {POST_NUMBER} platform {platform} — skipped")
    con.commit()
    print(f"Marked {len(scheduled_platforms)} destinations as scheduled for asset {asset_id}")
else:
    print(f"No draft asset found for post {POST_NUMBER} — destinations not updated")

con.close()
```

---

### STEP 7 — Report back

Tell the user:
- Which platforms were scheduled (✓) or skipped (—) and why
- Whether the infographic was attached (and the catbox URL)
- Whether Stories were scheduled
- The Buffer update IDs for each post
- Whether a scheduled time was applied or posts were queued to next slot
- Which destinations rows were marked scheduled in the DB

One short table or bullet list. No preamble.

---

## Rules

- Never confirm with the user mid-workflow
- If a caption section is not found in a file, skip that platform rather than failing the whole run
- Never modify the source content files
- If `scheduled_at` is provided as a natural phrase (e.g. "tomorrow at 9am"), convert to ISO 8601 UTC before passing to the MCP tool (assume Eastern time unless the user specifies)
- Instagram captions should include hashtags; LinkedIn captions should keep hashtags minimal (5 max, already in the file); Threads and Twitter captions use whatever is in the source file
- Always attach the infographic to Instagram and TikTok regular posts (not LinkedIn, Twitter, Threads, or YouTube)
- Stories are opt-in only — do not schedule them unless the user explicitly asks
