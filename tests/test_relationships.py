"""Directed authored references and independent full-vector cosine neighbors."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.archive import Entry
from scripts.relationships import annotate_references, collect_references, nearest_posts


def meditation(slug):
    return Entry("meditations", slug, slug, date(2026, 1, 1), "Shared term, no inferred link.")


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.first = meditation("first")
        self.second = meditation("second")
        self.encoded = meditation("space & café")
        self.log = Entry("logs", "experiment", "Experiment", datetime(2026, 1, 2, tzinfo=timezone.utc), "")
        self.entries = [self.first, self.second, self.encoded, self.log]

    def collect(self, html):
        return collect_references(self.entries, {self.first.key: html})

    def test_directed_reference_with_plain_text_paragraph_and_fragment(self):
        references = self.collect('<p>Read <a href="/second/#evidence">this <em>result</em></a> &amp; compare.</p>')
        self.assertEqual(references, [{
            "source": self.first.key,
            "target": self.second.key,
            "url": "/second/#evidence",
            "source_url": "/first/#post-reference-1",
            "excerpt": "Read this result & compare.",
        }])

    def test_relative_same_site_and_encoded_urls(self):
        html = ('<p><a href="../second/?a=1&amp;b=2#part">Second</a></p>'
                '<p><a href="https://yetanotherraj.com/space%20%26%20caf%C3%A9/#proof">Encoded</a></p>'
                '<p><a href="../logs/experiment/">Experiment</a></p>')
        references = self.collect(html)
        self.assertEqual([edge["target"] for edge in references], [
            self.second.key, self.encoded.key, self.log.key,
        ])
        self.assertEqual(references[0]["url"], "/second/?a=1&b=2#part")
        self.assertEqual(references[1]["url"], self.encoded.url + "#proof")
        backwards = collect_references(self.entries, {
            self.log.key: '<p><a href="../../first/">First</a></p>',
        })
        self.assertEqual(backwards[0]["target"], self.first.key)

    def test_excludes_self_external_terms_and_unlinked_shared_terms(self):
        self.assertEqual(self.collect('''
            <p>Shared term, second, experiment.</p>
            <a href="#local">Self fragment</a><a href="/first/">Self</a>
            <a href="https://other.example/second/">External</a>
            <a href="//other.example/second/">External protocol-relative</a>
            <a href="/terms/second/">Term</a><a href="/missing/">Missing</a>
            <a href="mailto:person@example.com">Mail</a>
            <a href="javascript:alert(1)">Script</a>
        '''), [])
        self.assertEqual(collect_references(self.entries, {}), [])
        self.assertEqual(collect_references([], {}), [])

    def test_code_pre_nav_and_escaped_anchor_are_not_references(self):
        self.assertEqual(self.collect('''
            <pre><code><a href="/second/">Example</a></code></pre>
            <code><a href="/second/">Inline code</a></code>
            <nav><span><a href="/second/">Navigation</a></span></nav>
            <p>&lt;a href="/second/"&gt;Escaped example&lt;/a&gt;</p>
            <script>const example = '<a href="/second/">script</a>';</script>
        '''), [])

    def test_repeated_target_collapses_to_first_authored_passage(self):
        references = self.collect('''<nav><a href="/second/">Not authored</a></nav>
            <p>First <a href="/second/#one">passage</a>.</p>
            <p>Other <a href="/second/#two">passage</a>.</p>''')
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0]["url"], "/second/#one")
        self.assertEqual(references[0]["excerpt"], "First passage.")

    def test_long_excerpt_includes_reference_near_end(self):
        references = self.collect('<p>' + 'Context ' * 120 + '<a href="/second/">Specific evidence</a> here.</p>')
        self.assertIn("Specific evidence", references[0]["excerpt"])
        self.assertLessEqual(len(references[0]["excerpt"]), 322)

    def test_annotation_preserves_raw_html_and_avoids_existing_ids(self):
        html = ("<h2 id='post-reference-1'>Evidence</h2>\n"
                "<nav><a href='/second/'>Navigation</a></nav>\n"
                "<p>Read <a\n href='../second/#part' data-note='&amp;'>this</a>.</p>\n"
                "<p><a href='/second/#again'>Repeated</a></p>\n"
                "<p><a id='saved-anchor' href='/logs/experiment/'>Experiment</a></p>")
        rendered = {self.first.key: html, self.second.key: "<p>Unchanged.</p>"}
        references = collect_references(self.entries, rendered)
        self.assertEqual([edge["source_url"] for edge in references], [
            "/first/#post-reference-2", "/first/#saved-anchor",
        ])
        annotated = annotate_references(rendered, references)
        self.assertIsNot(annotated, rendered)
        self.assertEqual(rendered[self.first.key], html)
        self.assertEqual(annotated[self.second.key], rendered[self.second.key])
        self.assertEqual(annotated[self.first.key], html.replace(
            "data-note='&amp;'>", "data-note='&amp;' id=\"post-reference-2\">",
        ))
        self.assertEqual(collect_references(self.entries, annotated), references)
        self.assertEqual(annotate_references(annotated, references), annotated)

    def test_ids_restart_per_source_and_links_are_directed(self):
        rendered = {
            self.first.key: '<p><a href="/second/">Second</a></p>',
            self.second.key: '<p><a href="/first/">First</a></p>',
        }
        references = collect_references(self.entries, rendered)
        self.assertEqual([edge["source_url"] for edge in references], [
            "/first/#post-reference-1", "/second/#post-reference-1",
        ])
        annotated = annotate_references(rendered, references)
        for html in annotated.values():
            self.assertIn('id="post-reference-1"', html)


class NearestPostTests(unittest.TestCase):
    def connection(self, vectors):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.execute("CREATE TABLE posts (slug TEXT PRIMARY KEY, embedding BLOB NOT NULL)")
        connection.executemany("INSERT INTO posts VALUES (?, ?)", [
            (key, np.asarray(vector, dtype="<f4").tobytes()) for key, vector in vectors.items()
        ])
        return connection

    def test_full_vector_cosine_and_deterministic_ties(self):
        connection = self.connection({
            "meditations/source": [1, 0, 1],
            "meditations/z": [2, 0, 2],
            "logs/a": [3, 0, 3],
            "meditations/partial": [1, 0, 0],
            "meditations/opposite": [-1, 0, -1],
        })
        result = nearest_posts(connection, 3)
        neighbors = result["meditations/source"]
        self.assertEqual([item["key"] for item in neighbors], [
            "logs/a", "meditations/z", "meditations/partial",
        ])
        self.assertAlmostEqual(neighbors[0]["score"], 1.0)
        self.assertAlmostEqual(neighbors[2]["score"], 1 / np.sqrt(2))
        self.assertTrue(connection.in_transaction)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0], 5)
        all_neighbors = nearest_posts(connection, 3, limit=10)["meditations/source"]
        self.assertAlmostEqual(all_neighbors[-1]["score"], -1.0)
        self.assertNotIn("meditations/source", [item["key"] for item in all_neighbors])

    def test_empty_single_and_zero_vectors(self):
        self.assertEqual(nearest_posts(self.connection({}), 3), {})
        self.assertEqual(nearest_posts(self.connection({"only": [1, 2, 3]}), 3), {"only": []})
        result = nearest_posts(self.connection({"zero": [0, 0], "a": [1, 0], "b": [0, 1]}), 2)
        self.assertEqual(result["zero"], [])
        self.assertEqual(result["a"], [{"key": "b", "score": 0.0}])
        self.assertEqual(result["b"], [{"key": "a", "score": 0.0}])

    def test_tiny_nonzero_vectors_and_limits(self):
        connection = self.connection({"a": [1e-35, 0], "b": [2e-35, 0]})
        self.assertAlmostEqual(nearest_posts(connection, 2)["a"][0]["score"], 1.0)
        self.assertEqual(nearest_posts(connection, 2, limit=0), {"a": [], "b": []})
        with self.assertRaises(ValueError):
            nearest_posts(connection, 0)
        with self.assertRaises(ValueError):
            nearest_posts(connection, 2, limit=-1)


if __name__ == "__main__":
    unittest.main()
