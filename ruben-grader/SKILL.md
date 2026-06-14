# Ruben LinkedIn Grader

Grade LinkedIn content or strategy against the Ruben Hassid framework from how-to-ai-1000000.md. LinkedIn only — this framework does not transfer to Instagram, TikTok, Threads, or YouTube.

## When This Skill Activates

**Explicit:**
- `/ruben-grader [filepath]` — grade the file at that path
- `/ruben-grader` — paste in content when prompted

**Intent detection:**
- "Grade this against the Ruben framework"
- "Ruben test this"
- "Does this pass the Ruben check?"
- "Score this against how-to-ai-1000000"
- "Is this reader-centric enough?"
- "Is the hook strong enough for LinkedIn?"

---

## Autonomy Rules

Read, grade, report. Do not fix — this grader scores and flags only. The user decides what to change.

---

## The Framework

All tests come from `/Users/kmalcolm/claude/iamkaymalcolm/strategy/how-to-ai-1000000.md`. Three pillars, LinkedIn only.

---

### Pillar 1 — Reader Centricity

Readers only care about themselves. Content about the creator — their habits, their journey, their achievements — does not grow an audience. Content about the reader's problem does.

**The test:** Replace every "I" / "me" / "my" in the framing with "you" / "your." Does it improve? If yes, it was written wrong.

**Automatic fail triggers:**
- Title or subject line starts with "I," "My," or "The [thing] That's Saving Me..."
- Opening line is about what the creator does, not what the reader needs
- Value is delivered as "here's what I do" rather than "here's what you can do"
- ManyChat giveaway copy describes Kay's workflow without a clear "so you can..." bridge to reader application

**Pass:** Reader sees themselves in the framing. The post reads like the reader is reading about their own problem, not watching someone else solve theirs.

---

### Pillar 2 — Hook Quality

*Applies to post content only — not strategy documents or newsletter titles.*

The hook is the first 2 lines of a LinkedIn post — roughly 2 sentences of ~55 characters each — before "...more." Its only job is to break the scroll and force the click. It does not introduce Kay. It does not set context. It creates an open loop.

**Hook technique check — must use one:**
1. Contradiction — says something that sounds wrong ("The worst LinkedIn posts get the most followers.")
2. Specific number + unexpected context ("I mass-unfollowed 2,000 people. My engagement tripled.")
3. Direct accusation — calls the reader out ("You're writing LinkedIn posts for your mom, not your audience.")
4. Stolen thought — says what the reader secretly thinks but won't say ("You know your LinkedIn posts are boring. So does everyone scrolling past them.")
5. Absurd reframe — makes something mundane dramatic ("Your LinkedIn hook has 1.2 seconds to live. Most die instantly.")

**Automatic fail triggers:**
- Hook is about Kay or her experience, not the reader or a universal tension
- Either line exceeds ~70 characters (won't land before "...more")
- Opens with an emoji
- Contains a hashtag
- Sounds like context-setting rather than a pattern interrupt
- Could have come from a brand account

**Pass:** Reads like a text someone would forward saying "wait, explain this." Creates an open loop. Stops the scroll.

---

### Pillar 3 — Media / Format

*Applies to posts and production briefs. Skip for strategy documents unless visual briefs are included.*

On LinkedIn, the media takes 80% of the screen. The hook takes 20%. Body text takes 0%. A single 1080x1350 image is the highest-performing format. It must look scrappy, useful, and sendable. The more it looks like an ad, the worse it performs.

**Automatic fail triggers:**
- Visual brief describes a polished, branded asset
- Document is described as a brand showcase rather than a useful reference
- Visual is decorative rather than informational
- No visual component planned at all ("wall of text" approach)
- Image described as something a designer would charge $500 for

**Note on video:** Reels and talking-head video work for Kay specifically because of her personality and credibility. But video is not the best organic reach format on LinkedIn for most posts — professionals are supposed to be working. Documents and single images outperform video for educational content.

**Pass:** The image or document looks like something a helpful colleague made quickly. Someone would send it to their team chat. They'd save it for later. It does not look like an ad.

---

## Workflow

### STEP 0 — Find the artifact

- If a file path is given, read it.
- If no argument, ask for the content to grade (paste or file path).

---

### STEP 1 — Identify what's being graded

| Content Type | Pillar 1 | Pillar 2 | Pillar 3 |
|---|---|---|---|
| Post hook only | Yes | Yes | No |
| Full post (hook + body + brief) | Yes | Yes | Yes |
| Newsletter title(s) | Yes | No | No |
| Strategy document | Yes (framing + titles) | No | No (unless visual briefs included) |

---

### STEP 2 — Grade each applicable pillar

Assign: **PASS / WEAK / FAIL**

- **PASS** — Meets the standard
- **WEAK** — Passes technically but has notable drift (e.g., reader-centric in framing but slips to first-person midway)
- **FAIL** — Violates the standard

---

### STEP 3 — Output the grade report

Format exactly:

```
RUBEN GRADE: [A / B / C / D]

PILLAR RESULTS
- Reader Centricity: [PASS / WEAK / FAIL] — [one-line reason]
- Hook Quality: [PASS / WEAK / FAIL / N/A] — [one-line reason or "not applicable for this content type"]
- Media/Format: [PASS / WEAK / FAIL / N/A] — [one-line reason or "not applicable for this content type"]

FLAGGED
[Quote the exact line or title] → [Problem: what's wrong and why]
[Quote the exact line or title] → [Problem: what's wrong and why]
...

SUGGESTIONS
[Specific rewrite suggestion for each flagged item — one per flag]
```

**Grading scale:**

| Grade | Meaning |
|---|---|
| A | All applicable pillars pass. Ready to ship. |
| B | One pillar weak, or one minor fail. Fixable in one pass. |
| C | One pillar fails, or two pillars weak. Needs targeted revision. |
| D | Two or more pillars fail. Structural rethink needed. |

---

## What This Skill Never Does

- Grades Instagram, TikTok, Threads, or YouTube content against this framework
- Fixes content — it reports only
- Changes factual claims or post structure in suggestions
- Applies Kay's voice standards — that is the `ai-for-you-grader` and `kay-voice-grader` jobs
- Conflates LinkedIn performance with other platform performance
- Gives an A when any applicable pillar is WEAK or FAIL
