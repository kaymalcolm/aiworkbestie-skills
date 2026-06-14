# ai-for-you-story

Generates 5 Instagram Story frames for a content post via the NotebookLM API, strips branding from the output images, and uploads all 5 to Google Drive automatically.

This is Step 4 of the content production pipeline. Run after `ai-for-you-infographic`.

---

## What It Does

1. Finds the target draft and brief file (if a brief exists, it's used for richer story context)
2. Extracts key content: main hook, core stat, use cases list, pull quote, CTA keyword, newsletter title
3. Creates a NotebookLM notebook and adds sources in parallel
4. Fires all 5 story generation commands simultaneously (parallel, not sequential)
5. Downloads and shows each story inline as it completes
6. Strips NotebookLM branding using a 2-pass Python image processing script
7. Uploads all 5 files to Google Drive via rclone
8. Updates your todo list and reports results

---

## The 5 Story Types

| # | Type | Description |
|---|------|-------------|
| 1 | The Poll | Curiosity question + 2-answer poll widget. Both answers trigger ManyChat DM flows. |
| 2 | The Stat Card | One bold stat, full-bleed. Secondary link sticker only. |
| 3 | The Countdown | Teaser list of use cases. Primary CTA is DM trigger; link sticker is secondary. |
| 4 | The Question | Intimate question + stacked list. Drives personal reflection. Ends with DM CTA. |
| 5 | The Pull Quote | Single editorial sentence from the newsletter. Lifestyle photo base or warm gradient. |

All stories are portrait 9:16 format.

---

## Usage

```
/ai-for-you-story
/ai-for-you-story [NNN]
```

Or natural language:
```
Generate the stories for post 003
Make the Instagram stories for the latest post
```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.12 | Same requirement as `ai-for-you-infographic` |
| `notebooklm-py` | `pip3.12 install notebooklm-py` |
| `Pillow` + `numpy` | `pip3.12 install Pillow numpy` |
| NotebookLM auth | `notebooklm login` |
| `rclone` with `gdrive:` remote | See `gdrive-upload` README for setup instructions |

---

## Setup

### 1. Install dependencies

```bash
pip install notebooklm-py Pillow numpy
notebooklm login
brew install rclone
rclone config   # set up gdrive: remote (one-time, see gdrive-upload README)
```

### 2. Create a Google Drive folder for stories

Create a folder in Google Drive for story uploads. Copy the folder ID from the URL (the string after `/folders/`).

### 3. Update paths and IDs in SKILL.md

Replace all hardcoded paths and IDs:

```
/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/
/Users/kmalcolm/claude/iamkaymalcolm/briefs/
/Users/kmalcolm/claude/iamkaymalcolm/stories/
/Users/kmalcolm/claude/iamkaymalcolm/todo.md
```

Replace the Google Drive folder ID:
```
1LBzJiAIjZ5IXCMbyzj0tCLY4G_El3z6A   ← replace with your folder ID
```

Update the Python executable path (find yours with `which python3.12`):
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli
```

---

## Color Palette

The default story palette uses warm, girlie tones:

| Color | Hex |
|-------|-----|
| Blush pink | `#F7CAD0` |
| Dusty rose | `#C9677A` |
| Mauve | `#B5838D` |
| Warm lavender | `#C4B0D8` |
| Champagne | `#F0E2C8` |
| Soft plum | `#7D4E6B` |

No two stories in a set use the same background color.

To adapt to your brand colors, update the palette in `SKILL.md` under the story prompt templates.

---

## ManyChat Integration

The default story templates use DM-trigger CTAs ("DM me 'KEYWORD'") rather than link-in-bio CTAs. This assumes ManyChat is configured and the keyword triggers an automated DM flow.

If you are not using ManyChat, update the CTA copy in the story prompt templates inside `SKILL.md`:
- Replace "DM me 'KEYWORD'" with your preferred CTA
- Replace poll widget copy ("Tap to get the guide → DM") with engagement-only poll copy

---

## Branding Removal

The skill uses an enhanced 2-pass branding removal script:

- **Pass 1:** Scans from the bottom upward for a light-colored strip (the full NotebookLM badge)
- **Pass 2:** Always applies a minimum 45px crop from the bottom to catch small watermark text that blends into the background

This is more aggressive than the `ai-for-you-infographic` version because story images sometimes have watermarks that blend with the background color.

---

## Output

Stories are saved to your `stories/` directory:

```
stories/
├── ai-for-you-003-story-poll.png
├── ai-for-you-003-story-stat.png
├── ai-for-you-003-story-countdown.png
├── ai-for-you-003-story-question.png
└── ai-for-you-003-story-quote.png
```

All 5 are uploaded to Google Drive automatically, and all 5 are shown inline in the terminal when complete.

---

## Notes

- All 5 generation commands are fired in parallel — total generation time is roughly the time for one story, not five
- Rate limiting is the most common failure. Wait 5–10 minutes and retry if hit
- The brief file is optional but improves story quality — run `ai-for-you-brief` first when possible
