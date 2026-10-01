@echo off
setlocal EnableExtensions

set "EXPECTED_REPO=JEREMI-Oh/codex-harness-builder"
set "COMMIT_MSG=Release Universal Agent Harness Builder v0.2.0"

for %%I in ("%~dp0..") do set "SOURCE=%%~fI"

if "%~1"=="" (
  set "TARGET=C:\Users\HNT_01\Downloads\codex-harness-builder-git"
) else (
  set "TARGET=%~1"
)

for %%I in ("%TARGET%") do set "TARGET=%%~fI"

echo ============================================================
echo Universal Agent Harness Builder v0.2.0 - GitHub Updater
echo ============================================================
echo Source : %SOURCE%
echo Target : %TARGET%
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Git is not installed or not on PATH.
  exit /b 1
)

if not exist "%SOURCE%\src\harness.py" (
  echo [ERROR] Source package is incomplete: src\harness.py not found.
  exit /b 1
)

if not exist "%TARGET%\.git" (
  echo [ERROR] Target is not a cloned Git repository: %TARGET%
  echo Clone it first with:
  echo   git clone https://github.com/%EXPECTED_REPO%.git "%TARGET%"
  exit /b 1
)

pushd "%TARGET%" || exit /b 1

for /f "delims=" %%R in ('git remote get-url origin 2^>nul') do set "ORIGIN=%%R"
if not defined ORIGIN (
  echo [ERROR] Target repository has no origin remote.
  popd
  exit /b 1
)

echo Origin : %ORIGIN%
echo.

git status --porcelain > "%TEMP%\uahb_git_status.txt"
for %%A in ("%TEMP%\uahb_git_status.txt") do if %%~zA GTR 0 (
  echo [ERROR] Target repository has uncommitted changes.
  echo Commit or discard them before running this updater.
  type "%TEMP%\uahb_git_status.txt"
  del "%TEMP%\uahb_git_status.txt" >nul 2>&1
  popd
  exit /b 1
)
del "%TEMP%\uahb_git_status.txt" >nul 2>&1

echo [1/5] Updating local main from GitHub...
git switch main >nul 2>&1
if errorlevel 1 git checkout main >nul 2>&1
git pull --ff-only origin main
if errorlevel 1 (
  echo [ERROR] git pull failed.
  popd
  exit /b 1
)

popd

echo [2/5] Replacing v0.1 files with Universal Harness v0.2 files...
robocopy "%SOURCE%" "%TARGET%" /MIR /XD ".git" "dist" "__pycache__" /XF "*.pyc" /R:1 /W:1 /NFL /NDL /NJH /NJS /NP
set "RC=%ERRORLEVEL%"
if %RC% GEQ 8 (
  echo [ERROR] File synchronization failed. Robocopy exit code: %RC%
  exit /b %RC%
)

pushd "%TARGET%" || exit /b 1

echo [3/5] Preparing Git commit...
git config user.name >nul 2>&1
if errorlevel 1 git config user.name "JEREMI-Oh"
git config user.email >nul 2>&1
if errorlevel 1 git config user.email "213302525+JEREMI-Oh@users.noreply.github.com"

git add -A

git diff --cached --quiet
if not errorlevel 1 (
  echo [INFO] No changes detected. Repository may already be on v0.2.0.
  goto VERIFY
)

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
  echo [ERROR] git commit failed.
  popd
  exit /b 1
)

echo [4/5] Pushing main to GitHub...
git push origin main
if errorlevel 1 (
  echo [ERROR] git push failed.
  popd
  exit /b 1
)

:VERIFY
echo [5/5] Verifying repository state...
git status --short
git log -1 --oneline

echo.
where gh >nul 2>&1
if not errorlevel 1 (
  gh repo view %EXPECTED_REPO% --json url,defaultBranchRef --jq "{url:.url,branch:.defaultBranchRef.name}"
)

echo.
echo ============================================================
echo Update complete.
echo GitHub: https://github.com/%EXPECTED_REPO%
echo ============================================================
popd
exit /b 0
