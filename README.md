# Claude Code Skills — AI For You Content Suite

Skills for the **AI For You** content production pipeline. Covers everything from research through social scheduling, plus utility and NotebookLM skills.

---

## Content Production Pipeline

Run these in order for each post:

| Step | Skill | Command | Output |
|------|-------|---------|--------|
| 1a | [ai-for-you-research](ai-for-you-research/) | `/ai-for-you-research "[topic]"` | Research file + reel script (stop and review before committing) |
| 1b | [ai-for-you](ai-for-you/) | `/ai-for-you [research-file-path]` | Full multi-platform draft `.md` files + DB registration |
| 2 | [ai-for-you-brief](ai-for-you-brief/) | `/ai-for-you-brief [NNN]` | 1-page SMM production brief |
| 3 | [ai-for-you-infographic](ai-for-you-infographic/) | `/ai-for-you-infographic [NNN]` | Cover + mid + download infographic `.png` files |
| 4 | [ai-for-you-story](ai-for-you-story/) | `/ai-for-you-story [NNN]` | 3 Instagram Story `.png` files |
| 5 | [ai-for-you-linkedin-doc](ai-for-you-linkedin-doc/) | `/ai-for-you-linkedin-doc [NNN]` | LinkedIn document slides + PDF |
| 6 | [ai-for-you-substack](ai-for-you-substack/) | `/ai-for-you-substack [NNN]` | Substack draft with images |
| 7 | [buffer](buffer/) | `/buffer [NNN]` | Social captions queued to Buffer |

**Step 1 shortcut:** Skip research mode and go straight to a full draft: `/ai-for-you "[topic]"` — runs research inline without stopping.

---

## Additional AI For You Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [ai-for-you-register](ai-for-you-register/) | `/ai-for-you-register [NNN]` | Register a completed draft in the asset DB (called automatically by `/ai-for-you`) |
| [ai-for-you-grader](ai-for-you-grader/) | `/ai-for-you-grader [NNN or path]` | Grade any artifact against brand standards; auto-fix anything below A+ |
| [ai-for-you-sync](ai-for-you-sync/) | `/ai-for-you-sync [post_number]` | Pull current DB state for a post and overwrite local `.md` files (EDITED/APPROVED assets only) |
| [ai-for-you-gemini](ai-for-you-gemini/) | `/ai-for-you-gemini [NNN]` | Generate Gemini green screen overlay prompts for talking-head reels |
| [ai-for-you-manychat](ai-for-you-manychat/) | `/ai-for-you-manychat [NNN]` | Generate ManyChat automation config for a post's comment keyword |

---

## NotebookLM Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [notebooklm](notebooklm/) | `/notebooklm` | Full NotebookLM API — notebooks, sources, podcasts, infographics, quizzes, and more |
| [notebooklm-ppt](notebooklm-ppt/) | `/notebooklm-ppt` | Transform outlines into styled `.pptx` presentations |

---

## Utility Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [window-switch](window-switch/) | `/window-switch` | Write a session summary so you can close this window and resume in a new one |
| [gdrive-upload](gdrive-upload/) | `/gdrive-upload <file>` | Upload any file to Google Drive via rclone |
| [todo-reminder](todo-reminder/) | `/todo-reminder` | Sync a `todo.md` file to macOS Reminders |

---

## Skill Directory

```
~/.claude/skills/
├── ai-for-you/              # Full content package generator
├── ai-for-you-research/     # Research-only: audience research + reel script → research file
├── ai-for-you-register/     # DB registration for a completed draft
├── ai-for-you-brief/        # SMM production brief
├── ai-for-you-infographic/  # 3 infographics (cover, mid, download)
├── ai-for-you-story/        # Instagram Stories
├── ai-for-you-linkedin-doc/ # LinkedIn carousel doc + PDF
├── ai-for-you-substack/     # Publish newsletter to Substack
├── ai-for-you-grader/       # Brand quality grader + auto-fix
├── ai-for-you-sync/         # Pull DB state → overwrite local files
├── ai-for-you-gemini/       # Gemini green screen prompts
├── ai-for-you-manychat/     # ManyChat automation config
├── buffer/                  # Buffer scheduling
├── notebooklm/
├── notebooklm-ppt/
├── window-switch/
├── gdrive-upload/
└── todo-reminder/
```

---

## Dependencies

| Dependency | Required By | Install |
|-----------|-------------|---------|
| Python 3.12+ | infographic, story, linkedin-doc, substack, register, sync | `brew install python@3.12` |
| `notebooklm-py` | notebooklm, infographic, story, linkedin-doc | `pip install notebooklm-py` |
| `Pillow` + `numpy` | infographic, story, linkedin-doc | `pip install Pillow numpy` |
| `rclone` | gdrive-upload, story | `brew install rclone` |
| `pptxgenjs` | notebooklm-ppt | `npm install -g pptxgenjs` |
| Buffer MCP | buffer | see buffer skill README |
| Substack MCP | ai-for-you-substack | see substack skill README |
| Oracle ADB + `oracle_db.py` | register, sync, ai-for-you | wallet at `~/oracle/wallet` |
