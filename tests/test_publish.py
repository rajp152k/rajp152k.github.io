"""Term-page escaping and failed-build preview protection."""
from datetime import date
from html import escape
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import publish
from archive import Entry
from term_pages import article_panel, term_card
from terms import Mention, Source, Term


class TermPublishingTests(unittest.TestCase):
    def test_editorial_text_is_escaped_in_cards_and_templates(self):
        payload = '</template><script>alert("x")</script>&'
        entry = Entry("meditations", "example", payload, date(2026, 1, 1), payload)
        term = Term("example", payload, (), payload, entry.key, (Source(entry.key, payload),))
        mention = Mention(term.id, entry.key, payload, entry.url, entry.date_label, payload)
        entries = {entry.key: entry}
        for html in (term_card(term, entries, [mention]), article_panel([term], entries, [mention], "other")):
            self.assertNotIn(payload, html)
            self.assertIn(escape(payload), html)
            self.assertIn('href="/example/#term-example"', html)
        panel = article_panel([term], entries, [mention], entry.key)
        self.assertEqual(panel.count("</template>"), 1)
        self.assertNotIn('href="/example/#term-example"', panel)
        self.assertIn('href="/terms/example/"', panel)

    def test_posts_without_terms_have_no_panel(self):
        self.assertEqual(article_panel([], {}, [], "example"), "")

    def test_invalid_registry_preserves_previous_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory) / "site"
            site.mkdir()
            preview = site / "index.html"
            preview.write_text("Previous preview", encoding="utf-8")
            with patch.object(publish, "SITE", site), patch.object(publish, "render_account_menu", return_value=""), \
                    patch("terms.load_terms", side_effect=ValueError("Stale source")), \
                    patch.object(publish, "node_output") as node:
                with self.assertRaisesRegex(ValueError, "Stale source"):
                    publish.build_site([], None, [], {}, None)
                node.assert_not_called()
            self.assertEqual(preview.read_text(encoding="utf-8"), "Previous preview")


if __name__ == "__main__":
    unittest.main()
