# Story Skill Update Plan
_Based on regen of 1046_1242 and 1046_1244 — June 2026_

---

## What broke and why

The original 1046 stories (01 and 03) came back severely text-overloaded — multiple bullet points, icon diagrams, stats blocks, explanatory paragraphs, all at unreadable size. Two root causes:

**1. Text rules live in the SKILL.md, not in the prompts.**
The "Story Text Rules" section at the bottom of the skill enforces max 2 lines, no bullets, one text element per frame — but NotebookLM only receives the generation prompt. It never reads those rules. Every type prompt needs those constraints embedded directly.

**2. Poll and Stat Card prompts don't say what's forbidden.**
Countdown, Question, and Pull Quote all have explicit NO-list lines inside their DESIGN RULES. Poll and Stat Card don't. That's why the overloaded stories came from those types — the generator filled the space because nothing told it not to.

**3. "Actually" appears in the Poll prompt.**
Line: `"Feels like a question from someone who actually knows you."` — banned word, inside the prompt text Claude sends to NotebookLM. It will show up in generated copy.

**4. Countdown Kay variant references a "list."**
`"The lead line and list occupy the upper two-thirds of the frame above and around her."` — this is in the Kay variant for Countdown, directly contradicting the DESIGN RULES that say no lists on this frame.

**5. No regen path exists.**
The skill only handles first-time generation (DB INSERT, new filenames, new assets_images INSERT). Regenerating specific frames requires: reuse existing asset IDs, overwrite existing filenames, MERGE into assets_images. There's nothing in the skill for this.

**6. .notebooks.json is not always written.**
The 1046 stories folder had no .notebooks.json, so regen created a fresh notebook instead of reusing. Need to confirm the notebook save step runs and verify why it was missing.

---

## Changes to make

### 1. Embed text rules in every type prompt

Add to DESIGN RULES in **Poll** and **Stat Card** (and audit the others for consistency):

```
- ZERO additional text elements. No bullets, no lists, no explanatory copy, no callouts.
  The question/stat is the ONLY text on this frame beyond the badge, handle, and link sticker.
- Max 7 words per line. Max 2 lines total. Fragment or punchy phrase only.
```

This mirrors what Countdown and Question already do.

### 2. Fix the Poll prompt — remove "actually"

Current: `"Cinematic, personal energy. Feels like a question from someone who actually knows you."`
Fix: `"Cinematic, personal energy. Feels like a question from someone who knows you."`

### 3. Fix the Countdown Kay variant — remove list reference

Current: `"The lead line and list occupy the upper two-thirds of the frame above and around her."`
Fix: `"The lead line occupies the upper two-thirds of the frame above her."`

Also fix the intro text — "Tappable list energy" is accurate for the vibe but misleads the generator into thinking a list should appear. Rename or clarify: `"Tappable teaser energy — one hook line that makes them want to tap through."`

### 4. Add a regen path to STEP 5

After the DB registration block, add a `## REGEN PATH` section for when asset IDs already exist:

- Skip DB INSERT entirely
- Use existing IDs for canonical filenames (same names = overwrite in place)
- After download and badge crop, run MERGE into assets_images (not INSERT)
- Update `updated_date` on the assets row
- Brief checklist: mark old `REGENERATE` items as `DONE — regen [date]`

Trigger condition: when the user says "regen" or names specific story file IDs.

### 5. Harden the .notebooks.json save step

Current STEP 2 creates the notebook and writes `.notebooks.json`, but if the stories folder doesn't exist yet, the write may fail silently. Add:

```python
stories_dir.mkdir(parents=True, exist_ok=True)  # ensure directory exists before writing
```

Also add a verification print after write: `print(f"Notebook ID saved: {notebook_id}")` so failures are visible.

---

## Priority order

| # | Change | Why first |
|---|--------|-----------|
| 1 | Embed text rules in Poll + Stat Card prompts | Prevents the core failure from repeating |
| 2 | Fix "actually" in Poll prompt | Banned word, will surface in generated copy |
| 3 | Fix Countdown Kay variant list reference | Contradicts the rules it sits next to |
| 4 | Add regen path | Missing workflow; had to improvise this entire session |
| 5 | Harden .notebooks.json save | Lower risk but caused a wasted notebook creation |

---

## Files to edit

- `/Users/kmalcolm/.claude/skills/content-kit-story/SKILL.md`
  - Poll DESIGN RULES: add NO-list/NO-bullets line; remove "actually"
  - Stat Card DESIGN RULES: add NO-list/NO-bullets line
  - Countdown intro: reframe "tappable list energy"
  - Countdown Kay variant: remove list reference
  - STEP 2: add `parents=True` to mkdir + verification print
  - After STEP 5: add REGEN PATH section
