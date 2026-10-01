# Security

The harness builder is designed to operate locally and does not require credentials or an MCP server in V0.2.

- Do not place API keys, access tokens, passwords, private keys, or secrets in `.project-context/`.
- The audit command scans `MEMORY.md` for common secret-like patterns but is not a complete secret scanner.
- Bootstrap/update never intentionally modify application source code.
- Existing unowned agent/rule files are preserved and reported as conflicts.
