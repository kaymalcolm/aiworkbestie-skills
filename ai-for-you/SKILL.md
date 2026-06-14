# AI For You  -  Content Draft Skill

Generate a complete multi-platform content package for Kay Malcolm's "AI For You" series. Accepts a research file (preferred) or a topic directly. Always runs to a full draft — no research-only mode. For research-only, use `/ai-for-you-research`.

## When This Skill Activates

**From newsletter file (Phase 3 in pipeline):** User provides a path to a newsletter file (matching `[POST_NUMBER]-[SLUG]-newsletter-[DATE].md`) or says "run Phase 3 on [newsletter file]" / "continue from the newsletter file." In this mode, the newsletter content is already written — skip to social content only.

**From research file (preferred):** User provides a path to a research file (e.g. `/Users/kmalcolm/claude/iamkaymalcolm/research/2026-05-18-what-are-skills-research.md`) or says "go full mode on the research file" / "build out the full package from the research."

**From topic:** User types `/ai-for-you "[topic]"` or `/ai-for-you "[topic]" --slug my-custom-slug`

**Transcript mode:** User pastes a video transcript (long-form text). Detect this when the input is more than ~3 sentences of continuous speech/narration. In this mode, run STEP 1-TRANSCRIPT before STEP 1.

**Pending-post mode:** User provides a path to a `.md` file in the `pending-posts/` directory, or says "use the pending post" / "process the pending file". In this mode, run STEP 1-PENDING-POST before STEP 1. After saving the content package in STEP 5, move the source file to the `archive/` subfolder in the same `pending-posts/` directory.

**Intent detection:** Recognize requests like:
- "Draft an AI For You post about [topic]"
- "Create content for the AI For You series on [topic]"
- "Write the next AI For You post"
- "Here's the transcript, build the full package"
- "Go full mode" / "build it out" / "run full mode on [research file]"

---

## Autonomy Rules

Run the full workflow with no confirmation unless:
- Oracle DB credentials are missing (ask once, then proceed without DB lookup)
- The topic is ambiguous (ask one clarifying question maximum)
- The user explicitly asks you to pause

No mode question. This skill always generates the full content package.

---

## Workflow  -  Run Every Step in Order

### Reading a Newsletter File (newsletter file mode)

When the input is a newsletter file path (or when called by the orchestrator after Phase 2):

1. Read the newsletter file. Extract from the header:
   - `COMMENT_KEYWORD` — already registered in DB; use this verbatim
   - `POST_TYPE` — TEASE or FULL_CONTENT
   - `POST_NUMBER`
   - `SLUG`

2. Find and read the research file to get the B-roll direction, on-screen text hook, and hooks:
   ```bash
   ls /Users/kmalcolm/claude/iamkaymalcolm/research/*[SLUG]*research*.md 2>/dev/null | tail -1
   ```
   If found: read it, carry forward B-roll Direction, On-screen Text Hook, Hook Options, Audience Research verbatim.
   If not found: note it and proceed — B-roll direction will be written fresh in STEP 3b.

3. **B-roll direction review pause:** Display the carried-forward B-roll direction and on-screen text hook in full, then pause:
   > "B-roll direction and on-screen hook above are carried forward from Phase 1. Review them — type **continue** when ready to generate the full social content package."
   Wait for "continue" before proceeding.

4. Skip these steps entirely — they are already done:
   - STEP 0, STEP 0b (source files and audience research — already read in Phase 1)
   - STEP 2b (keyword registration — keyword already registered in Phase 2)
   - STEP 3g-i (Substack newsletter — already in newsletter file)
   - STEP 3g-ii (LinkedIn newsletter — already in newsletter file)
   - STEP 3g-iii (Substack Note — already in newsletter file)

5. For STEP 3g-iv (LinkedIn caption): read the newsletter title from the `## NEWSLETTER TITLE` section of the newsletter file and reference it when writing the caption.

6. Proceed from STEP 1 (parse post number/slug from newsletter file) → STEP 2 → STEP 3 (skipping 3g-i, 3g-ii, 3g-iii) → STEP 3h → STEP 4 → STEP 5 → STEP 5c → register handoff → STEP 7.

---

### Reading a Research File (if a research file was provided)

Read the research file at the provided path. Extract:
- `TOPIC` — from the file header
- `PROPOSED_POST_NUMBER` — use as starting point, then verify against `content-drafts/` count
- `SLUG` — use the proposed slug unless the user has provided a different one via `--slug` or in their command. Confirm the final slug in one line before proceeding: "Using slug `[SLUG]` — override?" If they don't respond or say yes, proceed.
- `CANDIDATE_KEYWORD` — the proposed keyword from the research file (not yet registered)
- Audience Research, Hook Options, B-roll Direction, On-screen Text Hook — carry these forward; do not redo the research
- Helper Content section — if the user filled it in, incorporate it into the carousel and newsletter

Skip STEP 0 (source files — already read during research). Skip STEP 0b (audience research already done). Skip STEP 3a (hooks already written). Skip STEP 3b-BROLL (B-roll direction already written, carry it forward).

Proceed from STEP 1 → STEP 2 → STEP 2b (register keyword) → STEP 3 (carousel, captions, YouTube, Threads, Twitter, Substack, infographic briefs) → STEP 3h (brand grader) → STEP 4 → STEP 5 → STEP 5c → register handoff → STEP 7.

---

### STEP 0  -  Read the source files first (topic-direct path only)

Skip this step if a research file was provided. Otherwise, before writing a single word of content, read these files.

1. **Master brand guide (brand voice, visual brand, positioning — all in one):**
   `/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md`

2. **Content strategy:**
   `/Users/kmalcolm/claude/iamkaymalcolm/strategy/general-strategy.md`

3. **Content plan files (pain points and audience context):**
   List all `.md` files in `/Users/kmalcolm/claude/iamkaymalcolm/strategy/` and read any that contain content plans, pain points, or audience notes. Use these to sharpen the pain framing.

4. **Existing content drafts (scan for topic overlap):**
   List files in `/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/` and read any that look topically related.

---

### STEP 1-PENDING-POST  -  Extract topic from a pending markdown file (pending-post mode only)

Read the file at the provided path (or if no path was given, list files in `/Users/kmalcolm/claude/iamkaymalcolm/pending-posts/` and use the most recently modified `.md` file that is not in `archive/`). Extract:

- **TOPIC**: Summarize the core subject in 5-10 words — reframe in Kay's audience context: career women using AI at work, not a general tech audience.
- **PAIN POINT**: What frustration does the source content address? Translate into the pain Kay's audience actually feels.
- **KEY POINTS**: 3-7 most useful, actionable points in logical teaching order. Discard anything too technical or developer-focused.
- **HOOK CANDIDATES**: 2-3 phrases or ideas from the file, rewritten in Kay's voice. Do not lift phrasing verbatim.
- **TONE NOTES**: Tactical/list-based or narrative? How should Kay's version feel different?
- **FORMAT HINT**: Carousel (multiple discrete tips) or reel (single insight or story)?

Write these as a brief internal block under `## Pending Post Extraction`. Then continue to STEP 1 using the extracted TOPIC and FORMAT HINT.

Do NOT carry over branding, usernames, creator names, or source attribution.

**After saving the content package in STEP 5**, move the source file to archive:
```
mv [source file path] /Users/kmalcolm/claude/iamkaymalcolm/pending-posts/archive/
```
Confirm the move completed. Create the archive directory if it doesn't exist.

---

### STEP 1-TRANSCRIPT  -  Extract topic from transcript (transcript mode only)

If the input is a transcript, do this before STEP 1. Read the transcript and extract:

- **TOPIC**: Summarize the core subject in 5-10 words
- **PAIN POINT**: What problem does Kay open with or return to? Use her exact words if possible.
- **KEY POINTS**: 3-7 main points in the order she makes them
- **HOOK CANDIDATES**: 2-3 punchy lines — raw material for hook options in STEP 3a
- **TONE NOTES**: More serious/tactical or light/conversational? Any phrases distinctly Kay's voice?
- **FORMAT HINT**: Numbered list (good for carousel + list-format reel) or story/single insight (reel only)?

Write these under `## Transcript Extraction`. Then continue to STEP 1 using the extracted TOPIC and FORMAT HINT.

Do NOT invent points that aren't in the transcript. Note unclear sections as `[unclear in transcript]`.

---

### STEP 0b  -  Research the audience's real pain (topic-direct path only)

Skip this step if a research file was provided. Otherwise, do live research on what Kay's target audience is actually feeling right now about this topic. Generic pain framing is why content gets ignored.

**Who is Kay's audience:** Career women (35-50), corporate jobs, not developers, using AI as a tool at work. Many are mid-to-senior level, politically aware, financially stretched, and quietly afraid of being left behind. They scroll from exhaustion, not curiosity.

**Run 2-3 web searches using relevant queries:**
- `site:reddit.com "AI at work" [topic keyword] women career 2025 OR 2026`
- `"[topic keyword]" "at work" frustrating OR "I don't know" OR "nobody tells you" career`
- `LinkedIn OR TikTok comments "[topic]" corporate women professionals`

**What to extract:**
- The exact words real people use when they complain, confess, or ask for help. Verbatim phrasing is gold.
- The fear underneath the frustration.
- The specific situation where the pain hits.
- What they're embarrassed to admit.
- Any cultural or economic context from the past 2-4 weeks that sharpens urgency.

**Record findings in a `## Audience Research` block:**
- 3-5 real phrases or situations (quoted or paraphrased)
- The underlying fear in plain language (1-2 sentences)
- A "what nobody is saying out loud" observation
- Any current-events context

Use these findings to inform everything downstream: hook, pain framing, caption, newsletter opening.

If web search is unavailable, note it and proceed with Kay's content plan files + your knowledge of the audience.

---

### STEP 1  -  Parse the input

Extract:
- `TOPIC`: The content idea string
- `POST_NUMBER`: Count files in content-drafts matching `ai-for-you-0*.md`. Confirm this is accurate before proceeding.
- `SLUG`: The kebab-case short name used for all file names and the DB `short_name`. Use the slug from the research file, or accept a user-supplied override via `--slug my-slug`. If deriving from a topic directly: lowercase, hyphens, 3-5 meaningful words, drop stop words. This is the final slug — confirm it before writing any files.

If `POST_NUMBER` cannot be determined, use `NNN` as a placeholder.

---

### STEP 2  -  Determine post format

Based on the topic and the 1-in-3 full content rule:

- Is this every 3rd post? → FULL CONTENT post (everything in the post, lighter newsletter ask)
- Otherwise → TEASE post (full prompts/resources live in newsletter, social content teases)

**Video format (Instagram / TikTok / YouTube Short — same video):**

- **FORMAT 1 (Value post):** Topic delivers prompts, frameworks, or step-by-step guidance → multi-clip B-roll (desk, screen recording, laptop, lifestyle) + text overlay. Caption contains the actual value embedded.
- **FORMAT 2 (Take post):** Topic is a reaction, opinion, or commentary → single everyday lifestyle clip (coffee, car, airport, walking) + text overlay of Kay's take. Shorter conversational caption.

**Platform routing:**
- IG / TikTok / YouTube Short: same B-roll video, platform-adjusted captions
- LinkedIn: carousel / document only — no video
- Threads: caption only — no video, no ManyChat CTA
- YouTube Long: dropped — do not generate

Document the format decision (FORMAT 1 or FORMAT 2, FULL CONTENT or TEASE) at the top of the output file.

---

### STEP 2b  -  Generate and register the comment keyword

**Skip this entire step if coming from a newsletter file.** The keyword is already registered in Phase 2. Read `COMMENT_KEYWORD` from the newsletter file header and use it. Do not query or INSERT.

Every post uses a single comment keyword woven through Instagram caption, YouTube closing, and the last carousel slide. The keyword must be unique across all posts.

**If coming from a research file:** The candidate keyword is already in the file. Query to confirm it is still available. If available, register it. If it was taken since the research file was created, generate a new one and register that instead.

**If running from a topic directly:** Query for used keywords, generate a candidate, register immediately.

**Query the DB for all previously used keywords:**

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

**Generate a keyword candidate:**

Short (4-8 characters), easy to type, loosely relevant to the topic (e.g., topic is "AI in meetings" → MEET, BRIEF, ROOM, SYNC), all-caps when displayed, NOT in the `used` set, NOT a generic word like AI, YES, GO, MORE, TIPS, HELP, FREE.

Write as `COMMENT_KEYWORD = "[WORD]"` at the top of the output file.

**Register immediately:**

```python
import datetime, sys
sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import get_connection
today = datetime.date.today().isoformat()
keyword = "[CHOSEN KEYWORD]"
post_number = "[POST_NUMBER]"
topic = "[TOPIC]"

con = get_connection()
cur = con.cursor()
cur.execute("SELECT id FROM posts WHERE post_number = :1", (post_number,))
post_row = cur.fetchone()
post_id = post_row[0] if post_row else None
try:
    cur.execute(
        "INSERT INTO comment_keywords (keyword, post_id, topic, registered_date) VALUES (:1,:2,:3,:4)",
        (keyword.upper(), post_id, topic, today)
    )
    con.commit()
    print(f"Keyword '{keyword}' registered for post {post_number}")
except Exception as e:
    if "ORA-00001" in str(e) or "unique constraint" in str(e).lower():
        print(f"Keyword '{keyword}' already taken — choose another and re-run")
    else:
        raise
con.close()
```

If the INSERT fails (duplicate), generate a different word and try again before proceeding to STEP 3.

Use `COMMENT_KEYWORD` consistently everywhere: Instagram caption CTA, last carousel slide, YouTube Short description.

---

### STEP 3  -  Generate the content package

Write all of the following. Every section. No placeholders. Full content.

#### 3a. THE HOOK (non-negotiable  -  write this first)

**If coming from a research file:** The hooks are already written — carry forward all three from the research file and select the strongest for use in the content. No need to rewrite.

**If running from topic directly:** Write 3 hook options. One sentence each. Name the pain. Make the audience feel seen.

The hook must come from the STEP 0b research. If research turned up specific phrases, situations, or fears that real people expressed, that is the raw material. Refine into Kay's voice — do not sanitize the emotion.

**What a real hook does:**
- Names the specific situation, not the general problem. "You just watched a 23-year-old present the AI summary you spent 2 days writing by hand" lands harder than "AI is changing the workplace."
- Says the thing the audience is embarrassed to admit.
- Uses the ugly truth. Polite hooks get scrolled.
- Speaks to who they ARE, not who they should become.

**What a real hook does NOT do:**
- Offer to help. The help comes later.
- Compliment the audience.
- Start with "Have you ever..." or "Are you..."
- Use em dashes.
- Sound like an ad or a motivational poster.

**The test:** Read the hook out loud. If it sounds like something a polished brand account would say, rewrite it.

Write 3 hook options. Each must name a DIFFERENT specific pain or situation. Do not write three variations of the same angle.

**REQUIRED: One of the three must be an "Insider Access" type** naming a specific Kay credential in the first sentence:
- "20 years in enterprise tech"
- "LinkedIn Learning instructor"
- "VP at Oracle"
- "VP of Product Management for the AI Database"
- "tech executive at one of the largest tech companies"
- "I'm AI obsessed and I instruct my team to use it every day to innovate"

The authority signal must appear in the first 3 seconds on Instagram. If all three options are pain-forward without a credential anchor, rewrite one.

Example Insider Access hook: "After 20 years in enterprise tech, I can tell you exactly which AI skills your company is actually watching for — and it's not what the LinkedIn posts say."

#### 3b. INSTAGRAM

**B-ROLL VIDEO (IG / TikTok / YouTube Short — write this once, used across all three):**

**If coming from a research file:** Carry forward B-roll Direction and On-screen Text Hook verbatim. If the user added Helper Content or context, incorporate it into the carousel and newsletter rather than rewriting the B-roll direction.

**If running from topic directly:** Write the B-roll direction now.

---

**ON-SCREEN TEXT HOOK:**
The exact text that appears as an overlay on the first clip. Max 10 words. Must stop the scroll on its own — pain-naming or credential-anchoring. This is the first thing the viewer reads. Include a second line with Kay's credential (LinkedIn Top Voice for AI / VP at Oracle) if not already in the hook.

**B-ROLL DIRECTION:**
What footage to use, in what order.
- FORMAT 1: list 3-6 clips with timing and what each shows (desk, screen recording, typing, laptop, coffee, lifestyle). Pull from Kay's existing library where possible. Be specific — "Screen shows a ChatGPT or Claude response appearing" not "AI footage."
- FORMAT 2: one clip — name the specific setting (coffee shop, car, walking outside, airport). One lifestyle moment, no face required.

**TEXT OVERLAY PER CLIP:**
- FORMAT 1: what key text appears over each clip segment. One punchy phrase, stat, or prompt excerpt per clip (5-10 words each). These carry the content value.
- FORMAT 2: Kay's full take as text overlay — short enough to read in one screen pass.

**END CARD DIRECTION:**
Last 2-3 seconds. Specify what text appears on screen. Always ends with the comment keyword CTA formatted for the platform:
- IG end card: "Comment [KEYWORD] for [specific named thing]"
- TikTok end card: "DM me [KEYWORD] for [specific named thing]"
- YouTube Short end card: "Full guide linked below"

---

**CAROUSEL (7-9 slides):**

- Slide 1: Hook (same hook as reel, restated for static format)
- Slides 2-N-1: One point per slide. Concrete. Actionable.
- Last slide: CTA (named-promise comment keyword CTA — see caption rules below)

**Carousel body copy rules (apply to every slide):**

- **30-word body limit.** If the body won't fit in ~30 words, split into two slides.
- **Prompts and templates get their own slide each.** Never put two prompt templates on one slide — not pipe-separated, not line-break separated. One template = one slide.
- **Lists become bullets, not prose.** If a slide answers "what are the X things," write 3–5 short bullets. Prose that reads in a newsletter becomes unreadable at carousel scale.
- **No pipe separators.** `item A | item B` in a body field means the slide needs to split.
- **Headline carries the point, body carries the proof.** The headline should be specific enough to stand alone. Body adds the concrete detail — it does not restate the headline.

The carousel and reel are posted together as a pair.

**Instagram Caption (optimize for saves and shares):**

Instagram's algorithm ranks saves > shares > comments > likes. Every caption decision flows from this.

- **Caption length: FORMAT 1 captions embed the actual value (prompts, frameworks) so they can run longer — up to 200-300 words. FORMAT 2 captions are conversational and short — 80-120 words max.**
- First line is the only line visible before "more" — it must stop the scroll on its own.
- If there's a current-events anchor (layoffs, economic news, viral AI moment), lead with 1-2 sentences of warmth or empathy tied to it, then pivot immediately to the value.
- The caption is NOT a rewrite of the video/slides. Use emoji bullets as punchy one-liners, not paragraphs.
- Name specific tools by brand: "Claude, Gemini or ChatGPT" not "AI tools"
- Use thematic emoji bullets (🤔 📈 👀 💡 etc.) — pick emojis that add meaning. Reserve 1️⃣ 2️⃣ 3️⃣ only when sequence actually matters.
- Include one hot take with Kay's banter voice — "Don't be mad at me, but..." / "fight me in the comments, I said what I said."
- Add personal proof. First-person past tense beats generic every time.
- Directive framing: "This is what I want you to do" not "And it starts with one shift."
- Hashtags: 5-10, mix of broad (1-2M posts) and niche (under 100K). Place at end or first comment. No more than 10.
- No em dashes, no AI poetry, no corporate-speak.

**REQUIRED: Named-promise comment keyword CTA:**
Every caption must end with a comment keyword CTA that names the specific thing the audience receives.
- ALLOWED: "Comment STACK and I'll DM you the exact 4-tool list I use every day."
- NOT ALLOWED: "Comment AI for more." or "Comment AI and I'll send you something."

**REQUIRED: Separate share_trigger line:**
Every caption must include a distinct share trigger — not a save trigger, not the comment trigger. It drives distribution. Place it one line above the comment keyword CTA.
- ALLOWED: "Send this to your work bestie who got handed AI tools and no training."
- NOT ALLOWED: "Save this so you have it."

#### 3c. TIKTOK

**B-roll video:** Same video as Instagram. The TikTok file must be self-contained — include the full B-roll direction and TikTok-specific end card direction verbatim. Do NOT use a placeholder reference. Only the end card text changes from the Instagram version (DM trigger instead of comment trigger).

**Carousel:** Same slide content as Instagram carousel.

**TikTok Caption (optimize for watch time and DM triggers):**

TikTok's algorithm rewards watch time (rewatches, completion rate) and comments.

- First 1-3 lines show before "more." Write the first line to create a loop — a bold claim they want to test, a question they already have an answer to, a stat they don't believe.
- Keep it SHORT. 100-150 characters before the cut.
- **CTA must be a DM trigger, not a comment trigger.** Always use: "Message me the word [KEYWORD] and I'll send you [specific thing]." Never "comment below."
- Tone is more casual and unpolished than Instagram. Contractions. Sentence fragments. Direct address.
- Hashtags: 3-5 only. One broad trending, two niche.
- No em dashes. No corporate tone.

#### 3d. YOUTUBE SHORT

**B-roll video:** Same video as Instagram and TikTok. Do NOT rewrite the B-roll direction inline — reference the Instagram/TikTok file path. The YouTube Short file is a description-only asset in the DB.

YouTube Long-Form is a dropped format — do not generate it.

**YouTube Shorts Title (for search — not just scroll-stopping):**

YouTube is a search engine first. The title must contain the keyword someone would actually type, front-loaded. Under 60 characters. No clickbait that doesn't deliver.

Write 2 title options: one keyword-first, one curiosity-first (for Shorts feed discovery).

**YouTube Shorts Description:**

- Line 1: Restate the core value claim. Include the main keyword naturally.
- Line 2-3: 1-2 sentences of context. Who this is for. What they'll walk away with.
- Line 4: "Subscribe for weekly AI career content for corporate professionals. @iamkaymalcolm"
- Line 5: CTA — "The full guide is linked below and in the first pinned comment." Do NOT write "Comment [KEYWORD] and I'll send you..." — ManyChat does not support YouTube and there is no automation to fulfill it.
- Line 6+: Relevant links (Substack, Instagram) one per line, labeled clearly.
- Tags: 8-12 keyword tags. Mix broad (artificial intelligence, ChatGPT) and specific (AI at work, career AI tips).
- No em dashes. Write for someone who found this from search.

#### 3e. TWITTER / X

Twitter/X rewards full answers, not teases. Write a 5-7 tweet thread that actually delivers the content. A single-tweet tease does not get engagement on Twitter.

**Thread structure:**
- **Tweet 1 (1/N):** Hook — the specific pain or question. Include Kay's credential anchor in this tweet (LinkedIn Top Voice for AI, Oracle role, or LinkedIn Learning). Create forward pull: "Q[X] is where most people are making the mistake."
- **Tweets 2 through N-1:** One tweet per key point or Q&A answer. Give the actual answer — do not tease. Each tweet stands alone.
- **Final tweet (N/N):** CTA. The full guide or prompts are in the AI For You newsletter. "Link in bio. @iamkaymalcolm"

**Rules:**
- No ManyChat automation on Twitter — CTA is "link in bio" or a reply prompt (manual). Never promise an automated DM.
- No em dashes anywhere in the thread.
- No staccato bursts — never 3 or more short sentences in a row in any single tweet.
- Drop straight into the point in tweet 1 — no "Hey [X]" opener.
- No "Honest answers." as a standalone sentence — merge into the surrounding sentence.
- Avoid parallel lists within a single tweet (e.g. three em-dash bullets). Use colon or restructure instead.

#### 3f. THREADS

Threads rewards conversational, text-forward content and personal opinions. Write like you're in a room full of people who already like you and want to know what you think.

3 posts:
- Post 1: The personal observation or story behind the topic. 2-4 sentences. First-person. Specific detail that makes it real.
- Post 2: The condensed insight or practical takeaway. Short list (3 items max) or a single strong sentence. Something they'd screenshot.
- Post 3: A genuine question that invites personal stories. Something specific enough that they have an actual answer.

No hashtags on Threads.

#### 3g. NEWSLETTERS + LINKEDIN CAPTION

**If coming from a newsletter file:** Skip 3g-i, 3g-ii, and 3g-iii entirely. Jump directly to 3g-iv (LinkedIn caption). The newsletter title for the LinkedIn caption reference is in the `## NEWSLETTER TITLE` section of the newsletter file.

**Dependency order — generate in this sequence (topic or research file input only):**

1. Substack newsletter (3g-i) — generated first; this is the source of truth
2. LinkedIn newsletter (3g-ii) — derived from the finalized Substack; generate after Substack body is complete
3. Substack note (3g-iii) — written after the Substack body is locked; teases the issue
4. LinkedIn caption (3g-iv) — written last; depends on both the reel content and the finalized newsletters

---

#### 3g-i. SUBSTACK NEWSLETTER

Full issue. Full resources. This is where the depth lives.

**Header:**
- Title: This is the email subject line. Two proven angles:
  - **FOMO/peer comparison (Option A):** Makes the reader feel like people around them are already ahead. Example: "Your colleagues are already using these 4 AI prompts. Are you?"
  - **Counterintuitive/pain-naming (Option D):** Challenges bad advice they've already heard. Example: "Stop Googling 'how to use AI.' Do these 4 things instead."
  - Do NOT write: a description of the content, a vague promise, or anything that sounds like a company newsletter.
  - No em dashes anywhere in the title. Zero.
- Subtitle: 1 sentence that lands the punch the title started. No em dashes.

---

#### 3g-ii. LINKEDIN NEWSLETTER

Generated after the Substack body is complete. Do not write this first.

**Title:** Same as the Substack title. No subtitle field on LinkedIn — omit it.

**Content:** Verbatim identical to the Substack newsletter body — same byline, same opening, same moves, same prompts, same code blocks, same infographic placeholders, same signoff. Do not condense, summarize, or shorten. The only two differences:
- No subtitle
- The sign-off footer line omits the Substack URL since the reader is already in a LinkedIn newsletter

Label this section clearly as `## LINKEDIN NEWSLETTER` in the draft file.

---

#### 3g-iii. SUBSTACK NOTE

Write a standalone short post — 3-5 sentences max. Lives on Kay's Substack profile as a Note. Must be topically connected to the newsletter issue — it arcs around the pain or problem the newsletter addresses and makes the reader curious enough to click through. NOT a note on a different subject. Label clearly as `### Substack Note` in the draft.

---

#### 3g-iv. LINKEDIN CAPTION

Generated last — after the B-roll direction, carousel, and both newsletters are finalized.

**Format:**
- Opening: 1-2 sentences naming the specific pain the reel addresses. First-person, direct.
- Bullet list: 4-6 emoji bullets teasing the content (one per tip/mistake/move). Short.
- Bridge: 1 sentence pointing to the newsletter in the first comment.
- Closing: A specific question that invites a personal answer.

**Rules:**
- No ManyChat keyword trigger — LinkedIn does not support comment automation
- CTA drives to the LinkedIn newsletter only (not Substack)
- No em dashes
- No hashtags
- Tone: warm and direct, not polished brand voice

Label clearly as `## LINKEDIN CAPTION` in the draft file.

**Newsletter body formatting (Substack plain-text rules):**
Substack's editor does not render markdown.
- Section headers: Bold label style — **Move 01: [Name] | [time]** — no ## markdown headers
- Prompts: code blocks so they're visually distinct and easy to copy
- Featured resources: code blocks
- Links: full URL on its own line, no markdown hyperlink syntax
- Line spacing: blank line between every paragraph
- No em dashes anywhere. No markdown except code blocks.

**Newsletter voice rules:**
- Open in 3 short paragraphs: (1) empathy/relatable observation; (2) personal entry (Kay's own experience); (3) timely context + credential + what they're getting.
- Each section gets 2-3 sentences of narrative context before the code block or resource — the specific reason this move matters, not a story block, not one staccato sentence. Then the resource.
- Personal asides in parentheses are fine and encouraged when genuinely useful.
- Closing is two sentences: one concrete action + one reply ask.
- Sign-off: Kay [line break] title line. Nothing else.

**Structure (in order):**
1. Byline: `*AI For You | Kay Malcolm, VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor*`
2. Opening: 3 short paragraphs
3. MID-ARTICLE INFOGRAPHIC placeholder — place right after the opener, before any content moves
4. Content moves — for each move: **Bold label | time**, 2-3 sentences of context, full prompt in code block
5. END INFOGRAPHIC placeholder — after the last move, with one-line caption
6. Closing: one action sentence + reply ask
7. Sign-off: Rotate between these versions — pick the one that fits the post's tone; do not repeat the same version in consecutive posts.

   **Version A** (warm, full — use for community/relationship-forward posts):
   ```
   Signed 🫶🏾,

   Kay, Your AI Work Bestie

   *VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*

   *AI For You is a weekly newsletter for corporate women (guys you can read it too, relax fellas and let us girls support each other) navigating careers in the AI era. Real tools. Real prompts. No tech background required. -- iamkaymalcolm.substack.com*
   ```

   **Version B** (tight — use for tactical/prompt-heavy posts):
   ```
   Signed 🫶🏾,

   Kay, Your AI Work Bestie

   *VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*
   ```

   **Version C** (classic — use for thought leadership or longer-form posts):
   ```
   Signed 🫶🏾,

   Your AI Work Bestie,
   Kay

   *VP @ Oracle | LinkedIn Top Voice | LinkedIn Learning Instructor | Views are my own*

   *AI For You is a weekly newsletter for corporate women navigating careers in the AI era. Real tools. Real prompts. No tech background required. -- iamkaymalcolm.substack.com*
   ```

#### 3h. INFOGRAPHIC BRIEFS

Every post gets TWO infographics:

**INFOGRAPHIC 1  -  MID-ARTICLE (square, 1:1):**
A visual anchor placed right after the opener, before the first content move. Square format (1080x1080). IMAGE-FORWARD — a lifestyle photo or illustrated scene takes up most of the frame. The stat, quote, or insight appears as a text overlay. Pick the one insight, stat, or quote most shareable on its own.

```
Mid-article infographic brief:
Format: Square 1:1 (1080x1080px)
Series badge: AI FOR YOU | AI Work Bestie  -  top left, gold/amber. NO post number.
Visual suggestion: [describe the lifestyle photo or scene. When illustrating a human figure, she is always an African American woman with collarbone-length curly natural hair and glasses.]
Stat/quote overlay: [the one insight/stat/quote — short, readable over a photo]
Supporting line: [1 line max]
Style: MOSTLY PHOTO. Text overlays in white or gold. Dark photo treatment to ensure text reads. Minimal text.
CTA: @iamkaymalcolm  -  bottom corner, small
Color palette: Soft feminine tones  -  blush pink (#F7CAD0), warm lavender (#E8D5F5), champagne (#F0E2C8), light gold (#FDF3DC), or blush-to-champagne gradient. Accent in gold/amber (#F4A261). NO dark navy backgrounds.
```

Label clearly as `### MID-ARTICLE INFOGRAPHIC` in the newsletter body.

**INFOGRAPHIC 2  -  DOWNLOAD/SHARE (portrait, full layout):**
The full structured infographic — all rows, bottom stat, CTA bar. Portrait format. Goes at the end of the newsletter or referenced in the P.S.

```
Badge: AI FOR YOU | AI Work Bestie  -  top left, gold/amber. NO post number.
Color palette: Soft feminine tones  -  blush pink (#F7CAD0), warm lavender (#E8D5F5), champagne (#F0E2C8), light gold (#FDF3DC), or blush-to-champagne gradient. Text in deep plum (#2D1B2E) or near-black. Accent in gold/amber (#F4A261). NO dark navy. NO black backgrounds.
If any illustrated human figure appears, she is an African American woman with collarbone-length curly natural hair and glasses.
Title: [punchy, bold — must be a pain point or problem, never the solution]
Subtitle: [supporting line]

Row 1: [use case / tip name]  ⏱ [time estimate if applicable]
  Teaser: "[opening line of the full prompt or tip]..."
  What you get: [1-line description of output]
  📩 Full [resource] → AI For You newsletter

Row 2: [same format]
Row 3: [same format  -  or fewer rows if fewer points]

Bottom stat: [one striking data point]
CTA bar: [relevant URL] | @iamkaymalcolm | iamkaymalcolm.substack.com
```

Row labels are plain text only — NO numbered emoji (1️⃣ 2️⃣ 3️⃣) on infographic rows.

Note whether this is a FULL CONTENT infographic (all value shown) or TEASE infographic (opening line only, newsletter is the payoff).

---

### STEP 3h  -  Run the brand grader on ALL platform content (required)

After all content is drafted, run `/ai-for-you-grader` on every piece of platform content before saving any files. Do not write a single file or touch the DB until every section passes. Fix inline, then re-grade.

Run in this order:

**1. B-roll direction + on-screen text hook** — Extract: hook text, clip-by-clip direction, text overlay script, end card direction.
**2. Carousel slides** — Extract: hook slide + content slides + CTA slide.
**3. Instagram caption** — Extract: full caption including hashtags and share_trigger line.
**4. TikTok caption** — Extract: full caption.
**5. Threads posts** — Extract: all 3 posts verbatim.
**6. Twitter/X post** — Extract: the single post.
**7. YouTube Short** — Extract: both title options and the full description.
**8. Newsletter + Substack Note** — Extract: newsletter title, subtitle, full body, and Substack Note.

**Fix loop:** If the grader flags anything, fix it immediately, then re-run the grader on that section only. Do not proceed until the section passes. Maximum 3 fix iterations per section; if a section cannot pass after 3 attempts, flag it with a note to the user and stop.

Do not write any file and do not write to the DB until all eight sections have returned a passing grade.

---

### STEP 4  -  Note on publishing

All platforms post on the same day via Buffer. Do NOT suggest a posting sequence or stagger. Just note that everything in the package is ready to queue.

---

### STEP 5  -  Save the output files

Save the content package as separate platform files. All files go in the post folder:
`/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/`

Where `POST_FOLDER` = `[POST_NUMBER]-[slug]`. Create the folder if it doesn't exist.

**Files to generate:**

- **Instagram + TikTok:** `[POST_NUMBER]-[SHORT_NAME]-instagram-tiktok-[DATE].md`
  Contains: B-roll direction, on-screen text hook, text overlay script, end card direction, carousel slides, Instagram caption + hashtags, TikTok caption + hashtags.

- **Threads:** `[POST_NUMBER]-[SHORT_NAME]-threads-[DATE].md`

- **Twitter/X:** `[POST_NUMBER]-[SHORT_NAME]-twitter-[DATE].md`

- **YouTube Short:** `[POST_NUMBER]-[SHORT_NAME]-youtube-short-[DATE].md`
  Contains: YouTube Short title options, description, tags. References the Instagram/TikTok file for B-roll direction — do not duplicate.

- **Substack + LinkedIn:** `[POST_NUMBER]-newsletter-[SHORT_NAME]-[DATE].md`
  Contains (in order): Substack newsletter (title, subtitle, full body), Substack Note, LinkedIn newsletter (title, no subtitle, full body), LinkedIn caption.

**File header for each platform file (always at top):**

NEVER include issue numbers, series numbers, or sequential post counts in document headers, body, or series badges. Use the 4-digit post folder number only in the filename.

```
# AI For You  -  [PLATFORM]  -  "[Topic as stated by user]"

**Series:** AI For You
**Platform:** [INSTAGRAM-TIKTOK / THREADS / TWITTER / YOUTUBE / SUBSTACK]
**Format:** [B-ROLL + TEXT OVERLAY / B-ROLL + TEXT OVERLAY + CAROUSEL]
**Full content or tease:** [FULL CONTENT / TEASE - newsletter]
**Pain this speaks to:** "[one sentence]"
**Status:** Draft v1
**Date:** [today's date]
```

---

### STEP 5c  -  Sync brief to Drive (if brief exists)

After saving all platform files, check whether a brief already exists for this post.

**Find the brief:**
```bash
ls /Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_FOLDER]/[POST_NUMBER]-*-brief-*.md 2>/dev/null | tail -1
```

If a brief is found:
1. Read the brief and the updated platform files.
2. Replace the full `## 📋 CAPTIONS  -  READY TO PASTE` section with fresh verbatim content from the updated platform files.
3. Replace the B-roll direction and on-screen text hook inside `## 🎬 REEL DIRECTION` if they changed.
4. Save the brief file in place.
5. Upload to Bay's Drive:

```python
/opt/homebrew/bin/python3.12 - << 'PYEOF'
import subprocess
brief_path = "[BRIEF_FILE_PATH]"
post_folder = "[POST_FOLDER]"
subprocess.run(["rclone", "copy", brief_path,
                f"gdrive:AI LinkedIn 2026/{post_folder}",
                "--drive-root-folder-id", "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"], check=True)
print(f"Brief updated and synced to Drive: AI LinkedIn 2026/{post_folder}/{brief_path.split('/')[-1]}")
PYEOF
```

If no brief exists, skip this step silently.

---

### After STEP 5c  -  Register in the asset DB

Run `/ai-for-you-register [POST_NUMBER]` after all files are saved. The register skill reads the saved files and writes all DB rows (posts, assets, destinations, scripts, slides, captions, keywords, production, queue position). Do not proceed to STEP 7 until registration is confirmed.

---

### STEP 7  -  Confirm and offer next steps

After saving the file and confirming registration, tell the user:
- The file path
- Which format was chosen and why (1 sentence)
- Whether this is a full content or tease post
- Offer: "Want me to generate the infographic now?" (uses the `/ai-for-you-infographic` skill)

Do NOT summarize every section back to the user. Just tell them it's done and where it is.

---

## Voice Rules (Enforced  -  Non-Negotiable)

These apply to every word of content generated:

1. **No em dashes. Ever. Anywhere. Not in captions, not in scripts, not in the newsletter, not in headers, not in CTAs. Not one. Zero.** Use a period, a line break, or rewrite the sentence.
2. **No AI poetry.** No metaphors that sound like a robot trying to be deep.
3. **No generic motivational filler.** "You've got this." Delete on sight.
4. **Use Kay's terms of address.** "Boos," "love," "friend," "beloved" — not "ladies," not "girls," not "everyone."
5. **Sentence fragments are fine.** But do NOT cluster 3 or more short sentences in a row. Mix sentence lengths throughout. "Open Claude. Copy this prompt. Fill in the brackets. Hit send." sounds robotic. Write it as flowing prose: "Open Claude, copy this prompt, fill in the brackets, and hit send."
6. **Numbered lists with emoji.** 1️⃣ 2️⃣ 3️⃣ for advice content in captions.
7. **One CTA per post.** Not two. Not three. One.
8. **Name the pain before delivering the value.** Every time.
9. **Millennial energy.** Warm, direct, a little dry, occasionally funny. Not Gen Z chaotic. Not corporate distant.
10. **Read the real examples in the BRAND VOICE section of the brand guide before writing.** They are the calibration standard.
11. **Infographic title is always a pain point or problem, never the solution.** The solution goes in the subtitle or the rows.

12. **Anti-AI Writing Standards  -  Hard Requirements:**

   Every section must pass all four tests. These are not optional.

   **Test 1  -  Originality:** Could Claude write this without Kay's input? If yes, add something only Kay can provide: a specific observation, a real memory, a lived detail, an opinion with 20 years of receipts behind it.

   **Test 2  -  Human:** Would someone reading this know it was AI-assisted? If yes, rewrite it.

   **Test 3  -  Tone:** Is it casual, conversational, relatable, thought-provoking? If it reads like a brand account or a content template — rewrite it.

   **Test 4  -  Pattern:** Kill any AI rhetorical construction on sight:
   - "Whether X or Y..." framing
   - "That is not X. It is Y." / "Not X. It is Y." constructions
   - "No X. No Y. Just Z." triple negation
   - Triplets used for rhetorical effect ("every tool, every update, every workflow")
   - Perfectly balanced parallel arguments
   - "That's the whole point." / "That distinction is everything."
   - Any sentence that reads like a tagline or closing epigram
   - Three or more short staccato sentences in a row
   - Two consecutive sentences mirroring each other in structure
   - The word "exactly" — anywhere, any context. Filler affirmative.
   - Filler -ly adverbs: genuinely, honestly, literally, basically, simply, clearly, obviously, naturally, certainly, definitely, absolutely, truly, deeply, seamlessly, effortlessly, effectively, essentially, ultimately, particularly, especially. If removing the word changes nothing, kill it. If it changes meaning, find a stronger word.

   **Human imperfections — require at least one per major section:** a parenthetical aside, an unexpected turn, a specific detail that's too particular to be invented, a moment where Kay admits she didn't have it figured out.

---

## Source Attribution Rule

If the content, transcript, or idea was copied or adapted from another account or creator, do NOT reference, credit, or mention that account anywhere. The content is Kay's. Write it that way, full stop.

---

## AI Tool Reference Rule

When a skill, prompt, or tip works with any AI tool (Claude, ChatGPT, Gemini, etc.), refer to it simply as **"AI"** — not "free at claude.ai", not "Claude", not a specific platform. Only mention claude.ai by name when the post is explicitly about Claude as a platform.

---

## What This Skill Does NOT Do

- Does NOT post to any platform (no API calls to Instagram, TikTok, etc.)
- Does NOT generate the infographic (offers to, then hands off to `/ai-for-you-infographic`)
- Does NOT register the draft in the DB (hands off to `/ai-for-you-register`)
- Does NOT make assumptions about the topic beyond what's in the command — if the topic is vague, ask one clarifying question

---

## Error Handling

**If a source file is missing:**
Proceed without it. Note at the top of the output which files were unavailable.

**If the topic is too broad:**
Write the content for the most concrete, actionable interpretation and note the interpretation chosen.

**If the topic has been covered before (based on content-drafts scan):**
Flag it at the top of the output: "Note: ai-for-you-002 covered [related topic]. This post builds on that by focusing on [specific angle]."
