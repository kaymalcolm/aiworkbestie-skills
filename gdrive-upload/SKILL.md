---
name: gdrive-upload
description: Upload a local file to Google Drive using rclone. Defaults to Bay's social media manager folder. Supply a file path and optional post-folder/subfolder for structured post uploads.
---

# Google Drive Upload Skill

Upload any local file to Google Drive. Uses `rclone` — no Google Cloud Console or API keys needed. Auth happens through a normal Google browser login.

## Default Folder

**Folder ID Bay (social media manager / post content):** `1IMsrLBybekEcIkg2-BVw9_9udnDtQM48`
All uploads go here. Structure for post content: `AI LinkedIn 2026/{post-folder}/{type}/`

## When This Skill Activates

**Explicit:** User types `/gdrive-upload <filepath> [folder-id] [--post-folder <name>] [--subfolder <name>]`

**Intent detection:** Recognize requests like:
- "Upload [file] to my Drive"
- "Send [file] to Google Drive"
- "Put [file] in my Drive folder"
- "Upload this to the Drive folder"

---

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `filepath` | Yes | Absolute or relative path to the file to upload |
| `folder-id` | No | Google Drive folder ID. Defaults to `1IMsrLBybekEcIkg2-BVw9_9udnDtQM48` (Bay). |
| `--post-folder` | No | Post folder name, e.g. `1031-where-to-start-with-ai`. Enables structured upload into `AI LinkedIn 2026/{post-folder}/{subfolder}/`. |
| `--subfolder` | No | Type subdirectory inside the post folder, e.g. `infographic` or `stories`. Required when `--post-folder` is provided. |

---

## Workflow

### STEP 1 — Resolve and confirm the file

Check that the file exists:
```bash
ls -lh "<filepath>"
```
If it doesn't exist, stop and tell the user.

### STEP 2 — Check if rclone is installed

```bash
which rclone || echo "NOT_FOUND"
```

If not found, install it:
```bash
brew install rclone
```

### STEP 3 — Check if rclone has a Google Drive remote configured

```bash
rclone listremotes
```

Look for a remote named `gdrive:` in the output.

If `gdrive:` is NOT listed, stop and display these one-time setup instructions:

---
**One-time setup — takes about 2 minutes:**

Run this in your terminal:
```bash
rclone config
```

Follow the prompts:
- `n` → New remote
- Name it: `gdrive`
- Storage type: `drive` (Google Drive)
- Client ID and Secret: leave blank (press Enter)
- Scope: `drive` (full access)
- Root folder ID: leave blank
- Service account: leave blank
- Advanced config: `n`
- Auto config: `y` → browser will open, sign in with your Google account
- Team drive: `n`
- Confirm with `y`

Then run `/gdrive-upload` again.

---

### STEP 4 — Upload the file

**If `--post-folder` and `--subfolder` are provided** (structured post upload):

Build the target path: `AI LinkedIn 2026/{post-folder}/{subfolder}/`

```bash
# Create the folder hierarchy (idempotent)
rclone mkdir "gdrive:AI LinkedIn 2026/<post-folder>/<subfolder>" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"

# Upload the file into the subfolder
rclone copy "<filepath>" "gdrive:AI LinkedIn 2026/<post-folder>/<subfolder>" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48" \
  --progress \
  --stats-one-line
```

Then retrieve the subfolder's Drive folder ID:
```bash
rclone lsjson "gdrive:AI LinkedIn 2026/<post-folder>" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48" \
  --dirs-only
```
Parse the JSON to find the entry where `"Name"` equals `<subfolder>` and extract its `"ID"` field — that is the `GDRIVE_FOLDER_ID`.

Return both values to the caller:
- `GDRIVE_PATH` = `AI LinkedIn 2026/<post-folder>/<subfolder>/<filename>` (e.g. `AI LinkedIn 2026/1031-where-to-start-with-ai/infographic/1031-infographic-mid.png`)
- `GDRIVE_FOLDER_ID` = the Drive folder ID of the subfolder

**If `--post-folder` and `--subfolder` are NOT provided** (flat upload, existing behavior):

Use the folder ID (default or user-supplied):

```bash
rclone copy "<filepath>" "gdrive:" \
  --drive-root-folder-id "<folder-id>" \
  --progress \
  --stats-one-line
```

### STEP 5 — Confirm success

After upload, verify the file is there:

**Structured upload:**
```bash
rclone ls "gdrive:AI LinkedIn 2026/<post-folder>/<subfolder>" \
  --drive-root-folder-id "1IMsrLBybekEcIkg2-BVw9_9udnDtQM48"
```

Report: `GDRIVE_PATH`, `GDRIVE_FOLDER_ID`, and filename confirmation.

**Flat upload:**
```bash
rclone ls "gdrive:" --drive-root-folder-id "<folder-id>"
```

Report back to the user:
- The filename that was uploaded
- Confirmation it appears in the folder listing

---

## Notes

- rclone credentials are stored in `~/.config/rclone/rclone.conf` — no setup needed after the first time.
- To re-authenticate: `rclone config reconnect gdrive:`
- Works with any Google Drive folder you have access to, including shared folders.
- To upload multiple files, you can also point at a directory and rclone will copy its contents.
