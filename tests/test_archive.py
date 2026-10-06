"""Archive source identities, YAML metadata, and published artifact boundaries."""

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

    def test_safe_yaml_supports_quoted_titles_structured_metadata_and_utc_dates(self):
        path = self.source(
            'title: "Session: #1"\ndate: 2026-10-02T00:15:00+05:30\nstatus: complete\n'
            'agent: {name: omp, provider: OpenAI, model: null, effort: null}\n'
            'task: |\n  A structured task\nrelated: [/studying/, "https://example.com/result"]\n'
            'contributors:\n  - {name: Reviewer, model: known-model, effort: high, role: review}\n'
            'source_kind: meditations\nprivate_field: {not_published: true}'
        )
        entry = parse(path, "logs")
        self.assertEqual((entry.key, entry.url, entry.title, entry.published_iso, entry.date_label),
                         ("logs/session", "/logs/session/", "Session: #1", "2026-10-01T18:45:00+00:00", "2026-10-01"))
        self.assertEqual(entry.metadata, {
            "status": "complete", "agent": {"name": "omp", "provider": "OpenAI", "model": None, "effort": None},
            "task": "A structured task", "related": ["/studying/", "https://example.com/result"],
            "contributors": [{"name": "Reviewer", "model": "known-model", "effort": "high", "role": "review"}],
        })
        self.assertEqual(prepared_text(entry), "Session: #1\n\nVisible prose.")

    def test_duplicate_keys_and_unsafe_yaml_tags_are_rejected(self):
        invalid = [
            "title: One\ntitle: Two\ndate: 2026-10-01T12:00:00Z\nstatus: complete",
            "title: One\ndate: 2026-10-01T12:00:00Z\nstatus: complete\nagent: {model: one, model: two}",
            "title: !!python/object/apply:builtins.str [unsafe]\ndate: 2026-10-01T12:00:00Z\nstatus: complete",
        ]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                parse(self.source(fields), "logs")

    def test_only_relevant_metadata_is_validated_for_each_source(self):
        meditation = parse(self.source(
            'title: "A meditation"\ndate: "2026-10-01"\nstatus: anything\n'
            'agent: not-a-record\nartifacts: ignore-this\nsource_kind: logs', kind="meditations"), "meditations")
        self.assertEqual((meditation.kind, meditation.published_iso, meditation.metadata, meditation.artifacts),
                         ("meditations", "2026-10-01", {}, ()))
        invalid = [
            "date: 2026-10-01",
            "date: 2026-10-01T12:00:00",
            "date: 2026-10-01T12:00:00Z\nstatus: unknown",
            "date: 2026-10-01T12:00:00Z\nstatus: complete\nagent: not-a-record",
            "date: 2026-10-01T12:00:00Z\nstatus: complete\nagent: {model: 42}",
            "date: 2026-10-01T12:00:00Z\nstatus: complete\nrelated: [javascript:alert(1)]",
            "date: 2026-10-01T12:00:00Z\nstatus: complete\ncontributors: [not-a-record]",
        ]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                parse(self.source("title: Session\n" + fields), "logs")

    def test_read_entries_uses_top_level_sources_and_total_utc_order(self):
        self.source("title: Same\ndate: 2026-10-01\nsource_kind: logs", kind="meditations", slug="same")
        self.source("title: Same\ndate: 2026-10-01T02:00:00+02:00\nstatus: complete\nsource_kind: meditations", slug="same")
        self.source("title: Earlier\ndate: 2026-10-01T00:30:00+01:00\nstatus: complete", slug="earlier")
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
        for kind, slug in [("meditations", "search"), ("meditations", "logs"), ("meditations", "meditations"), ("logs", "artifacts")]:
            fields = "title: Reserved\ndate: 2026-10-01" if kind == "meditations" else "title: Reserved\ndate: 2026-10-01T12:00:00Z\nstatus: complete"
            with self.subTest(kind=kind, slug=slug), self.assertRaises(ValueError):
                parse(self.source(fields, kind=kind, slug=slug), kind)

    def artifact_source(self, record):
        return self.source("title: Session\ndate: 2026-10-01T12:00:00Z\nstatus: complete\nartifacts:\n  - " + record)

    def test_local_artifacts_and_external_https_links_exclude_content_from_text(self):
        artifact = self.logs / "artifacts" / "session" / "result file.txt"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("ARTIFACT_PRIVATE_CONTENT", encoding="utf-8")
        path = self.source(
            "title: Session\ndate: 2026-10-01T12:00:00Z\nstatus: complete\n"
            "task: METADATA_NOT_SEARCHABLE\nartifacts:\n"
            "  - {label: Local result, path: 'artifacts/session/result file.txt'}\n"
            "  - {label: External result, url: 'https://example.com/artifact'}"
        )
        entry = parse(path, "logs")
        self.assertEqual([(item.label, item.url, item.source) for item in entry.artifacts], [
            ("Local result", "/logs/artifacts/session/result%20file.txt", artifact.resolve()),
            ("External result", "https://example.com/artifact", None),
        ])
        self.assertNotIn("artifacts", entry.metadata)
        self.assertEqual(prepared_text(entry), "Session\n\nVisible prose.")

    def test_artifacts_reject_traversal_missing_files_directories_and_ambiguous_urls(self):
        directory = self.logs / "artifacts" / "session" / "directory"
        directory.mkdir(parents=True)
        invalid = [
            "{label: Missing, path: artifacts/session/missing.txt}",
            "{label: Directory, path: artifacts/session/directory}",
            "{label: Traversal, path: artifacts/session/../../../secret.txt}",
            "{label: Absolute, path: /etc/passwd}",
            "{label: Other root, path: ../secret.txt}",
            "{label: Both, path: artifacts/session/file.txt, url: 'https://example.com/file'}",
            "{label: Insecure, url: 'http://example.com/file'}",
            "{label: Relative, url: '/logs/artifacts/session/file.txt'}",
        ]
        for record in invalid:
            with self.subTest(record=record), self.assertRaises(ValueError):
                parse(self.artifact_source(record), "logs")

    def test_artifacts_reject_file_and_directory_symlink_escape(self):
        outside = self.root / "private.txt"
        outside.write_text("PRIVATE", encoding="utf-8")
        directory = self.logs / "artifacts" / "session"
        directory.mkdir(parents=True)
        (directory / "leak.txt").symlink_to(outside)
        with self.assertRaises(ValueError):
            parse(self.artifact_source("{label: Leak, path: artifacts/session/leak.txt}"), "logs")
        (directory / "outside").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            parse(self.artifact_source("{label: Leak, path: artifacts/session/outside/private.txt}"), "logs")

    def test_artifacts_root_symlink_must_not_escape_logs(self):
        outside = self.root / "outside" / "session"
        outside.mkdir(parents=True)
        (outside / "leak.txt").write_text("PRIVATE", encoding="utf-8")
        (self.logs / "artifacts").symlink_to(outside.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            parse(self.artifact_source("{label: Leak, path: artifacts/session/leak.txt}"), "logs")


if __name__ == "__main__":
    unittest.main()
