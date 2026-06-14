# todo-reminder

Sync a `todo.md` file to the macOS Reminders app. Creates new reminders for unchecked tasks, marks reminders complete when tasks are checked off, sets due dates from section headers, and never creates duplicates.

---

## What It Does

1. Reads a `todo.md` file in your project directory
2. Parses all `- [ ]` and `- [x]` task items
3. Extracts due dates from section headers (e.g., `## DO THIS WEEK`)
4. Creates new reminders in a named Reminders list for any unchecked task not already synced
5. Marks reminders complete when the corresponding task is checked off in `todo.md`
6. Tracks synced tasks in a `.reminders-cache.json` file to prevent duplicates

---

## Usage

```
/todo-reminder
```

Or natural language:

```
Sync my todo to Reminders
Update my Reminders from todo.md
```

**Reset mode** (deletes all previously-synced reminders and starts fresh — requires confirmation):

```bash
python3 sync-reminders.py --reset
```

---

## Prerequisites

- macOS with the Reminders app
- Python 3
- Terminal/Claude Code must have Reminders permission

---

## Setup

### 1. Grant Reminders permission

Go to **System Settings > Privacy & Security > Reminders** and enable access for Terminal (or your IDE).

### 2. Create your Reminders list

Open Reminders and create a list with the name you want to sync to. The default list name in `sync-reminders.py` is `"Social"`. Update line 24 of `sync-reminders.py` to match your list name:

```python
REMINDERS_LIST = "Social"  # ← change this to your list name
```

### 3. Place the supporting files

The skill requires two files in the same directory as your `todo.md`:

| File | Purpose |
|------|---------|
| `sync-reminders.py` | The sync script (included in this skill package) |
| `.reminders-cache.json` | Created automatically on first run; tracks synced tasks |

### 4. Update paths in SKILL.md

Open `SKILL.md` and update the hardcoded path to `sync-reminders.py`:

```
Run: python3 /Users/kmalcolm/claude/iamkaymalcolm/sync-reminders.py
```

Replace with the absolute path to where you placed `sync-reminders.py`.

---

## Adapting the Section Dates

`sync-reminders.py` contains a `SECTION_DATES` dictionary that maps section header keywords to due dates. Before each sync, the skill verifies these dates are current for the week:

```python
SECTION_DATES = {
    "DO THIS WEEK":    "04/01/2026",
    "THIS WEEKEND":    "04/05/2026",
    "BEFORE APRIL 15": "04/15/2026",
    ...
}
```

**How to customize:**
- Add, remove, or rename any section keys to match the headings you use in your `todo.md`
- Update the date values to match the current week before each sync
- The skill will remind you to update these dates before running

---

## todo.md Format

The script parses standard GitHub-flavored markdown task syntax:

```markdown
## DO THIS WEEK

- [ ] Write newsletter draft
- [ ] Review analytics report
- [x] Reply to DMs

## THIS WEEKEND

- [ ] Batch film content
```

- `- [ ]` tasks are created as new reminders (if not already cached)
- `- [x]` tasks mark existing reminders complete
- Section headers set the due date for all tasks beneath them

---

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Claude Code skill definition |
| `sync-reminders.py` | Python sync script (uses AppleScript via `osascript`) |
| `.reminders-cache.json` | Auto-generated; do not edit manually |
