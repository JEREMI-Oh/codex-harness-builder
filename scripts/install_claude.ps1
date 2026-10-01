$ErrorActionPreference = "Stop"
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    throw "Claude Code CLI is not available on PATH."
}
claude plugin marketplace add JEREMI-Oh/codex-harness-builder
claude plugin install universal-agent-harness-builder@universal-agent-harness
Write-Host "If Claude Code asks for reload, run /reload-plugins in the session."
