#!/usr/bin/env python3
"""
sync-reminders.py — Sync @iamkaymalcolm content queue to Mac Reminders

Source of truth: Oracle ADB — AI_FOR_YOU schema (queue_order column on draft assets)

- Creates reminders in your "Social" Reminders list
  (update your iamkaymalcolm smart list to filter by List = Social)
- Marks reminders complete when draft status = 'done' in the DB
- Skips already-synced items — no duplicates ever

Usage:
    python3 sync-reminders.py           # normal sync
    python3 sync-reminders.py --reset   # delete synced reminders & start fresh
"""

import subprocess
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/kmalcolm/claude/iamkaymalcolm/assets")
from oracle_db import Connection

CACHE_FILE     = Path(__file__).parent / ".reminders-cache.json"
REMINDERS_LIST = "Social"

# ── DB query ──────────────────────────────────────────────────────────────────

def get_queue_tasks():
    """Return active queue items ordered by queue_order."""
    with Connection() as con:
        rows = con.execute("""
            SELECT
                d.id,
                d.queue_order,
                d.short_name,
                d.edit_notes,
                d.status
            FROM assets d
            WHERE d.type = 'draft'
              AND d.pipeline = 'ai-for-you'
              AND d.queue_order IS NOT NULL
            ORDER BY d.queue_order
        """).fetchall()

    tasks = []
    for r in rows:
        asset_id, queue_order, short_name, edit_notes, status = (
            r["id"], r["queue_order"], r["short_name"], r["edit_notes"] or "", r["status"]
        )
        display = short_name.replace("-", " ").title()
        title = f"[{queue_order}] {asset_id} – {display}"
        tasks.append({
            "title": title,
            "body": edit_notes or "",
            "completed": (status == "done"),
        })
    return tasks

# ── AppleScript helpers ───────────────────────────────────────────────────────

def run_as(script):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip(), r.stderr.strip()

def create_reminder(title, body=None):
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    safe_body  = (body or "").replace("\\", "\\\\").replace('"', '\\"')
    body_line  = f'set body of r to "{safe_body}"' if safe_body else ""
    script = f"""tell application "Reminders"
    set r to make new reminder at end of list "{REMINDERS_LIST}"
    set name of r to "{safe_title}"
    {body_line}
end tell"""
    ok, _, err = run_as(script)
    if not ok:
        print(f"    WARNING  {err}")
    return ok

def complete_reminder(title):
    safe = title.replace("\\", "\\\\").replace('"', '\\"')
    script = f"""tell application "Reminders"
    set matches to (every reminder of list "{REMINDERS_LIST}" whose name is "{safe}" and completed is false)
    repeat with r in matches
        set completed of r to true
    end repeat
end tell"""
    ok, _, err = run_as(script)
    if not ok:
        print(f"    WARNING  {err}")
    return ok

def delete_reminder(title):
    safe = title.replace("\\", "\\\\").replace('"', '\\"')
    script = f"""tell application "Reminders"
    set matches to (every reminder of list "{REMINDERS_LIST}" whose name is "{safe}")
    repeat with r in matches
        delete r
    end repeat
end tell"""
    ok, _, _ = run_as(script)
    return ok

# ── Cache ─────────────────────────────────────────────────────────────────────

def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

# ── Reset ─────────────────────────────────────────────────────────────────────

def reset(cache):
    print(f"\nResetting — deleting previously synced reminders from '{REMINDERS_LIST}'...\n")
    deleted = 0
    for title, status in cache.items():
        if delete_reminder(title):
            print(f"  Deleted: {title}")
            deleted += 1
    CACHE_FILE.unlink(missing_ok=True)
    print(f"\n  {deleted} reminders deleted. Cache cleared. Run again without --reset to re-create.\n")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    tasks = get_queue_tasks()
    cache = load_cache()

    if "--reset" in sys.argv:
        reset(cache)
        return

    created = completed = skipped = 0
    print(f"\nSyncing {len(tasks)} queue items to Reminders list: '{REMINDERS_LIST}'\n")

    for t in tasks:
        title, body, is_done = t["title"], t["body"], t["completed"]
        cached = cache.get(title)

        if not is_done:
            if cached is None:
                if create_reminder(title, body):
                    cache[title] = "pending"
                    print(f"  Created:   {title}")
                    if body:
                        print(f"             {body}")
                    created += 1
                else:
                    print(f"  Failed:    {title}")
            else:
                skipped += 1
        else:
            if cached == "pending":
                if complete_reminder(title):
                    cache[title] = "completed"
                    print(f"  Completed: {title}")
                    completed += 1
                else:
                    print(f"  Failed to complete: {title}")
            else:
                skipped += 1

    save_cache(cache)
    print(f"""
──────────────────────────────────
  {created} created  |  {completed} completed  |  {skipped} unchanged
  Open Reminders → iamkaymalcolm smart list to see them.
──────────────────────────────────
""")

if __name__ == "__main__":
    main()
