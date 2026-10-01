$ErrorActionPreference = "Stop"
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "Codex CLI is not available on PATH."
}
codex plugin marketplace add JEREMI-Oh/codex-harness-builder --ref main
codex plugin marketplace list
Write-Host "Open Codex, run /plugins, and install 'Universal Agent Harness Builder'."
