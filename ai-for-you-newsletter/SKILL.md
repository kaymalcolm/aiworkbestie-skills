# AI For You — Newsletter Skill

Generate the AI For You newsletter from a research file. Produces one shared newsletter body with two platform-specific endings (Substack + LinkedIn) and a Substack Note. This is Phase 2 of the content pipeline — everything downstream keys off this output.

## When This Skill Activates

**Explicit:** `/ai-for-you-newsletter [path to research file]` or `/ai-for-you-newsletter [post number]`

**Intent detection:** Recognize requests like:
- "Write the newsletter for post 1043"
- "Generate the newsletter from the research file"
- "Build the newsletter from [research file]"
- "Run Phase 2 on [research file]"

---

## Autonomy Rules

Run the full workflow with no confirmation unless:
- The research file cannot be found (ask for the path)
- Oracle credentials are missing (ask once, then proceed without DB lookup)
- The topic is ambiguous (ask one clarifying question maximum)

---

## Position in the Pipeline

```
Phase 1: /ai-for-you-research   → research file
Phase 2: /ai-for-you-newsletter → newsletter file  ← this skill
Phase 3: /ai-for-you            → social content package (reads newsletter file)
Phase 4: parallel visual assets
Phase 5: /ai-for-you-substack-publish, /ai-for-you-manychat
```

This skill creates the post record and registers the comment keyword before generating content, so Phase 3 can pull both from the DB.

---

## Workflow

### STEP 0 — Read the research file

- If a post number is given, find the research file: glob `/Users/kmalcolm/claude/iamkaymalcolm/research/[POST_NUMBER]-*-research-*.md`
- If a path is given, read it directly
- Extract from the research file:
  - `TOPIC`
  - `PROPOSED_POST_NUMBER` (verify by counting files in `content-drafts/` matching `ai-for-you-0*.md`)
  - `SLUG` — use the slug from the research file unless the user overrides with `--slug`
  - `CANDIDATE_KEYWORD` — the proposed comment keyword
  - Audience Research block — carry forward verbatim
  - Hook Options (3) — carry forward verbatim; do not rewrite
  - B-roll Direction and On-screen Text Hook — carry forward verbatim if present; used for context framing

Confirm the final slug in one line before proceeding: "Using slug `[SLUG]` — override?" If no response, proceed.

---

### STEP 0b — Read brand and strategy source files

1. **Brand guide:** `/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md`
2. **Content strategy:** `/Users/kmalcolm/claude/iamkaymalcolm/strategy/general-strategy.md`
3. **Any content plan files** in `/Users/kmalcolm/claude/iamkaymalcolm/strategy/` that contain pain points or audience notes
4. **Existing drafts** in `/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/` — scan for topic overlap

---

### STEP 1 — Determine post type

Count files in `content-drafts/` matching `ai-for-you-0*.md`. Every 3rd post is a FULL CONTENT post; others are TEASE posts.

- **FULL CONTENT:** All value in the social post. Newsletter CTA is lighter — "go deeper" not "get the thing."
- **TEASE:** The full prompts, templates, or resource live only in the newsletter. Social content teases. Newsletter CTA is the payoff.

Document this decision at the top of the output file as `POST_TYPE: TEASE` or `POST_TYPE: FULL_CONTENT`.

---

### STEP 2 — Register the comment keyword

**Query existing keywords:**
```python
import sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

con = get_connection()
cur = con.cursor()
cur.execute("SELECT keyword FROM comment_keywords")
used = {row[0].upper() for row in cur.fetchall()}
con.close()
print("Used keywords:", used)
```

**Evaluate the candidate keyword from the research file.** If it is in `used`, generate a new one. Rules: 4-8 characters, all caps, loosely relevant to the topic, not in `used`, not a generic word (AI, YES, GO, MORE, TIPS, HELP, FREE).

**Create or verify the post record, then register:**
```python
import datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
import oracledb

today = datetime.date.today().isoformat()
post_number = "[POST_NUMBER]"
slug = "[SLUG]"
topic = "[TOPIC]"
keyword = "[CHOSEN_KEYWORD]"

con = get_connection()
cur = con.cursor()

# Create post record if it doesn't exist
cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
if not post_row:
    post_var = cur.var(oracledb.NUMBER)
    cur.execute(
        "INSERT INTO posts (post_number, short_name, title, pipeline, status, created_date) "
        "VALUES (:1,:2,:3,'ai-for-you','DRAFT',:4) RETURNING id INTO :5",
        (post_number, slug, topic, today, post_var)
    )
    post_id = int(post_var.getvalue())
    con.commit()
    print(f"Created post record id={post_id}")
else:
    post_id = post_row[0]
    print(f"Post record exists id={post_id}")

# Register keyword
try:
    cur.execute(
        "INSERT INTO comment_keywords (keyword, post_id, topic, registered_date) VALUES (:1,:2,:3,:4)",
        (keyword.upper(), post_id, topic, today)
    )
    con.commit()
    print(f"Keyword '{keyword}' registered")
except Exception as e:
    if "ORA-00001" in str(e) or "unique constraint" in str(e).lower():
        print(f"Keyword '{keyword}' already taken — generate another")
    else:
        raise

con.close()
```

If the INSERT fails (duplicate), generate a new keyword and retry before proceeding.

Write `COMMENT_KEYWORD = "[WORD]"` at the top of the output file.

---

### STEP 3 — Generate the newsletter

Write the newsletter in three parts: shared body, Substack ending, LinkedIn ending.

#### 3a. NEWSLETTER TITLE AND SUBTITLE

Write the newsletter title and subtitle. These appear in both editions; the LinkedIn edition omits the subtitle (LinkedIn doesn't support it).

**Title** — the email subject line. Two proven angles:
- **FOMO/peer comparison (Option A):** "Your colleagues are already using these 4 AI prompts. Are you?"
- **Counterintuitive/pain-naming (Option D):** "Stop Googling 'how to use AI.' Do these 4 things instead."

No em dashes anywhere in the title. No vague promises. No description of content.

**Subtitle** — 1 sentence that lands the punch the title started. No em dashes. Substack edition only.

---

#### 3b. SHARED NEWSLETTER BODY

Write the full newsletter body. This is verbatim identical in both editions — do not modify it between editions.

**Byline:**
`*AI For You | Kay Malcolm, VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor*`

**Opening — 3 short paragraphs:**
- Para 1: Empathy/relatable observation. Pulls from the Audience Research in the research file. Use the specific phrases and fears the research surfaced — not sanitized versions.
- Para 2: Personal entry. Kay's own experience. First-person past tense. Specific, not generic.
- Para 3: Timely context + credential + what they're getting today.

**MID-ARTICLE INFOGRAPHIC placeholder** — place immediately after the opener, before any content moves:
```
**[INFOGRAPHIC: Mid-article — [brief description of what the infographic shows]]**
```

**Content moves** — for each key point or use case from the research file:
- Label: `**Move 0N: [Name] | [time estimate]**`
- 2-3 sentences of narrative context. Specific reason this matters. Not a story block, not a staccato list.
- Full prompt in a code block (for TEASE posts) or full resource/tip (for FULL CONTENT posts)
- Personal aside in parentheses if it adds genuine color

**END INFOGRAPHIC placeholder** — after the last move:
```
**[INFOGRAPHIC: Download/share — [title of the reference guide]]**
*[one-line caption, e.g. "All four prompts in one place. Save it to your phone."]*
```

**Closing** — two sentences:
- One concrete action for this week
- One reply ask — a specific question that invites a personal answer

**Body formatting rules (Substack plain-text rules apply):**
- Section headers: Bold label style — `**Move 01: Name | time**` — no `##` markdown headers
- Prompts: code blocks
- Links: full URL on its own line, no markdown hyperlink syntax
- Line spacing: blank line between every paragraph
- No em dashes anywhere. No AI poetry. No corporate-speak.

---

#### 3c. SUBSTACK ENDING

Write the sign-off for the Substack edition. Rotate between these three versions — pick the one that fits the post's tone; do not repeat the same version in consecutive posts. Check the last 3 posts' newsletter files to see which was used most recently.

**Version A** (warm, community-forward):
```
Signed 🫶🏾,

Kay, Your AI Work Bestie

*VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*

*AI For You is a weekly newsletter for corporate women (guys you can read it too, relax fellas and let us girls support each other) navigating careers in the AI era. Real tools. Real prompts. No tech background required. -- iamkaymalcolm.substack.com*
```

**Version B** (tight — tactical/prompt-heavy posts):
```
Signed 🫶🏾,

Kay, Your AI Work Bestie

*VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*
```

**Version C** (classic — thought leadership or longer-form):
```
Signed 🫶🏾,

Your AI Work Bestie,
Kay

*VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*

*AI For You is a weekly newsletter for corporate women navigating careers in the AI era. Real tools. Real prompts. No tech background required. -- iamkaymalcolm.substack.com*
```

---

#### 3d. LINKEDIN ENDING

Write the sign-off for the LinkedIn edition. Same structure as the chosen Substack version with one difference: **omit any line that references `iamkaymalcolm.substack.com`** — LinkedIn readers are already in a LinkedIn newsletter; promoting Substack here is misplaced. The LinkedIn newsletter description line is also removed.

Example (Version A adapted for LinkedIn):
```
Signed 🫶🏾,

Kay, Your AI Work Bestie

*Vice President @ Oracle, AI Database | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*
```

---

#### 3e. SUBSTACK NOTE

Write a standalone 3-5 sentence post for Kay's Substack Notes. Must be topically connected to this newsletter issue — arc around the pain or problem and make the reader curious enough to click through. NOT a note on a different subject. NOT a summary. First-person, Kay's voice, casual but specific.

Do not include a URL (the newsletter isn't published yet).  Come back and update once the newsletter is published in the /ai-for-you-substack-publish skill.

---

### STEP 4 — Run the brand grader

Before saving any files, run `/ai-for-you-grader` on:
1. Newsletter title + subtitle
2. Newsletter body (opening + all moves)
3. Substack Note

If the grader flags anything, fix and re-grade that section. Maximum 3 fix iterations per section. If a section cannot pass after 3 attempts, flag it and stop.

Do not save files until all sections pass.

---

### STEP 5 — Save the newsletter file

Save to: `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-[SLUG]/[POST_NUMBER]-[SLUG]-newsletter-[YYYY-MM-DD].md`

Create the post folder if it doesn't exist.

**File structure:**

```
COMMENT_KEYWORD: [KEYWORD]
POST_TYPE: [TEASE|FULL_CONTENT]
POST_NUMBER: [POST_NUMBER]
SLUG: [SLUG]
DATE: [YYYY-MM-DD]

---

## NEWSLETTER TITLE

**Title:** [the title]
**Subtitle:** [the subtitle — Substack edition only]

---

## SHARED BODY

[Byline]

[Opening — 3 paragraphs]

[MID-ARTICLE INFOGRAPHIC placeholder]

[Content moves]

[END INFOGRAPHIC placeholder]

[Closing — action + reply ask]

---

## SUBSTACK EDITION

**Title:** [same title]
**Subtitle:** [subtitle]

[Shared body verbatim]

[Substack ending]

---

## LINKEDIN EDITION

**Title:** [same title]
(no subtitle)

[Shared body verbatim]

[LinkedIn ending]

---

## SUBSTACK NOTE

[3-5 sentences]
```

The `## SUBSTACK EDITION` section is what `/ai-for-you-substack-publish` reads.
The `## LINKEDIN EDITION` section is what the LinkedIn publishing step reads.

---

### STEP 6 — Register in the DB

Register the newsletter asset:

```python
import oracledb, datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

today = datetime.date.today().isoformat()
post_number = "[POST_NUMBER]"
slug = "[SLUG]"
file_path = "[FULL PATH TO NEWSLETTER FILE]"

con = get_connection()
cur = con.cursor()

cur.execute("SELECT id FROM assets WHERE type='newsletter' AND post_number=:1", (post_number,))
existing = cur.fetchone()

if not existing:
    asset_var = cur.var(oracledb.NUMBER)
    cur.execute("""
        INSERT INTO assets (type, pipeline, short_name, description, status,
                            created_date, updated_date, file_path, post_number)
        VALUES ('newsletter','ai-for-you',:1,:2,'DRAFT',:3,:4,:5,:6)
        RETURNING id INTO :7""",
        [slug + "-newsletter",
         f"Newsletter for post {post_number} — Substack + LinkedIn editions",
         today, today, file_path, post_number, asset_var])
    asset_id = int(asset_var.getvalue())
    con.commit()
    print(f"Registered newsletter as asset {asset_id}")
else:
    print(f"Already registered as asset {existing[0]}")

# Register item statuses for the newsletter
cur.execute("SELECT id FROM posts WHERE post_number=:1", (post_number,))
post_row = cur.fetchone()
if post_row:
    post_id = post_row[0]
    for item_type in ('newsletter', 'substack_note'):
        cur.execute(
            "SELECT 1 FROM asset_item_status WHERE asset_id=:1 AND item_type=:2",
            (post_id, item_type)
        )
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO asset_item_status (asset_id, item_type, status) VALUES (:1,:2,'DRAFT')",
                (post_id, item_type)
            )
    con.commit()

con.close()
```

Then sync captions to PostVault — write the newsletter content to `post_captions` for the newsletter tab:

```python
import datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection

con = get_connection()
cur = con.cursor()

today = datetime.date.today().isoformat()
post_number = "[POST_NUMBER]"

# Resolve post_id
cur.execute("SELECT id FROM posts WHERE post_number=:1", (post_number,))
post_id = cur.fetchone()[0]

substack_edition = """[FULL SUBSTACK EDITION TEXT]"""
linkedin_edition = """[FULL LINKEDIN EDITION TEXT]"""
substack_note = """[SUBSTACK NOTE TEXT]"""

for platform, content in [
    ('substack-newsletter', substack_edition),
    ('linkedin-newsletter', linkedin_edition),
    ('substack-note', substack_note),
]:
    cur.execute(
        "SELECT id FROM post_captions WHERE post_id=:1 AND platform=:2",
        (post_id, platform)
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            "UPDATE post_captions SET caption=:1, updated_date=:2 WHERE id=:3",
            (content, today, row[0])
        )
    else:
        cur.execute(
            "INSERT INTO post_captions (post_id, platform, caption, created_date, updated_date) "
            "VALUES (:1,:2,:3,:4,:5)",
            (post_id, platform, content, today, today)
        )

con.commit()
con.close()
print("Captions synced to PostVault")
```

---

### STEP 7 — Report back

Tell the user:
- Newsletter file path
- Post number and slug confirmed
- Keyword registered
- Substack edition: title + subtitle
- LinkedIn edition: title (no subtitle)
- Substack Note: first sentence
- Asset DB ID
- "Ready for Phase 3: `/ai-for-you [path to newsletter file]`"

---

## Rules

- Never write the LinkedIn edition first. The shared body is the source of truth; endings are applied after.
- No em dashes anywhere in newsletter content. Zero.
- No markdown headers in the newsletter body (Substack does not render them). Bold labels only.
- The Substack Note is NOT a teaser for a different topic. It must arc around this issue's pain.
- Do not start Phase 3 (social content) from this skill. This skill stops at STEP 7.
