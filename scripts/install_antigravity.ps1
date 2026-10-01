param(
    [ValidateSet("Global", "Workspace")][string]$Scope = "Global",
    [string]$ProjectPath = "."
)
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Source = Join-Path $RepoRoot "plugins\universal-harness-antigravity"
if (-not (Test-Path $Source)) { throw "Antigravity plugin package not found: $Source" }

if ($Scope -eq "Global") {
    $Destination = Join-Path $HOME ".gemini\config\plugins\universal-agent-harness-builder"
} else {
    $ProjectRoot = (Resolve-Path $ProjectPath).Path
    $Destination = Join-Path $ProjectRoot ".agents\plugins\universal-agent-harness-builder"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
Copy-Item -Path (Join-Path $Source "*") -Destination $Destination -Recurse -Force
Write-Host "Installed Antigravity plugin to: $Destination"
Write-Host "Reopen/refresh Antigravity Customizations if the plugin is not immediately visible."
