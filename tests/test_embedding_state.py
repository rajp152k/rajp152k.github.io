"""Regression coverage for embedding freshness and public-data boundaries."""

from __future__ import annotations

import sqlite3
import struct
import sys
import tempfile
import unittest
from contextlib import closing
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.archive import Artifact, Entry, prepared_text, visible_blocks
from scripts.embedding_state import (
    check_fresh,
    export_public,
    load_spec,
    open_database,
    pending_entries,
    prepare_entries,
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
        self.entries = [
            Entry("meditations", "studying", "Studying", date(2026, 10, 1), "Understanding concepts."),
            Entry("meditations", "programming", "Programming", date(2026, 9, 25), "Building programs."),
        ]
        self.prepared = prepare_entries(self.entries, self.spec)
        self.vector = struct.pack("<" + "f" * self.spec["dimension"], 1.0, *([0.0] * (self.spec["dimension"] - 1)))
        synchronize(self.connection, self.prepared, self.spec, {entry.key: self.vector for entry in self.prepared})

    def test_date_updates_preserve_embeddings_but_content_and_model_invalidate(self):
        revised_date = [replace(self.entries[0], published=date(2026, 10, 2)), self.entries[1]]
        prepared = prepare_entries(revised_date, self.spec)
        self.assertEqual(pending_entries(self.connection, prepared, self.spec), [])
        with self.assertRaises(ValueError):
            check_fresh(self.connection, prepared, self.spec)
        synchronize(self.connection, prepared, self.spec, {})
        check_fresh(self.connection, prepared, self.spec)
        self.assertEqual(
            self.connection.execute("SELECT embedding FROM posts WHERE slug = ?", ("meditations/studying",)).fetchone()[0],
            self.vector,
        )

        revised_body = [replace(revised_date[0], body="Understanding concepts and their relationships."), self.entries[1]]
        pending = pending_entries(self.connection, prepare_entries(revised_body, self.spec), self.spec)
        self.assertEqual([entry.key for entry in pending], ["meditations/studying"])

        changed_model = dict(self.spec, revision="1" * 40)
        pending = pending_entries(self.connection, prepare_entries(revised_date, changed_model), changed_model)
        self.assertEqual({entry.key for entry in pending}, {"meditations/studying", "meditations/programming"})

    def test_log_metadata_and_artifacts_do_not_invalidate_vectors(self):
        log = Entry("logs", "session", "Session", datetime(2026, 10, 1, tzinfo=timezone.utc), "Understanding concepts.",
                    {"status": "in-progress", "agent": {"model": None, "effort": None}})
        prepared = prepare_entries([log], self.spec)
        synchronize(self.connection, prepared, self.spec, {log.key: self.vector})
        revised = replace(log, published=datetime(2026, 10, 2, 12, tzinfo=timezone.utc),
                          metadata={"status": "complete", "agent": {"model": "known-model", "effort": "high"}, "task": "Metadata only"},
                          artifacts=(Artifact("Result", "https://example.com/result", None),))
        updated = prepare_entries([revised], self.spec)
        self.assertEqual(pending_entries(self.connection, updated, self.spec), [])
        synchronize(self.connection, updated, self.spec, {})
        check_fresh(self.connection, updated, self.spec)
        self.assertEqual(self.connection.execute("SELECT published_date, embedding FROM posts").fetchone()[:],
                         ("2026-10-02T12:00:00+00:00", self.vector))

    def test_legacy_bare_slug_migration_reuses_every_vector_byte(self):
        with self.connection:
            for entry in self.prepared:
                self.connection.execute("UPDATE posts SET slug = ? WHERE slug = ?", (entry.slug, entry.key))
        self.assertEqual(pending_entries(self.connection, self.prepared, self.spec), [])
        with self.assertRaises(ValueError):
            check_fresh(self.connection, self.prepared, self.spec)
        synchronize(self.connection, self.prepared, self.spec, {})
        check_fresh(self.connection, self.prepared, self.spec)
        self.assertEqual({row[0]: row[1] for row in self.connection.execute("SELECT slug, embedding FROM posts")},
                         {entry.key: self.vector for entry in self.prepared})

    def test_unchanged_sync_does_not_modify_database(self):
        before = self.path.read_bytes()
        synchronize(self.connection, self.prepared, self.spec, {})
        self.assertEqual(self.path.read_bytes(), before)

    def test_nonfinite_cached_vector_is_not_publishable(self):
        corrupt = struct.pack("<f", float("nan")) + self.vector[4:]
        with self.connection:
            self.connection.execute("UPDATE posts SET embedding = ? WHERE slug = ?", (corrupt, "meditations/studying"))
        self.assertEqual([entry.key for entry in pending_entries(self.connection, self.prepared, self.spec)], ["meditations/studying"])
        with self.assertRaises(ValueError):
            check_fresh(self.connection, self.prepared, self.spec)

    def test_public_export_distinguishes_same_slug_sources_and_excludes_local_deleted_data(self):
        secret = "PRIVATE_UNUSED_PAGE_CANARY_1924"
        with self.connection:
            self.connection.execute("CREATE TABLE private_notes (body TEXT)")
            self.connection.execute("INSERT INTO private_notes VALUES (?)", (secret,))
        log = Entry("logs", "studying", "Study session", datetime(2026, 10, 2, 12, tzinfo=timezone.utc), "A different session.",
                    {"status": "complete"})
        current = prepare_entries([self.entries[0], log], self.spec)
        log_vector = struct.pack("<" + "f" * self.spec["dimension"], 0.0, 1.0, *([0.0] * (self.spec["dimension"] - 2)))
        synchronize(self.connection, current, self.spec, {log.key: log_vector})
        check_fresh(self.connection, current, self.spec)
        destination = Path(self.directory.name) / "public.sqlite"
        export_public(self.connection, destination, current, self.spec)
        with closing(sqlite3.connect(destination)) as public:
            self.assertEqual(public.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertEqual(public.execute("SELECT entry_key, kind, slug, published_date, url, embedding FROM posts ORDER BY entry_key").fetchall(), [
                ("logs/studying", "logs", "studying", "2026-10-02T12:00:00+00:00", "/logs/studying/", log_vector),
                ("meditations/studying", "meditations", "studying", "2026-10-01", "/studying/", self.vector),
            ])
            columns = {row[1] for row in public.execute("PRAGMA table_info(posts)")}
            self.assertFalse(columns & {"text", "body", "text_hash", "embedding_key"})
            tables = {row[0] for row in public.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            self.assertNotIn("private_notes", tables)
        self.assertNotIn(secret.encode(), destination.read_bytes())

    def test_prepared_dates_require_source_specific_canonical_formats(self):
        log = Entry("logs", "session", "Session", datetime(2026, 10, 1, tzinfo=timezone.utc), "Session prose.")
        prepared_log = prepare_entries([log], self.spec)[0]
        invalid = [
            replace(self.prepared[0], published_date="2026-10-01T00:00:00+00:00"),
            replace(prepared_log, published_date="2026-10-01"),
            replace(prepared_log, published_date="2026-10-01T00:00:00"),
            replace(prepared_log, published_date="2026-10-01T01:00:00+01:00"),
        ]
        for entry in invalid:
            with self.subTest(date=entry.published_date, kind=entry.kind), self.assertRaises(ValueError):
                pending_entries(self.connection, [entry], self.spec)

    def test_failed_sync_does_not_partially_update_state(self):
        modified = prepare_entries([replace(entry, body=entry.body + " Revised.") for entry in self.entries], self.spec)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            synchronize(self.connection, modified, self.spec, {modified[0].key: self.vector})
        self.assertEqual(self.path.read_bytes(), before)
        check_fresh(self.connection, self.prepared, self.spec)

    def test_empty_archive_removes_deleted_entries(self):
        synchronize(self.connection, [], self.spec, {})
        check_fresh(self.connection, [], self.spec)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0], 0)


class PreparedTextTests(unittest.TestCase):
    def test_visible_blocks_preserve_heading_body_code_and_visible_html_text(self):
        entry = Entry(
            "meditations", "visible", "Title", date(2026, 10, 1),
            "## A **heading**\n\n"
            "Read [the outline](https://example.com/private) and ![diagram](private.png).\n\n"
            "<!-- hidden comment -->\n\n"
            "<script>hidden script</script>\n\n"
            "```python\n  x = \"<value>\"\n  return x\n```\n\n"
            "Math $x_1 + y^2$ and `inline_code`.",
        )
        self.assertEqual(visible_blocks(entry), [
            {"kind": "heading", "text": "A heading"},
            {"kind": "body", "text": "Read the outline and diagram."},
            {"kind": "code", "text": '  x = "<value>"\n  return x'},
            {"kind": "body", "text": "Math $x_1 + y^2$ and inline_code."},
        ])

    def test_code_math_and_link_text_survive_without_comments_or_urls(self):
        entry = Entry(
            "meditations", "concepts", "Concepts", date(2026, 10, 1),
            "Read [the outline](https://example.com/private-target).\n\n"
            "<!-- unpublished comment -->\n\n"
            "```python\ntotal = sum(values)\nreturn total\n```\n\n"
            "The formula is $x^2 + y^2$.",
        )
        text = prepared_text(entry)
        self.assertIn("the outline", text)
        self.assertIn("total = sum(values)\nreturn total", text)
        self.assertIn("$x^2 + y^2$", text)
        self.assertNotIn("unpublished comment", text)
        self.assertNotIn("private-target", text)


if __name__ == "__main__":
    unittest.main()
