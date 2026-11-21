"""Source-backed term records and deterministic HTML annotations.

Run ``python scripts/terms.py --check`` to validate records and report mentions.
No model calls or source changes occur during this check or a site build.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Mapping

from archive import ROOT, Entry, read_entries


@dataclass(frozen=True)
class Source:
    entry: str
    quote: str


@dataclass(frozen=True)
class Term:
    id: str
    name: str
    aliases: tuple[str, ...]
    definition: str
    introduction: str
    sources: tuple[Source, ...]
    annotation: str = "first-term"

    @property
    def url(self) -> str:
        return f"/terms/{self.id}/"


@dataclass(frozen=True)
class Registry:
    terms: tuple[Term, ...]

    @property
    def by_id(self) -> dict[str, Term]:
        return {term.id: term for term in self.terms}


@dataclass(frozen=True)
class Match:
    term_id: str
    text: str
    excerpt: str


@dataclass(frozen=True)
class TransformResult:
    html: str
    mentions: tuple[Match, ...]


@dataclass(frozen=True)
class Mention:
    term_id: str
    entry_key: str
    title: str
    entry_url: str
    date: str
    excerpt: str

    @property
    def url(self) -> str:
        return f"{self.entry_url}#term-{self.term_id}"


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key {key!r}.")
        result[key] = value
    return result


def _fields(value, required, label, optional=()):
    if not isinstance(value, dict) or not set(required) <= set(value) or set(value) - set(required) - set(optional):
        raise ValueError(f"{label} requires {', '.join(required)}; optional fields: {', '.join(optional) or 'none'}.")


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{label} must be nonempty text without outer whitespace.")
    return value


def _alias_key(value):
    return re.sub(r"\s+", " ", value).casefold()


def load_terms(entries: Iterable[Entry], path: Path = ROOT / "terms.json") -> Registry:
    """Load strict version-1 JSON; reject stale quotes and ambiguous aliases.

    Quotes are exact substrings of Entry.body (Markdown, excluding front matter).
    Introduction is an entry key, not an inferred earliest mention. Definitions
    are edited records; validation checks evidence integrity, not entailment.
    """
    entries = list(entries)
    by_key = {entry.key: entry for entry in entries}
    if len(by_key) != len(entries):
        raise ValueError("Duplicate archive entry keys.")
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_object)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(f"Invalid terms JSON: {error}") from error
    _fields(data, ("version", "terms"), "Registry")
    if type(data["version"]) is not int or data["version"] != 1:
        raise ValueError("Registry version must be integer 1.")
    if not isinstance(data["terms"], list):
        raise ValueError("terms must be a list.")
    terms, ids, aliases = [], set(), {}
    for row in data["terms"]:
        _fields(row, ("id", "name", "aliases", "definition", "introduction", "sources"), "Term", optional=("annotation",))
        annotation = row.get("annotation", "first-term")
        if annotation not in ("first-term", "first-spelling"):
            raise ValueError("annotation must be first-term or first-spelling.")
        for key in ("id", "name", "definition", "introduction"):
            _text(row[key], key)
        ident = row["id"]
        if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", ident) or ident in {"index", "search", "terms", "logs", "meditations"}:
            raise ValueError(f"Invalid or reserved term id {ident!r}.")
        if ident in ids:
            raise ValueError(f"Duplicate term id {ident!r}.")
        ids.add(ident)
        if not isinstance(row["aliases"], list):
            raise ValueError(f"{ident}: aliases must be a list.")
        local = set()
        for alias in [row["name"], *row["aliases"]]:
            _text(alias, "alias")
            key = _alias_key(alias)
            if key in local or key in aliases or any(re.fullmatch(re.escape(previous), re.sub(r"\s+", " ", alias), re.IGNORECASE) for previous in aliases.values()):
                raise ValueError(f"Duplicate or ambiguous alias {alias!r}.")
            local.add(key)
            aliases[key] = re.sub(r"\s+", " ", alias)
        if row["introduction"] not in by_key:
            raise ValueError(f"{ident}: unknown introduction {row['introduction']!r}.")
        if not isinstance(row["sources"], list) or not row["sources"]:
            raise ValueError(f"{ident}: sources must be a nonempty list.")
        sources, seen_sources = [], set()
        for source in row["sources"]:
            _fields(source, ("entry", "quote"), "Source")
            entry_key = _text(source["entry"], "source entry")
            quote = _text(source["quote"], "source quote")
            if entry_key not in by_key:
                raise ValueError(f"{ident}: unknown source {entry_key!r}.")
            if quote not in by_key[entry_key].body:
                raise ValueError(f"{ident}: stale source quote in {entry_key}; review definition and evidence.")
            if (entry_key, quote) in seen_sources:
                raise ValueError(f"{ident}: duplicate source.")
            seen_sources.add((entry_key, quote))
            sources.append(Source(entry_key, quote))
        terms.append(Term(ident, row["name"], tuple(row["aliases"]), row["definition"], row["introduction"], tuple(sources), annotation))
    return Registry(tuple(sorted(terms, key=lambda term: term.id)))


# These nodes are not prose references. Existing annotations are also excluded.
EXCLUDED = frozenset({
    "a", "code", "pre", "blockquote", "q", "script", "style", "textarea", "title",
    "h1", "h2", "h3", "h4", "h5", "h6", "nav", "button", "select",
    "option", "template", "svg", "math", "noscript", "kbd", "samp",
})
VOID = frozenset({"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"})
ENTITY = re.compile(r"&(?:#[xX][0-9a-fA-F]+;?|#[0-9]+;?|[a-zA-Z][a-zA-Z0-9]+;?)")


def _decoded_offsets(raw):
    """Map decoded characters back to untouched entity spellings."""
    text, ranges, pos = [], [], 0
    for match in ENTITY.finditer(raw):
        for index in range(pos, match.start()):
            text.append(raw[index])
            ranges.append((index, index + 1))
        decoded = unescape(match.group())
        text.extend(decoded)
        ranges.extend([(match.start(), match.end())] * len(decoded))
        pos = match.end()
    for index in range(pos, len(raw)):
        text.append(raw[index])
        ranges.append((index, index + 1))
    return "".join(text), ranges


class _ExistingTerms(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.anchors = {}
        self.reference_anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        anchor = attrs.get("id")
        if anchor:
            self.anchors[anchor] = self.anchors.get(anchor, 0) + 1
        if "term-reference" in (attrs.get("class") or "").split():
            ident = attrs.get("data-term")
            self.ids.add(ident)
            if anchor == f"term-{ident}":
                self.reference_anchors.add(anchor)


class _Annotator(HTMLParser):
    def __init__(self, html, registry):
        super().__init__(convert_charrefs=False)
        self.source = html
        self.lines = [0]
        self.lines.extend(match.end() for match in re.finditer("\n", html))
        self.stack = []
        self.run = None
        self.edits = []
        self.matches = []
        existing = _ExistingTerms()
        existing.feed(html)
        for term in registry.terms:
            anchor = f"term-{term.id}"
            if existing.anchors.get(anchor, 0) > 1:
                raise ValueError(f"Duplicate reserved term anchor {anchor!r}.")
            if anchor in existing.anchors and anchor not in existing.reference_anchors:
                raise ValueError(f"Reserved term anchor {anchor!r} is already used by source HTML.")
        self.seen = existing.ids
        self.existing = set(existing.ids)
        self.spellings = set()
        self.by_id = registry.by_id
        alternatives = [(alias, term.id) for term in registry.terms for alias in (term.name, *term.aliases)]
        alternatives.sort(key=lambda item: (-len(item[0]), item[0].casefold(), item[0]))
        self.owners = {}
        expressions = []
        for index, (alias, ident) in enumerate(alternatives):
            group = f"alias{index}"
            self.owners[group] = ident
            expression = r"\s+".join(re.escape(part) for part in alias.split())
            expressions.append(f"(?P<{group}>{expression})")
        self.pattern = re.compile(r"(?<!\w)(?:" + "|".join(expressions) + r")(?!\w)", re.IGNORECASE) if expressions else None

    def source_offset(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def flush(self, end):
        if self.run is None:
            return
        start, self.run = self.run, None
        if not self.pattern:
            return
        raw = self.source[start:end]
        text, offsets = _decoded_offsets(raw)
        for match in self.pattern.finditer(text):
            ident = self.owners[match.lastgroup]
            spelling = (ident, _alias_key(match.group()))
            if ident in self.existing or spelling in self.spellings:
                continue
            if ident in self.seen and self.by_id[ident].annotation == "first-term":
                continue
            left, right = offsets[match.start()][0], offsets[match.end() - 1][1]
            # Do not split an entity that expands to several Unicode characters.
            if (match.start() and offsets[match.start() - 1] == offsets[match.start()]) or (match.end() < len(offsets) and offsets[match.end()] == offsets[match.end() - 1]):
                continue
            first = ident not in self.seen
            self.seen.add(ident)
            self.spellings.add(spelling)
            anchor = f' id="term-{ident}"' if first else ""
            replacement = f'<span class="term-reference" data-term="{ident}"{anchor}>{raw[left:right]}</span>'
            self.edits.append((start + left, start + right, replacement))
            if first:
                excerpt = re.sub(r"\s+", " ", text[max(0, match.start() - 90):match.end() + 150]).strip()
                self.matches.append(Match(ident, match.group(), excerpt))

    def handle_starttag(self, tag, attrs):
        self.flush(self.source_offset())
        attrs = dict(attrs)
        excluded = tag in EXCLUDED or "term-reference" in (attrs.get("class") or "").split() or "hidden" in attrs or attrs.get("aria-hidden") == "true"
        if tag not in VOID:
            self.stack.append((tag, excluded or any(item[1] for item in self.stack)))

    def handle_startendtag(self, tag, attrs):
        self.flush(self.source_offset())

    def handle_endtag(self, tag):
        self.flush(self.source_offset())
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if not any(item[1] for item in self.stack) and self.run is None:
            self.run = self.source_offset()

    def handle_entityref(self, name):
        self.handle_data("")

    def handle_charref(self, name):
        self.handle_data("")

    def handle_comment(self, data):
        self.flush(self.source_offset())

    def handle_decl(self, decl):
        self.flush(self.source_offset())

    def handle_pi(self, data):
        self.flush(self.source_offset())


def transform_html(html: str, registry: Registry) -> TransformResult:
    """Mark the first eligible occurrence per term, or per spelling when opted in.

    Match Unicode word boundaries, case-insensitively, longest alias first.
    Whitespace in aliases matches any prose whitespace. Matches may include
    entities but do not cross HTML tags. All other HTML bytes are preserved.
    """
    parser = _Annotator(html, registry)
    parser.feed(html)
    parser.close()
    parser.flush(len(html))
    result = html
    for start, end, replacement in reversed(parser.edits):
        result = result[:start] + replacement + result[end:]
    return TransformResult(result, tuple(parser.matches))


def collect_mentions(entries: Iterable[Entry], registry: Registry, rendered_by_key: Mapping[str, str] | None = None) -> tuple[Mention, ...]:
    """Collect one eligible mention per term/post, newest posts first.

    Pass the builder's rendered article bodies to use precisely its HTML.
    Without them, render Markdown with the archive's standard extensions.
    """
    import markdown
    mentions = []
    for entry in sorted(entries, key=lambda item: item.sort_key, reverse=True):
        html = rendered_by_key[entry.key] if rendered_by_key is not None else markdown.markdown(entry.body, extensions=["fenced_code", "tables"])
        for match in transform_html(html, registry).mentions:
            mentions.append(Mention(match.term_id, entry.key, entry.title, entry.url, entry.date_label, match.excerpt))
    return tuple(mentions)


def terms_for_post(entry_key: str, mentions: Iterable[Mention], registry: Registry) -> tuple[Term, ...]:
    by_id = registry.by_id
    return tuple(by_id[mention.term_id] for mention in mentions if mention.entry_key == entry_key)


def mentions_for_term(term_id: str, mentions: Iterable[Mention]) -> tuple[Mention, ...]:
    return tuple(mention for mention in mentions if mention.term_id == term_id)


def maintenance_report(entries: Iterable[Entry], registry: Registry, mentions: Iterable[Mention]) -> dict:
    """Report checked records and unmatched posts for editorial review.

    An unmatched post is a review candidate, not proof of a missing term.
    """
    entries = sorted(entries, key=lambda entry: entry.sort_key, reverse=True)
    mentions = tuple(mentions)
    matched_entries = {mention.entry_key for mention in mentions}
    return {
        "version": 1,
        "entries": len(entries),
        "terms": [
            {"id": term.id, "sources": len(term.sources), "mentions": len(mentions_for_term(term.id, mentions))}
            for term in registry.terms
        ],
        "mentions": [asdict(mention) for mention in mentions],
        "review_candidates": [
            {"entry": entry.key, "title": entry.title, "url": entry.url,
             "reason": "No matched terms. Review only; a term may not be needed."}
            for entry in entries if entry.key not in matched_entries
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate source records (also done by default).")
    parser.add_argument("--json", action="store_true", help="Print the deterministic maintenance report as JSON.")
    parser.add_argument("--terms", type=Path, default=ROOT / "terms.json")
    args = parser.parse_args(argv)
    try:
        entries = read_entries()
        registry = load_terms(entries, args.terms)
        mentions = collect_mentions(entries, registry)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Terms check failed: {error}\n")
    report = maintenance_report(entries, registry, mentions)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Terms are valid: {len(registry.terms)} terms, {len(entries)} entries, {len(mentions)} post references.")
        for row in report["terms"]:
            print(f"{row['id']}: {row['sources']} sources; {row['mentions']} post references")
        print(f"Review candidates without matched terms: {len(report['review_candidates'])} (a term may not be needed).")
        for candidate in report["review_candidates"]:
            print(f"  {candidate['entry']}: {candidate['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
