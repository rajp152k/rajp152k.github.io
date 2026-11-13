"""Term-page escaping and failed-build preview protection."""
from datetime import date, datetime, timezone
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
            self.assertEqual(html.count('href="/example/"'), 1)
        panel = article_panel([term], entries, [mention], entry.key)
        self.assertEqual(panel.count("</template>"), 1)
        self.assertNotIn('href="/example/#term-example"', panel)
        self.assertIn('href="/terms/example/"', panel)

    def test_sources_group_quotes_and_do_not_repeat_reading_links(self):
        entries = {
            name: Entry("logs", name, name, datetime(2026, 1, 1, tzinfo=timezone.utc), "")
            for name in ("intro", "source", "other")
        }
        term = Term("example", "Example", (), "Definition", "intro", (
            Source("source", "First quote."), Source("intro", "Intro quote."),
            Source("source", "Second quote."),
        ))
        mentions = [Mention(term.id, key, item.title, item.url, item.date_label, "Mention.")
                    for key, item in entries.items()]
        for current in ("", "intro", "other"):
            with self.subTest(current=current):
                html = term_card(term, entries, iter(mentions), current=current)
                self.assertEqual(html.count('href="/logs/intro/"'), 1)
                self.assertEqual(html.count('href="/logs/source/"'), 1)
                self.assertNotIn('href="/logs/intro/#term-example"', html)
                self.assertNotIn('href="/logs/source/#term-example"', html)
                self.assertEqual(html.count('href="/logs/other/#term-example"'), int(current != "other"))
                source_row = html.split('href="/logs/source/"')[1].split('</li>')[0]
                self.assertIn("First quote.", source_row)
                self.assertIn("Second quote.", source_row)
                self.assertIn("Intro quote.", html)

    def test_separate_introduction_is_not_repeated_as_a_mention(self):
        intro = Entry("logs", "intro", "Introduction", datetime(2026, 1, 1, tzinfo=timezone.utc), "")
        source = Entry("logs", "source", "Source", datetime(2026, 1, 2, tzinfo=timezone.utc), "")
        term = Term("example", "Example", (), "Definition", intro.key, (Source(source.key, "Evidence."),))
        mention = Mention(term.id, intro.key, intro.title, intro.url, intro.date_label, "Mention.")
        html = term_card(term, {item.key: item for item in (intro, source)}, [mention])
        self.assertEqual(html.count(f'href="{intro.url}"'), 1)
        self.assertEqual(html.count(f'href="{source.url}"'), 1)
        self.assertNotIn(f'href="{mention.url}"', html)

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
