# Contributing

1. Keep the core dependency-free unless a dependency has a clear cross-platform benefit.
2. Never make bootstrap edit application source code.
3. Preserve user-owned files; generated files must carry the product sentinel.
4. Keep always-on instructions short. Put task-specific procedures in skills.
5. Add tests for every new platform adapter or migration behavior.

Run tests with:

```bash
python -m unittest discover -s tests -v
```
