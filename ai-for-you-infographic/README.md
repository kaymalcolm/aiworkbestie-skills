# ai-for-you-infographic

Generates one or two infographics for a content post via the NotebookLM API, then strips NotebookLM branding from the output images automatically.

This is Step 3 of the content production pipeline. Run after `ai-for-you-brief`.

---

## What It Does

1. Identifies the target draft and detects whether to generate one or both infographic types
2. Extracts the infographic briefs written inside the content draft
3. Reads your brand guide for visual identity context
4. Creates a NotebookLM notebook, adds sources in parallel
5. Fires infographic generation commands (both simultaneously if generating both)
6. Waits for completion and downloads each image
7. Strips NotebookLM branding using a Python image processing script (Pillow + NumPy)
8. Updates your posting order tracker and todo list

---

## Two Infographic Types

| Type | Orientation | Purpose | Filename |
|------|-------------|---------|---------|
| Mid-article | Square (1:1) | Image-forward lifestyle/illustrated scene with stat overlay; goes inside the newsletter | `ai-for-you-[NNN]-infographic-mid.png` |
| Download/Share | Portrait | Full layout with all rows, bottom stat, CTA bar; save-worthy standalone asset | `ai-for-you-[NNN]-infographic.png` |

---

## Usage

```
/ai-for-you-infographic
/ai-for-you-infographic [NNN]
/ai-for-you-infographic [NNN] mid
/ai-for-you-infographic [NNN] download
```

- No argument: generates both infographics for the most recent draft
- `[NNN]`: target a specific post number
- `mid` / `download`: generate only one type

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.12 | Must be Python 3.12 specifically — `notebooklm-py` may fail on 3.9 |
| `notebooklm-py` | `pip3.12 install notebooklm-py` |
| `Pillow` | `pip3.12 install Pillow` |
| `numpy` | `pip3.12 install numpy` |
| NotebookLM auth | `notebooklm login` (one-time Google OAuth) |

---

## Setup

### 1. Install dependencies

```bash
pip install notebooklm-py Pillow numpy
notebooklm login
```

### 2. Create your brand guide

The skill reads `strategy/iamkaymalcolm-brand-guide.md` for visual brand context passed to NotebookLM. Create a `strategy/brand-guide.md` in your project with:

- Brand colors (hex values)
- Typography
- Visual aesthetic description
- Logo/watermark guidelines
- Examples of on-brand imagery

### 3. Update paths in SKILL.md

Replace all hardcoded paths with your project directory:

```
/Users/kmalcolm/claude/iamkaymalcolm/content-drafts/
/Users/kmalcolm/claude/iamkaymalcolm/strategy/iamkaymalcolm-brand-guide.md
/Users/kmalcolm/claude/iamkaymalcolm/infographic/
/Users/kmalcolm/claude/iamkaymalcolm/posting-order.md
/Users/kmalcolm/claude/iamkaymalcolm/todo.md
```

### 4. Update the Python executable path

`SKILL.md` calls Python via:
```
/opt/homebrew/bin/python3.12 -m notebooklm.notebooklm_cli
```

Find your Python 3.12 path with `which python3.12` and update accordingly.

---

## Branding Removal

NotebookLM adds a watermark/badge to the bottom of generated images. The skill runs a Python script using Pillow and NumPy that:

1. Scans from the bottom of the image upward for light-colored rows (the badge area)
2. Detects the badge boundary and crops the image above it
3. Always applies a minimum 45px crop from the bottom to catch small watermark text that blends into the background

The cropped images replace the originals — the original NotebookLM output is not preserved.

---

## Output

Images are saved to your `infographic/` directory:

```
infographic/
├── ai-for-you-003-infographic-mid.png
└── ai-for-you-003-infographic.png
```

Images are shown inline in the Claude Code terminal after generation.

---

## Notes

- Both infographics are fired simultaneously when generating both — total time is roughly the time for one infographic, not two
- Rate limiting is the most common failure. If generation fails, wait 5–10 minutes and retry
- The NotebookLM notebook created during this run is not deleted — you can reuse it with the `/notebooklm` skill if you need to regenerate
