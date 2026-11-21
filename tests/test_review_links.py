"""Direct queue/import contracts for outgoing links and empty results."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import review
from review_links import earlier, post_date


class OutlinkReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "meditations").mkdir()
        self.source = self.root / "meditations/new.md"
        self.source.write_text('---\ntitle: New\ndate: 2026-10-07\n---\nExact phrase.\n')
        self.target = self.root / "meditations/old.md"
        self.target.write_text('---\ntitle: Old\ndate: 2026-10-03\n---\nTarget evidence.\n')
        card = dict(placement="Opening paragraph", passage="Exact phrase.",
                    proposed="[Exact phrase](/old/).", purpose="related-reading",
                    evidence="Target evidence.", reason="Earlier background <script>.")
        self.meta = dict(kind="outlink-review", cycle=1,
                         links=[dict(id="L1", revision=1, state="proposed", entry="meditations/new", target="meditations/old", card=card)],
                         no_links=[dict(id="N1", revision=1, state="proposed", entry="meditations/old", card=dict(placement="Whole post", passage="Target evidence.", proposed="No outlinks needed.", purpose="related-reading", reason="Earliest post."))])
        self.write()

    def write(self):
        self.meta["posts"] = {str(p.relative_to(self.root).with_suffix("")): review.digest(p.read_bytes()) for p in (self.source, self.target)}
        (self.root / "review.md").write_text("---\n" + yaml.safe_dump(self.meta) + "---\nFull record\n")

    def queue(self):
        return review.prepare(self.root, ["review.md"])

    def test_cards_snapshot_dates_escaping_and_identity(self):
        session = self.queue()
        self.assertEqual(session, self.queue())
        manifest = json.loads((session / "manifest.json").read_text())
        self.assertEqual([i["kind"] for i in manifest["items"]], ["link", "no-links"])
        card = manifest["items"][0]["text"]
        for value in ("2026-10-07", "2026-10-03", "Exact phrase.", "Target evidence.", "strictly earlier", "&lt;script&gt;"):
            self.assertIn(value, card)
        self.assertNotIn("<script>", card)
        self.assertEqual(set(manifest["sources"]), {"review.md", "meditations/new.md", "meditations/old.md"})
        data = json.loads((session / "data.json").read_text())
        self.assertTrue(all(i["card_html"] and not i["text"] for i in data))
        self.meta["links"][0]["revision"] = 2
        self.write()
        self.assertNotEqual(session, self.queue())

    def test_link_and_empty_decisions_import_without_implicit_approval(self):
        session = self.queue()
        items = json.loads((session / "manifest.json").read_text())["items"]
        user = session / "annotation_output/raj"
        user.mkdir(parents=True)
        state = {items[0]["id"]: [[{"schema": "decision", "name": "approve"}, True]],
                 items[1]["id"]: [[{"schema": "comment", "name": "text_box"}, "Check this"]]}
        review.dump(user / "user_state.json", {"instance_id_to_label_to_value": state})
        output = review.import_session(self.root, session)
        report = json.loads(output.read_text())
        self.assertEqual([r["decision"] for r in report["responses"]], ["approve", None])
        state[items[1]["id"]].append([{"schema": "decision", "name": "defer"}, True])
        review.dump(user / "user_state.json", {"instance_id_to_label_to_value": state})
        self.target.write_text(self.target.read_text() + "Changed\n")
        report = json.loads(review.import_session(self.root, session).read_text())
        self.assertEqual(report["responses"][1]["decision"], "defer")
        self.assertEqual(report["changed_sources"], ["meditations/old.md"])
        self.assertTrue(output.exists())

    def test_stale_hash_and_missing_passages(self):
        self.target.write_text("Changed")
        with self.assertRaisesRegex(ValueError, "stale"):
            self.queue()
        self.target.write_text('---\ndate: 2026-10-03\n---\nDifferent evidence.\n')
        self.write()
        with self.assertRaisesRegex(ValueError, "Target evidence"):
            self.queue()
        self.meta["links"][0]["card"]["passage"] = "Absent"
        self.write()
        with self.assertRaisesRegex(ValueError, "Source passage"):
            self.queue()

    def test_equal_future_and_unknown_same_day_order_refused(self):
        for value in ("2026-10-07", "2026-10-08", "2026-10-07T01:00:00Z"):
            self.target.write_text(f'---\ndate: {value}\n---\nTarget evidence.\n')
            self.write()
            with self.assertRaisesRegex(ValueError, "strictly earlier"):
                self.queue()
        before = post_date('---\ndate: 2026-10-07T01:00:00Z\n---\n')
        after = post_date('---\ndate: 2026-10-07T03:00:00Z\n---\n')
        self.assertTrue(earlier(before, after))
        self.assertFalse(earlier(after, before))

    def test_wrong_path_and_duplicate_ids_refused(self):
        self.meta["links"][0]["card"]["proposed"] = "[Exact phrase](/meditations/old/)."
        self.write()
        with self.assertRaisesRegex(ValueError, "target path"):
            self.queue()
        self.meta["links"][0]["card"]["proposed"] = "[Exact phrase](/old/)."
        self.meta["links"].append(self.meta["links"][0])
        self.write()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.queue()


if __name__ == "__main__":
    unittest.main()
