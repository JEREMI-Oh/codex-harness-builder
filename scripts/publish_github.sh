#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
OWNER=${1:-$(gh api user --jq .login)}
REPO=${2:-codex-harness-builder}
FULL="$OWNER/$REPO"
[ -d .git ] || { git init; git branch -M main; }
git config user.name >/dev/null 2>&1 || git config user.name "$OWNER"
USER_ID=$(gh api user --jq .id)
git config user.email >/dev/null 2>&1 || git config user.email "$USER_ID+$OWNER@users.noreply.github.com"
git add .
if ! git diff --cached --quiet; then git commit -m "Release Universal Agent Harness Builder v0.2.0"; fi
if gh repo view "$FULL" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$FULL.git"
  git push -u origin main
else
  gh repo create "$FULL" --public --source=. --remote=origin --push
fi
