# Text-to-Speech Skill

Control Claude's voice responses. Uses macOS `say` via a Stop hook that fires after every Claude turn when enabled.

## When This Skill Activates

**Explicit:** `/tts [subcommand]`

**Intent detection:**
- "Turn on voice" / "Speak to me" / "Read that back"
- "Turn off voice" / "Stop speaking" / "Mute"
- "Change voice" / "Use a different voice"
- "Stop talking" / "Be quiet"

---

## Subcommands

| Command | What it does |
|---|---|
| `/tts on` | Enable TTS — Claude speaks every response |
| `/tts off` | Disable TTS — silent |
| `/tts stop` | Kill the current speech mid-sentence |
| `/tts voice` | List available voices and switch |
| `/tts test` | Speak a short test phrase with the current voice |
| `/tts` (no args) | Show current status (on/off, current voice) |

---

## Workflow

### `/tts on`

```bash
touch /Users/kmalcolm/.claude/tts_enabled
```

Confirm: "Voice is on. I'll read every response aloud. Say /tts off to silence me or /tts stop to cut me off mid-sentence."

---

### `/tts off`

```bash
rm -f /Users/kmalcolm/.claude/tts_enabled
pkill -x say 2>/dev/null || true
```

Confirm: "Voice is off."

---

### `/tts stop`

```bash
pkill -x say 2>/dev/null || true
```

Confirm: "Stopped."

---

### `/tts voice`

List the available macOS US English voices, highlighting which ones are natural-sounding:

```bash
say -v '?' 2>/dev/null | grep "en_US" | grep -v "# Hello" | awk '{print $1, $2}' | head -30
```

Show the list and ask which voice to use. When the user picks one, save it:

```bash
echo "[chosen voice name]" > /Users/kmalcolm/.claude/tts_voice
```

Test the new voice immediately:
```bash
say -v "[chosen voice name]" "Hi, I'm your new voice. How do I sound?"
```

Good voice picks on this machine:
- **Flo** — natural, warm female voice (recommended)
- **Sandy** — clear, friendly
- **Shelley** — warm, slightly slower pace
- **Samantha** — classic, reliable (current default)

---

### `/tts test`

Read the current voice setting:
```bash
cat /Users/kmalcolm/.claude/tts_voice 2>/dev/null || echo "Samantha"
```

Then speak:
```bash
say -v "[voice]" "This is a test. If you can hear me clearly, voice responses are working."
```

---

### `/tts` (status check)

```bash
# Check if enabled
[ -f /Users/kmalcolm/.claude/tts_enabled ] && echo "ON" || echo "OFF"

# Check current voice
cat /Users/kmalcolm/.claude/tts_voice 2>/dev/null || echo "Samantha"
```

Report: "TTS is [ON/OFF]. Current voice: [name]."

---

## How it works

A `Stop` hook in `settings.json` runs `~/.claude/scripts/tts_hook.py` after every Claude response.
The hook checks for `~/.claude/tts_enabled`. If present, it:
1. Extracts the last assistant turn from the hook JSON
2. Pipes it through `~/.claude/scripts/tts_clean.py` to strip markdown and non-speakable content
3. Calls `say -v [voice]` in the background (non-blocking)

**What gets spoken:** prose, decisions, confirmations, questions, summaries.

**What gets skipped:** code blocks (announced as "code block follows"), file paths, URLs, tables, emoji, raw tool output.

**Word cap:** responses over 400 words are truncated at 400, ending with "Response continues in text."

---

## Installing better voices (optional upgrade)

macOS Enhanced voices are much more natural. To install:
1. System Settings → Accessibility → Spoken Content → System Voice → Customize
2. Download any voice marked "(Enhanced)" or "(Premium)"
3. Run `/tts voice` to switch to the new voice

Recommended: **Ava (Enhanced)**, **Zoe (Enhanced)**, or **Nicky (Enhanced)**

---

## Troubleshooting

**No sound:** Run `/tts test` — if nothing plays, check System Volume and that `say` works: `say "test"` in Terminal.

**Wrong content being read:** The hook reads the full assistant turn. If tool output is leaking in, run `/tts stop` and report the issue.

**Voice not found:** Run `say -v '?' | grep en_US` to see what's installed, then `/tts voice` to pick one from the list.
