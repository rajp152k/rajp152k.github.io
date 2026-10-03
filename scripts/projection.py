"""Exact, unscaled PCA coordinates for the current archive embeddings."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Projection:
    points: dict[str, tuple[float, float]]
    variance: float | None


def project(connection: sqlite3.Connection, dimension: int) -> Projection:
    """Read validated vectors inside the caller's existing read transaction."""
    rows = connection.execute("SELECT slug, embedding FROM posts ORDER BY slug").fetchall()
    if not rows:
        return Projection({}, None)

    centered = np.empty((len(rows), dimension), dtype=np.float64)
    for index, (_, blob) in enumerate(rows):
        centered[index] = np.frombuffer(blob, dtype="<f4", count=dimension)
    # Translate first to preserve tiny differences around a large common offset
    # and make identical vectors exactly zero, even with a rounded mean.
    centered -= centered[0].copy()
    centered -= centered.mean(axis=0)

    coordinates = np.zeros((len(rows), 2), dtype=np.float64)
    variance = None
    components = min(2, len(rows) - 1, dimension)
    if components and np.any(centered):
        left, singular, loadings = np.linalg.svd(centered, full_matrices=False)
        coordinates[:, :components] = left[:, :components] * singular[:components]
        for axis in range(components):
            pivot = np.argmax(np.abs(loadings[axis]))
            if loadings[axis, pivot] < 0:
                coordinates[:, axis] *= -1
        # Float64 can represent squared variation across the entire float32
        # input range. No absolute epsilon should erase genuinely small maps.
        energy = singular * singular
        variance = float(np.clip(energy[:components].sum() / energy.sum(), 0.0, 1.0))

    return Projection(
        {row[0]: (float(point[0]), float(point[1])) for row, point in zip(rows, coordinates)},
        variance,
    )
