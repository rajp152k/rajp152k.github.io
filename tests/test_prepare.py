"""Editorial receipts, dependency invalidation, and safe draft preparation."""
from __future__ import annotations

from contextlib import ExitStack, redirect_stderr, redirect_stdout
from copy import deepcopy
from dataclasses import replace
from datetime import date, timedelta
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts import prepare
from scripts.archive import Entry
from scripts.terms import Registry, Source, Term


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.state_path = self.root / "state.json"
        self.policy_path = self.root / "policy.md"
        self.policy_path.write_text("Explain unfamiliar names.", encoding="utf-8")
        self.source = Entry("meditations", "source", "Source", date(2026, 1, 1),
                            "Widget means a shared tool. Original context.")
        self.post = Entry("meditations", "post", "Post", date(2026, 1, 2),
                          "A Widget helps readers.")
        self.older = Entry("meditations", "older", "Older", date(2025, 1, 1),
                           "Widget also appeared earlier.")
        self.plain = Entry("meditations", "plain", "Plain", date(2026, 1, 3),
                           "An ordinary account needs no glossary.")
        self.entries = [self.source, self.post, self.older, self.plain]
        self.term = Term("widget", "Widget", (), "A shared tool.", self.source.key,
                         (Source(self.source.key, "Widget means a shared tool."),))
        self.registry = Registry((self.term,))
        self.preparation = self.make_preparation()
        self.state = {"version": 1, "posts": {}}

    def make_preparation(self, entries=None, terms=None, policy="Explain unfamiliar names."):
        return prepare.Preparation(self.entries if entries is None else entries,
                                   self.registry if terms is None else Registry(tuple(terms)), policy)

    def review(self, key=None, **kwargs):
        key = self.post.key if key is None else key
        self.preparation.review(self.state, key, "reader", "Read the draft.")
        self.preparation.review(self.state, key, "references", "Checked references.", **kwargs)

    def statuses(self, preparation=None, key=None):
        report = (preparation or self.preparation).report(self.state)
        return {stage: item["status"] for stage, item in
                report["posts"][key or self.post.key].items()}

    def cli(self, argv, run_stage=None):
        # Redirect every external input and every write to synthetic fixtures.
        with ExitStack() as stack:
            stack.enter_context(patch.object(prepare, "read_entries", return_value=self.entries))
            stack.enter_context(patch.object(prepare, "load_terms", return_value=self.registry))
            stack.enter_context(patch.object(prepare, "POLICY", self.policy_path))
            stack.enter_context(patch.object(prepare, "load_state", side_effect=lambda: prepare_load(self.state_path)))
            stack.enter_context(patch.object(prepare, "save_state", side_effect=lambda data: prepare_save(data, self.state_path)))
            runner = stack.enter_context(patch.object(prepare, "run_stage", side_effect=run_stage))
            output, errors = io.StringIO(), io.StringIO()
            stack.enter_context(redirect_stdout(output))
            stack.enter_context(redirect_stderr(errors))
            result = prepare.main(argv)
            return result, runner, output.getvalue(), errors.getvalue()

    def test_new_post_is_pending_and_status_does_not_mutate_state(self):
        before = deepcopy(self.state)
        self.assertEqual(self.statuses(), {"reader": "pending", "references": "pending"})
        self.assertFalse(self.preparation.report(self.state)["ready"])
        self.assertEqual(self.state, before)

    def test_reader_must_be_current_before_reference_review(self):
        with self.assertRaises(ValueError):
            self.preparation.review(self.state, self.post.key, "references", "Checked.")
        self.preparation.review(self.state, self.post.key, "reader", "Read.")
        changed = self.make_preparation(entries=[replace(e, body=e.body + " New.")
                                                if e == self.post else e for e in self.entries])
        with self.assertRaises(ValueError):
            changed.review(self.state, self.post.key, "references", "Checked.")
        self.preparation.review(self.state, self.post.key, "references", "Checked.")
        self.assertEqual(set(self.statuses().values()), {"current"})

    def test_post_with_no_terms_can_have_current_reviews(self):
        self.review(self.plain.key, decisions=["No definition is needed for this audience."])
        self.assertEqual(set(self.statuses(key=self.plain.key).values()), {"current"})
        self.assertFalse(any(key.startswith("term:") for key in
                             self.preparation.inputs(self.plain.key, "references")))

    def test_body_and_title_changes_invalidate_both_stages(self):
        self.review()
        for field, value in (("body", "A different Widget passage."), ("title", "Changed title")):
            with self.subTest(field=field):
                entries = [replace(e, **{field: value}) if e == self.post else e for e in self.entries]
                self.assertEqual(set(self.statuses(self.make_preparation(entries=entries)).values()), {"stale"})

    def test_dates_and_unrelated_terms_do_not_invalidate_reviews(self):
        self.review()
        entries = [replace(e, published=e.published + timedelta(days=7)) for e in self.entries]
        unrelated = Term("other", "Unmentioned", (), "Another meaning.", self.plain.key,
                         (Source(self.plain.key, "An ordinary account"),))
        changed = self.make_preparation(entries=entries, terms=[self.term, unrelated])
        self.assertEqual(set(self.statuses(changed).values()), {"current"})
        unrelated = replace(unrelated, definition="Revised unrelated meaning.", aliases=("Elsewhere",))
        self.assertEqual(set(self.statuses(self.make_preparation(terms=[self.term, unrelated])).values()), {"current"})

    def test_shared_definition_alias_and_evidence_changes_invalidate_all_dependents(self):
        for key in (self.post.key, self.older.key):
            self.review(key)
        changes = [replace(self.term, definition="A more precise shared tool."),
                   replace(self.term, aliases=("Shared widget",)),
                   replace(self.term, sources=(Source(self.source.key, "Original context."),))]
        for term in changes:
            for key in (self.post.key, self.older.key):
                with self.subTest(term=term, key=key):
                    self.assertEqual(self.statuses(self.make_preparation(terms=[term]), key),
                                     {"reader": "current", "references": "stale"})

    def test_source_context_change_invalidates_references_without_quote_change(self):
        self.review()
        self.review(self.older.key)
        entries = [replace(e, body=e.body + " New surrounding explanation.")
                   if e == self.source else e for e in self.entries]
        for key in (self.post.key, self.older.key):
            self.assertEqual(self.statuses(self.make_preparation(entries=entries), key),
                             {"reader": "current", "references": "stale"})

    def test_new_alias_match_invalidates_previous_no_term_review(self):
        self.review(self.plain.key)
        changed = self.make_preparation(terms=[replace(self.term, aliases=("ordinary account",))])
        self.assertEqual(self.statuses(changed, self.plain.key),
                         {"reader": "current", "references": "stale"})

    def test_removed_term_invalidates_references(self):
        self.review()
        self.assertEqual(self.statuses(self.make_preparation(terms=[])),
                         {"reader": "current", "references": "stale"})

    def test_policy_change_invalidates_both_stages(self):
        self.review()
        changed = self.make_preparation(policy="Use the new reader review policy.")
        self.assertEqual(set(self.statuses(changed).values()), {"stale"})

    def test_related_post_change_or_deletion_invalidates_references(self):
        self.review(related=[self.plain.key])
        for entries in ([replace(e, body="Changed related reading.") if e == self.plain else e
                         for e in self.entries], [e for e in self.entries if e != self.plain]):
            with self.subTest(entries=entries):
                self.assertEqual(self.statuses(self.make_preparation(entries=entries)),
                                 {"reader": "current", "references": "stale"})

    def test_blocking_questions_block_check_but_optional_questions_allow_current(self):
        for entry in self.entries:
            self.review(entry.key)
        self.preparation.review(self.state, self.post.key, "references", "Awaiting meaning.",
                                blocking_questions=["Which meaning is intended?"])
        prepare.save_state(self.state, self.state_path)
        self.assertEqual(self.cli(["check"])[0], 1)
        self.assertEqual(self.statuses()["references"], "blocked")
        self.preparation.review(self.state, self.post.key, "references", "Optional follow-up.",
                                questions=["Would another example help?"])
        prepare.save_state(self.state, self.state_path)
        self.assertEqual(self.cli(["check"])[0], 0)
        self.assertTrue(self.preparation.report(self.state)["ready"])

    def test_review_rejects_unknown_posts_invalid_stages_and_bad_lists(self):
        self.review()
        calls = [dict(key="meditations/missing", stage="reader", note="Read."),
                 dict(key=self.post.key, stage="invalid", note="Read."),
                 dict(key=self.post.key, stage="reader", note=" "),
                 dict(key=self.post.key, stage="reader", note="Read.", related=[self.plain.key]),
                 dict(key=self.post.key, stage="references", note="Read.", related=[self.post.key]),
                 dict(key=self.post.key, stage="references", note="Read.", related=["missing"]),
                 dict(key=self.post.key, stage="references", note="Read.", decisions=["Same", "Same"]),
                 dict(key=self.post.key, stage="references", note="Read.", questions=[" "])]
        for kwargs in calls:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.preparation.review(self.state, **kwargs)

    def test_missing_state_and_save_load_round_trip(self):
        self.assertEqual(prepare.load_state(self.state_path), self.state)
        self.review(decisions=["Reuse Widget."], questions=["Optional question?"])
        prepare.save_state(self.state, self.state_path)
        self.assertEqual(prepare.load_state(self.state_path), self.state)
        self.assertEqual(list(self.root.glob(".state.json.*")), [])

    def test_failed_save_preserves_existing_file_and_removes_temporary_file(self):
        prepare.save_state(self.state, self.state_path)
        previous = self.state_path.read_bytes()
        self.review()
        with patch.object(prepare.os, "replace", side_effect=OSError("replace failed")):
            with self.assertRaises(OSError):
                prepare.save_state(self.state, self.state_path)
        self.assertEqual(self.state_path.read_bytes(), previous)
        self.assertEqual(list(self.root.glob(".state.json.*")), [])

    def test_load_rejects_invalid_schema_and_receipt_fields(self):
        self.review()
        invalid = [[], {}, {"version": True, "posts": {}}, {"version": 2, "posts": {}},
                   {"version": 1, "posts": []}, {"version": 1, "posts": {"bad": {"other": {}}}}]
        for mutate in (lambda r: r.pop("note"), lambda r: r.update(note=" "),
                       lambda r: r.update(inputs={}), lambda r: r.update(inputs={"draft": "x" * 64}),
                       lambda r: r.update(questions=["same", "same"]),
                       lambda r: r.update(decisions="not a list"),
                       lambda r: r.update(related=[" "])):
            state = deepcopy(self.state)
            mutate(state["posts"][self.post.key]["reader"])
            invalid.append(state)
        for state in invalid:
            with self.subTest(state=state):
                self.state_path.write_text(json.dumps(state), encoding="utf-8")
                with self.assertRaises(ValueError):
                    prepare.load_state(self.state_path)

    def test_load_rejects_duplicate_json_fields_at_any_depth(self):
        for content in ('{"version":1,"version":1,"posts":{}}',
                        '{"version":1,"posts":{"a":{},"a":{}}}'):
            self.state_path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                prepare.load_state(self.state_path)

    def test_removed_receipts_prevent_readiness_and_prune_removes_only_deleted(self):
        for entry in self.entries:
            self.review(entry.key)
        self.state["posts"]["meditations/deleted"] = deepcopy(self.state["posts"][self.post.key])
        self.assertEqual(self.preparation.report(self.state)["removed"], ["meditations/deleted"])
        self.assertFalse(self.preparation.report(self.state)["ready"])
        prepare.save_state(self.state, self.state_path)
        result, runner, _, _ = self.cli(["prune"])
        self.assertEqual(result, 0)
        runner.assert_not_called()
        saved = prepare.load_state(self.state_path)
        self.assertEqual(set(saved["posts"]), {e.key for e in self.entries})
        self.assertTrue(self.preparation.report(saved)["ready"])

    def test_cli_check_pending_and_json_status_do_not_write_or_run_stages(self):
        result, runner, _, _ = self.cli(["check"])
        self.assertEqual(result, 1)
        runner.assert_not_called()
        result, runner, output, _ = self.cli(["status", "--json"])
        self.assertEqual(result, 0)
        self.assertFalse(json.loads(output)["ready"])
        runner.assert_not_called()
        self.assertFalse(self.state_path.exists())

    def test_cli_review_persists_only_explicit_review(self):
        result, runner, _, _ = self.cli(["review", self.post.key, "--stage", "reader", "--note", "Read draft."])
        self.assertEqual(result, 0)
        saved = prepare.load_state(self.state_path)
        self.assertEqual(set(saved["posts"][self.post.key]), {"reader"})
        self.assertEqual(set(saved["posts"]), {self.post.key})
        runner.assert_not_called()

    def test_cli_build_allows_pending_runs_in_order_and_does_not_record_reviews(self):
        prepare.save_state(self.state, self.state_path)
        previous = self.state_path.read_bytes()
        result, runner, _, _ = self.cli(["build"])
        self.assertEqual(result, 0)
        self.assertEqual([call.args[0] for call in runner.call_args_list], ["embed.py", "publish.py"])
        self.assertEqual(self.state_path.read_bytes(), previous)

    def test_cli_build_stops_before_site_build_when_embedding_fails(self):
        result, runner, _, errors = self.cli(
            ["build"], run_stage=subprocess.CalledProcessError(1, ["embed.py"]))
        self.assertEqual(result, 1)
        runner.assert_called_once_with("embed.py")
        self.assertIn("prepare:", errors)
        self.assertFalse(self.state_path.exists())


# Keep original functions for CLI tests whose module functions are patched.
prepare_load = prepare.load_state
prepare_save = prepare.save_state


if __name__ == "__main__":
    unittest.main()
