"""Consumer-visible geometry and explained-variance invariants for the map."""

from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.projection import project


class ProjectionTests(unittest.TestCase):
    def projection(self, vectors, dimension=None):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.execute("CREATE TABLE posts (slug TEXT PRIMARY KEY, embedding BLOB NOT NULL)")
        stored = {slug: np.asarray(vector, dtype="<f4") for slug, vector in vectors.items()}
        connection.executemany(
            "INSERT INTO posts VALUES (?, ?)",
            ((slug, vector.tobytes()) for slug, vector in stored.items()),
        )
        if dimension is None:
            dimension = len(next(iter(stored.values())))
        result = project(connection, dimension)
        originals = np.array([stored[slug] for slug in result.points], dtype=np.float64)
        coordinates = np.array(list(result.points.values()), dtype=np.float64)
        return result, originals, coordinates

    def assert_preserves_geometry(self, originals, coordinates):
        self.assertTrue(np.isfinite(coordinates).all())
        scale = np.max(np.abs(originals - originals[0]))
        np.testing.assert_allclose(coordinates.mean(axis=0), 0.0, atol=scale * 1e-14)
        original_distances = np.linalg.norm(originals[:, None] - originals[None, :], axis=2)
        map_distances = np.linalg.norm(coordinates[:, None] - coordinates[None, :], axis=2)
        np.testing.assert_allclose(map_distances, original_distances, rtol=1e-12, atol=0.0)

    def test_empty_archive(self):
        result, _, _ = self.projection({}, dimension=3)
        self.assertEqual(result.points, {})
        self.assertIsNone(result.variance)

    def test_single_post_is_at_origin_without_explained_variance(self):
        result, _, coordinates = self.projection({"only": [0.1, -0.2, 0.3]})
        np.testing.assert_array_equal(coordinates, [[0.0, 0.0]])
        self.assertIsNone(result.variance)

    def test_identical_vectors_do_not_invent_separation(self):
        result, _, coordinates = self.projection(
            {f"post-{index}": [0.1, -0.2, 0.3] for index in range(7)}
        )
        np.testing.assert_array_equal(coordinates, np.zeros((7, 2)))
        self.assertIsNone(result.variance)

    def test_two_and_three_posts_preserve_all_pairwise_distances(self):
        for vectors in (
            {"later": [2.0, -1.0, 4.0], "earlier": [-3.0, 2.0, 1.0]},
            {"c": [2.0, -1.0, 4.0], "a": [-3.0, 2.0, 1.0], "b": [1.0, 3.0, -2.0]},
        ):
            with self.subTest(count=len(vectors)):
                result, originals, coordinates = self.projection(vectors)
                self.assert_preserves_geometry(originals, coordinates)
                self.assertAlmostEqual(result.variance, 1.0)
                reordered, _, other_coordinates = self.projection(dict(reversed(list(vectors.items()))))
                self.assertEqual(list(result.points), list(reordered.points))
                np.testing.assert_allclose(coordinates, other_coordinates, rtol=1e-12, atol=1e-14)

    def test_one_dimensional_archive_has_zero_y_and_preserves_distances(self):
        result, originals, coordinates = self.projection({"c": [5.0], "a": [-2.0], "b": [1.0]})
        self.assert_preserves_geometry(originals, coordinates)
        np.testing.assert_array_equal(coordinates[:, 1], 0.0)
        self.assertAlmostEqual(result.variance, 1.0)

    def test_tiny_real_variation_is_not_treated_as_identical(self):
        result, originals, coordinates = self.projection(
            {"a": [0.0, 0.0, 0.0], "b": [1e-35, 0.0, 0.0], "c": [0.0, 2e-35, 0.0]}
        )
        self.assert_preserves_geometry(originals, coordinates)
        self.assertAlmostEqual(result.variance, 1.0)

    def test_small_differences_around_common_offset_are_preserved(self):
        step = float(np.spacing(np.float32(1.0)))
        result, originals, coordinates = self.projection(
            {"a": [1.0, 1.0], "b": [1.0 + step, 1.0], "c": [1.0, 1.0 + step]}
        )
        self.assert_preserves_geometry(originals, coordinates)
        self.assertAlmostEqual(result.variance, 1.0)

    def test_truncation_retains_largest_variances_without_whitening(self):
        vectors = {
            "x-positive": [3.0, 0.0, 0.0], "x-negative": [-3.0, 0.0, 0.0],
            "y-positive": [0.0, 2.0, 0.0], "y-negative": [0.0, -2.0, 0.0],
            "z-positive": [0.0, 0.0, 1.0], "z-negative": [0.0, 0.0, -1.0],
        }
        result, originals, coordinates = self.projection(vectors)
        self.assertTrue(np.isfinite(coordinates).all())
        np.testing.assert_allclose(coordinates.mean(axis=0), 0.0, atol=1e-14)
        self.assertAlmostEqual(result.variance, 13.0 / 14.0)
        retained_energy = float(np.sum(coordinates * coordinates))
        self.assertAlmostEqual(retained_energy / float(np.sum(originals * originals)), result.variance)
        for axis, expected_distance in (("x", 6.0), ("y", 4.0), ("z", 0.0)):
            positive = np.array(result.points[f"{axis}-positive"])
            negative = np.array(result.points[f"{axis}-negative"])
            self.assertAlmostEqual(float(np.linalg.norm(positive - negative)), expected_distance)
        original_distances = np.linalg.norm(originals[:, None] - originals[None, :], axis=2)
        map_distances = np.linalg.norm(coordinates[:, None] - coordinates[None, :], axis=2)
        self.assertTrue(np.all(map_distances <= original_distances + 1e-12))


if __name__ == "__main__":
    unittest.main()
