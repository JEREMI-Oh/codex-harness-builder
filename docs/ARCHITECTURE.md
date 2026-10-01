# Architecture

Universal Agent Harness Builder separates **project knowledge** from **runtime adapters**.

```text
Repository
├─ AGENTS.md                    shared always-on instructions
├─ .project-context/            durable project knowledge
├─ .harness/                    manifest + complex execution plans
├─ .codex/                      Codex adapter
├─ .agents/                     Antigravity adapter
└─ .claude/ + CLAUDE.md         Claude Code adapter
```

## Shared layer

`AGENTS.md` contains only compact cross-platform development rules. `.project-context/` stores durable facts, current architecture, decisions, reusable lessons, and current work. Agents are instructed to read only the relevant file instead of loading all context every turn.

## Adapter layer

- **Codex:** `.codex/config.toml` and `.codex/agents/*.toml`.
- **Antigravity:** `.agents/agents/*.md` plus model-decision rules under `.agents/rules/`.
- **Claude Code:** `CLAUDE.md` imports `@AGENTS.md`; `.claude/agents/*.md` adds project subagents.

## Complexity policy

- SMALL: common context only; no custom roles by default.
- MEDIUM: researcher, developer, tester, reviewer.
- LARGE: architect plus the MEDIUM roles and durable plan scaffolding.

## Non-destructive ownership

Managed blocks are delimited with `UNIVERSAL-HARNESS` markers. Generated standalone files contain a generator sentinel. User-owned files without that sentinel are never overwritten.
