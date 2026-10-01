# Architecture

## V1

Codex Harness Builder is intentionally skills-first and serverless.

```text
User request
   |
   v
Plugin skill trigger
   |
   v
scripts/harness.py
   |
   +--> repository analyzer
   +--> complexity classifier
   +--> managed-block writer
   +--> custom-agent generator
   +--> audit / compaction
   |
   v
Target project
```

No source code or project metadata is sent to a project-owned external service by the plugin itself. Codex's own execution environment and configured tools remain subject to their normal product behavior.

## Why no MCP in V1

The first use case is local repository analysis and file generation. Adding a server would add authentication, deployment, tool-schema context, and operational overhead without being necessary for the core workflow.

## V2 candidates

A future optional MCP service could provide cross-project durable knowledge, shared organizational skills, solution lookup, or project history. It should remain opt-in so the default harness stays lean.

## Context model

- `AGENTS.md`: small, always-relevant operating rules.
- `.project-context/PROJECT.md`: stable facts and entry points.
- `.project-context/ARCHITECTURE.md`: current system structure.
- `.project-context/DECISIONS.md`: durable design decisions.
- `.project-context/MEMORY.md`: deliberately small non-secret memory.
- `.project-context/LESSONS.md`: reusable failure/solution patterns.
- `.project-context/TODO.md`: current work.

This separation avoids turning a single instruction file into an ever-growing prompt.
