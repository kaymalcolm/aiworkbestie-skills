# AI For You — Research Skill

Run audience research, generate hook options, and write the B-roll direction + on-screen text hook for a new AI For You post. Saves a research file and stops — no content package, no DB writes. Use this when you want to review the direction before committing to a full draft.

## When This Skill Activates

**Explicit:** User types `/ai-for-you-research "[topic]"`

**Transcript mode:** User pastes a video transcript (long-form text). Detect this when the input is more than ~3 sentences of continuous speech/narration. In this mode, run STEP 1-TRANSCRIPT before STEP 1.

**Pending-post mode:** User provides a path to a `.md` file in the `pending-posts/` directory, or says "use the pending post" / "process the pending file". In this mode, run STEP 1-PENDING-POST before STEP 1.

**Intent detection:** Recognize requests like:
- "Research [topic] for the AI For You series"
- "Start the research for my next AI For You post"
- "Draft the B-roll direction for [topic] for review before I commit"
- "Turn this transcript into a research file"
- "Process the pending post, save the research"

---

## Autonomy Rules

Run the full workflow with no confirmation unless:
- Oracle DB credentials are missing (ask once, then proceed without the keyword query)
- The topic is ambiguous (ask one clarifying question maximum)
- The user explicitly asks you to pause

No mode question. This skill is research-only. Save the research file and stop.

---

## Workflow — Run Every Step in Order

### STEP 0 — Read the source files first (required)

Before writing a single word of content, read these files. Do not skip this step.

1. **Master brand guide:**
   `/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md`

2. **Content strategy:**
   `/Users/kmalcolm/claude/iamkaymalcolm/strategy/general-strategy.md`

3. **Content plan files (pain points and audience context):**
   List all `.md` files in `/Users/kmalcolm/claude/iamkaymalcolm/strategy/` and read any that contain content plans, pain points, or audience notes. Use these to sharpen the pain framing — these files may name specific pains the audience has expressed.

4. **Existing content drafts (scan for topic overlap):**
   List files in `/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/` and read any that look topically related.

---

### STEP 1-PENDING-POST — Extract topic from a pending markdown file (pending-post mode only)

Read the file at the provided path (or if no path was given, list files in `/Users/kmalcolm/claude/iamkaymalcolm/pending-posts/` and use the most recently modified `.md` file that is not in `archive/`). Extract:

- **TOPIC**: Summarize the core subject in 5-10 words. Reframe in Kay's audience context: career women using AI at work, not a general tech audience.
- **PAIN POINT**: What frustration does the source address? Translate into the pain Kay's audience actually feels.
- **KEY POINTS**: 3-7 most useful, actionable points in logical teaching order. Discard anything too technical or developer-focused.
- **HOOK CANDIDATES**: 2-3 phrases or ideas from the file, rewritten in Kay's voice. Do not lift phrasing verbatim.
- **TONE NOTES**: Is the source tactical/list-based or narrative? How should Kay's version feel different?
- **FORMAT HINT**: Does the structure suggest FORMAT 1 (multiple discrete tips, prompts, or steps) or FORMAT 2 (a single take, opinion, or reaction)?

Write these as a brief internal block under `## Pending Post Extraction`. Then continue to STEP 1 using the extracted TOPIC and FORMAT HINT.

Do NOT carry over branding, usernames, creator names, or source attribution into the content.

**After the research file is saved in STEP R-SAVE**, move the source file to the `archive/` folder:
```
mv [source file path] /Users/kmalcolm/claude/iamkaymalcolm/pending-posts/archive/
```
Confirm the move completed. If the archive directory does not exist, create it first.

---

### STEP 1-TRANSCRIPT — Extract topic from transcript (transcript mode only)

If the input is a transcript, do this before STEP 1. Read the transcript and extract:

- **TOPIC**: Summarize the core subject in 5-10 words
- **PAIN POINT**: What problem does Kay open with or return to? Use her exact words if possible.
- **KEY POINTS**: 3-7 main points in the order she makes them
- **HOOK CANDIDATES**: 2-3 punchy lines — raw material for hook options in STEP 3a
- **TONE NOTES**: More serious/tactical or light/conversational? Any phrases distinctly Kay's voice?
- **FORMAT HINT**: Multiple discrete tips, prompts, or steps (FORMAT 1) or single take, opinion, or reaction (FORMAT 2)?

Write these as a brief internal block under `## Transcript Extraction`. Then continue to STEP 1 using the extracted TOPIC and FORMAT HINT.

Do NOT invent points that aren't in the transcript. Note unclear sections as `[unclear in transcript]`.

---

### STEP 0b — Research the audience's real pain (required — do not skip)

Before writing a single word of content, do live research on what Kay's target audience is actually feeling right now about this topic. This is not optional. Generic pain framing is why content gets ignored.

**Who is Kay's audience:** Career women (35-50), corporate jobs, not developers, using AI as a tool at work. Many are mid-to-senior level, politically aware, financially stretched, and quietly afraid of being left behind. They scroll from exhaustion, not curiosity.

**Run 2-3 web searches:**
- `site:reddit.com "AI at work" [topic keyword] women career 2025 OR 2026`
- `"[topic keyword]" "at work" frustrating OR "I don't know" OR "nobody tells you" career`
- `LinkedIn OR TikTok comments "[topic]" corporate women professionals`

**What to extract from research:**
- The exact words and phrases real people use when they complain, confess, or ask for help. Verbatim phrasing is gold.
- The fear underneath the frustration.
- The specific situation where the pain hits.
- What they're embarrassed to admit.
- Any cultural or economic context from the past 2-4 weeks that makes this topic land harder right now.

**Record findings in a `## Audience Research` block:**
- 3-5 real phrases or situations (quoted or paraphrased from sources)
- The underlying fear in plain language (1-2 sentences)
- A "what nobody is saying out loud" observation
- Any current-events context that sharpens urgency

Use these findings to inform everything downstream: hook, pain framing, B-roll direction.

If web search is unavailable or returns nothing relevant, note it and proceed with Kay's content plan files + your own knowledge of the audience. But attempt the search first.

---

### STEP 1 — Parse the input

Extract:
- `TOPIC`: The content idea string
- `POST_NUMBER` (tentative): Count files in content-drafts matching `ai-for-you-0*.md`. Write as "Proposed post number" — not finalized until full mode.
- `SLUG` (working): Derive from topic (lowercase, hyphens, 3-5 meaningful words, drop stop words). Save as "Proposed slug" — not finalized, can be overridden in full mode.

If `POST_NUMBER` cannot be determined, use `NNN`.

---

### STEP 2 — Determine post format

Based on the topic and the 1-in-3 full content rule:
- Is this every 3rd post? → FULL CONTENT post (everything in the post, lighter newsletter ask)
- Otherwise → TEASE post (full prompts/resources live in newsletter, social content teases)

Document the format decision. This is tentative at the research stage.

---

### STEP 2b — Generate the comment keyword (read-only — do not INSERT)

Query the DB for all previously used keywords. Read only — do not write.

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

Generate a candidate keyword: short (4-8 characters), easy to type, loosely relevant to the topic (e.g., topic is "AI in meetings" → keyword could be MEET, BRIEF, ROOM, SYNC), all-caps when displayed, NOT in the `used` set, NOT a generic word like AI, YES, GO, MORE, TIPS, HELP, FREE.

Record as `Proposed keyword` in the research file. The keyword is not registered until full mode.

---

### STEP 3a — Hook options

One sentence each. Names the pain. Makes the audience feel seen. No fluff.

**The hook must come from the STEP 0b research, not from general assumptions.** If the research turned up specific phrases, situations, or fears that real people expressed, that is your raw material. Refine into Kay's voice — do not sanitize the emotion.

**What a real hook does:**
- Names the specific situation, not the general problem
- Says the thing the audience is embarrassed to admit
- Uses the ugly truth — polite hooks get scrolled
- Speaks to who they ARE, not who they should become

**What a real hook does NOT do:**
- Offer to help (the help comes later)
- Compliment the audience
- Start with "Have you ever..." or "Are you..."
- Use em dashes
- Sound like an ad or a motivational poster

**The test:** Read out loud. If it sounds like a polished brand account, rewrite it. If it sounds like Kay talking to her best friend who's about to get passed over for a promotion, it's ready.

Write 3 hook options. Each must name a DIFFERENT specific pain or situation from the research. Do not write three variations of the same angle.

**REQUIRED: One of the three must be an "Insider Access" type** — names a specific Kay credential in the first sentence. Choose the one that fits the topic best:
- "20 years in enterprise tech"
- "LinkedIn Learning instructor"
- "VP at Oracle"
- "VP of Product Management for the AI Database"
- "tech executive at one of the largest tech companies"
- "I'm AI obsessed and I instruct my team to use it every day to innovate"

The authority signal must appear in the first 3 seconds on Instagram. If all three options are pain-forward without a credential anchor, rewrite one.

Example Insider Access hook: "After 20 years in enterprise tech, I can tell you exactly which AI skills your company is actually watching for — and it's not what the LinkedIn posts say."

---

### STEP 3b-BROLL — B-roll direction + on-screen text hook

Determine the format from the FORMAT HINT in STEP 1 (or derived from topic):
- **FORMAT 1 (Value post):** topic delivers prompts, frameworks, or step-by-step guidance
- **FORMAT 2 (Take post):** topic is a reaction, opinion, or commentary

---

**ON-SCREEN TEXT HOOK:**
The exact text that appears as an overlay on the first clip. Max 10 words per line, 2 lines total. Must stop the scroll on its own — pain-naming or credential-anchoring. Second line: Kay's credential (LinkedIn Top Voice for AI / VP at Oracle) if not already in the first line.

**B-ROLL DIRECTION:**
- FORMAT 1: List 3-6 clips with timing and what each shows. Examples: hands on laptop, screen showing AI response appearing, desk setup, phone screen showing output, coffee + laptop. Pull from Kay's existing lifestyle library. Be specific — "Screen shows a ChatGPT or Claude response appearing" not "AI footage."
- FORMAT 2: One clip — name the specific setting (coffee shop, car, walking outside, airport). One lifestyle moment. No face required.

**TEXT OVERLAY PER CLIP:**
- FORMAT 1: One punchy phrase, stat, or prompt excerpt per clip. 5-10 words each. These carry the content value.
- FORMAT 2: Kay's full take as text overlay — short enough to read in one screen pass.

**END CARD DIRECTION:**
Last 2-3 seconds. Specify text on screen. Platform-specific:
- IG end card: "Comment [KEYWORD] for [specific named thing]"
- TikTok end card: "DM me [KEYWORD] for [specific named thing]"
- YouTube Short end card: "Full guide linked below"

---

### STEP R-SAVE — Save the research file

Save to:
`/Users/kmalcolm/claude/iamkaymalcolm/research/[DATE]-[TOPIC-SLUG]-research.md`

Where `DATE` = today (YYYY-MM-DD) and `TOPIC-SLUG` is the working slug from STEP 1.

**Research file contents (in order):**

```
# Research: [TOPIC as stated by user]

**Date:** [today's date]
**Proposed post number:** [POST_NUMBER or TBD]
**Proposed slug:** [TOPIC-SLUG — working slug, can be overridden in full mode]
**Proposed keyword:** [CANDIDATE_KEYWORD — not yet registered in DB]
**Format decision:** [FULL CONTENT / TEASE — with 1-sentence reason]
**Full content or tease:** [FULL CONTENT / TEASE]

---

## Audience Research
[Full STEP 0b findings block]

---

## Hook Options
[All 3 hook options from STEP 3a]

---

## B-Roll Direction

**Format:** FORMAT 1 (Value Post) / FORMAT 2 (Take Post) — [pick based on topic]

**On-screen text hook:**
[hook line — max 10 words]
[Kay's credential line]

**Clip-by-clip direction:**
[Shot 1 | 0-Xs]: [footage description] | Text overlay: "[exact text]"
[Shot 2 | ...]: ...
[End card | last 3 sec]: [text on screen — includes comment keyword placeholder e.g. "Comment KEYWORD for [thing]"]

**B-roll sourcing notes:** [which shots are likely in Kay's library vs. new shots needed]

---

## Helper Content / Notes
[Leave this section blank — user fills this in before running full mode]
```

After saving, tell the user:
- The file path
- The proposed keyword (not yet registered) and proposed slug
- "Run `/ai-for-you [file-path]` when you're ready for the full draft — edit the Helper Content section first if you want to add context or adjust the B-roll direction."

Do not write to the database. Do not register the keyword. Do not generate carousel, captions, YouTube, Threads, Twitter, Substack, or infographic content.

---

## Voice Rules (Enforced — Non-Negotiable)

Apply to every word of content generated (hooks, text overlays, B-roll direction copy):

1. **No em dashes. Ever. Anywhere.** Use a period, a line break, or rewrite the sentence.
2. **No AI poetry.** No metaphors that sound like a robot trying to be deep.
3. **No generic motivational filler.** "You've got this." Delete on sight.
4. **Use Kay's terms of address.** "Boos," "love," "friend," "beloved" — not "ladies," not "girls," not "everyone."
5. **Sentence fragments are fine.** But do NOT cluster 3 or more short sentences in a row. Mix sentence lengths. Humans do not write in staccato bursts back to back.
6. **Name the pain before delivering the value.** Every time.
7. **Millennial energy.** Warm, direct, a little dry, occasionally funny. Not Gen Z chaotic. Not corporate distant.
8. **Read the real examples in the BRAND VOICE section of the brand guide before writing.** They are the calibration standard.

**Anti-AI Writing Standards — all generated content must pass all four tests:**

- **Test 1 — Originality:** Could Claude write this without Kay's input? If yes, add something only Kay can provide: a specific observation, a real memory, a lived detail, an opinion with 20 years of receipts behind it.
- **Test 2 — Human:** Would someone reading this know it was AI-assisted? If yes, rewrite it.
- **Test 3 — Tone:** Is it casual, conversational, relatable, thought-provoking? If it reads like a brand account or a content template, rewrite it.
- **Test 4 — Pattern:** Kill any AI rhetorical construction: "Whether X or Y..." framing; "That is not X. It is Y." pairs; "No X. No Y. Just Z." triples; triplets for rhetorical effect; perfectly balanced parallel arguments; tagline-energy closing lines; three consecutive short sentences.

At least one human imperfection per major section: a parenthetical aside, an unexpected turn, a specific detail too particular to be invented, a moment where Kay admits she didn't have it figured out.

---

## Source Attribution Rule

If the content was adapted from another account or creator, do NOT reference, credit, or mention that account anywhere — not in the research file, not in a note, not in the file header. The content is Kay's. Write it that way.

---

## AI Tool Reference Rule

When a skill, prompt, or tip works with any AI tool (Claude, ChatGPT, Gemini, etc.), refer to it as **"AI"** — not a specific platform — unless the post is explicitly about Claude as a platform.
