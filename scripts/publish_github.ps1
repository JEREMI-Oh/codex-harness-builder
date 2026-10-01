param(
    [string]$Owner = "",
    [string]$RepoName = "codex-harness-builder",
    [string]$CommitMessage = "Release Universal Agent Harness Builder v0.2.0"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI (gh) is required." }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required." }
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw "Run 'gh auth login' first." }

$Login = (& gh api user --jq .login).Trim()
$UserId = (& gh api user --jq .id).Trim()
if ([string]::IsNullOrWhiteSpace($Owner)) { $Owner = $Login }
$FullName = "$Owner/$RepoName"

& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    git init
    git branch -M main
}

& git config user.name *> $null
if ($LASTEXITCODE -ne 0) { git config user.name $Login }
& git config user.email *> $null
if ($LASTEXITCODE -ne 0) { git config user.email "$UserId+$Login@users.noreply.github.com" }

git add .
$Staged = git diff --cached --name-only
if ($Staged) {
    git commit -m $CommitMessage
}

gh repo view $FullName --json name *> $null
if ($LASTEXITCODE -ne 0) {
    gh repo create $FullName --public --source=. --remote=origin --push
} else {
    git remote get-url origin *> $null
    if ($LASTEXITCODE -ne 0) { git remote add origin "https://github.com/$FullName.git" }
    git push -u origin main
}
Write-Host "Published: https://github.com/$FullName"
