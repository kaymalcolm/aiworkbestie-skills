# AI For You - Brand Grader Skill

Evaluate any AI For You artifact against Kay Malcolm's brand standards, grade it, and fix everything below A+.

## When This Skill Activates

**Explicit:**
- `/ai-for-you-grader [filepath]` - grade and fix the file at that path
- `/ai-for-you-grader [post#]` - grade and fix the newsletter for that post number

**Intent detection:** Recognize requests like:
- "Grade this newsletter against my brand"
- "Does this sound like AI wrote it?"
- "Check this against my brand strategy"
- "Run the brand grader on post 1031"
- "Grade and fix this"

---

## Autonomy Rules

Run the full workflow with no confirmation. Read the artifact, grade it, then immediately rewrite any section that fails. Show the grade report first, then the fixed version. Never ask the user to choose — just fix it.

---

## Workflow

### STEP 0 - Find the artifact

- If a file path is given, read it directly.
- If a post number is given (e.g. `1031`), find the newsletter file under `/Users/kmalcolm/claude/iamkaymalcolm/posts/[POST_NUMBER]-*/` matching `*-newsletter-*.md`. If none, find the draft matching `*-draft-*.md`.
- If no argument, ask for a file path.

---

### STEP 1 - Read the brand voice reference

Read the brand guide at `/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md`. Focus on:
- The Brand Voice section
- The three calibration examples (Hey boos, Coastal, Networking posts)
- The Anti-AI Writing Standards section and all four tests
- The AI Rhetorical Constructions kill list
- The Repetitive Sentence Structures flags
- The Subtle Human Imperfections requirement

---

### STEP 2 - Grade the artifact

Apply all four hard tests. Fail means the content is not ready.

**Test 1 — Originality**
Does each section contain something only Kay could provide?
- ✅ Pass: Specific observation, lived detail, opinion with receipts (Oracle/20 years/LinkedIn Learning), or a real moment
- ❌ Fail: Generic insight in warm language. Could be written by any AI coach without Kay's input.

**Test 2 — Human**
Would a reader suspect AI assistance?
- ✅ Pass: Reads like a text from a person
- ❌ Fail: Reads polished in the wrong way — like a brand account, a PR-written LinkedIn post, or a template with the blanks filled in

**Test 3 — Tone**
Is it casual, conversational, relatable, thought-provoking?
- ✅ Pass: Warm opener, specific language, rhythm that sounds like Kay
- ❌ Fail: Sounds like a TED talk, a press release, or a generic AI post

**Test 4 — Pattern**
Does any line contain a banned AI rhetorical construction?

**Kill on sight — any of these is an automatic fail:**
- The word "actually" anywhere in the artifact — no exceptions, no context where it's acceptable
- The word "quietly" anywhere in the artifact — same rule as "actually", zero exceptions
- "Whether X or Y..." framing
- "That is not X. It is Y." / "Not X. It is Y." pairs
- "No X. No Y. Just Z." triple negation
- Triplets for rhetorical effect ("every tool, every update, every workflow")
- "The X is Y. The Y is Z." parallel chains
- Perfectly balanced parallel structures ("didn't start with A or B / started with C")
- "That's the whole point." / "That distinction is everything." / "And that matters."
- "Not a framework. Not a list of tips." as opener or closer
- Any sentence that reads like a tagline or closing epigram
- "You're editing toward X, not replacing X" style contrasts
- Em dashes (—) anywhere — in prose, in titles, in subtitles, in captions, in headers, in CTAs. Zero exceptions. An em dash in a title or subject line is an automatic fail, same as in body copy.
- Three or more consecutive short sentences (under ~12 words each) — real people don't speak in rapid-fire fragments. This is the most common AI tell. Merge or expand them into natural human rhythm.

**Flag and vary (not automatic fail but must be fixed):**
- Multiple consecutive sentences starting with the same word
- Two consecutive parallel phrases mirroring each other in structure

**Imperfection check — required per major section:**
Does each section have at least one: conversational aside in parentheses, unexpected trail-off, admission that Kay didn't have it figured out, or a specific detail too particular to be generic?

**Missing Kay markers check:**
For AI/career content: Is there at least one credential anchor? ("LinkedIn Top Voice for AI" / "I teach AI on LinkedIn Learning" / "20 years in enterprise tech" / "from someone who's been in the room")
For any content: Are Kay's voice markers present where appropriate? ("boo/love/beloved/no bueno/keep those receipts")

---

### STEP 3 - Output the grade report

Format exactly like this:

```
GRADE: [A+ / A / B / C / D]

TEST RESULTS
- Originality: [PASS / FAIL] — [one-line reason]
- Human: [PASS / FAIL] — [one-line reason]
- Tone: [PASS / FAIL] — [one-line reason]
- Pattern: [PASS / FAIL] — [one-line reason]

EM-DASH SCAN: Before listing flagged lines, scan every line of the artifact — including title, subtitle, headers, CTAs, and captions — for em dashes (—). Flag every instance. This is a required pre-check.

FLAGGED LINES
[Quote the exact line] → [Problem: what's wrong]
[Quote the exact line] → [Problem: what's wrong]
...

MISSING
- [List any missing credential anchors, voice markers, or human imperfections]
```

If the grade is A+, output the grade report and stop. Do not rewrite a passing artifact.

---

### STEP 4 - Fix everything below A+

Rewrite only the failing sections. Rules:
- Never touch prompt blocks inside code fences — those are products
- Never touch factual content, post structure, or move/section order
- Only fix: openers, transitions, closing lines, CTAs, taglines, descriptions, framing copy
- When adding Kay's voice, use her actual patterns:
  - Warm openers: "Real talk." / "Bestie, you need to hear this" / "Friend, listen." — ("Hey boos" and "Hey love" are IG/TikTok captions only, never LinkedIn or newsletters)
  - Credential anchors: "LinkedIn Top Voice for AI" / "I teach AI on LinkedIn Learning." / "After 20 years in enterprise tech..."
  - Coinages and asides: parenthetical admissions, a sentence that trails somewhere unexpected
  - Numbered lists with emoji (1️⃣ 2️⃣ 3️⃣) for advice content
  - Sign-offs: "Kay" or "Your Work Bestie 💼" (short punchy posts only)
- Every fixed section must pass all four tests before output

---

### STEP 5 - Output the fixed artifact

Show the complete fixed version, clearly labeled:

```
--- FIXED VERSION ---
[full artifact with fixes applied]
--- END ---
```

Then ask: "Want me to save this over the original file?"

If yes, write the fixed content back to the source file.

---

## Grading Scale

| Grade | Meaning |
|-------|---------|
| A+ | Passes all four tests. Every section has a human imperfection. Kay's credential anchor present in AI content. Ready to publish. |
| A | Passes all four tests. Minor voice gaps but no structural problems. Light edits only. |
| B | Fails one test or has 1-2 pattern violations. Fixable in one pass. |
| C | Fails two tests or heavy pattern violations throughout. Significant rewrite needed. |
| D | Fails three or more tests. Structural problems. Sounds like a template. Major rewrite. |

---

## What This Skill Never Does

- Rewrites prompts inside code blocks
- Adds features, sections, or content the original didn't have
- Changes the meaning or factual claims in the artifact
- Invents Kay details (only uses credentials she has on record: Oracle VP, LinkedIn Top Voice for AI, LinkedIn Learning instructor, 20 years enterprise tech)
- Calls the output "done" without running all four tests on the rewritten version
- Uses em dashes in any output it generates — the fixed version must be em-dash-free
