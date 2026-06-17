# Good Morning Skill

Pull the latest files from both GitHub repos to start the day with everything up to date.

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

### STEP 1 — Pull the skills repo

```bash
cd ~/.claude/skills && git pull public main
```

Capture stdout/stderr. Note whether it was already up to date or what changed.

### STEP 2 — Pull the content repo

```bash
cd ~/claude/iamkaymalcolm && git pull origin main
```

Capture stdout/stderr. Note whether it was already up to date or what changed.

### STEP 3 — Report

Print a clean summary:

```
Good morning.

Skills (~/.claude/skills/)
  [Already up to date. / {N} files updated: list changed files]

Content (~/claude/iamkaymalcolm/)
  [Already up to date. / {N} files updated: list changed files]
```

If either pull fails (network error, merge conflict, etc.), show the error and stop — do not proceed to the next repo.
