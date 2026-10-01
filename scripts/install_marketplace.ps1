$ErrorActionPreference = "Stop"
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "Codex CLI is not available on PATH."
}
codex plugin marketplace add JEREMI-Oh/codex-harness-builder
codex plugin marketplace list
