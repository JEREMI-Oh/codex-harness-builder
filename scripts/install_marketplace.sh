#!/usr/bin/env bash
set -euo pipefail
command -v codex >/dev/null || { echo "Codex CLI is not available on PATH." >&2; exit 1; }
codex plugin marketplace add JEREMI-Oh/codex-harness-builder
codex plugin marketplace list
