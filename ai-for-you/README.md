# ai-for-you

Generates a complete multi-platform content package from a single topic, transcript, or pending post. Produces Instagram, TikTok, YouTube (Short + Long-Form), Twitter/X, Threads, and Substack content in a single run.

This is Step 1 of the content production pipeline. Run this first, then follow with `ai-for-you-brief`, `ai-for-you-infographic`, and `ai-for-you-story`.

---

## What It Does

1. Reads your brand strategy files and recent content drafts for context
2. Runs live web research to find real audience pain language (Reddit, LinkedIn, TikTok comments, forums)
3. Detects the current post number and determines the next content format in the rotation
4. Generates a full content package across all platforms — no placeholders, no stubs
5. Saves the draft to your content-drafts directory
6. Updates your posting order tracker and todo list
7. Offers to run `ai-for-you-brief` next

---

## Usage

```
/ai-for-you "[topic]"
/ai-for-you-draft "[topic]"
```

**Three input modes:**

**1. Topic string (standard):**
```
/ai-for-you "how to use AI to prep for performance reviews"
```

**2. Transcript mode** — paste a long-form transcript directly; the skill extracts and reframes it:
```
/ai-for-you [paste transcript]
```

**3. Pending-post mode** — reads a `.md` file from your pending-posts directory:
```
/ai-for-you pending-posts/my-draft.md
```
After generating, the source file is archived automatically.

---

## Prerequisites

- Claude Code with `WebSearch` permission enabled (for audience research step)
- Strategy files in your project directory (see Setup below)

---

## Setup

### 1. Create your project directory structure

```
your-project/
├── strategy/
│   ├── brand-guide.md         ← brand voice, visual identity, audience definition
│   └── general-strategy.md    ← content strategy, b-roll shot bank, platform rules
├── content-drafts/             ← generated drafts saved here
├── briefs/                     ← generated briefs saved here (used by ai-for-you-brief)
├── infographic/                ← infographic output directory
├── stories/                    ← story output directory
├── pending-posts/              ← optional: place draft ideas here for pending-post mode
├── posting-order.md            ← status tracker (create as empty file)
└── todo.md                     ← task list (create as empty file)
```

### 2. Create your strategy files

**`strategy/brand-guide.md`** should include:
- Your brand name and tagline
- Target audience (demographics, psychographics, pain points)
- Brand voice and tone (words to use, words to avoid)
- Visual identity (colors, fonts, aesthetic)
- Series name and premise

**`strategy/general-strategy.md`** should include:
- Content pillars
- Platform-specific rules and character limits
- B-roll shot bank (list of pre-filmed clip descriptions)
- Posting schedule and platform order
- Hashtag strategy

### 3. Update paths in SKILL.md

Open `SKILL.md` and find all hardcoded paths (they reference `/Users/kmalcolm/claude/iamkaymalcolm/`). Replace every instance with your project directory path.

Search for these patterns:
```
/Users/kmalcolm/claude/iamkaymalcolm/strategy/
/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/
/Users/kmalcolm/claude/iamkaymalcolm/posting-order.md
/Users/kmalcolm/claude/iamkaymalcolm/todo.md
/Users/kmalcolm/claude/iamkaymalcolm/pending-posts/
```

### 4. Enable WebSearch

Ensure your Claude Code settings (`.claude/settings.local.json` in the skills directory) includes:
```json
{
  "permissions": {
    "allow": ["WebSearch"]
  }
}
```

---

## What Gets Generated

Every run produces all of the following — no optional sections:

| Section | Content |
|---------|---------|
| Audience Research | Live findings from web searches — verbatim pain language |
| Hooks | 3 hook options (one must be a credential/insider-access hook) |
| Instagram / TikTok / YouTube Short | B-roll direction, on-screen text hook, text overlay script, end card — one video used across all three |
| Instagram Caption | With named-promise keyword CTA (e.g., "Comment STACK") and share trigger line |
| TikTok Caption | Platform-optimized, DM trigger CTA |
| YouTube Short | Description and tags — references the B-roll direction from the IG/TikTok file |
| Twitter/X | One post, under 280 characters |
| Threads | 3 posts, conversational, ends with a low-effort question |
| Substack Newsletter | Full issue with conversational section headers and brand sign-off |
| Substack Note | 3–5 sentences, topically connected to the issue |
| Mid-Article Infographic Brief | Brief for the square in-newsletter infographic |
| Download/Share Infographic Brief | Brief for the portrait save-worthy infographic |

---

## Content Format

Every post uses B-roll + text overlay video (no talking-head reel). Two sub-formats based on topic:

- **FORMAT 1 (Value post):** Multi-clip B-roll + text overlay. Caption embeds actual prompts and frameworks.
- **FORMAT 2 (Take post):** Single lifestyle clip + text overlay of Kay's take. Shorter conversational caption.

---

## Adapting the Voice Rules

`SKILL.md` contains hard voice rules that apply to every piece of content. Replace the Kay-specific rules with your own:

**Current rules (examples to replace):**
- Terms of address: "boos," "love," "friend," "beloved"
- No em dashes — ever
- No AI poetry or generic motivational filler
- Millennial energy: warm, direct, a little dry

**To adapt:** Find the `VOICE RULES` section in `SKILL.md` and rewrite it with your brand voice guidelines.

---

## Output File Naming

Drafts are saved as:
```
content-drafts/ai-for-you-[NNN]-[topic-slug].md
```

Rename the prefix (`ai-for-you`) in `SKILL.md` to match your series name.
