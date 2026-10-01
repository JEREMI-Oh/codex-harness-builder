#!/usr/bin/env sh
set -eu
command -v claude >/dev/null 2>&1 || { echo "Claude Code CLI is not available on PATH." >&2; exit 1; }
claude plugin marketplace add JEREMI-Oh/codex-harness-builder
claude plugin install universal-agent-harness-builder@universal-agent-harness
echo "If Claude Code asks for reload, run /reload-plugins in the session."
