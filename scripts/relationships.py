"""Authored post references and full-vector similarity, kept as separate signals."""

from __future__ import annotations

import sqlite3
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

import numpy as np

from archive import ROOT, Entry


class _References(HTMLParser):
    """Collect anchors with their surrounding visible paragraph text."""

    BLOCKS = {
        "address", "article", "aside", "blockquote", "dd", "div", "dl", "dt",
        "figcaption", "figure", "footer", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "hr", "li", "main", "ol", "p", "section", "table", "td", "tr", "ul",
    }
    IGNORED = {"code", "pre", "nav", "script", "style", "template"}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.line_offsets = [0]
        for line in source.split("\n"):
            self.line_offsets.append(self.line_offsets[-1] + len(line) + 1)
        self.ids = set()
        self.ignored = []
        self.parts = []
        self.anchors = []
        self.references = []

    def flush(self):
        text = " ".join("".join(self.parts).split())
        for href, part_index, position, raw, anchor_id in self.anchors:
            offset = len(" ".join("".join(self.parts[:part_index]).split()))
            # Keep the linked passage in view even in a long paragraph.
            start = max(0, offset - 120)
            if start:
                boundary = text.find(" ", start)
                start = boundary + 1 if boundary != -1 and boundary < offset else start
            excerpt = text[start:start + 320]
            if start + 320 < len(text):
                excerpt = excerpt.rsplit(" ", 1)[0] + "…"
            if start:
                excerpt = "…" + excerpt
            self.references.append((href, excerpt, position, raw, anchor_id))
        self.parts = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag in self.IGNORED:
            self.ignored.append(tag)
        if self.ignored:
            return
        if tag in self.BLOCKS:
            self.flush()
        if tag == "br":
            self.parts.append(" ")
        if tag == "a":
            href = attributes.get("href")
            if href:
                line, column = self.getpos()
                position = self.line_offsets[line - 1] + column
                self.anchors.append((
                    href, len(self.parts), position, self.get_starttag_text(), attributes.get("id"),
                ))

    def handle_endtag(self, tag):
        if self.ignored:
            if tag in self.ignored:
                index = len(self.ignored) - 1 - self.ignored[::-1].index(tag)
                del self.ignored[index:]
            return
        if tag in self.BLOCKS:
            self.flush()

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def _post_path(path: str) -> str:
    """Compare URL paths after one percent-decoding pass."""
    path = unquote(path)
    if path.endswith("/index.html"):
        path = path[:-len("index.html")]
    return path.rstrip("/")


def _select(source_key, source_url, html, posts, domain):
    parser = _References(html)
    parser.feed(html)
    parser.close()
    parser.flush()
    references, edits, seen = [], [], set()
    number = 0
    for href, excerpt, position, raw, anchor_id in parser.references:
        try:
            resolved = urlsplit(urljoin(f"https://{domain}{source_url}", href.strip()))
            if (resolved.scheme not in {"http", "https"}
                    or resolved.hostname != domain
                    or resolved.username is not None
                    or resolved.port not in {None, 80, 443}):
                continue
        except ValueError:
            continue
        target = posts.get(_post_path(resolved.path))
        if target is None:
            continue
        target_key, target_url = target
        if target_key == source_key or target_key in seen:
            continue
        seen.add(target_key)
        if not anchor_id:
            while True:
                number += 1
                anchor_id = f"post-reference-{number}"
                if anchor_id not in parser.ids:
                    break
            parser.ids.add(anchor_id)
            # Insert one attribute; do not serialize or rewrite the authored HTML.
            end = len(raw) - (2 if raw.endswith("/>") else 1)
            edits.append((position + end, f' id="{anchor_id}"'))
        references.append({
            "source": source_key,
            "target": target_key,
            "url": urlunsplit(("", "", target_url, resolved.query, resolved.fragment)),
            "source_url": source_url + "#" + quote(anchor_id, safe=""),
            "excerpt": excerpt,
        })
    return references, edits


def collect_references(entries: list[Entry], rendered: dict[str, str]) -> list[dict]:
    """Read raw bodies before term enhancement; return the first anchor per pair.

    Each directed edge has source/target keys, a canonical target URL (including
    query and fragment), a source_url passage anchor, and a plain-text excerpt
    of at most 322 characters. Existing anchor IDs are reused. New IDs use
    post-reference-N, counting per source and skipping all existing IDs.
    """
    domain = (ROOT / "CNAME").read_text(encoding="utf-8").strip().lower()
    posts = {_post_path(entry.url): (entry.key, entry.url) for entry in entries}
    references = []
    for source in entries:
        selected, _ = _select(source.key, source.url, rendered.get(source.key, ""), posts, domain)
        references.extend(selected)
    return references


def annotate_references(rendered: dict[str, str], references: list[dict]) -> dict[str, str]:
    """Return fresh HTML with passage IDs on the collected reference anchors.

    Call with the same raw rendered bodies passed to collect_references, before
    term enhancement. Preserve every original character except inserted ID
    attributes. Existing anchor IDs need no edit.
    """
    domain = (ROOT / "CNAME").read_text(encoding="utf-8").strip().lower()
    grouped = {}
    for reference in references:
        grouped.setdefault(reference["source"], []).append(reference)
    result = dict(rendered)
    for key, edges in grouped.items():
        posts = {
            _post_path(urlsplit(edge["url"]).path): (edge["target"], urlsplit(edge["url"]).path)
            for edge in edges
        }
        source_url = urlsplit(edges[0]["source_url"]).path
        _, edits = _select(key, source_url, rendered[key], posts, domain)
        for position, attribute in reversed(edits):
            result[key] = result[key][:position] + attribute + result[key][position:]
    return result


def nearest_posts(connection: sqlite3.Connection, dimension: int, limit: int = 3) -> dict[str, list[dict]]:
    """Read the caller's transaction without opening, committing, or closing it.

    Compare complete, uncentered float32 vectors with float64 arithmetic.
    Zero-norm posts have no neighbors and are not candidates for other posts.
    Equal scores sort by post key. Scores are cosine similarities, not distances.
    """
    if dimension < 1:
        raise ValueError("Embedding dimension must be positive.")
    if limit < 0:
        raise ValueError("Neighbor limit must not be negative.")
    rows = connection.execute("SELECT slug, embedding FROM posts ORDER BY slug").fetchall()
    result = {key: [] for key, _ in rows}
    if not rows or not limit:
        return result
    vectors = np.empty((len(rows), dimension), dtype=np.float64)
    for index, (_, blob) in enumerate(rows):
        vectors[index] = np.frombuffer(blob, dtype="<f4", count=dimension)
    norms = np.linalg.norm(vectors, axis=1)
    valid = np.isfinite(vectors).all(axis=1) & np.isfinite(norms) & (norms > 0)
    vectors[valid] /= norms[valid, None]
    for index, (key, _) in enumerate(rows):
        if not valid[index]:
            continue
        scores = vectors @ vectors[index]
        candidates = [
            {"key": other_key, "score": float(np.clip(scores[other], -1.0, 1.0))}
            for other, (other_key, _) in enumerate(rows)
            if other != index and valid[other]
        ]
        result[key] = sorted(candidates, key=lambda item: (-item["score"], item["key"]))[:limit]
    return result
