# gdrive-upload

Upload any local file to Google Drive using `rclone`. No Google Cloud Console setup, no service accounts, no API keys — just a one-time browser OAuth login.

---

## What It Does

1. Verifies the file exists
2. Checks that `rclone` is installed (installs via Homebrew if not)
3. Checks for a configured `gdrive:` rclone remote (guides you through setup if not)
4. Uploads the file to a target Google Drive folder
5. Verifies the upload succeeded

---

## Usage

```
/gdrive-upload <filepath>
/gdrive-upload <filepath> <folder-id>
```

Or natural language:

```
Upload ~/Desktop/report.pdf to Drive
Upload this file to my content folder
```

**Arguments:**
- `filepath` (required) — absolute or relative path to the file
- `folder-id` (optional) — Google Drive folder ID (the string after `/folders/` in a Drive URL). Falls back to the default folder ID configured in `SKILL.md`.

---

## Prerequisites

- macOS (or Linux with Homebrew available)
- [rclone](https://rclone.org/) — installed automatically if missing

---

## Setup

### One-time rclone configuration

The first time you run this skill on a machine without a `gdrive:` remote configured, Claude will print these instructions and ask you to run them:

```bash
rclone config
```

In the interactive config:
1. Choose `n` for New remote
2. Name it `gdrive`
3. Choose `drive` (Google Drive) as the storage type
4. Leave client ID and secret blank (uses rclone's shared credentials — fine for personal use)
5. Choose scope `drive` (full access) or `drive.file` (only files rclone created)
6. Leave root folder ID blank
7. Complete the browser OAuth flow when prompted

Your credentials are saved to `~/.config/rclone/rclone.conf` and persist across sessions.

---

## Adapting to Your Environment

Open `SKILL.md` and update the default folder ID:

```
Default target folder ID: 1IMsrLBybekEcIkg2-BVw9_9udnDtQM48
```

Replace with your own Google Drive folder ID. To find a folder ID: open the folder in Google Drive, copy the URL, and take the string after `/folders/`.

---

## Notes

- Works with any file type and any size rclone supports
- The `rclone.conf` auth file lives at `~/.config/rclone/rclone.conf` — back it up if you want to preserve the auth between machines
- To use a shared drive instead of My Drive, add `--drive-shared-with-me` to the rclone command in `SKILL.md`
