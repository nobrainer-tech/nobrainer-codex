from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BrowserRunbookTest(unittest.TestCase):
    def test_recovery_requires_conversation_identity(self):
        text = (ROOT / "docs/external-ssd.md").read_text(encoding="utf-8")
        self.assertIn("codexSessionId", text)
        self.assertIn("exact browser and tab IDs", text)
        self.assertIn("session metadata is absent or mismatched", text)
        self.assertIn("at least two conversations", text)
        self.assertNotIn('{browser: "iab"}', text)

    def test_readback_is_not_interaction_or_global_recovery(self):
        text = (ROOT / "docs/external-ssd.md").read_text(encoding="utf-8")
        self.assertIn("without that change is not a pass", text)
        self.assertIn("New-tab success must not be reported as recovery", text)
        self.assertIn("untrusted-process-ancestry", text)
        self.assertIn("Preserve the user's original tab", text)


if __name__ == "__main__":
    unittest.main()
