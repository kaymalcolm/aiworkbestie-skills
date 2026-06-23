---

## Platform Detection

Before any file operations, detect the base directory:

```bash
python3 -c "import platform; print('/Users/kmalcolm/claude/iamkaymalcolm' if platform.system() == 'Darwin' else '/home/opc/iamkaymalcolm')"
```

- **Mac (Darwin):** `BASE_DIR = /Users/kmalcolm/claude/iamkaymalcolm`
- **OCI (Linux):** `BASE_DIR = /home/opc/iamkaymalcolm`

Use `BASE_DIR` for every file path in this skill.

---

# AI For You — Local Refresh Skill (Renamed)

This skill has been renamed to `content-kit-sync`.

Use `/content-kit-sync [post_number]` going forward.

The sync skill also responds to `/content-kit-refresh` as a legacy alias, so existing muscle memory still works.
