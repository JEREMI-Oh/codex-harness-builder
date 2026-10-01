---
name: harness-audit
description: Audit a Codex project harness for missing files, excessive context, too many agents, unmanaged conflicts, or token-wasting configuration. Use for requests like "하네스 점검해줘" or "audit my Codex harness".
---

# Harness Audit

1. Resolve the repository root and plugin script path.
2. Run:
   `python <plugin-root>/scripts/harness.py audit --project <repo-root> --json`
3. Explain findings in priority order.
4. Do not modify files unless the user also asked to fix them.

Prioritize context bloat, duplicated managed blocks, missing required role files, and accidental secret-like content in project memory.
