# Migration from Codex Harness Builder V0.1

V0.2 recognizes the old `CODEX-HARNESS` managed markers and generated-file sentinel.

From an existing project:

```bash
python src/harness.py migrate --project /path/to/project --target all --dry-run
python src/harness.py migrate --project /path/to/project --target all
python src/harness.py audit --project /path/to/project --target all
```

The migration preserves `.project-context/` contents. Legacy `.agent/PLANS.md` is not deleted automatically; V0.2 uses `.harness/PLANS.md` and reports the old location during audit.
