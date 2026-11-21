"""Snapshot and import checks independent of the optional Potato installation."""

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import review


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "logs").mkdir()
        self.post = self.root / "logs/probe.md"
        self.post.write_text("A full exact post.\n")
        self.record = self.root / "record.md"
        self.meta = {"kind": "post-review", "entry": "logs/probe", "cycle": 1,
                     "post_sha256": review.digest(self.post.read_bytes()),
                     "terms": [{"id": "T1", "revision": 2, "state": "proposed"}]}
        self.write_record()

    def write_record(self):
        self.record.write_text("---\n" + yaml.safe_dump(self.meta) + "---\n# T1\nDefinition and evidence.\n")

    def prepare(self):
        return review.prepare(self.root, ["record.md"])

    def save(self, session):
        user = session / "annotation_output/raj"
        user.mkdir(parents=True, exist_ok=True)
        review.dump(user / "user_state.json", {"user_id": "raj", "instance_id_to_label_to_value": {
            "logs/probe:cycle-1:T1:r2": [[{"schema": "decision", "name": "approve"}, True],
                                        [{"schema": "comment", "name": "text_box"}, "Exact details"]]}})

    def test_stable_ids_and_complete_snapshots(self):
        session = self.prepare()
        self.assertEqual(session, self.prepare())
        manifest = json.loads((session / "manifest.json").read_text())
        self.assertEqual(manifest["items"][0]["id"], "logs/probe:cycle-1:T1:r2")
        self.assertEqual(manifest["sources"]["logs/probe.md"]["text"], self.post.read_text())
        self.meta["terms"][0]["revision"] = 3
        self.write_record()
        self.assertNotEqual(session, self.prepare())

    def test_stale_review_and_meditation_terms_refused(self):
        self.post.write_text("Changed")
        with self.assertRaisesRegex(ValueError, "stale"):
            self.prepare()
        (self.root / "meditations").mkdir()
        (self.root / "meditations/probe.md").write_bytes(self.post.read_bytes())
        self.meta.update(entry="meditations/probe", post_sha256=review.digest(self.post.read_bytes()))
        self.write_record()
        with self.assertRaisesRegex(ValueError, "no terms"):
            self.prepare()

    def test_import_is_idempotent_and_flags_changed_sources(self):
        session = self.prepare()
        self.save(session)
        self.post.write_text("New post")
        before = self.record.read_bytes()
        output = review.import_session(self.root, session)
        self.assertEqual(output, review.import_session(self.root, session))
        report = json.loads(output.read_text())
        self.assertEqual(report["changed_sources"], ["logs/probe.md"])
        self.assertEqual(report["responses"][0]["decision"], "approve")
        self.assertEqual(report["responses"][0]["comment"], "Exact details")
        self.assertEqual(before, self.record.read_bytes())
        self.assertEqual(report["manifest"]["sources"]["logs/probe.md"]["text"], "A full exact post.\n")
        review.clean(self.root, session)
        self.assertTrue(output.exists())
        self.assertFalse(session.exists())

    def test_cleanup_refuses_unimported_or_new_responses(self):
        session = self.prepare()
        with self.assertRaises(FileNotFoundError):
            review.clean(self.root, session)
        self.save(session)
        review.import_session(self.root, session)
        state = session / "annotation_output/raj/user_state.json"
        state.write_text('{"new":"response"}')
        with self.assertRaisesRegex(ValueError, "New responses"):
            review.clean(self.root, session)
        self.assertTrue(session.exists())

    def test_memos_replies_and_issue_state_are_preserved(self):
        session = self.prepare()
        with sqlite3.connect(session / "project.sqlite") as db:
            db.executescript("CREATE TABLE memos(id TEXT, instance_id TEXT, anchor TEXT, body TEXT);"
                             "CREATE TABLE memo_threads(memo_id TEXT, parent_id TEXT, status TEXT);")
            db.execute("INSERT INTO memos VALUES(?, ?, ?, ?)", ("m1", "logs/probe:cycle-1:log", '{"start":2,"end":8}', "Question"))
            db.execute("INSERT INTO memos VALUES(?, ?, ?, ?)", ("m2", "logs/probe:cycle-1:log", None, "Reply"))
            db.execute("INSERT INTO memo_threads VALUES('m1', NULL, 'open')")
            db.execute("INSERT INTO memo_threads VALUES('m2', 'm1', NULL)")
        report = json.loads(review.import_session(self.root, session).read_text())
        self.assertEqual(len(report["evidence"]["memos"]), 2)
        self.assertEqual(report["evidence"]["memo_threads"][1]["parent_id"], "m1")
        self.assertEqual(report["evidence"]["memo_threads"][0]["status"], "open")

    def test_named_evidence_is_frozen_and_shown(self):
        (self.root / "evidence.md").write_text("Exact source passage")
        session = review.prepare(self.root, ["record.md"], ["evidence.md"])
        manifest = json.loads((session / "manifest.json").read_text())
        self.assertEqual(manifest["sources"]["evidence.md"]["text"], "Exact source passage")
        self.assertIn("Exact source passage", manifest["items"][0]["text"])

    def test_paths_cannot_escape(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            review.inside(self.root, "../outside")


if __name__ == "__main__":
    unittest.main()
