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

# AI For You — Substack Publisher (Redirect)

This skill has been renamed. Use `/content-kit-substack-publish` instead.

## When This Skill Activates

Any invocation of `/content-kit-substack` — redirect immediately.

## What To Do

Tell the user: "This skill is now `/content-kit-substack-publish`." Then run `/content-kit-substack-publish` with the same arguments the user provided.
