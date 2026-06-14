# Window Switch Skill

Write a session summary markdown file so the user can close this context window and continue in a new one.

## When This Skill Activates

**Explicit:** User types `/window-switch`

**Intent detection:** Recognize requests like:
- "Write a summary so I can close this window"
- "I'm going to start a new context window"
- "Summarize this session so I can switch"
- "Create a handoff doc for this chat"

---

## Workflow

### STEP 1 — Identify the working directory
Check which project the user is working in (primary or additional working directories).

### STEP 2 — Write the session summary
Always save the session file to `/Users/kmalcolm/claude/sessions/`, creating the folder if it doesn't exist. Name the file:
```
/Users/kmalcolm/claude/sessions/session-YYYY-MM-DD-[short-slug].md
```
Use today's date. The slug should be 2-4 words describing what was done (e.g. `content-cleanup`, `db-updates`, `archive-setup`).

### STEP 3 — Summary structure
The file must include:

```markdown
# Session Summary — [Title]
**Date:** YYYY-MM-DD

## What Was Done
Numbered list of every meaningful action taken this session. Be specific:
- file paths created, moved, or deleted
- database changes (tables, fields, values)
- status updates and what they changed from/to
- any decisions made

## Current State
What is true right now that wasn't true at the start of the session.
Bullet points. Keep it scannable.

## Next Steps
What should be done next. Pulled from context — don't fabricate.
```

### STEP 4 — Confirm to the user
Tell the user:
- The file path where the summary was saved
- That they can safely close this window and open a new one
- That they can resume in the next window by saying: "Read from my last session and pick up where we left off."

---

## Resuming from a Previous Session

When the user says something like:
- "Read from my last session and pick up where we left off"
- "Resume from last session"
- "What were we working on?"

**Do this:**
1. Look in `/Users/kmalcolm/claude/sessions/`
2. Read the most recently modified file in that folder
3. Summarize what was done and what the next steps are
4. Ask the user how they'd like to proceed

---

## Rules
- Be complete — the summary must be enough to fully resume work with zero context from this window
- Include file paths, IDs, and specific values — not vague descriptions
- Do not summarize what the user said, only what was actually done
- Always use absolute dates, never relative ones ("2026-04-22" not "today")
