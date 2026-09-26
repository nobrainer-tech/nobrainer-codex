import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "install.py"


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / ".codex"
        self.home.mkdir()
        self.catalog = self.home / "catalog.json"
        self.catalog.write_text(json.dumps({"models": [
            {"slug": "gpt-6-astra", "max_context_window": 872000,
             "supported_reasoning_levels": [{"effort": "low"}, {"effort": "max"}]},
            {"slug": "old-model", "max_context_window": 128000},
        ]}))
        self.config = self.home / "config.toml"
        self.config.write_text('model = "gpt-6-astra"\nmodel_reasoning_effort = "low"\n'
                               f'model_catalog_json = {json.dumps(str(self.catalog))}\n'
                               'approval_policy = "on-request"\n\n[agents]\n'
                               'max_concurrent_threads_per_session = 3\n\n[tui]\n'
                               'screen_reader_detection_done = true\n')
        self.agents = self.home / "AGENTS.md"
        self.agents.write_text("user-original\n")

    def run_installer(self, flag):
        return subprocess.run([sys.executable, str(SCRIPT), flag, "--codex-home", str(self.home)],
                              text=True, capture_output=True, timeout=30)

    def test_check_is_read_only_and_apply_is_idempotent(self):
        original = self.config.read_bytes()
        preview = self.run_installer("--check")
        self.assertEqual(preview.returncode, 0)
        self.assertEqual(json.loads(preview.stdout)["reasoning_levels_in_catalog"], ["low", "max"])
        self.assertTrue(json.loads(preview.stdout)["max_reasoning_in_catalog"])
        self.assertEqual(self.config.read_bytes(), original)
        self.assertEqual(self.agents.read_text(), "user-original\n")
        applied = self.run_installer("--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        state = tomllib.loads(self.config.read_text())
        self.assertEqual((state["model"], state["model_reasoning_effort"]), ("gpt-6-astra", "low"))
        self.assertEqual(state["approval_policy"], "on-request")
        self.assertEqual(state["model_context_window"], 872000)
        self.assertEqual(state["model_auto_compact_token_limit"], 784800)
        self.assertEqual(state["agents"], {"max_concurrent_threads_per_session": 15,
                                           "default_subagent_model": "openai/gpt-6-luna"})
        self.assertEqual(state["tui"]["status_line"][1], "context-remaining")
        self.assertIn("https://github.com/nobrainer-tech/nobrainer-tech-flow", self.agents.read_text())
        self.assertIn("Use nobrainer-tech-flow", self.agents.read_text())
        self.assertEqual(self.run_installer("--apply").returncode, 0)
        self.assertEqual(len(list(self.home.glob("nobrainer-codex-backup-*"))), 1)

    def test_lower_capability_never_gets_872k(self):
        self.config.write_text(self.config.read_text().replace('model = "gpt-6-astra"', 'model = "old-model"'))
        self.assertEqual(self.run_installer("--apply").returncode, 0)
        self.assertEqual(tomllib.loads(self.config.read_text())["model_context_window"], 128000)
        self.assertFalse(json.loads(self.run_installer("--check").stdout)["max_reasoning_in_catalog"])

    def test_missing_catalog_keeps_existing_window(self):
        self.config.write_text(self.config.read_text().replace('[agents]', 'model_context_window = 256000\n\n[agents]'))
        self.catalog.unlink()
        self.assertEqual(self.run_installer("--apply").returncode, 0)
        self.assertEqual(tomllib.loads(self.config.read_text())["model_context_window"], 256000)

    def test_legacy_conflict_fails_before_any_write(self):
        self.config.write_text(self.config.read_text().replace("max_concurrent_threads_per_session = 3", "max_threads = 3"))
        original = self.config.read_bytes()
        self.assertNotEqual(self.run_installer("--apply").returncode, 0)
        self.assertEqual(self.config.read_bytes(), original)
        self.assertEqual(self.agents.read_text(), "user-original\n")


if __name__ == "__main__":
    unittest.main()
