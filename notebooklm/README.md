# notebooklm

Full programmatic access to Google NotebookLM via the `notebooklm-py` library. Includes capabilities not available in the NotebookLM web UI — programmatic sharing, artifact export to multiple formats, parallel source ingestion, and parallel agent workflows.

This skill is also used internally by `ai-for-you-infographic` and `ai-for-you-story`.

---

## What It Does

Provides a Claude Code interface to all NotebookLM API operations:

**Notebooks:** Create, list, describe, delete, share, use (set active context)

**Sources:** Add (URL, file, or text), list, delete — with parallel ingestion support

**Artifact generation:**
| Type | Formats | Notes |
|------|---------|-------|
| Podcast | `.mp3` | deep-dive, brief, critique, debate |
| Video | `.mp4` | explainer, brief; multiple visual styles |
| Slide deck | `.pdf`, `.pptx` | detailed or presenter format |
| Infographic | `.png` | landscape / portrait / square; 10 styles |
| Report | `.md` | briefing-doc, study-guide, blog-post, custom |
| Mind map | `.json` | instant/synchronous |
| Data table | `.csv` | |
| Quiz | `.json`, `.md`, `.html` | |
| Flashcards | `.json`, `.md`, `.html` | |

---

## Usage

```
/notebooklm
```

Or intent phrases:
```
Create a podcast about my research
Make an infographic from this document
Generate a quiz from my notes
```

---

## Prerequisites

- Python 3.8+
- Google account

---

## Setup

```bash
pip install notebooklm-py
notebooklm login
```

`notebooklm login` opens a browser for Google OAuth. Auth is saved to `~/.notebooklm/` and persists across sessions.

**Optional environment variables:**

| Variable | Purpose |
|----------|---------|
| `NOTEBOOKLM_HOME` | Override the default config directory (`~/.notebooklm`) |
| `NOTEBOOKLM_AUTH_JSON` | Inline auth JSON — useful for CI/CD or parallel agent workflows |

---

## Autonomy Rules

The skill runs most operations without asking for confirmation. The following operations **always require user confirmation** before proceeding:

- `delete` (notebook or source deletion)
- Artifact generation (audio, video, infographic, slide deck, quiz)
- Download operations

---

## Timing Reference

| Operation | Typical duration |
|-----------|-----------------|
| Source processing | 30 seconds – 10 minutes |
| Audio (podcast) | 10 – 20 minutes |
| Video | 15 – 45 minutes |
| Infographic | 5 – 15 minutes |
| Mind map | Instant (synchronous) |

---

## Parallel Workflow Note

When using multiple agents in parallel, **always pass `-n <notebook_id>` explicitly** rather than relying on `notebooklm use`. The `use` command writes to `~/.notebooklm/context.json` and will cause race conditions across parallel agents.

---

## Error Handling

**Rate limiting** is the most common failure for audio, video, infographic, and quiz generation. If you hit a rate limit error:
1. Wait 5–10 minutes
2. Retry once
3. Fall back to the NotebookLM web UI if retry fails

---

## CLI Reference

```bash
# Notebook management
notebooklm create "My Notebook"
notebooklm list
notebooklm use <notebook_id>
notebooklm delete <notebook_id>

# Sources
notebooklm add-source <url_or_filepath>
notebooklm list-sources

# Generation
notebooklm generate podcast
notebooklm generate infographic --orientation square --style minimalist
notebooklm generate quiz

# Download
notebooklm download <artifact_id> --output output.mp3
```

See `notebooklm --help` for the full command reference.
