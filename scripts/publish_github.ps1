param(
    [string]$Owner = "JEREMI-Oh",
    [string]$RepoName = "codex-harness-builder"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install it, run 'gh auth login', then rerun this script."
}

$null = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login' first."
}

$FullName = "$Owner/$RepoName"
gh repo view $FullName *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating public repository $FullName ..."
    gh repo create $FullName --public --source=. --remote=origin --push
} else {
    Write-Host "Repository $FullName already exists. Pushing main ..."
    $origin = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        git remote add origin "https://github.com/$FullName.git"
    }
    git push -u origin main
}

Write-Host "Published: https://github.com/$FullName"
Write-Host "Next: codex plugin marketplace add $FullName"
