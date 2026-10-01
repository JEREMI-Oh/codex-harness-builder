from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins" / "codex-harness-builder" / "scripts" / "harness.py"
spec = importlib.util.spec_from_file_location("harness", SCRIPT)
harness = importlib.util.module_from_spec(spec)
sys.modules["harness"] = harness
assert spec.loader is not None
spec.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def test_manifests_are_valid_json(self):
        paths = [
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / "plugins" / "codex-harness-builder" / "plugin.json",
            ROOT / "plugins" / "codex-harness-builder" / ".codex-plugin" / "plugin.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_small_project_stays_lean_and_preserves_existing_agents(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('hi')\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Existing rules\n\nKeep me.\n", encoding="utf-8")

            analysis = harness.detect(root)
            self.assertEqual(analysis.complexity, "SMALL")
            self.assertEqual(analysis.suggested_agents, [])

            first = harness.build(root, dry_run=False)
            self.assertFalse(first["conflicts"])
            content = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("# Existing rules", content)
            self.assertIn("Keep me.", content)
            self.assertEqual(content.count(harness.HTML_START), 1)
            self.assertFalse((root / ".codex" / "agents").exists())

            second = harness.build(root, dry_run=False)
            content2 = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(content2.count(harness.HTML_START), 1)
            self.assertEqual(second["changes"]["AGENTS.md"], "unchanged")

    def test_medium_project_gets_four_roles(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "package.json").write_text(
                json.dumps({"dependencies": {"react": "1", "vite": "1"}}), encoding="utf-8"
            )
            src = root / "src"
            src.mkdir()
            for i in range(60):
                (src / f"m{i}.ts").write_text(f"export const n{i} = {i};\n", encoding="utf-8")

            analysis = harness.detect(root)
            self.assertEqual(analysis.complexity, "MEDIUM")
            self.assertEqual(
                analysis.suggested_agents,
                ["researcher", "developer", "tester", "reviewer"],
            )
            harness.build(root, dry_run=False)
            for role in analysis.suggested_agents:
                self.assertTrue((root / ".codex" / "agents" / f"{role}.toml").exists())
            cfg = (root / ".codex" / "config.toml").read_text(encoding="utf-8")
            self.assertIn("[agents.researcher]", cfg)
            self.assertNotIn("[agents.architect]", cfg)

    def test_monorepo_is_large_and_gets_plans(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "package.json").write_text(
                json.dumps({"workspaces": ["apps/*"], "dependencies": {"react": "1"}}),
                encoding="utf-8",
            )
            (root / "src").mkdir()
            for i in range(5):
                (root / "src" / f"a{i}.ts").write_text("export {};\n", encoding="utf-8")
            analysis = harness.detect(root)
            self.assertEqual(analysis.complexity, "LARGE")
            self.assertIn("architect", analysis.suggested_agents)
            harness.build(root, dry_run=False)
            self.assertTrue((root / ".agent" / "PLANS.md").exists())
            self.assertTrue((root / ".agent" / "plans" / ".gitkeep").exists())

    def test_custom_role_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "package.json").write_text("{}", encoding="utf-8")
            (root / "src").mkdir()
            for i in range(80):
                (root / "src" / f"a{i}.js").write_text("module.exports = {};\n", encoding="utf-8")
            agent_dir = root / ".codex" / "agents"
            agent_dir.mkdir(parents=True)
            custom = agent_dir / "developer.toml"
            custom.write_text('developer_instructions = "CUSTOM"\n', encoding="utf-8")
            result = harness.build(root, dry_run=False)
            self.assertEqual(result["changes"][".codex/agents/developer.toml"], "conflict")
            self.assertEqual(custom.read_text(encoding="utf-8"), 'developer_instructions = "CUSTOM"\n')

    def test_secret_like_material_is_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\n", encoding="utf-8")
            harness.build(root, dry_run=False)
            memory = root / ".project-context" / "MEMORY.md"
            memory.write_text(memory.read_text(encoding="utf-8") + "api_key = sk-abcdefghijklmnopqrstuvwxyz123\n", encoding="utf-8")
            result = harness.audit(root)
            self.assertEqual(result["status"], "error")
            self.assertTrue(any(x["code"] == "possible_secret" for x in result["findings"]))


    def test_generated_toml_is_valid(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "package.json").write_text("{}", encoding="utf-8")
            (root / "src").mkdir()
            for i in range(50):
                (root / "src" / f"f{i}.ts").write_text("export {};\n", encoding="utf-8")
            harness.build(root, dry_run=False)
            tomllib.loads((root / ".codex" / "config.toml").read_text(encoding="utf-8"))
            for role in harness.detect(root).suggested_agents:
                tomllib.loads((root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8"))

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "app.py").write_text("print('x')\n", encoding="utf-8")
            result = harness.build(root, dry_run=True)
            self.assertEqual(result["changes"]["AGENTS.md"], "created")
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertFalse((root / ".project-context").exists())


if __name__ == "__main__":
    unittest.main()
