#!/usr/bin/env python3
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-harness-builder"
IGNORE = {".git", "__pycache__", ".pytest_cache", ".venv", "dist"}


def add_tree(zf: zipfile.ZipFile, source: Path, prefix: str = "") -> None:
    for path in sorted(source.rglob("*")):
        if path.is_dir() or any(part in IGNORE for part in path.parts):
            continue
        rel = path.relative_to(source).as_posix()
        arc = f"{prefix}/{rel}" if prefix else rel
        zf.write(path, arc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="0.1.0")
    args = parser.parse_args()
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)

    repo_zip = dist / f"codex-harness-builder-v{args.version}.zip"
    plugin_zip = dist / f"codex-harness-builder-plugin-v{args.version}.zip"

    with zipfile.ZipFile(repo_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        add_tree(zf, ROOT, "codex-harness-builder")
    with zipfile.ZipFile(plugin_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        add_tree(zf, PLUGIN)

    print(repo_zip)
    print(plugin_zip)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
