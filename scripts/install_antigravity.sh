#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SRC="$ROOT/plugins/universal-harness-antigravity"
SCOPE=${1:-global}
PROJECT=${2:-.}
if [ "$SCOPE" = "workspace" ]; then
  DEST="$(cd "$PROJECT" && pwd)/.agents/plugins/universal-agent-harness-builder"
else
  DEST="$HOME/.gemini/config/plugins/universal-agent-harness-builder"
fi
mkdir -p "$DEST"
cp -R "$SRC"/. "$DEST"/
echo "Installed Antigravity plugin to: $DEST"
