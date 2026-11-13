"""Render term pages and the desktop article reference panel from saved records."""
from __future__ import annotations

from html import escape
from typing import Iterable, Mapping

from archive import Entry
from terms import Mention, Term


def entry_link(entry: Entry, label: str | None = None) -> str:
    return f'<a href="{escape(entry.url, quote=True)}">{escape(label or entry.title)}</a>'


def reference_list(mentions: Iterable[Mention], *, current: str = "") -> str:
    rows = []
    for mention in mentions:
        if mention.entry_key == current:
            continue
        rows.append(
            f'<li><a href="{escape(mention.url, quote=True)}">{escape(mention.title)}</a>'
            f'<div class="term-meta">{escape(mention.date)}</div>'
            f'<p class="term-excerpt">{escape(mention.excerpt)}</p></li>'
        )
    return f'<ul class="term-sources">{"".join(rows)}</ul>' if rows else '<p class="term-meta">No other posts yet.</p>'


def term_card(term: Term, entries: Mapping[str, Entry], mentions: Iterable[Mention], *, current: str = "", heading: str = "h3") -> str:
    introduction = entries[term.introduction]
    subheading = "h2" if heading == "h1" else "h4"
    # Keep every evidence quote, but link each post only once in the card.
    grouped_sources: dict[str, list[str]] = {}
    for source in term.sources:
        grouped_sources.setdefault(source.entry, []).append(source.quote)
    source_rows = []
    for key, quotes in grouped_sources.items():
        start_label = ' <span class="term-meta">(Start here)</span>' if key == term.introduction else ""
        excerpts = "".join(f'<p class="term-excerpt">{escape(quote)}</p>' for quote in quotes)
        source_rows.append(f'<li>{entry_link(entries[key])}{start_label}{excerpts}</li>')
    sources = "".join(source_rows)
    start = "" if term.introduction in grouped_sources else (
        f'<p class="term-meta">Start here: {entry_link(introduction)}</p>'
    )
    linked = set(grouped_sources) | {term.introduction}
    other_mentions = [mention for mention in mentions if mention.entry_key not in linked]
    return (
        f'<{heading} tabindex="-1">{escape(term.name)}</{heading}>'
        f'<p>{escape(term.definition)}</p>'
        f'{start}'
        f'<{subheading}>Definition sources</{subheading}><ul class="term-sources">{sources}</ul>'
        f'<{subheading}>Other posts</{subheading}>'
        f'{reference_list(other_mentions, current=current)}'
    )


def article_panel(terms: Iterable[Term], entries: Mapping[str, Entry], mentions: Iterable[Mention], current: str) -> str:
    terms, mentions = tuple(terms), tuple(mentions)
    if not terms:
        return ""
    rows, templates = [], []
    for term in terms:
        rows.append(f'<li><button type="button" data-select-term="{term.id}">{escape(term.name)}</button></li>')
        relevant = [mention for mention in mentions if mention.term_id == term.id]
        card = term_card(term, entries, relevant, current=current)
        templates.append(
            f'<template data-term-card="{term.id}">{card}'
            f'<p><a href="{term.url}">Full reference</a></p></template>'
        )
    return f'''<aside id="terms-panel" class="terms-panel" aria-labelledby="terms-panel-title" hidden>
  <div class="terms-panel-header"><h2 id="terms-panel-title">Terms and references</h2><button type="button" data-terms-close aria-label="Close references">close</button></div>
  <button type="button" data-terms-back hidden>Terms in this post</button>
  <div data-terms-list><p class="term-meta">Terms in this post. Select a name or a dotted reference in the article.</p><ul>{"".join(rows)}</ul><a href="/terms/">Browse all terms</a></div>
  <div data-terms-content></div>
</aside>{"".join(templates)}'''


def terms_index(terms: Iterable[Term]) -> str:
    rows = "".join(
        f'<li><h2><a href="{term.url}">{escape(term.name)}</a></h2><p>{escape(term.definition)}</p></li>'
        for term in sorted(terms, key=lambda term: (term.name.casefold(), term.id))
    )
    return f'<h1>Terms and references</h1><p>Names and ideas from the archive. Select a term for its sources and related posts.</p><ul class="term-page-list">{rows}</ul>'
