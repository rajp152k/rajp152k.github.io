"""Lab-note rendering, evidence links, and directed map endpoints."""
from datetime import date
from pathlib import Path
import sys
import unittest
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from archive import Entry
from lab_notes import map_inspector, post_notes
from projection import Projection
from publish import render_map


class LabNotesTests(unittest.TestCase):
    def setUp(self):
        self.entries = [Entry("meditations", slug, title, date(2026, 1, 1), "")
                        for slug, title in (("a", "A <script>"), ("b", 'B & "quoted"'))]
        self.by_key = {entry.key: entry for entry in self.entries}
        self.codes = {entry.key: f"mx{index}" for index, entry in enumerate(self.entries)}
        self.reference = {"source": "meditations/a", "target": "meditations/b", "url": "/b/#context",
                          "source_url": "/a/#post-reference-1", "excerpt": "Evidence <script>alert(1)</script> & text"}

    def test_notes_link_to_authored_target_and_exact_source_passage(self):
        source = post_notes(self.entries[0], self.by_key, self.codes, [self.reference])
        target = post_notes(self.entries[1], self.by_key, self.codes, [self.reference])
        self.assertIn('href="/b/#context"', source)
        self.assertIn('href="/a/#post-reference-1"', source)
        self.assertIn('href="/a/#post-reference-1"', target)
        self.assertIn("Evidence &lt;script&gt;alert(1)&lt;/script&gt; &amp; text", source)
        self.assertNotIn("<script>", source + target)
        self.assertEqual(post_notes(self.entries[0], self.by_key, self.codes, []), "")

    def test_inspector_escapes_titles_and_formats_full_vector_score(self):
        nearest = {"meditations/a": [{"key": "meditations/b", "score": .876543}]}
        html = map_inspector(self.entries, self.codes, [self.reference], nearest)
        self.assertIn("A &lt;script&gt;", html)
        self.assertIn("B &amp; &quot;quoted&quot;", html)
        self.assertNotIn("<script>", html)
        self.assertIn('class="similarity-score">0.877</span>', html)

    def test_reference_lines_use_the_same_coordinates_as_their_endpoints(self):
        projection = Projection({"meditations/a": (-2., 1.), "meditations/b": (3., -4.)}, .8)
        svg = ET.fromstring(render_map(self.entries, projection, self.codes, {"meditations/a"}, [self.reference]))
        line = svg.find('.//line')
        points = {node.attrib["data-post"]: node.find("circle[@class='map-dot']")
                  for node in svg.findall('.//a')}
        self.assertEqual(line.attrib["data-source"], "meditations/a")
        self.assertEqual(line.attrib["data-target"], "meditations/b")
        for end, key in (("1", "meditations/a"), ("2", "meditations/b")):
            self.assertEqual(line.attrib["x" + end], points[key].attrib["cx"])
            self.assertEqual(line.attrib["y" + end], points[key].attrib["cy"])


if __name__ == "__main__":
    unittest.main()
