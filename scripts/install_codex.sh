#!/usr/bin/env sh
set -eu
command -v codex >/dev/null 2>&1 || { echo "Codex CLI is not available on PATH." >&2; exit 1; }
codex plugin marketplace add JEREMI-Oh/codex-harness-builder --ref main
codex plugin marketplace list
echo "Open Codex, run /plugins, and install 'Universal Agent Harness Builder'."
