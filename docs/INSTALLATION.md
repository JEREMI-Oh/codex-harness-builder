# Installation

## Codex

```powershell
codex plugin marketplace add JEREMI-Oh/codex-harness-builder --ref main
codex plugin marketplace list
```

Install **Universal Agent Harness Builder** from `/plugins`, then start a new Codex session in the target project and say `하네스 구성해줘`.

## Google Antigravity IDE

Workspace install: copy `plugins/universal-harness-antigravity` to:

```text
<project>/.agents/plugins/universal-agent-harness-builder/
```

Global install: copy it to:

```text
~/.gemini/config/plugins/universal-agent-harness-builder/
```

Use `scripts/install_antigravity.ps1` on Windows for an automatic copy.

## Claude Code

```powershell
claude plugin marketplace add JEREMI-Oh/codex-harness-builder
claude plugin install universal-agent-harness-builder@universal-agent-harness
```

Then start/reload Claude Code and say `하네스 구성해줘`, or invoke the namespaced bootstrap skill explicitly.

## Direct CLI

```powershell
python src\harness.py init --project C:\path\to\project --target all --dry-run
python src\harness.py init --project C:\path\to\project --target all
```
