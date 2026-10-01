---
name: harness-update
description: Update an existing Universal Agent Harness after the project structure or stack changes. Use for "하네스 업데이트해줘" or equivalent.
---

# Harness Update

1. Identify the current repository root. Do not scan unrelated parent directories.
2. Resolve this skill package root and locate `scripts/harness.py` two levels above `skills/`.
3. Run `python <plugin-root>/scripts/harness.py analyze --project <repo-root> --json` first.
4. Preview with `python <plugin-root>/scripts/harness.py update --project <repo-root> --target codex --dry-run --json`.
5. If the preview is non-destructive, run the same `update` command without `--dry-run`.
6. Validate with `python <plugin-root>/scripts/harness.py audit --project <repo-root> --target codex --json`.
7. Report detected stack/complexity, selected target, files created or updated, and any warnings/conflicts. Keep the report concise.

## Safety and context rules
- Do not modify application source code while configuring the harness.
- Preserve existing user content outside managed markers.
- Never overwrite unowned agent/rule files; report conflicts instead.
- Never put credentials, tokens, passwords, private keys, or secrets in `.project-context/`.
- Prefer no custom subagents for SMALL projects.
- Do not add MCP servers automatically.
- Do not read all project documents just to initialize the harness.
