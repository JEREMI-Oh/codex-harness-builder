from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.0"
DIST = ROOT / "dist"
PLUGINS = {
    "openai": ROOT / "plugins" / "universal-harness-openai",
    "antigravity": ROOT / "plugins" / "universal-harness-antigravity",
    "claude": ROOT / "plugins" / "universal-harness-claude",
}


def sync_core() -> None:
    source = ROOT / "src" / "harness.py"
    for plugin in PLUGINS.values():
        target = plugin / "scripts" / "harness.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def add_tree(zf: zipfile.ZipFile, base: Path, prefix: str, excludes: set[str] | None = None) -> None:
    excludes = excludes or set()
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if any(part in excludes for part in rel.parts):
            continue
        zf.write(path, f"{prefix}/{rel.as_posix()}")


def main() -> None:
    sync_core()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    source_zip = DIST / f"universal-agent-harness-builder-v{VERSION}.zip"
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        add_tree(zf, ROOT, "universal-agent-harness-builder", {"dist", ".git", "__pycache__", ".pytest_cache"})

    for platform, plugin in PLUGINS.items():
        out = DIST / f"universal-agent-harness-builder-{platform}-v{VERSION}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            add_tree(zf, plugin, "universal-agent-harness-builder", {"__pycache__"})

    print(source_zip)
    for p in sorted(DIST.glob("*.zip")):
        print(p)


if __name__ == "__main__":
    main()
