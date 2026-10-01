---
name: harness-compact
description: Safely reduce unnecessary Codex harness context without deleting user knowledge. Use for requests like "하네스 경량화해줘", "reduce Codex token usage", or "compact the harness".
---

# Harness Compact

1. Run `audit --json` first.
2. Preview:
   `python <plugin-root>/scripts/harness.py compact --project <repo-root> --dry-run`
3. If safe, run `compact` without `--dry-run`.
4. Re-run `audit --json`.
5. Report what was reduced and what was intentionally left untouched.

Compaction may normalize only tool-managed sections and whitespace in generated context files. It must not summarize or delete user-authored project knowledge automatically.
