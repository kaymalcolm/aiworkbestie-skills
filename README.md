# Claude Code Skills — AI For You Content Suite

Skills for the **AI For You** content production pipeline. Covers everything from research through social scheduling, plus utility and NotebookLM skills.

---

## Content Production Pipeline

Run these in order for each post:

| Step | Skill | Command | Output |
|------|-------|---------|--------|
| 1a | [content-kit-research](content-kit-research/) | `/content-kit-research "[topic]"` | Research file + reel script (stop and review before committing) |
| 1b | [content-kit](content-kit/) | `/content-kit [research-file-path]` | Full multi-platform draft `.md` files + DB registration |
| 2 | [content-kit-brief](content-kit-brief/) | `/content-kit-brief [NNN]` | 1-page SMM production brief |
| 3 | [content-kit-infographic](content-kit-infographic/) | `/content-kit-infographic [NNN]` | Cover + mid + download infographic `.png` files |
| 4 | [content-kit-story](content-kit-story/) | `/content-kit-story [NNN]` | 3 Instagram Story `.png` files |
| 5 | [content-kit-linkedin-doc](content-kit-linkedin-doc/) | `/content-kit-linkedin-doc [NNN]` | LinkedIn document slides + PDF |
| 6 | [content-kit-substack](content-kit-substack/) | `/content-kit-substack [NNN]` | Substack draft with images |
| 7 | [buffer](buffer/) | `/buffer [NNN]` | Social captions queued to Buffer |

**Step 1 shortcut:** Skip research mode and go straight to a full draft: `/content-kit "[topic]"` — runs research inline without stopping.

---

## Additional AI For You Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| [content-kit-register](content-kit-register/) | `/content-kit-register [NNN]` | Register a completed draft in the asset DB (called automatically by `/content-kit`) |
| [content-kit-grader](content-kit-grader/) | `/content-kit-grader [NNN or path]` | Grade any artifact against brand standards; auto-fix anything below A+ |
| [content-kit-sync](content-kit-sync/) | `/content-kit-sync [post_number]` | Pull current DB state for a post and overwrite local `.md` files (EDITED/APPROVED assets only) |
| [content-kit-manychat](content-kit-manychat/) | `/content-kit-manychat [NNN]` | Generate ManyChat automation config for a post's comment keyword |

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
├── content-kit/              # Full content package generator
├── content-kit-research/     # Research-only: audience research + reel script → research file
├── content-kit-register/     # DB registration for a completed draft
├── content-kit-brief/        # SMM production brief
├── content-kit-infographic/  # 3 infographics (cover, mid, download)
├── content-kit-story/        # Instagram Stories
├── content-kit-linkedin-doc/ # LinkedIn carousel doc + PDF
├── content-kit-substack/     # Publish newsletter to Substack
├── content-kit-grader/       # Brand quality grader + auto-fix
├── content-kit-sync/         # Pull DB state → overwrite local files
├── content-kit-manychat/     # ManyChat automation config
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
| Substack MCP | content-kit-substack | see substack skill README |
| Oracle ADB + `oracle_db.py` | register, sync, content-kit | wallet at `~/oracle/wallet` |
