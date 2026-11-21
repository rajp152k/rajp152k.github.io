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
        self.root = Path(self.temp.name).resolve()
        (self.root / "logs").mkdir()
        self.post = self.root / "logs/probe.md"
        self.post.write_text("A full exact post.\n")
        self.record = self.root / "record.md"
        self.meta = {"kind": "post-review", "entry": "logs/probe", "cycle": 1,
                     "post_sha256": review.digest(self.post.read_bytes()),
                     "terms": [{"id": "T1", "revision": 2, "state": "proposed", "card": {
                         "name": "Probe", "definition": "A test term.", "aliases": [],
                         "passage": "A full exact post.", "introduction": "This log.",
                         "use_scope": "This log only."}}]}
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

    def test_card_escapes_candidate_and_evidence(self):
        self.meta["terms"][0]["card"]["name"] = '<script>alert("x")</script>'
        self.write_record()
        session = review.prepare(self.root, ["record.md"], terms_only=True)
        card = json.loads((session / "data.json").read_text())[0]["card_html"]
        self.assertNotIn("<script>", card)
        self.assertIn("&lt;script&gt;", card)
        self.assertIn("<details><summary>Full post snapshot</summary>", card)
        self.assertNotIn("<details open", card)
        self.assertIn("A full exact post.", card)
        self.assertEqual(len(json.loads((session / "manifest.json").read_text())["items"]), 1)
        config = yaml.safe_load((session / "config.yaml").read_text())
        self.assertEqual(config["instance_display"]["fields"], [{"key": "card_html", "type": "html"}])

    def test_definition_references_are_clickable_and_escaped(self):
        definition = '<b>State</b>. See [A & B](https://example.org/doc?a=1&b=2).'
        self.meta["terms"][0]["card"]["definition"] = definition
        self.write_record()
        session = review.prepare(self.root, ["record.md"], terms_only=True)
        card = json.loads((session / "data.json").read_text())[0]["card_html"]
        self.assertIn('<a href="https://example.org/doc?a=1&amp;b=2">A &amp; B</a>', card)
        self.assertIn('&lt;b&gt;State&lt;/b&gt;', card)
        self.assertNotIn('<b>State</b>', card)
        self.assertNotIn('<a ', review.definition_html('[unsafe](javascript:alert(1))'))
        self.assertNotIn('<a ', review.definition_html('[relative](/local)'))

    def test_only_proposed_terms_are_queued(self):
        for index, state in enumerate(("applied", "approved", "rejected", "deferred",
                                       "stale", "revision-requested"), start=2):
            self.meta["terms"].append({"id": f"T{index}", "revision": 1, "state": state})
        self.write_record()
        session = review.prepare(self.root, ["record.md"], terms_only=True)
        manifest = json.loads((session / "manifest.json").read_text())
        self.assertEqual([item["id"] for item in manifest["items"]],
                         ["logs/probe:cycle-1:T1:r2"])
        self.assertEqual(review.native_evidence(session)["users"], {})

    def test_empty_batch_is_frozen_without_a_fake_term_card(self):
        empty = dict(self.meta, terms=[])
        (self.root / "empty.md").write_text("---\n" + yaml.safe_dump(empty) + "---\nEmpty batch.\n")
        session = review.prepare(self.root, ["empty.md", "record.md"], terms_only=True)
        manifest = json.loads((session / "manifest.json").read_text())
        self.assertIn("empty.md", manifest["sources"])
        self.assertEqual(len(manifest["items"]), 1)

    def test_incomplete_card_refused(self):
        del self.meta["terms"][0]["card"]["definition"]
        self.write_record()
        with self.assertRaisesRegex(ValueError, "term card field definition"):
            self.prepare()

    def test_current_selection_and_prior_evidence(self):
        old = self.prepare()
        self.save(old)
        prior = {p.relative_to(old): p.read_bytes() for p in old.rglob("*") if p.is_file()}
        new = review.prepare(self.root, ["record.md"], terms_only=True)
        self.assertEqual(review.select_session(self.root), new)
        self.assertEqual(review.select_session(self.root, old.name), old)
        self.assertEqual(prior, {p.relative_to(old): p.read_bytes() for p in old.rglob("*") if p.is_file()})
        self.assertEqual(review.native_evidence(new)["users"], {})
        self.save(new)
        review.import_session(self.root, new)
        review.clean(self.root, new)
        self.assertFalse((self.root / ".reviews/current").exists())
        self.assertEqual(review.select_session(self.root), old)
        (self.root / ".reviews/current").write_text("../outside")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            review.select_session(self.root)

    def memo_batch(self):
        posts = {}
        for index in range(3):
            name = f"logs/memo-{index}.md"
            (self.root / name).write_text(
                f"---\ntitle: 'Log {index} & context'\ndate: 2026-11-21T12:00:00Z\n---\n"
                "# Context\n\nA complete passage.\n\n```text\nexact output\n```\n\n# Conclusion\n\nEnd.\n")
            posts[name[:-3]] = review.digest((self.root / name).read_bytes())
        batch = {"kind": "log-memo-review", "cycle": 1, "posts": posts}
        (self.root / "memos.md").write_text("---\n" + yaml.safe_dump(batch) + "---\nProse feedback.\n")
        return batch

    def test_memo_batch_has_three_complete_logs_and_no_decision_form(self):
        batch = self.memo_batch()
        session = review.prepare(self.root, ["memos.md"])
        self.assertEqual(session, review.prepare(self.root, ["memos.md"]))
        manifest = json.loads((session / "manifest.json").read_text())
        data = json.loads((session / "data.json").read_text())
        self.assertEqual(len(manifest["items"]), 3)
        self.assertEqual({item["entry"] for item in manifest["items"]}, set(batch["posts"]))
        for item, row in zip(manifest["items"], data):
            self.assertEqual(item["kind"], "log")
            self.assertEqual(item["id"], f"{item['entry']}:memo-cycle-1:log")
            self.assertEqual(item["text"], (self.root / item["post"]).read_text())
            self.assertEqual(row["text"], item["text"])
            self.assertEqual(manifest["sources"][item["post"]]["text"], item["text"])
            self.assertIn("&amp; context</h2>", row["card_html"])
        config = yaml.safe_load((session / "config.yaml").read_text())
        self.assertTrue(config["annotation_ui"]["memos"])
        self.assertEqual([s["name"] for s in config["annotation_schemes"]], ["comment"])
        field = next(f for f in config["instance_display"]["fields"] if f["key"] == "text")
        self.assertEqual(field["type"], "text")
        self.assertFalse(field.get("display_options", {}).get("collapsible", False))

    def test_memo_batch_refuses_stale_sources_meditations_and_terms_only(self):
        batch = self.memo_batch()
        with self.assertRaisesRegex(ValueError, "terms-only"):
            review.prepare(self.root, ["memos.md"], terms_only=True)
        (self.root / "logs/memo-0.md").write_text("Changed draft")
        with self.assertRaisesRegex(ValueError, "stale"):
            review.prepare(self.root, ["memos.md"])
        batch["posts"] = {"meditations/probe": "hash"}
        (self.root / "memos.md").write_text("---\n" + yaml.safe_dump(batch) + "---\n")
        with self.assertRaisesRegex(ValueError, "only logs"):
            review.prepare(self.root, ["memos.md"])

    def test_memo_only_import_keeps_comments_anchors_replies_and_issue_state(self):
        self.memo_batch()
        session = review.prepare(self.root, ["memos.md"])
        item_id = "logs/memo-0:memo-cycle-1:log"
        user = session / "annotation_output/raj"
        user.mkdir(parents=True)
        review.dump(user / "user_state.json", {"instance_id_to_label_to_value": {
            item_id: [[{"schema": "comment", "name": "text_box"}, "Whole-log feedback"]]}})
        quote = "A complete passage"
        start = (self.root / "logs/memo-0.md").read_text().index(quote)
        anchor = json.dumps({"field": "text", "start": start, "end": start + len(quote), "quote": quote})
        with sqlite3.connect(session / "project.sqlite") as db:
            db.executescript("CREATE TABLE memos(id TEXT, instance_id TEXT, anchor TEXT, body TEXT);"
                             "CREATE TABLE memo_threads(memo_id TEXT, parent_id TEXT, status TEXT);")
            db.execute("INSERT INTO memos VALUES(?, ?, ?, ?)", ("m1", item_id, anchor, "Passage feedback"))
            db.execute("INSERT INTO memos VALUES(?, ?, ?, ?)", ("m2", item_id, None, "Reply"))
            db.execute("INSERT INTO memo_threads VALUES('m1', NULL, 'open')")
            db.execute("INSERT INTO memo_threads VALUES('m2', 'm1', NULL)")
        output = review.import_session(self.root, session)
        report = json.loads(output.read_text())
        self.assertEqual(report["changed_sources"], [])
        self.assertEqual(report["responses"][0]["comment"], "Whole-log feedback")
        self.assertIsNone(report["responses"][0]["decision"])
        self.assertEqual(report["evidence"]["memos"][0]["anchor"], anchor)
        self.assertEqual(report["evidence"]["memo_threads"][0]["status"], "open")
        self.assertEqual(report["evidence"]["memo_threads"][1]["parent_id"], "m1")
        self.assertEqual(output, review.import_session(self.root, session))

    def test_paths_cannot_escape(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            review.inside(self.root, "../outside")


if __name__ == "__main__":
    unittest.main()
