# AI For You — Newsletter Adapt Skill

Adapts external source material (another creator's newsletter, article, or URL) into Kay's AI For You newsletter format. Produces all four platform outputs in one pass: Substack newsletter, Substack note, LinkedIn newsletter, LinkedIn caption.

## When This Skill Activates

**Explicit:**
- `/content-kit-newsletter-adapt [source URL or file path] [post number]`
- `/content-kit-newsletter-adapt [post number]` — if source URL is already in the plan file

**Intent detection:** Recognize requests like:
- "Adapt Ruben's newsletter on X into my format"
- "Turn this article into my newsletter"
- "Convert this into the AI For You format for post 1048"
- "Build the newsletter from this source"

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

Run the full workflow with no confirmation. Do not ask for approval before writing the file. Auto-detect the next post number if not given (count folders in `{BASE_DIR}/posts/` matching `[0-9][0-9][0-9][0-9]-*`). Read the source, pick the structure, map the content, write all four sections, grade, fix, save.

---

## Workflow

### STEP 0 — Read source material

If a URL is given, fetch it with WebFetch.
If a file path is given, read it directly.
If neither, check for a plan file under `/Users/kmalcolm/.claude/plans/` referencing the post number — source URL may be in there.

Extract from the source:
- Core topic and angle
- All key points, claims, examples, data
- The intended audience the source was written for (note: Kay's audience is corporate women 28-45, not the source's audience)

---

### STEP 1 — Determine post number and create folder

If not passed as an argument:
```bash
ls {BASE_DIR}/posts/ | grep -E '^[0-9]{4}-' | sort | tail -1
```
Increment by 1 for the new post number.

Derive `SLUG` from the topic (kebab-case, 3-5 words, no stop words).

Create the post folder:
```bash
mkdir -p {BASE_DIR}/posts/[POST_NUMBER]-[SLUG]
```

---

### STEP 2 — Select structure type

Pick one of the six structures based on what the source content is best suited to deliver to Kay's audience. Do not default to Moves. Match the structure to the content type.

| # | Structure | Header format | Best for |
|---|---|---|---|
| 1 | **Moves** | `Move 01: [action] \| X min` | Action-oriented — reader is DOING something: running a prompt, taking a concrete step |
| 2 | **To Do** | `To Do 01: [task] \| X min` | Homework-framed checklist — "here's your assignment this week" |
| 3 | **Questions** | `Q01: [question the reader is already asking]` | Explainer/educational — reader has questions they don't know how to phrase. Best for "what is this?" beginner topics |
| 4 | **Rules** | `Rule 01: [principle]` | Mindset or behavioral shift — what to do differently, how to think about something |
| 5 | **Truths** | `Truth 01: [reframe or myth-bust]` | Corrects misconceptions — strong for "what AI really is/isn't" topics |
| 6 | **Prompts** | `Prompt 01: [what this prompt does]` | Prompt-collection — the deliverable IS the prompt. Copy-paste ready, high save value |

Write one sentence explaining why this structure fits, then proceed.

---

### STEP 3 — Map source content to Kay's format

Kay's audience doesn't need a comprehensive guide. They need: "What do I need to know to use this at work this week?"

**Kay's angle:** She manages an AI Database product management team at Oracle. She's been using Claude every day. This isn't a review — it's an insider's field guide, grounded in 20 years of enterprise tech experience.

Build a content map:

| Source section | Kay's section (using chosen structure) |
|---|---|
| [source point 1] | [structure item 01]: [Kay's angle on it] |
| [source point 2] | [structure item 02]: [Kay's angle on it] |
| ... | ... |

Drop source content that is:
- Too technical for a non-engineer audience
- Covered by a previous AI For You post (check recent posts in `{BASE_DIR}/posts/`)
- Not actionable for a corporate professional

Add Kay's angle where the source is generic — her Oracle VP perspective, specific corporate use cases, things she has done herself.

**Data privacy note:** When a content item covers using Claude for corporate work, include Kay's standing guidance: do not paste private company data into consumer Claude; distinguish between consumer tools and enterprise-licensed AI subscriptions. Kay uses an Oracle enterprise ChatGPT subscription for anything involving confidential data.

---

### STEP 4 — Draft all four sections

Write all four in sequence. Grade and fix each before moving to the next.

---

#### 4a. SUBSTACK NEWSLETTER

**File header:**
```
# AI For You - NEWSLETTER - "[working title]"

**Series:** AI For You | [Series name if applicable, e.g. "Summer School, Term 2"]
**Platform:** SUBSTACK + LINKEDIN NEWSLETTER
**Format:** B-ROLL + TEXT OVERLAY + CAROUSEL
**Full content or tease:** FULL CONTENT
**Status:** Draft v1
**Date:** [YYYY-MM-DD]
```

**Title and subtitle:**
- Title: the email subject line. Must make the reader stop. Use the Questions / Rules / Truths / Prompts frame in the title where natural (e.g. "Top 5 Questions About Claude"). No em dashes. No vague promises.
- Subtitle: 1 punchy sentence that completes what the title started. Substack edition only.

**Byline:**
`*AI For You | Kay Malcolm, VP @ Oracle | LinkedIn Top Voice for AI | LinkedIn Learning Instructor*`

**Opening — 2-3 paragraphs:**
- Para 1: Hook from lived experience. A real DM, a real moment, something specific that names what the reader is feeling. Not "Many people wonder..." — something concrete.
- Para 2: Kay's personal entry. Why she is the right person to answer this. Oracle, 20 years, real usage.
- Para 3 (optional): What they're getting today. Brief. No "In this newsletter I will..."

**Question list** (for Questions structure) or **Moves list** (for Moves structure) — preview bullets after the opening, before the content. Format:
```
- Q01: [question]
- Q02: [question]
...
```

**COVER INFOGRAPHIC placeholder** — place *inside* the first content item body, after the first 1-2 introductory paragraphs and before the item's deeper or more specific content. Do not wait until the end of Q01/Move 01. It belongs high up in the newsletter where cover images appear:
```
### COVER INFOGRAPHIC
*[Cover infographic: generated via /content-kit-infographic [POST_NUMBER] cover]*
```

**Content items** — for each item in the structure:

Bold header: `**Q01: [question]**` or `**Move 01: [name] | X min**`

Write Q and Move headers in Kay's direct, real voice — not sanitized corporate speak. "How do I talk to it so I do not get crap back?" is right. "How do I get better results from Claude?" is wrong. The header should sound like something Kay would say out loud at lunch.

Body: 2-4 paragraphs of narrative. Specific. Kay's voice. The thing only Kay could say about this — the Oracle lens, the corporate use case, the thing that surprised her. Include at least one conversational aside per item.

For **Questions** structure: answer the question fully. Include a prompt block in a code fence where relevant (especially for the "how do I use this" question).

For **Moves** structure: give context, then the prompt or action in a code fence.

**MID-ARTICLE INFOGRAPHIC placeholder** — place after Q01/Q02 block (roughly halfway through the content items), before the remaining items:
```
### MID-ARTICLE INFOGRAPHIC
*[Mid-article infographic: Square 1:1 (1080x1080px). Visual: [scene description — African American woman, warm amber/gold tones, editorial style, specific expression that matches the newsletter's emotional moment]. Text overlay: "[the one insight from this newsletter worth screenshotting]." Supporting line: "[1 supporting line]." @iamkaymalcolm bottom corner. Gold/amber accent, warm editorial style.]*
```

The visual spec in the mid placeholder IS the brief the `/content-kit-infographic` skill reads. Write it with enough detail that the illustration prompt can be generated from it. Match the scene to the newsletter's emotional moment — not generic "woman at laptop."

**END INFOGRAPHIC placeholder** — after the last content item, before the closing:
```
### END INFOGRAPHIC
*[Download infographic: Portrait format. Title: "[title]." Subtitle: "[subtitle]." Row 1 | [label]: "[summary of item 1]." Row 2 | [label]: "[summary of item 2]." ... Bottom: @iamkaymalcolm | iamkaymalcolm.substack.com. Gold/amber editorial style.]*
```

Include one row per content item. Keep each row to one punchy sentence.

**Closing:**
- One concrete action for this week (specific — "pick question 3 and try it" not "try AI today")
- Sign-off: `Signed 🫶🏾,\n\nKay, Your AI Work Bestie`
- Credential line: `*VP @ Oracle | LinkedIn Top Voice for AI | LinkedIn Learning Instructor | Views are my own*`
- Footer tagline: `*AI For You is a weekly newsletter for corporate women (and yes, the guys reading this too, welcome) navigating careers in the AI era. Real tools, real context, no tech background required. iamkaymalcolm.substack.com*`

---

#### 4b. SUBSTACK NOTE

2-3 sentences. Standalone. Punchy hook that names the pain, then what the newsletter delivers. End with one specific callout (e.g. "Q03 has a prompt you can use in the next ten minutes."). Must stand alone — no "in today's newsletter I..." opener.

---

#### 4c. LINKEDIN NEWSLETTER

Same content as the Substack newsletter with three changes:
1. **Tighter opener** — cut the opener to 1-2 paragraphs. Drop the personal-story warmup paragraph if it runs long. Get to the value faster.
2. **No Substack footer tagline** — omit the `*AI For You is a weekly newsletter...` line entirely.
3. **Different closing CTA** — replace the Substack closing action with: `Reply and tell me what you tried. I read every one.`

Everything else (content items, infographic placeholders, sign-off, credential line) stays identical to the Substack version.

---

#### 4d. LINKEDIN CAPTION

- Line 1: Scroll-stopping. The number, the problem, the specific scenario. No "Hey [x]" opener.
- Lines 2-3: Kay's credential anchor woven in naturally — who she is makes this different from every other post about the same topic.
- Line 4-5: The most specific thing in the newsletter — the prompt, the tactic, the stat — enough to prove the value, not enough to skip clicking.
- Final line: "Full newsletter is linked in the first comment." (no URL in the body)

No em dashes. No lists with bullets. No generic "let me know in the comments." Keep it under 8 lines total.

---

### STEP 5 — Grade all four sections

Run `/content-kit-grader` on each section before saving. Fix any section that grades below A+. Maximum 3 fix iterations per section.

Specific checks for adapted content:
- Every content item must contain something Kay could only say from her Oracle/enterprise position — not just the source's point rephrased in warmer language
- The Substack note must stand alone without reading the newsletter
- The LinkedIn caption must not have a URL in the body
- The mid-article infographic spec must be specific enough to generate the illustration (not "woman at laptop" — describe the expression, the light, the moment)

---

### STEP 6 — Save the file

Save to: `{BASE_DIR}/posts/[POST_NUMBER]-[SLUG]/[POST_NUMBER]-[SLUG]-newsletter-[YYYY-MM-DD].md`

File structure (in this order):
1. File header (Series, Platform, Format, Full content or tease, Status, Date)
2. `## SUBSTACK NEWSLETTER` — full Substack content
3. `## SUBSTACK NOTE`
4. `## LINKEDIN NEWSLETTER`
5. `## LINKEDIN CAPTION`

---

### STEP 6.5 — Generate cover infographic

After saving the post file, run the cover infographic skill:

```
/content-kit-infographic [POST_NUMBER] cover
```

This generates the cover image from the COVER INFOGRAPHIC placeholder in the file. Do not skip this step. It runs automatically — no user confirmation needed.

---

### STEP 7 — Save session

Save a session file to `/Users/kmalcolm/claude/sessions/session-[YYYY-MM-DD]-[POST_NUMBER]-[SLUG].md`

Include:
- What was done (source, structure chosen, why)
- Current state of the file
- Any edits Kay made and why (if known)
- Next steps (grader, infographics, publish)
- "To resume: Say 'Read from my last session and pick up where we left off.'"

---

### STEP 8 — Report back

Tell the user:
- File path
- Structure chosen and why
- Title and subtitle confirmed
- Grade on each section
- Next steps: `/content-kit-infographic [POST_NUMBER]`, then publish

---

## Voice Rules (applied throughout)

These are not preferences. Every section must pass before saving.

- No em dashes anywhere — prose, titles, subtitles, captions, headers. Zero exceptions.
- No "actually" — anywhere, ever
- No staccato sentences under 6 words standing alone
- No triplets for rhetorical effect
- No "Not X. It is Y." pairs
- No tagline-style closing epigrams
- No three or more consecutive short sentences (under 12 words each)
- Every major section needs at least one: a conversational aside in parentheses, an unexpected admission, a specific detail too particular to be generic
- Credential anchor required in every section: LinkedIn Top Voice for AI, Oracle, or LinkedIn Learning
- "Hey boos" and "Hey love" are IG/TikTok only — never LinkedIn or newsletters

## What This Skill Never Does

- Writes the source creator's newsletter with Kay's name on it — always remaps to Kay's angle and audience
- Invents Kay credentials — only uses what's on record (Oracle VP, LinkedIn Top Voice for AI, LinkedIn Learning Instructor, 20 years enterprise tech)
- Saves a file that has not passed the grader at A+
- Asks for approval before writing files in `~/.claude/` or `~/claude/iamkaymalcolm/`
