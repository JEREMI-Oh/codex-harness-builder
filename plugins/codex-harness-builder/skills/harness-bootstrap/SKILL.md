---
name: harness-bootstrap
description: Build a project-aware Codex development harness. Use when the user asks to configure a harness, development agents, project memory/context, multi-agent coding setup, or says phrases such as "하네스 구성해줘", "개발 하네스 만들어줘", "프로젝트 에이전트 구성해줘", "코덱스 개발환경 설정해줘", or "멀티에이전트 구성해줘".
---

# Harness Bootstrap

Build the smallest useful harness for the current software project.

## Workflow

1. Identify the current repository root. Do not scan unrelated parent directories.
2. Resolve this skill's plugin root and locate `scripts/harness.py` two levels above `skills/`.
3. Run the analyzer first:
   `python <plugin-root>/scripts/harness.py analyze --project <repo-root> --json`
4. Review the analyzer result. Do not manually read the entire repository unless a detected ambiguity materially affects setup.
5. Preview generated changes:
   `python <plugin-root>/scripts/harness.py init --project <repo-root> --dry-run`
6. If the preview is non-destructive, run the same command without `--dry-run`.
7. Validate with:
   `python <plugin-root>/scripts/harness.py audit --project <repo-root> --json`
8. Report only:
   - detected stack and complexity
   - files created/updated
   - any warnings or conflicts
   - one short example of what the user can ask next

## Rules

- Preserve existing user content outside managed markers.
- Never overwrite an unowned custom agent file.
- Do not put secrets, credentials, private keys, access tokens, or passwords into project context.
- Prefer no subagents for small projects.
- Do not add MCP servers during V1 bootstrap.
- Avoid editing application source code while configuring the harness.
