"""Evidence validation and lossless, deterministic term matching."""
import copy
import json
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from archive import Entry, read_entries
from terms import (Registry, Source, Term, collect_mentions, load_terms,
                   maintenance_report, mentions_for_term, terms_for_post, transform_html)


def term(ident="orch", name="Orch", aliases=()):
    return Term(ident, name, aliases, "An agent in this example.", "meditations/example", (Source("meditations/example", "Orch coordinates."),))


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.entry = Entry("meditations", "example", "Example", date(2026, 1, 1), "Orch coordinates.")
        self.row = {"id": "orch", "name": "Orch", "aliases": [],
                    "definition": "An agent in this example.", "introduction": self.entry.key,
                    "sources": [{"entry": self.entry.key, "quote": "Orch coordinates."}]}
        self.data = {"version": 1, "terms": [self.row]}
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "terms.json"

    def load(self, data=None):
        self.path.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")
        return load_terms([self.entry], self.path)

    def test_valid_record_and_exact_evidence(self):
        registry = self.load()
        self.assertEqual(registry.by_id["orch"].sources[0].quote, self.entry.body)
        self.assertEqual(registry.terms[0].url, "/terms/orch/")

    def test_strict_schema_and_types(self):
        cases = [[], {"version": True, "terms": []}, {"version": 1, "terms": {}},
                 {"version": 1, "terms": [], "other": True}]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.load(data)
        for field, bad in [("id", 2), ("name", ""), ("aliases", "Orch"),
                           ("aliases", [None]), ("definition", " leading"),
                           ("sources", []), ("sources", [{}]), ("introduction", [])]:
            data = copy.deepcopy(self.data)
            data["terms"][0][field] = bad
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                self.load(data)

    def test_duplicate_json_key(self):
        self.path.write_text('{"version":1,"terms":[],"terms":[]}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            load_terms([self.entry], self.path)

    def test_duplicate_ids_and_ambiguous_aliases(self):
        for second_id, second_name in [("orch", "Other"), ("other", "ORCH")]:
            data = copy.deepcopy(self.data)
            second = dict(self.row, id=second_id, name=second_name)
            data["terms"].append(second)
            with self.subTest(second=second), self.assertRaises(ValueError):
                self.load(data)
        self.row["aliases"] = ["orch"]
        with self.assertRaisesRegex(ValueError, "ambiguous alias"):
            self.load()

    def test_unicode_case_alias_collision(self):
        self.row["name"] = "I"
        self.row["aliases"] = ["İ"]
        with self.assertRaisesRegex(ValueError, "ambiguous alias"):
            self.load()

    def test_stale_quotes_and_missing_posts(self):
        for field, value in [("quote", "Orch used to coordinate."), ("entry", "meditations/missing")]:
            data = copy.deepcopy(self.data)
            data["terms"][0]["sources"][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "stale source|unknown source"):
                self.load(data)
        self.row["introduction"] = "meditations/missing"
        with self.assertRaisesRegex(ValueError, "unknown introduction"):
            self.load()

    def test_reserved_and_unsafe_ids(self):
        for ident in ["index", "terms", "../bad", "<bad>", "Upper", "a--b", "a/"]:
            self.row["id"] = ident
            with self.subTest(ident=ident), self.assertRaises(ValueError):
                self.load()

    def test_archive_records_and_repeatable_report(self):
        entries = read_entries()
        registry = load_terms(entries)
        mentions = collect_mentions(entries, registry)
        self.assertEqual(mentions, collect_mentions(reversed(entries), registry))
        self.assertTrue(all(mentions_for_term(item.id, mentions) for item in registry.terms))

    def test_unmatched_posts_are_only_review_candidates(self):
        registry = self.load()
        unmentioned = Entry("meditations", "other", "Another subject", date(2026, 1, 2), "No agent here.")
        entries = [self.entry, unmentioned]
        mentions = collect_mentions(entries, registry)
        report = maintenance_report(entries, registry, mentions)
        self.assertEqual(report, maintenance_report(reversed(entries), registry, mentions))
        self.assertEqual(report["review_candidates"], [{
            "entry": unmentioned.key, "title": unmentioned.title, "url": unmentioned.url,
            "reason": "No matched terms. Review only; a term may not be needed.",
        }])
        self.assertEqual(report["entries"], 2)


class TransformTests(unittest.TestCase):
    def setUp(self):
        self.registry = Registry((term(),))

    def test_preserve_source_ids_and_reject_reserved_anchor_collisions(self):
        source = '<p id="existing-id">Orch</p>'
        result = transform_html(source, self.registry)
        self.assertTrue(result.html.startswith('<p id="existing-id"><span'))
        for source in [
            '<p id="term-orch">Orch</p>',
            '<p id="term-orch">First</p><p id="term-orch">Orch</p>',
            '<span class="term-reference" data-term="orch" id="term-orch">Orch</span><p id="term-orch">Other</p>',
        ]:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "[Rr]eserved term anchor"):
                transform_html(source, self.registry)

    def test_only_first_eligible_occurrence_and_lossless_surroundings(self):
        source = '<!-- Orch --><P data-note="Orch &amp; x">Orch &amp; Orch.</P>'
        result = transform_html(source, self.registry)
        self.assertEqual(result.html, '<!-- Orch --><P data-note="Orch &amp; x"><span class="term-reference" data-term="orch" id="term-orch">Orch</span> &amp; Orch.</P>')
        self.assertEqual(result.mentions[0].excerpt, "Orch & Orch.")
        self.assertEqual(len(result.mentions), 1)

    def test_excluded_nodes_nested_nodes_and_hidden_content(self):
        tags = ["a", "code", "pre", "h1", "h6", "blockquote", "q", "script", "style", "textarea", "button", "template", "svg", "math", "noscript", "kbd"]
        source = "".join(f'<{tag}><em>Orch</em></{tag}>' for tag in tags)
        source += '<div hidden>Orch</div><div aria-hidden="true">Orch</div><p>Orch</p>'
        result = transform_html(source, self.registry)
        self.assertTrue(result.html.startswith(source[:-11]))
        self.assertEqual(result.html.count('data-term="orch"'), 1)
        self.assertTrue(result.html.endswith('>Orch</span></p>'))

    def test_inline_quotation_does_not_consume_first_prose_reference(self):
        result = transform_html('<p><q>Orch</q> Then Orch coordinates.</p>', self.registry)
        self.assertEqual(result.html, '<p><q>Orch</q> Then <span class="term-reference" data-term="orch" id="term-orch">Orch</span> coordinates.</p>')

    def test_entities_are_matched_and_preserved(self):
        result = transform_html('<p>&#79;rch &copy; &unknown;</p>', self.registry)
        self.assertIn('>&#79;rch</span> &copy; &unknown;', result.html)
        self.assertEqual(result.mentions[0].text, "Orch")
        registry = Registry((term("head", "machine head"),))
        result = transform_html('<p>machine&nbsp;head</p>', registry)
        self.assertIn('>machine&nbsp;head</span>', result.html)

    def test_unicode_boundaries_and_case(self):
        result = transform_html('<p>Orchestra xOrch Orché _Orch ORCH!</p>', self.registry)
        self.assertEqual(result.mentions[0].text, "ORCH")
        self.assertIn('_Orch <span', result.html)
        result = transform_html('<p>İ</p>', Registry((term("letter", "i"),)))
        self.assertEqual(result.mentions[0].term_id, "letter")

    def test_longest_alias_and_source_order(self):
        registry = Registry((term("agent", "agent"), term("project", "project agent", ("project agents",))))
        result = transform_html('<p>project agents, agent, project agent</p>', registry)
        self.assertEqual([match.term_id for match in result.mentions], ["project", "agent"])
        self.assertEqual(result.mentions[0].text, "project agents")
        self.assertEqual(result, transform_html('<p>project agents, agent, project agent</p>', Registry(tuple(reversed(registry.terms)))))

    def test_inline_formatting_and_comments_do_not_merge_words(self):
        registry = Registry((term("head", "machine head"),))
        source = '<p>machine <em>head</em>; machine<!-- note --> head</p>'
        self.assertEqual(transform_html(source, registry).html, source)

    def test_no_nested_annotations_and_idempotence(self):
        result = transform_html('<p>Orch then Orch</p>', self.registry)
        self.assertEqual(transform_html(result.html, self.registry).html, result.html)
        source = '<p>Orch</p><span class="term-reference" data-term="orch" id="term-orch">Orch</span>'
        self.assertEqual(transform_html(source, self.registry).html, source)

    def test_empty_registry_and_plain_text(self):
        self.assertEqual(transform_html("Orch", Registry(())).html, "Orch")
        self.assertEqual(len(transform_html("Orch", self.registry).mentions), 1)

    def test_mentions_include_post_reference_and_visible_excerpt(self):
        entry = Entry("meditations", "example", "Example", date(2026, 1, 1), "unused")
        mentions = collect_mentions([entry], self.registry, {entry.key: '<p>Before Orch &amp; after.</p>'})
        self.assertEqual(mentions[0].excerpt, "Before Orch & after.")
        self.assertEqual(mentions[0].url, "/example/#term-orch")
        self.assertEqual(terms_for_post(entry.key, mentions, self.registry), self.registry.terms)
        self.assertEqual(mentions_for_term("orch", mentions), mentions)


if __name__ == "__main__":
    unittest.main()
