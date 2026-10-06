"""Archive source identities, title/date parsing, and chronological ordering."""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.archive import Entry, display_ids, parse, prepared_text, read_entries


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.meditations = self.root / "meditations"
        self.logs = self.root / "logs"
        self.meditations.mkdir()
        self.logs.mkdir()

    def source(self, fields, *, kind="logs", slug="session", body="Visible prose."):
        path = (self.logs if kind == "logs" else self.meditations) / f"{slug}.md"
        path.write_text(f"---\n{fields}\n---\n\n{body}\n", encoding="utf-8")
        return path

    def test_title_and_date_only_logs_support_quoted_titles_and_utc_dates(self):
        path = self.source(
            'title: "Session: #1"\ndate: 2026-10-02T00:15:00+05:30'
        )
        entry = parse(path, "logs")
        self.assertEqual((entry.key, entry.url, entry.title, entry.published_iso, entry.date_label),
                         ("logs/session", "/logs/session/", "Session: #1", "2026-10-01T18:45:00+00:00", "2026-10-01"))
        self.assertEqual(prepared_text(entry), "Session: #1\n\nVisible prose.")

    def test_duplicate_keys_and_unsafe_yaml_tags_are_rejected(self):
        invalid = [
            "title: One\ntitle: Two\ndate: 2026-10-01T12:00:00Z",
            "title: !!python/object/apply:builtins.str [unsafe]\ndate: 2026-10-01T12:00:00Z",
        ]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                parse(self.source(fields), "logs")

    def test_publication_dates_are_validated_for_each_source(self):
        meditation = parse(self.source(
            'title: "A meditation"\ndate: "2026-10-01"', kind="meditations"), "meditations")
        self.assertEqual((meditation.kind, meditation.published_iso), ("meditations", "2026-10-01"))
        invalid = ["date: 2026-10-01", "date: 2026-10-01T12:00:00", "date: 42", "date: invalid"]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                parse(self.source("title: Session\n" + fields), "logs")

    def test_read_entries_uses_top_level_sources_and_total_utc_order(self):
        self.source("title: Same\ndate: 2026-10-01", kind="meditations", slug="same")
        self.source("title: Same\ndate: 2026-10-01T02:00:00+02:00", slug="same")
        self.source("title: Earlier\ndate: 2026-10-01T00:30:00+01:00", slug="earlier")
        for directory in (self.meditations, self.logs):
            (directory / "nested").mkdir()
            (directory / "nested" / "ignored.md").write_text("not front matter", encoding="utf-8")
        entries = read_entries(self.meditations, self.logs)
        self.assertEqual([entry.key for entry in entries], ["meditations/same", "logs/same", "logs/earlier"])
        self.assertEqual(display_ids(entries), {"logs/earlier": "lx0", "logs/same": "lx1", "meditations/same": "mx0"})
        self.assertEqual([entry.key for entry in read_entries(self.meditations, self.root / "missing")], ["meditations/same"])
        with self.assertRaises(ValueError):
            read_entries(self.root / "missing", self.logs)

    def test_display_codes_have_independent_hex_counters(self):
        base = date(2026, 9, 1)
        meditations = [Entry("meditations", f"m{i}", f"M{i}", base + timedelta(days=i), "Body") for i in range(18)]
        logs = [Entry("logs", f"l{i}", f"L{i}", datetime(2026, 9, 2 + i, tzinfo=timezone.utc), "Body") for i in range(3)]
        codes = display_ids(list(reversed(meditations + logs)))
        self.assertEqual((codes["meditations/m0"], codes["meditations/m15"], codes["meditations/m16"], codes["logs/l2"]),
                         ("mx0", "mxf", "mx10", "lx2"))

    def test_reserved_native_routes_are_rejected_before_preparation(self):
        for kind, slug in [("meditations", "search"), ("meditations", "logs"), ("meditations", "meditations")]:
            fields = "title: Reserved\ndate: 2026-10-01"
            with self.subTest(kind=kind, slug=slug), self.assertRaises(ValueError):
                parse(self.source(fields, kind=kind, slug=slug), kind)



if __name__ == "__main__":
    unittest.main()
