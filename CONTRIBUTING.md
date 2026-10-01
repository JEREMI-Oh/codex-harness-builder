# Contributing

Contributions are welcome.

## Development

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

The project intentionally has no runtime Python dependencies.

## Pull requests

Please keep changes focused and preserve these invariants:

- setup is non-destructive
- repeated setup is idempotent
- existing user content outside managed markers is preserved
- small projects do not receive unnecessary agent configuration
- secrets are never copied into generated context files
