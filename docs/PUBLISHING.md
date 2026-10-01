# Publishing

The repository is prepared for:

`JEREMI-Oh/codex-harness-builder`

## 1. Publish the GitHub repository

From the project directory on a machine authenticated to GitHub CLI:

```bash
gh repo create JEREMI-Oh/codex-harness-builder --public --source=. --remote=origin --push
```

Without GitHub CLI, create an empty public repository named `codex-harness-builder` in the `JEREMI-Oh` account, then:

```bash
git remote add origin https://github.com/JEREMI-Oh/codex-harness-builder.git
git push -u origin main
```

## 2. Install as a repo marketplace

After the repository is public:

```bash
codex plugin marketplace add JEREMI-Oh/codex-harness-builder
```

Open the Plugins Directory in the ChatGPT/Codex desktop app and install **Codex Harness Builder**.

## 3. Submit to the universal Plugins Directory

Use the standalone plugin ZIP from the release artifacts. Universal directory publication requires the OpenAI plugin submission/review flow and the publisher's verified organization/project permissions.

For a skills-only package, keep the archive root at the plugin package root containing `plugin.json`, `skills/`, and the bundled scripts.

## Release checklist

- Run `python -m unittest discover -s tests -v`.
- Validate JSON manifests.
- Run analyzer against the repository.
- Create the repository ZIP and plugin-only ZIP.
- Tag a semantic version such as `v0.1.0`.
- Upload plugin ZIP to the plugin submission portal if public-directory publication is desired.
