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

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href"))
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


class SiteTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
