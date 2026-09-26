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
        self.assertIn('If your Mac mini is running out of space', text)
        self.assertIn('nobrainer-tech-flow (https://github.com/nobrainer-tech/nobrainer-tech-flow)', text)
        self.assertIn('assets/codex-flow.svg', text)
        self.assertIn('Codex and nobrainer-tech-flow workflow', (ROOT / 'site/assets/codex-flow.svg').read_text(encoding='utf-8'))
        self.assertIn('https://nobrainer.tech/codex/assets/social-card.png', text)
        self.assertTrue((ROOT / 'site/assets/social-card.png').is_file())
        self.assertIn('A configured 872k window cannot enlarge a smaller model', text)
        self.assertIn("python3 install.py --check", text)


if __name__ == "__main__":
    unittest.main()
