#!/usr/bin/env bash
set -euo pipefail
OWNER="${1:-JEREMI-Oh}"
REPO="${2:-codex-harness-builder}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v gh >/dev/null || { echo "GitHub CLI (gh) is required." >&2; exit 1; }
gh auth status >/dev/null
FULL="$OWNER/$REPO"
if gh repo view "$FULL" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$FULL.git"
  git push -u origin main
else
  gh repo create "$FULL" --public --source=. --remote=origin --push
fi
echo "Published: https://github.com/$FULL"
echo "Next: codex plugin marketplace add $FULL"
