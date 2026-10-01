from __future__ import annotations

import importlib.util
import json
import tempfile
import tomllib
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "harness.py"
spec = importlib.util.spec_from_file_location("universal_harness", SCRIPT)
harness = importlib.util.module_from_spec(spec)
sys.modules["universal_harness"] = harness
assert spec.loader is not None
spec.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def make_medium(self, root: Path) -> None:
        (root / "package.json").write_text(
            json.dumps({"dependencies": {"react": "1", "vite": "1"}}), encoding="utf-8"
        )
        src = root / "src"
        src.mkdir()
        for i in range(60):
            (src / f"m{i}.ts").write_text(f"export const n{i} = {i};\n", encoding="utf-8")

    def test_manifests_are_valid_json(self):
        paths = [
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / "plugins" / "universal-harness-openai" / "plugin.json",
            ROOT / "plugins" / "universal-harness-openai" / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "universal-harness-antigravity" / "plugin.json",
            ROOT / "plugins" / "universal-harness-claude" / ".claude-plugin" / "plugin.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_small_project_common_only_is_lean_and_preserves_existing_agents(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('hi')\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Existing rules\n\nKeep me.\n", encoding="utf-8")

            analysis = harness.detect(root)
            self.assertEqual(analysis.complexity, "SMALL")
            self.assertEqual(analysis.suggested_agents, [])

            result = harness.build(root, dry_run=False, target="common")
            self.assertFalse(result["conflicts"])
            content = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Existing rules", content)
            self.assertIn("Keep me.", content)
            self.assertEqual(content.count(harness.HTML_START), 1)
            self.assertFalse((root / ".codex").exists())
            self.assertFalse((root / ".agents" / "agents").exists())
            self.assertFalse((root / ".claude").exists())
            self.assertTrue((root / ".harness" / "manifest.json").exists())

    def test_codex_medium_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            result = harness.build(root, dry_run=False, target="codex")
            self.assertEqual(result["targets"], ["codex"])
            for role in ["researcher", "developer", "tester", "reviewer"]:
                self.assertTrue((root / ".codex" / "agents" / f"{role}.toml").exists())
                tomllib.loads((root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8"))
            cfg = (root / ".codex" / "config.toml").read_text(encoding="utf-8")
            self.assertIn("[agents.researcher]", cfg)
            tomllib.loads(cfg)
            self.assertFalse((root / ".agents" / "agents").exists())
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_antigravity_medium_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            result = harness.build(root, dry_run=False, target="antigravity")
            self.assertEqual(result["targets"], ["antigravity"])
            for role in ["researcher", "developer", "tester", "reviewer"]:
                text = (root / ".agents" / "agents" / f"{role}.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                self.assertIn(f"name: {role}", text)
                self.assertIn("model: inherit", text)
                self.assertIn("subagent: true", text)
            self.assertTrue((root / ".agents" / "rules" / "harness-context-efficiency.md").exists())
            self.assertTrue((root / ".agents" / "rules" / "harness-project-safety.md").exists())
            self.assertFalse((root / ".codex").exists())
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_claude_medium_adapter_imports_agents(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            result = harness.build(root, dry_run=False, target="claude-code")
            self.assertEqual(result["targets"], ["claude-code"])
            claude = (root / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("@AGENTS.md", claude)
            for role in ["researcher", "developer", "tester", "reviewer"]:
                text = (root / ".claude" / "agents" / f"{role}.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                self.assertIn(f"name: {role}", text)
                self.assertIn("model: inherit", text)
            self.assertFalse((root / ".codex").exists())

    def test_all_target_builds_all_adapters(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            result = harness.build(root, dry_run=False, target="all")
            self.assertEqual(set(result["targets"]), set(harness.TARGETS))
            self.assertTrue((root / ".codex" / "config.toml").exists())
            self.assertTrue((root / ".agents" / "agents" / "developer.md").exists())
            self.assertTrue((root / ".claude" / "agents" / "developer.md").exists())
            self.assertIn("@AGENTS.md", (root / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_large_project_gets_architect_and_plans(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "package.json").write_text(
                json.dumps({"workspaces": ["apps/*"], "dependencies": {"react": "1"}}), encoding="utf-8"
            )
            (root / "src").mkdir()
            for i in range(5):
                (root / "src" / f"a{i}.ts").write_text("export {};\n", encoding="utf-8")
            analysis = harness.detect(root)
            self.assertEqual(analysis.complexity, "LARGE")
            self.assertIn("architect", analysis.suggested_agents)
            harness.build(root, dry_run=False, target="all")
            self.assertTrue((root / ".harness" / "PLANS.md").exists())
            self.assertTrue((root / ".harness" / "plans" / ".gitkeep").exists())
            self.assertTrue((root / ".codex" / "agents" / "architect.toml").exists())
            self.assertTrue((root / ".agents" / "agents" / "architect.md").exists())
            self.assertTrue((root / ".claude" / "agents" / "architect.md").exists())

    def test_unowned_platform_agent_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            agent_dir = root / ".agents" / "agents"
            agent_dir.mkdir(parents=True)
            custom = agent_dir / "developer.md"
            custom.write_text("---\nname: developer\n---\nCUSTOM\n", encoding="utf-8")
            result = harness.build(root, dry_run=False, target="antigravity")
            self.assertEqual(result["changes"][".agents/agents/developer.md"], "conflict")
            self.assertIn("CUSTOM", custom.read_text(encoding="utf-8"))

    def test_legacy_codex_markers_are_migrated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            (root / "AGENTS.md").write_text(
                "# Team rules\n\n<!-- CODEX-HARNESS:START -->\nold\n<!-- CODEX-HARNESS:END -->\n",
                encoding="utf-8",
            )
            cfg = root / ".codex" / "config.toml"
            cfg.parent.mkdir(parents=True)
            cfg.write_text("# CODEX-HARNESS:START\nold\n# CODEX-HARNESS:END\n", encoding="utf-8")
            harness.build(root, dry_run=False, target="codex", mode="migrate")
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Team rules", agents)
            self.assertIn(harness.HTML_START, agents)
            self.assertNotIn(harness.LEGACY_HTML_START, agents)
            config = cfg.read_text(encoding="utf-8")
            self.assertIn(harness.TOML_START, config)
            self.assertNotIn(harness.LEGACY_TOML_START, config)

    def test_secret_like_material_is_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\n", encoding="utf-8")
            harness.build(root, dry_run=False, target="common")
            memory = root / ".project-context" / "MEMORY.md"
            memory.write_text(
                memory.read_text(encoding="utf-8") + "api_key = sk-abcdefghijklmnopqrstuvwxyz123\n",
                encoding="utf-8",
            )
            result = harness.audit(root, "common")
            self.assertEqual(result["status"], "error")
            self.assertTrue(any(x["code"] == "possible_secret" for x in result["findings"]))

    def test_update_auto_reuses_manifest_targets(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_medium(root)
            harness.build(root, dry_run=False, target="claude-code")
            # Presence of .claude is also a signal, but manifest reuse is the intended update behavior.
            result = harness.build(root, dry_run=False, target="auto", mode="update")
            self.assertEqual(result["targets"], ["claude-code"])
            self.assertFalse((root / ".codex").exists())

    def test_auto_detects_antigravity_marker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\n", encoding="utf-8")
            (root / ".agents" / "rules").mkdir(parents=True)
            self.assertIn("antigravity", harness.detect_platforms(root))
            result = harness.build(root, dry_run=False, target="auto")
            self.assertEqual(result["targets"], ["antigravity"])

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\n", encoding="utf-8")
            result = harness.build(root, dry_run=True, target="all")
            self.assertEqual(result["changes"]["AGENTS.md"], "created")
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertFalse((root / ".project-context").exists())
            self.assertFalse((root / ".harness").exists())


if __name__ == "__main__":
    unittest.main()
