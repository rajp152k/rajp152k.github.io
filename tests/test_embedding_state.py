"""Regression coverage for embedding freshness and public-data boundaries."""

from __future__ import annotations

import sqlite3
import struct
import sys
import tempfile
import unittest
from contextlib import closing
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.archive import prepared_text, visible_blocks
from scripts.embedding_state import (
    check_fresh,
    export_public,
    load_spec,
    open_database,
    pending_posts,
    prepare_posts,
    synchronize,
)


class EmbeddingStateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "state.sqlite"
        self.connection = open_database(self.path, writable=True)
        self.addCleanup(self.connection.close)
        self.spec = load_spec()
        self.posts = [
            (date(2026, 10, 1), "Studying", "studying", "Understanding concepts."),
            (date(2026, 9, 25), "Programming", "programming", "Building programs."),
        ]
        self.prepared = prepare_posts(self.posts, self.spec)
        self.vector = struct.pack("<" + "f" * self.spec["dimension"], 1.0, *([0.0] * (self.spec["dimension"] - 1)))
        synchronize(self.connection, self.prepared, self.spec, {post.slug: self.vector for post in self.prepared})

    def test_date_updates_preserve_embeddings_but_content_and_model_invalidate(self):
        revised_date = [(date(2026, 10, 2), *self.posts[0][1:]), self.posts[1]]
        prepared = prepare_posts(revised_date, self.spec)
        self.assertEqual(pending_posts(self.connection, prepared, self.spec), [])
        with self.assertRaises(ValueError):
            check_fresh(self.connection, prepared, self.spec)
        synchronize(self.connection, prepared, self.spec, {})
        check_fresh(self.connection, prepared, self.spec)
        self.assertEqual(
            self.connection.execute("SELECT embedding FROM posts WHERE slug = ?", ("studying",)).fetchone()[0],
            self.vector,
        )

        revised_body = [(*revised_date[0][:3], "Understanding concepts and their relationships."), self.posts[1]]
        pending = pending_posts(self.connection, prepare_posts(revised_body, self.spec), self.spec)
        self.assertEqual([post.slug for post in pending], ["studying"])

        changed_model = dict(self.spec, revision="1" * 40)
        pending = pending_posts(self.connection, prepare_posts(revised_date, changed_model), changed_model)
        self.assertEqual({post.slug for post in pending}, {"studying", "programming"})

    def test_unchanged_sync_does_not_modify_database(self):
        before = self.path.read_bytes()
        synchronize(self.connection, self.prepared, self.spec, {})
        self.assertEqual(self.path.read_bytes(), before)

    def test_nonfinite_cached_vector_is_not_publishable(self):
        corrupt = struct.pack("<f", float("nan")) + self.vector[4:]
        with self.connection:
            self.connection.execute("UPDATE posts SET embedding = ? WHERE slug = ?", (corrupt, "studying"))
        self.assertEqual([post.slug for post in pending_posts(self.connection, self.prepared, self.spec)], ["studying"])
        with self.assertRaises(ValueError):
            check_fresh(self.connection, self.prepared, self.spec)

    def test_public_export_excludes_local_data_and_deleted_posts(self):
        secret = "PRIVATE_UNUSED_PAGE_CANARY_1924"
        with self.connection:
            self.connection.execute("CREATE TABLE private_notes (body TEXT)")
            self.connection.execute("INSERT INTO private_notes VALUES (?)", (secret,))
        current = self.prepared[:1]
        synchronize(self.connection, current, self.spec, {})
        destination = Path(self.directory.name) / "public.sqlite"
        export_public(self.connection, destination, current, self.spec)
        with closing(sqlite3.connect(destination)) as public:
            self.assertEqual(public.execute("PRAGMA user_version").fetchone()[0], 1)
            self.assertEqual(public.execute("SELECT slug FROM posts").fetchall(), [("studying",)])
            columns = {row[1] for row in public.execute("PRAGMA table_info(posts)")}
            self.assertFalse(columns & {"text", "body", "text_hash", "embedding_key"})
            tables = {row[0] for row in public.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            self.assertNotIn("private_notes", tables)
            self.assertEqual(public.execute("SELECT embedding FROM posts").fetchone()[0], self.vector)
        self.assertNotIn(secret.encode(), destination.read_bytes())

    def test_failed_sync_does_not_partially_update_state(self):
        modified = prepare_posts([(*post[:3], post[3] + " Revised.") for post in self.posts], self.spec)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            synchronize(self.connection, modified, self.spec, {modified[0].slug: self.vector})
        self.assertEqual(self.path.read_bytes(), before)
        check_fresh(self.connection, self.prepared, self.spec)

    def test_empty_archive_removes_deleted_posts(self):
        synchronize(self.connection, [], self.spec, {})
        check_fresh(self.connection, [], self.spec)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0], 0)


class PreparedTextTests(unittest.TestCase):
    def test_visible_blocks_preserve_heading_body_code_and_visible_html_text(self):
        post = (
            date(2026, 10, 1), "Title", "visible",
            "## A **heading**\n\n"
            "Read [the outline](https://example.com/private) and ![diagram](private.png).\n\n"
            "<!-- hidden comment -->\n\n"
            "<script>hidden script</script>\n\n"
            "```python\n  x = \"<value>\"\n  return x\n```\n\n"
            "Math $x_1 + y^2$ and `inline_code`.",
        )
        self.assertEqual(visible_blocks(post), [
            {"kind": "heading", "text": "A heading"},
            {"kind": "body", "text": "Read the outline and diagram."},
            {"kind": "code", "text": '  x = "<value>"\n  return x'},
            {"kind": "body", "text": "Math $x_1 + y^2$ and inline_code."},
        ])

    def test_code_math_and_link_text_survive_without_comments_or_urls(self):
        post = (
            date(2026, 10, 1),
            "Concepts",
            "concepts",
            "Read [the outline](https://example.com/private-target).\n\n"
            "<!-- unpublished comment -->\n\n"
            "```python\ntotal = sum(values)\nreturn total\n```\n\n"
            "The formula is $x^2 + y^2$.",
        )
        text = prepared_text(post)
        self.assertIn("the outline", text)
        self.assertIn("total = sum(values)\nreturn total", text)
        self.assertIn("$x^2 + y^2$", text)
        self.assertNotIn("unpublished comment", text)
        self.assertNotIn("private-target", text)


if __name__ == "__main__":
    unittest.main()
