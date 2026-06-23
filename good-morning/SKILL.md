# Good Morning Skill

Commit any local changes, then pull the latest from both GitHub repos to start the day fully synced.

## When This Skill Activates

**Explicit:** User types `/good-morning`

**Intent detection:** Recognize requests like:
- "Pull the latest from GitHub"
- "Sync my repos"
- "Morning pull"
- "Pull down any changes from GitHub"

---

## Autonomy Rules

Run all steps automatically with no confirmation.

---

## Repos

| Repo | Local path | Remote | Branch |
|---|---|---|---|
| Skills (public) | `~/.claude/skills/` | `public` | `main` |
| Content/app (private) | `~/claude/iamkaymalcolm/` | `origin` | `main` |

---

## Workflow

### STEP 1 — Commit local changes in the skills repo

```bash
cd ~/.claude/skills && git status --short
```

If there are any changes (modified, new, deleted files):

```bash
cd ~/.claude/skills && git add -A && git commit -m "Morning sync: local changes"
```

Note what was committed, or "Nothing to commit" if clean.

### STEP 2 — Commit local changes in the content repo

```bash
cd ~/claude/iamkaymalcolm && git status --short
```

If there are any changes (modified, new, deleted files):

```bash
cd ~/claude/iamkaymalcolm && git add -A && git commit -m "Morning sync: local changes"
```

Note what was committed, or "Nothing to commit" if clean.

### STEP 3 — Pull the skills repo

```bash
cd ~/.claude/skills && git pull public main
```

Capture stdout/stderr. Note whether it was already up to date or what changed.

### STEP 4 — Pull the content repo

```bash
cd ~/claude/iamkaymalcolm && git pull origin main
```

Capture stdout/stderr. Note whether it was already up to date or what changed.

### STEP 5 — Push committed local changes (if any)

If either repo had local commits in Steps 1–2, push them now:

```bash
cd ~/.claude/skills && git push public main       # only if Step 1 committed
cd ~/claude/iamkaymalcolm && git push origin main  # only if Step 2 committed
```

### STEP 6 — Report

Print a clean summary:

```
Good morning.

Skills (~/.claude/skills/)
  Committed: [Nothing. / {N} files: list]
  Pull: [Already up to date. / {N} files updated: list]

Content (~/claude/iamkaymalcolm/)
  Committed: [Nothing. / {N} files: list]
  Pull: [Already up to date. / {N} files updated: list]
```

If any step fails (network error, merge conflict, etc.), show the error and stop.
