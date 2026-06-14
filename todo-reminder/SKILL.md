# Todo Reminder Sync Skill

Sync the @iamkaymalcolm content queue from `assets.db` to Mac Reminders. Runs the sync script, reports what was created, completed, or unchanged.

## When This Skill Activates

**Explicit:** User types `/todo-reminder`

**Intent detection:** Recognize requests like:
- "Sync my queue to Reminders"
- "Update my Reminders"
- "Push my tasks to Reminders"
- "Reset my Reminders and re-sync"

---

## Autonomy Rules

Run automatically with no confirmation, except for `--reset` which deletes all previously synced reminders  -  confirm once before running that.

---

## Workflow

### STEP 1  -  Run the sync

```bash
python3 /Users/kmalcolm/claude/iamkaymalcolm/sync-reminders.py
```

The script reads `assets.db` directly  -  no date or file edits needed before running.

### Reset (delete all synced reminders and start fresh)

Confirm with user first: "This will delete all previously synced reminders from the Social list and re-create them. Confirm?"

```bash
python3 /Users/kmalcolm/claude/iamkaymalcolm/sync-reminders.py --reset
```

---

## What the Script Does

- Queries `assets.db` for all draft assets where `queue_order IS NOT NULL`, ordered by `queue_order`
- Creates a reminder per item: title = `[N] Post NNN  -  Name`, body = `edit_notes`
- Marks reminders complete when `status = 'done'` in the DB
- Never creates duplicates  -  skips anything already in `.reminders-cache.json`

---

## Report Back

After running, tell the user:
- How many tasks were created
- How many were marked complete
- How many were unchanged
- Remind them: **Open Reminders → iamkaymalcolm smart list** to see them

If the script errors, show the raw error output and note whether it looks like a Reminders permissions issue (fix: System Settings → Privacy & Security → Reminders → grant Terminal/Claude Code access).

---

## Files

| File | Purpose |
|------|---------|
| `iamkaymalcolm/sync-reminders.py` | The sync script |
| `iamkaymalcolm/assets/assets.db` | Source of truth  -  queue and status |
| `iamkaymalcolm/.reminders-cache.json` | Tracks what has been synced  -  do not delete unless resetting |
