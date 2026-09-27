from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = []
        self.in_title = False
        self.copy_buttons = []
        self.copy_status = None
        self.in_prompt = False
        self.prompt_text = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href"))
        if tag == "button" and "data-copy-prompt" in values:
            self.copy_buttons.append(values)
        if values.get("id") == "copy-status":
            self.copy_status = values
        if values.get("id") == "install-prompt":
            self.in_prompt = True
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "code" and self.in_prompt:
            self.in_prompt = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_prompt:
            self.prompt_text.append(data)


class SiteTest(unittest.TestCase):
    def test_shared_brand_typography_is_loaded_last(self):
        text = (ROOT / "site/index.html").read_text(encoding="utf-8")
        css = (ROOT / "site/assets/brand-typography.css").read_text(encoding="utf-8")
        self.assertIn('href="assets/brand-typography.css?v=20260927"', text)
        self.assertGreater(text.index("assets/brand-typography.css"), text.rfind("</style>"))
        self.assertIn("font-family: var(--font-brand)", css)
        self.assertIn("font-weight: 700", css)
        self.assertIn("clamp(54px, 6.15vw, 88px)", css)
        self.assertIn("header .wordmark .product-path", css)
        self.assertIn("@media (max-width: 360px)", css)

    def test_install_and_source_links_have_real_targets(self):
        text = (ROOT / "site/index.html").read_text(encoding="utf-8")
        parser = Page()
        parser.feed(text)
        self.assertIn("Codex", "".join(parser.title))
        self.assertIn("https://github.com/nobrainer-tech/nobrainer-codex", parser.links)
        self.assertIn("https://github.com/nobrainer-tech/nobrainer-codex/blob/main/docs/external-ssd.md", parser.links)
        self.assertIn("https://github.com/nobrainer-tech/nobrainer-tech-flow", parser.links)
        self.assertIn('<html lang="en">', text)
        self.assertNotIn('id="language"', text)
        self.assertNotIn('hreflang="pl"', text)
        self.assertIn('Your model may have more to give', text)
        self.assertIn('Use nobrainer-tech-flow (https://github.com/nobrainer-tech/nobrainer-tech-flow)', text)
        self.assertIn('15</strong><span>configured agent slots', text)
        self.assertIn('1M+</strong><span>GPT-6 API context*', text)
        self.assertIn('your Codex client may expose less', text)
        self.assertIn('assets/codex-flow.svg', text)
        self.assertIn('Codex and nobrainer-tech-flow orchestration tree', (ROOT / 'site/assets/codex-flow.svg').read_text(encoding='utf-8'))
        self.assertIn('LUNA 01', (ROOT / 'site/assets/codex-flow.svg').read_text(encoding='utf-8'))
        self.assertIn('You do not need Colima or Docker', text)
        self.assertIn('ChatGPT icon above the external drive', text)
        for image in ('mac-mini-before.webp', 'mac-mini-after.webp', 'chatgpt-official-icon.webp'):
            self.assertTrue((ROOT / 'site/assets' / image).is_file())
        self.assertIn('https://nobrainer.tech/codex/assets/social-card.png', text)
        self.assertTrue((ROOT / 'site/assets/social-card.png').is_file())
        self.assertIn('See when max is available', text)
        self.assertIn('Bought a Mac mini, then ran out of space?', text)
        self.assertGreater(text.index('<section id="ssd">'), text.index('<section id="start">'))
        self.assertIn("python3 install.py --check", text)
        self.assertIn('id="copy-prompt"', text)
        self.assertIn('id="install-prompt"', text)
        self.assertIn('role="status" aria-live="polite"', text)
        self.assertIn('href="codex://"', text)
        self.assertIn('Paste the copied prompt into a new conversation yourself', text)

    def test_prompt_panel_has_shared_copy_controls_and_live_feedback(self):
        text = (ROOT / "site/index.html").read_text(encoding="utf-8")
        parser = Page()
        parser.feed(text)
        self.assertEqual(len(parser.copy_buttons), 2)
        self.assertIn("copy-prompt-hero", [button.get("id") for button in parser.copy_buttons])
        self.assertIn("copy-prompt", [button.get("id") for button in parser.copy_buttons])
        self.assertTrue(parser.prompt_text)
        self.assertIn("Install NoBrainer Codex from https://github.com/nobrainer-tech/nobrainer-codex.", "".join(parser.prompt_text))
        self.assertIn("codex://", parser.links)
        self.assertEqual(parser.copy_status.get("role"), "status")
        self.assertEqual(parser.copy_status.get("aria-live"), "polite")
        self.assertEqual(parser.copy_status.get("aria-atomic"), "true")


if __name__ == "__main__":
    unittest.main()
