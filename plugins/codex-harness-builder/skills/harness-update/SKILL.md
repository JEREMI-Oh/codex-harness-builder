---
name: harness-update
description: Update an existing Codex development harness after the repository changes. Use for requests like "하네스 업데이트해줘", "refresh the harness", or when a project's stack or structure has materially changed.
---

# Harness Update

1. Resolve the repository root and plugin script path.
2. Run `analyze --json` to detect the current project state.
3. Run `update --dry-run` and inspect proposed changes.
4. Run `update` if changes remain non-destructive.
5. Run `audit --json`.
6. Summarize only the differences from the previous harness.

Never rewrite user-owned sections of `AGENTS.md`, `.codex/config.toml`, or custom agent files.
