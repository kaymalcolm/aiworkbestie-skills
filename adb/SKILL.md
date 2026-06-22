# Oracle ADB Skill

Query, inspect, and manage the **kmalcolm Oracle 26ai Autonomous Database** — the source of truth for the AI For You asset registry.

## When This Skill Activates

**Explicit:** `/adb [query or command]`

**Intent detection:** Recognize requests like:
- "Query the database for…"
- "Show me all assets with status ready"
- "How many posts are in the queue?"
- "Run this SQL against the ADB"
- "What's in the destinations table for post 1031?"
- "Check the Oracle DB"

---

## Connection Method: SQLcl MCP

**RULE: All Oracle database access MUST use the SQLcl MCP tools. Never use Python (`oracledb`, `oracle_db.py`, `manage-assets.py`) for database connections.**

### MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__sqlcl__execute` | Run SQL — SELECT, INSERT, UPDATE, DELETE, DDL |
| `mcp__sqlcl__sqlcl` | Run SQLcl commands — CONNECT, DESC, SET, COMMIT, etc. |
| `mcp__sqlcl__connect` | Connect using a saved connection name |
| `mcp__sqlcl__schema` | Retrieve schema / object information |
| `mcp__sqlcl__list` | List available saved connections |
| `mcp__sqlcl__status` | Check current connection status |

### First-Time Setup (run once to save the connection)

The wallet is an extracted directory (not a zip). TNS_ADMIN is set in mcp.json, so just:
```
mcp__sqlcl__sqlcl:
  sqlcl: "CONNECT -save 26ai -savepwd -replace AI_FOR_YOU/<YOUR_PASSWORD>@<YOUR_DSN>"
```

**Already done** — `26ai` is saved in `~/.sqlcl/connections.json` with password.

### Connect at the Start of Each Session

```
mcp__sqlcl__connect:
  name: "26ai"
```

---

## Connection Details

```
Host     : Oracle 23ai Autonomous Database (Canada Montreal)
DSN      : kmalcolm_tp
User     : AI_FOR_YOU
Wallet   : /Users/kmalcolm/oracle/wallet
```

---

## ERD Diagram

Visual schema reference (PDF + PNG) — update whenever DDL changes:

```
ERD PDF   : /Users/kmalcolm/claude/iamkaymalcolm/apps/db-erd.pdf
ERD PNG   : /Users/kmalcolm/claude/iamkaymalcolm/apps/db-erd.png
Generator : /Users/kmalcolm/claude/iamkaymalcolm/apps/generate_erd.py
```

**Rule:** After any DDL change (CREATE/ALTER/DROP TABLE or column), run:
```bash
PATH="/opt/homebrew/bin:$PATH" python3.12 /Users/kmalcolm/claude/iamkaymalcolm/apps/generate_erd.py
```
And update the TABLES dict in `generate_erd.py` to match the new schema.

---

## Schema

**Color groups in ERD:**
- Orange = Core pipeline (ASSETS, ASSET_LINKS)
- Purple = Post content (POSTS, POST_SCRIPTS, POST_SLIDES, POST_CAPTIONS, POST_KEYWORDS)
- Brown/orange = Production & review (POST_PRODUCTION, ASSET_ITEM_STATUS, ASSET_ITEM_STATUS_HISTORY, PRODUCTION_CHECKLIST)
- Green = Publishing (DESTINATIONS)
- Gray = System (APP_USERS, COMMENT_KEYWORDS, POST_CONTENT_DV)
- Teal = SmugMug library (SMUG_GALLERIES, SMUG_PHOTOS, SMUG_SYNC_LOG)

### assets
Core content asset registry — one row per content item.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| type | VARCHAR2(100) | draft, brief, infographic-mid, infographic-download, story, raw-infographic, processed-infographic, raw-script, transcript, raw-video |
| pipeline | VARCHAR2(100) | content-kit, raw-content |
| short_name | VARCHAR2(255) | URL-slug identifier |
| description | VARCHAR2(4000) | nullable |
| status | VARCHAR2(50) | needs-naming, pending, processing, ready, posted, archived |
| created_date | VARCHAR2(50) | YYYY-MM-DD |
| updated_date | VARCHAR2(50) | YYYY-MM-DD |
| file_path | VARCHAR2(4000) | nullable — local filesystem path |
| archive_path | VARCHAR2(4000) | nullable — path after archiving |
| post_id | NUMBER | FK → posts(id), nullable |
| notes | VARCHAR2(4000) | nullable |
| edit_notes | VARCHAR2(4000) | nullable — notes for video editor |
| approval_status | VARCHAR2(50) | draft, submitted, approved, rejected |
| submitted_by | VARCHAR2(100) | nullable — username who submitted |
| submitted_at | TIMESTAMP | nullable |
| approved_by | VARCHAR2(100) | nullable — username who approved |
| approved_at | TIMESTAMP | nullable |
| reviewer_notes | VARCHAR2(4000) | nullable — reviewer feedback |

### posts
Content campaign registry — one row per post. Assets FK to this table.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| post_number | VARCHAR2(20) | UNIQUE display identifier, e.g. '1043' |
| slug | VARCHAR2(255) | URL slug, e.g. 'switching-to-claude' |
| topic | VARCHAR2(1000) | human-readable post topic |
| status | VARCHAR2(50) | draft, active, posted, archived |
| queue_order | NUMBER | nullable — queue position for scheduling |
| created_date | VARCHAR2(50) | YYYY-MM-DD |

### asset_links
Many-to-many directed graph edges between assets.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| from_id | NUMBER | FK → assets(id) |
| to_id | NUMBER | FK → assets(id) |
| relationship | VARCHAR2(100) | processed-from, drafted-from, infographic-for, brief-for, story-from, transcript-from, source-for |

### destinations
Publishing targets — one row per asset × platform.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| platform | VARCHAR2(100) | instagram, tiktok, youtube-short, twitter, threads, substack-newsletter, substack-note, instagram-stories, linkedin-document, linkedin-newsletter |
| status | VARCHAR2(50) | pending, ready, posted, skipped |
| planned_post_date | VARCHAR2(50) | nullable |
| posted_date | VARCHAR2(50) | nullable |
| post_url | VARCHAR2(4000) | nullable — live URL after posting |
| notes | VARCHAR2(4000) | nullable |
| repost_count | NUMBER | default 0 |
| last_reposted_date | VARCHAR2(50) | nullable |

### post_scripts
All script and brief content for a draft asset.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| reel_script | CLOB | talking-head reel script |
| companion_script | CLOB | companion/B-roll script |
| brief | CLOB | full content brief |
| youtube_short | CLOB | YouTube Shorts script |
| reel_ending_instagram | VARCHAR2(1000) | Instagram-specific CTA ending |
| reel_ending_tiktok | VARCHAR2(1000) | TikTok-specific CTA ending |
| reel_ending_linkedin | VARCHAR2(1000) | LinkedIn-specific CTA ending |

### post_slides
Individual carousel slides — one row per slide per asset.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| slide_number | NUMBER | 1-indexed position |
| headline | VARCHAR2(1000) | slide headline |
| body | CLOB | slide body copy |

### post_captions
Platform-specific captions for a post.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| platform | VARCHAR2(100) | target platform |
| caption | CLOB | full caption text |
| hashtags | VARCHAR2(4000) | space-separated hashtag string |

### post_keywords
ManyChat trigger keyword and pinned comment per post.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| comment_keyword | VARCHAR2(255) | keyword viewers type to trigger DM |
| pinned_comment | CLOB | pinned comment directing to DM |
| manychat_notes | VARCHAR2(4000) | notes for ManyChat flow config |

### post_production
Production tracking — reel, companion video, and carousel status.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| has_reel | NUMBER | 1 = post includes a talking-head reel |
| has_companion | NUMBER | 1 = post includes companion/B-roll video |
| has_carousel | NUMBER | 1 = post includes a carousel |
| reel_record_date | VARCHAR2(50) | scheduled recording date |
| reel_recorded_date | VARCHAR2(50) | actual recording date |
| reel_editor | VARCHAR2(200) | editor name/handle |
| reel_edit_date | VARCHAR2(50) | scheduled edit date |
| reel_edited_date | VARCHAR2(50) | actual edit completion date |
| reel_video_ready | NUMBER | 1 = approved and ready |
| reel_file_url | VARCHAR2(4000) | final reel file URL/path |
| companion_record_date | VARCHAR2(50) | scheduled companion recording date |
| companion_recorded_date | VARCHAR2(50) | actual companion recording date |
| companion_editor | VARCHAR2(200) | companion editor name/handle |
| companion_video_ready | NUMBER | 1 = approved and ready |
| companion_file_url | VARCHAR2(4000) | final companion file URL/path |
| carousel_designer | VARCHAR2(200) | carousel designer name/handle |
| carousel_canva_url | VARCHAR2(4000) | Canva link for carousel design |
| carousel_artwork_ready | NUMBER | 1 = approved and ready |
| production_notes | VARCHAR2(4000) | general production notes |
| updated_at | TIMESTAMP | last update timestamp |

### asset_item_status
Current review/approval status of each deliverable within an asset.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| item_type | VARCHAR2(50) | deliverable type (e.g., reel_script, carousel_slides, caption) |
| status | VARCHAR2(50) | READY_TO_REVIEW, APPROVED, REVISION_REQUESTED, IN_PROGRESS |
| updated_at | TIMESTAMP | last status change |
| updated_by | VARCHAR2(100) | username who last updated |

### asset_item_status_history
Audit trail of all status transitions per deliverable.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| item_type | VARCHAR2(50) | deliverable type |
| from_status | VARCHAR2(50) | previous status |
| to_status | VARCHAR2(50) | new status |
| changed_at | TIMESTAMP | change timestamp |
| changed_by | VARCHAR2(100) | username who changed |

### production_checklist
Checkbox-style sign-off checklist for a post asset.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| asset_id | NUMBER | FK → assets(id) |
| item_key | VARCHAR2(100) | checklist item ID (e.g., caption_written, reel_uploaded) |
| checked | NUMBER | 1 = complete |
| checked_by | VARCHAR2(100) | username who checked it |
| checked_at | TIMESTAMP | when it was checked |
| note | VARCHAR2(4000) | optional note on the item |

### comment_keywords
Global ManyChat trigger keyword registry across all posts.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| keyword | VARCHAR2(255) | UNIQUE trigger keyword |
| post_id | NUMBER | FK → posts(id), nullable |
| topic | VARCHAR2(500) | nullable — topic description |
| registered_date | VARCHAR2(50) | nullable — YYYY-MM-DD |

### app_users
Application user accounts for PostVault and other apps.

| Column | Type | Notes |
|--------|------|-------|
| id | NUMBER (IDENTITY) | PK |
| username | VARCHAR2(100) | unique login username |
| display_name | VARCHAR2(200) | UI display name |
| password_hash | VARCHAR2(255) | bcrypt-hashed password |
| role | VARCHAR2(50) | admin, viewer, editor |
| active | NUMBER | 1 = active; 0 = disabled |
| created_at | TIMESTAMP | account creation time |

### post_content_dv
JSON document view — denormalized read-only snapshot of post content.

| Column | Type | Notes |
|--------|------|-------|
| data | JSON | aggregated JSON of all post content fields |

### smug_galleries
SmugMug gallery catalog synced from the API.

| Column | Type | Notes |
|--------|------|-------|
| gallery_id | VARCHAR2(100) | PK — SmugMug natural key |
| gallery_name | VARCHAR2(500) | gallery title |
| gallery_url | VARCHAR2(2000) | public SmugMug URL |
| last_synced | TIMESTAMP | last sync timestamp |
| photo_count | NUMBER | count of photos/videos |

### smug_photos
SmugMug photo/video catalog with AI descriptions and vector embeddings.

| Column | Type | Notes |
|--------|------|-------|
| photo_id | VARCHAR2(100) | PK — SmugMug natural key |
| gallery_id | VARCHAR2(100) | FK → smug_galleries(gallery_id) |
| media_type | VARCHAR2(10) | photo or video |
| filename | VARCHAR2(500) | original filename |
| title | VARCHAR2(1000) | SmugMug title/caption |
| smugmug_url | VARCHAR2(2000) | SmugMug page URL |
| thumbnail_url | VARCHAR2(2000) | thumbnail URL |
| original_url | VARCHAR2(2000) | full-resolution URL |
| ai_description | CLOB | Claude-generated description for semantic search |
| original_tags | VARCHAR2(4000) | tags from SmugMug |
| date_taken | TIMESTAMP | capture date/time |
| duration_seconds | NUMBER | video duration (null for photos) |
| frame_count | NUMBER | video frame count (null for photos) |
| embedding | VECTOR(8200) | Oracle 23ai vector embedding for similarity search |
| indexed_at | TIMESTAMP | when AI description + embedding were generated |

### smug_sync_log
Audit log of SmugMug sync runs.

| Column | Type | Notes |
|--------|------|-------|
| run_id | NUMBER (IDENTITY) | PK |
| triggered_by | VARCHAR2(20) | manual, cron, webhook |
| started_at | TIMESTAMP | sync start |
| finished_at | TIMESTAMP | sync completion |
| photos_added | NUMBER | new photos inserted |
| photos_updated | NUMBER | existing photos updated |
| errors | CLOB | JSON array of errors |
| status | VARCHAR2(20) | success, partial, failed |

---

## How to Run Queries

### Step 1 — Connect (if not already connected)

```
mcp__sqlcl__connect  →  name: "26ai"
```

If "26ai" isn't saved yet, save it (wallet is an extracted directory, not a zip):
```
mcp__sqlcl__sqlcl  →  sqlcl: "CONNECT -save 26ai -savepwd -replace AI_FOR_YOU/<YOUR_PASSWORD>@<YOUR_DSN>"
```
with env `TNS_ADMIN=/Users/kmalcolm/oracle/wallet` already set in mcp.json.

### Step 2 — Execute SQL

**SELECT:**
```sql
-- via mcp__sqlcl__execute
SELECT id, type, short_name, status FROM assets
WHERE pipeline = 'content-kit'
ORDER BY id DESC
FETCH FIRST 20 ROWS ONLY
```

**INSERT / UPDATE / DELETE:**
```sql
-- via mcp__sqlcl__execute
UPDATE assets SET status = 'posted', updated_date = '2026-05-29' WHERE id = 1031
```

After DML, commit explicitly if not auto-committed:
```
mcp__sqlcl__sqlcl  →  sqlcl: "COMMIT"
```

**Describe a table:**
```
mcp__sqlcl__sqlcl  →  sqlcl: "DESC assets"
```

### Oracle SQL Notes
- Limit rows: `FETCH FIRST N ROWS ONLY` (not `LIMIT`)
- NULL-safe string: `NVL(column, '')`
- No `AUTOINCREMENT` — columns use `GENERATED BY DEFAULT AS IDENTITY`
- String literals use single quotes only

---

## Common Queries

**Queue (ordered post list):**
```sql
SELECT queue_order, post_number, slug, status
FROM posts
WHERE queue_order IS NOT NULL
ORDER BY queue_order
```

**All assets for a post:**
```sql
SELECT a.id, a.type, a.short_name, a.status, a.file_path
FROM assets a
JOIN posts p ON p.id = a.post_id
WHERE p.post_number = '1043'
ORDER BY a.id
```

**Pending destinations by platform:**
```sql
SELECT a.id, a.short_name, p.post_number, d.status
FROM assets a
JOIN posts p ON p.id = a.post_id
JOIN destinations d ON d.asset_id = a.id
WHERE d.platform = 'instagram' AND d.status IN ('pending','ready')
ORDER BY a.post_id, a.id
```

**Comment keywords:**
```sql
SELECT ck.keyword, p.post_number, ck.topic
FROM comment_keywords ck
LEFT JOIN posts p ON p.id = ck.post_id
ORDER BY ck.id
```

---

## Workflow

1. Connect via `mcp__sqlcl__connect` with name "26ai"
2. Run SQL via `mcp__sqlcl__execute`
3. For SQLcl commands (DESC, SET, COMMIT), use `mcp__sqlcl__sqlcl`
4. Present results clearly — table format for lists, key-value for single assets
5. After any write operation: confirm what changed and new state
