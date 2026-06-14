# ai-for-you-brief

Generates a 1-page production brief for your social media manager from a completed content draft. The brief is execution-only — ready to hand off with zero strategic context or creative reasoning included.

This is Step 2 of the content production pipeline. Run after `ai-for-you`.

---

## What It Does

1. Auto-detects the most recently modified draft in `content-drafts/` (or reads a specified post number)
2. Reads `strategy/general-strategy.md` for the b-roll shot bank and platform rules
3. Extracts all execution-ready content from the draft verbatim
4. Writes a structured 1-page brief covering every platform and every setup step
5. Saves the brief to your `briefs/` directory
6. Updates your posting order tracker and todo list

---

## Usage

```
/ai-for-you-brief
/ai-for-you-brief [NNN]
/ai-for-you-brief content-drafts/ai-for-you-003-my-post.md
```

Or natural language:
```
Create a brief for post 003
Generate the production brief for the latest draft
```

If no argument is provided, it automatically uses the most recently modified draft.

---

## Prerequisites

- A completed draft from `ai-for-you` (Step 1)
- `strategy/general-strategy.md` with a b-roll shot bank section

---

## Setup

### Update paths in SKILL.md

Open `SKILL.md` and replace all hardcoded paths with your project directory:

```
/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/
/Users/kmalcolm/claude/iamkaymalcolm/strategy/general-strategy.md
/Users/kmalcolm/claude/iamkaymalcolm/briefs/
/Users/kmalcolm/claude/iamkaymalcolm/posting-order.md
/Users/kmalcolm/claude/iamkaymalcolm/todo.md
/Users/kmalcolm/claude/iamkaymalcolm/infographic/
```

---

## Brief Structure

Every brief contains these sections in order:

| Section | Contents |
|---------|---------|
| **Reel Direction** | Format type (FORMAT 1 Value / FORMAT 2 Take), B-roll shot list, on-screen text hook, end card direction |
| **Carousel Specs** | Slide-by-slide text, layout notes (FORMAT 1 posts only) |
| **Captions** | Ready-to-paste captions for every platform (verbatim from draft) |
| **Comment Setup** | ManyChat keyword + named-promise CTA + pinned comment timing |
| **Posting Schedule** | Platform order and timing |
| **Pre-Post Checklist** | Checklist covering B-roll sourcing, video edit, carousel design, captions, ManyChat activation |

---

## Key Rules

- **Every caption is verbatim** — no rewriting or paraphrasing from the draft
- **B-roll directions** reference the shot bank from `general-strategy.md` with specific clip descriptions
- **ManyChat setup** is flagged on every brief that has a comment keyword CTA
- **No em dashes** — replaced with hyphens before writing into the brief
- The companion reel caption goes inside the `COMPANION 30-SECOND SCRIPT` section, not as a separate Instagram caption

---

## Output

Briefs are saved as:
```
briefs/ai-for-you-[NNN]-brief.md
```

When complete, the skill reports:
- File path
- Section count
- Whether a pinned comment is needed and the recommended timing
