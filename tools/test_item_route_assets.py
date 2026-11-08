"""The route gate validates static HTML destinations, not only Markdown pages."""
import tempfile
import unittest
from pathlib import Path
from check_item_routes import audit


class StaticAssets(unittest.TestCase):
    def test_static_html_exists_and_has_requested_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs/assets').mkdir(parents=True)
            (root / 'docs/index.md').write_text('[Demo](assets/demo.html#chart)')
            (root / 'docs/assets/demo.html').write_text('<main id="chart">Demo</main>')
            (root / 'mkdocs.yml').write_text('nav: []\nmarkdown_extensions: [toc]\n')
            records = {'original_urls': {}, 'original_fragments': {}, 'canonical_pages': [], 'moves': {}, 'fragment_overrides': {}}
            errors, _ = audit(root, records)
            self.assertFalse([e for e in errors if 'documentation URL' in e or 'fragment' in e], errors)
            (root / 'docs/assets/demo.html').write_text('<main>Demo</main>')
            errors, _ = audit(root, records)
            self.assertTrue(any('missing target fragment' in e for e in errors), errors)
            (root / 'docs/assets/demo.html').unlink()
            errors, _ = audit(root, records)
            self.assertTrue(any('unresolved documentation URL' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
