# Universal Agent Harness Builder v0.2.0

A dependency-free, non-destructive harness builder for **OpenAI Codex**, **Google Antigravity**, and **Anthropic Claude Code**.

It keeps project knowledge in one shared layer and generates only the runtime-specific adapter you need.

```text
PROJECT/
├─ AGENTS.md
├─ .project-context/
├─ .harness/
├─ .codex/                 # Codex adapter
├─ .agents/                # Antigravity adapter
└─ .claude/ + CLAUDE.md    # Claude Code adapter
```

## Commands

```bash
python src/harness.py analyze --project /path/to/repo
python src/harness.py init --project /path/to/repo --target codex
python src/harness.py init --project /path/to/repo --target antigravity
python src/harness.py init --project /path/to/repo --target claude-code
python src/harness.py init --project /path/to/repo --target all
python src/harness.py update --project /path/to/repo --target auto
python src/harness.py audit --project /path/to/repo --target auto
python src/harness.py compact --project /path/to/repo --target auto
python src/harness.py migrate --project /path/to/repo --target all
```

Use `--dry-run` with init/update/migrate/compact to preview changes.

## Install as a Codex plugin

```bash
codex plugin marketplace add JEREMI-Oh/codex-harness-builder --ref main
```

Then install **Universal Agent Harness Builder** from `/plugins` and ask `하네스 구성해줘` or “configure the project harness”.

## Install in Antigravity

Copy `plugins/universal-harness-antigravity` to either:

- `<workspace>/.agents/plugins/universal-agent-harness-builder/`
- `~/.gemini/config/plugins/universal-agent-harness-builder/`

On Windows you can run `scripts/install_antigravity.ps1`.

## Install in Claude Code

```bash
claude plugin marketplace add JEREMI-Oh/codex-harness-builder
claude plugin install universal-agent-harness-builder@universal-agent-harness
```

Claude Code receives shared instructions through a generated `CLAUDE.md` that imports `@AGENTS.md`.

## Design goals

- minimal always-on context
- project-aware but non-destructive setup
- role-based subagents only when complexity justifies them
- shared durable knowledge without duplicating it across runtimes
- migration from the V0.1 Codex-only harness
- no MCP server required for V0.2

See `README.ko.md`, `docs/ARCHITECTURE.md`, `docs/INSTALLATION.md`, and `docs/MIGRATION.md`.

MIT License.
