"""Definition links and approved entry scopes in generated term HTML."""
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from archive import Entry
from term_pages import article_panel, term_card, terms_index
from terms import Registry, Source, Term, collect_mentions, transform_html


class TermPageTests(unittest.TestCase):
    def setUp(self):
        self.entry = Entry("logs", "example", "Example", datetime(2026, 1, 1, tzinfo=timezone.utc), "Lisp image. Lisp image.")
        self.term = Term("lisp-image", "Lisp image", (),
                         '<b>State</b>. See [A & B](https://example.org/doc?a=1&b=2).',
                         self.entry.key, (Source(self.entry.key, "Lisp image."),),
                         entries=(self.entry.key,))

    def test_public_definition_references(self):
        entries = {self.entry.key: self.entry}
        for rendered in (term_card(self.term, entries, ()),
                         article_panel((self.term,), entries, (), self.entry.key),
                         terms_index((self.term,))):
            self.assertIn('<a href="https://example.org/doc?a=1&amp;b=2">A &amp; B</a>', rendered)
            self.assertIn('&lt;b&gt;State&lt;/b&gt;', rendered)
            self.assertNotIn('<b>State</b>', rendered)
        unsafe = replace(self.term, definition='[bad](javascript:alert(1)) [local](/path)')
        rendered = term_card(unsafe, entries, ())
        self.assertNotIn('href="javascript:', rendered)
        self.assertNotIn('href="/path"', rendered)

    def test_scope_in_annotations_and_mentions(self):
        registry = Registry((self.term,))
        html = '<h1>Lisp image</h1><p>Lisp image. Lisp image.</p>'
        accepted = transform_html(html, registry, entry_key=self.entry.key)
        self.assertEqual(len(accepted.mentions), 1)
        self.assertEqual(accepted.html.count('id="term-lisp-image"'), 1)
        for key in (None, "logs/other", "meditations/example"):
            self.assertEqual(transform_html(html, registry, entry_key=key).html, html)
        entries = [self.entry, replace(self.entry, slug="other"),
                   replace(self.entry, kind="meditations", published=date(2026, 1, 1))]
        mentions = collect_mentions(entries, registry)
        self.assertEqual([(m.term_id, m.entry_key) for m in mentions],
                         [(self.term.id, self.entry.key)])
