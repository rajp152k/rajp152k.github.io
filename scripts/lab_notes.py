"""Render measured map details and explicit post references for the lab journal."""
from html import escape


def post_link(entry, codes, url=None):
    return (f'<a href="{escape(url or entry.url, quote=True)}">'
            f'<span class="note-id">{escape(codes[entry.key])}</span> {escape(entry.title)}</a>')


def reference_rows(entry, entries, codes, references, *, incoming=False):
    rows = []
    for reference in references:
        if reference["target" if incoming else "source"] != entry.key:
            continue
        other = entries[reference["source" if incoming else "target"]]
        url = reference.get("source_url", other.url) if incoming else reference["url"]
        passage = reference.get("source_url", entry.url)
        evidence = (f'<a class="passage-link" href="{escape(passage, quote=True)}">source passage</a>'
                    if not incoming else "")
        rows.append(f'<li>{post_link(other, codes, url)}{evidence}'
                    f'<p class="reference-excerpt">{escape(reference["excerpt"])}</p></li>')
    return "".join(rows)


def relationship_sections(entry, entries, codes, references, nearest=()):
    sections = []
    for incoming, title in ((False, "References"), (True, "Referenced by")):
        rows = reference_rows(entry, entries, codes, references, incoming=incoming)
        count = sum(reference["target" if incoming else "source"] == entry.key for reference in references)
        content = f'<ol>{rows}</ol>' if rows else '<p class="term-meta">No explicit post references.</p>'
        sections.append(f'<section><h3>{title} <span class="note-count">{count}</span></h3>{content}</section>')
    if nearest is not None:
        rows = "".join(f'<li>{post_link(entries[item["key"]], codes)} '
                       f'<span class="similarity-score">{item["score"]:.3f}</span></li>' for item in nearest)
        content = f'<ol>{rows}</ol>' if rows else '<p class="term-meta">No comparable vectors.</p>'
        sections.append(f'<section><h3>Nearest by cosine</h3>{content}'
                        '<p class="term-meta">Full embedding vectors; across the archive. Similarity is not a citation.</p></section>')
    return '<div class="relationship-sections">' + "".join(sections) + '</div>'


def map_inspector(entries, codes, references, nearest):
    by_key = {entry.key: entry for entry in entries}
    options, templates = [], []
    for entry in entries:
        key = escape(entry.key, quote=True)
        label = escape(f'{codes[entry.key]} {entry.title}')
        options.append(f'<option value="{key}">{label}</option>')
        content = relationship_sections(entry, by_key, codes, references, nearest.get(entry.key, ()))
        templates.append(f'<template data-map-note="{key}">{content}</template>')
    return ('<div class="map-inspector" hidden><label for="map-inspect">Inspect</label>'
            '<select id="map-inspect"><option value="">Choose a post</option>' + "".join(options) + '</select>'
            '<button type="button" data-map-reset aria-label="Clear inspected post">clear</button></div>'
            '<div class="map-details" hidden></div>' + "".join(templates))


def post_notes(entry, entries, codes, references):
    if not any(entry.key in (item["source"], item["target"]) for item in references):
        return ""
    content = relationship_sections(entry, entries, codes, references, nearest=None)
    return ('<aside class="post-relations" aria-labelledby="post-relations-title">'
            '<h2 id="post-relations-title">Post references</h2>' + content + '</aside>')
