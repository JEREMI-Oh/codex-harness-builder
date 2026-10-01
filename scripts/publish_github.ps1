param(
    [string]$Owner = "",
    [string]$RepoName = "codex-harness-builder"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

function Invoke-NativeQuiet {
    param(
        [Parameter(Mandatory=$true)][string]$Command,
        [Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments
    )

    $previousPreference = $ErrorActionPreference
    try {
        # Windows PowerShell can promote native stderr into a terminating error
        # when ErrorActionPreference is Stop. Suppress it for existence checks.
        $ErrorActionPreference = "SilentlyContinue"
        & $Command @Arguments *> $null
        return $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install it, run 'gh auth login', then rerun this script."
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required. Install Git for Windows, then rerun this script."
}

$authExit = Invoke-NativeQuiet gh auth status
if ($authExit -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login' first."
}

if ([string]::IsNullOrWhiteSpace($Owner)) {
    $Owner = (& gh api user --jq .login).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Owner)) {
        throw "Could not determine the authenticated GitHub username. Pass -Owner explicitly."
    }
}

$FullName = "$Owner/$RepoName"

# Source ZIPs intentionally do not contain .git. Initialize a local repo when needed.
$insideGit = Invoke-NativeQuiet git rev-parse --is-inside-work-tree
if ($insideGit -ne 0) {
    Write-Host "Initializing local Git repository ..."
    git init
    if ($LASTEXITCODE -ne 0) { throw "git init failed." }

    git branch -M main
    git add .
    if ($LASTEXITCODE -ne 0) { throw "git add failed." }

    $hasName = Invoke-NativeQuiet git config user.name
    if ($hasName -ne 0) {
        git config user.name $Owner
    }

    $hasEmail = Invoke-NativeQuiet git config user.email
    if ($hasEmail -ne 0) {
        # GitHub accepts a noreply address for local commit metadata.
        git config user.email "$Owner@users.noreply.github.com"
    }

    git commit -m "Initial release: Codex Harness Builder"
    if ($LASTEXITCODE -ne 0) { throw "Initial git commit failed." }
}
else {
    # Ensure the publication branch is main.
    git branch -M main
}

$repoExit = Invoke-NativeQuiet gh repo view $FullName --json name
if ($repoExit -ne 0) {
    Write-Host "Creating public repository $FullName ..."

    # Remove a stale origin if it points somewhere else.
    $originExit = Invoke-NativeQuiet git remote get-url origin
    if ($originExit -eq 0) {
        $origin = (& git remote get-url origin).Trim()
        $expectedHttps = "https://github.com/$FullName.git"
        $expectedSsh = "git@github.com:$FullName.git"
        if ($origin -ne $expectedHttps -and $origin -ne $expectedSsh) {
            Write-Host "Removing stale origin: $origin"
            git remote remove origin
        }
    }

    gh repo create $FullName --public --source=. --remote=origin --push
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub repository creation or initial push failed."
    }
}
else {
    Write-Host "Repository $FullName already exists. Pushing main ..."

    $originExit = Invoke-NativeQuiet git remote get-url origin
    if ($originExit -ne 0) {
        git remote add origin "https://github.com/$FullName.git"
    }

    git push -u origin main
    if ($LASTEXITCODE -ne 0) {
        throw "git push failed. Check repository permissions and the origin remote."
    }
}

Write-Host ""
Write-Host "Published: https://github.com/$FullName"
Write-Host "Next: codex plugin marketplace add $FullName"
