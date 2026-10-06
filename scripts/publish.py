#!/usr/bin/env python3
"""Build the meditation/log archive, shared PCA, and lexical search surface."""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote, unquote

from archive import ROOT, Entry, display_ids, read_entries, visible_blocks
from embedding_state import (
    DATABASE, PreparedEntry, check_fresh, export_public, load_spec,
    open_database, prepare_entries,
)
from projection import Projection, project

SITE = ROOT / "site"
ACCOUNTS = ROOT / "accounts.json"
COLLECTIONS = {"all": "/", "meditations": "/meditations/", "logs": "/logs/"}


def render_account_menu() -> str:
    accounts = json.loads(ACCOUNTS.read_text(encoding="utf-8"))
    links = []
    for account in accounts:
        label = escape(account["label"], quote=True)
        icon = (ROOT / "assets" / "icons" / f"{account['icon']}.svg").read_text(encoding="utf-8")
        links.append(
            f'<a class="account-link" href="{escape(account["url"], quote=True)}" '
            f'aria-label="{label}" title="{label}">{icon}</a>'
        )
    return f'<nav class="account-menu" aria-label="Accounts">{"".join(links)}</nav>'


def site_header(account_menu: str, *, index: bool = False, scope: str = "all") -> str:
    title_tag = "h1" if index else "span"
    return f"""<header class="site-header">
  <{title_tag} class="site-title"><a class="site-name" href="/" aria-label="Meditations of yet another raj — index">meditations of yet another raj</a></{title_tag}>
  <form class="search-form" role="search" action="/search/" method="get">
    <input name="kind" type="hidden" value="{scope}">
    <label for="search-query">search</label>
    <input id="search-query" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="words…" aria-describedby="search-help">
    <button type="submit">go</button>
    <button class="search-clear" type="reset" aria-label="Clear search">clear</button>
    <span class="visually-hidden" id="search-help">All words required. Word prefixes of three or more characters also match. No phrase or operator syntax. Collection can be selected on the results page.</span>
  </form>
  {account_menu}
</header>"""


def collection_nav(scope: str, *, search: bool = False) -> str:
    links = []
    for kind, url in COLLECTIONS.items():
        if search:
            url = "/search/" + (f"?kind={kind}" if kind != "all" else "")
        current = ' aria-current="page"' if kind == scope else ""
        links.append(f'<a href="{url}" data-kind="{kind}"{current}>{kind}</a>')
    return f'<nav class="collection-nav" aria-label="Collections">{"".join(links)}</nav>'


def post_attributes(entry: Entry, code: str) -> str:
    return (
        f'data-post="{escape(entry.key, quote=True)}" data-kind="{entry.kind}" '
        f'data-post-id="{code}" data-title="{escape(entry.title, quote=True)}" '
        f'data-date="{entry.published_iso}" data-display-date="{entry.date_label}" data-url="{escape(entry.url, quote=True)}"'
    )


def render_map(entries: list[Entry], projection: Projection, codes: dict[str, str], selected: set[str]) -> str:
    points = list(projection.points.values())
    if points:
        xs, ys = zip(*points)
        spans = (max(xs) - min(xs), max(ys) - min(ys))
        scales = [size / span for size, span in zip((512, 400), spans) if span > 0]
        scale = min(scales) if scales else 1
        center_x, center_y = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    else:
        scale, center_x, center_y = 1, 0, 0
    origin_x, origin_y = 320 - center_x * scale, 260 + center_y * scale
    context_nodes, match_nodes = [], []
    for entry in entries:
        score_x, score_y = projection.points[entry.key]
        x, y = 320 + (score_x - center_x) * scale, 260 - (score_y - center_y) * scale
        matches = entry.key in selected
        navigation = f'href="{escape(entry.url, quote=True)}" tabindex="0"' if matches else 'tabindex="-1" aria-hidden="true"'
        classes = "map-point" + (" is-log" if entry.kind == "logs" else "") + (" is-context" if not matches else "")
        label = f"{entry.kind} {codes[entry.key]} — {entry.title} — {entry.published_iso}"
        node = f"""<a class="{classes}" {navigation} aria-label="{escape(label, quote=True)}" {post_attributes(entry, codes[entry.key])}>
  <circle class="map-hit" cx="{x:.3f}" cy="{y:.3f}" r="24"/>
  <circle class="map-halo" cx="{x:.3f}" cy="{y:.3f}" r="14"/>
  <circle class="map-dot" cx="{x:.3f}" cy="{y:.3f}" r="6"/>
</a>"""
        (match_nodes if matches else context_nodes).append(node)
    empty = '<text class="map-empty" x="320" y="260">Publish an entry to begin the map.</text>' if not entries else ""
    return f"""<svg class="embedding-map" viewBox="0 0 640 520" role="group" aria-labelledby="map-title" aria-describedby="map-description">
  <desc id="map-description">Archive-wide PCA of meditation and log text. Filled circles are meditations; outlined circles are logs. Nearby points suggest similar text. Faint points are noninteractive context. Hover or focus reveals identity below.</desc>
  <g aria-hidden="true">
    <path class="map-axes" d="M 32 {origin_y:.3f} H 608 M {origin_x:.3f} 32 V 488"/>
    <text class="map-axis-label" x="604" y="{max(44, origin_y - 8):.3f}" text-anchor="end">PC1</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="42">PC2</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="{origin_y + 16:.3f}">0</text>
  </g>
  <g class="map-context">{''.join(context_nodes)}</g>
  <g class="map-matches">{''.join(match_nodes)}</g>
  {empty}
</svg>"""


def render_archive(
    entries: list[Entry], projection: Projection, dimension: int, model_id: str,
    account_menu: str, codes: dict[str, str], *, scope: str = "all", search: bool = False,
) -> str:
    visible = [entry for entry in entries if scope == "all" or entry.kind == scope]
    selected = set() if search else {entry.key for entry in visible}
    rows = []
    for entry in entries if search else visible:
        hidden = " hidden" if search else ""
        excerpt_id = f"excerpt-{quote(entry.key, safe='')}"
        excerpt = f'<span class="post-excerpt" id="{excerpt_id}" hidden></span>' if search else ""
        rows.append(
            f'<tr data-post="{escape(entry.key, quote=True)}" data-kind="{entry.kind}"{hidden}>'
            f'<td class="archive-date"><time datetime="{entry.published_iso}">{entry.date_label}</time></td>'
            f'<td class="post-cell"><a class="post-link" href="{escape(entry.url, quote=True)}" '
            f'aria-label="{entry.kind} {codes[entry.key]} {escape(entry.title, quote=True)}" '
            f'{post_attributes(entry, codes[entry.key])}><span class="post-id">{codes[entry.key]}</span> '
            f'<span class="post-title">{escape(entry.title)}</span>{excerpt}</a></td></tr>'
        )
    if not rows and not search:
        rows.append('<tr><td colspan="2" class="archive-empty">No entries published in this collection yet.</td></tr>')
    variance = f"{projection.variance:.0%} variance" if projection.variance is not None else "zero variance"
    count = '<span class="panel-meta search-count" role="status" aria-live="polite" aria-atomic="true">Search</span>' if search else f'<span class="panel-meta">{len(visible)} entries</span>'
    message = '<p class="search-message" hidden></p><noscript><p class="archive-empty">Search needs JavaScript. <a href="/">Browse the full index</a> or choose <a href="/meditations/">meditations</a> / <a href="/logs/">logs</a>.</p></noscript>' if search else ""
    id_width = max((len(code) for code in codes.values()), default=3)
    return f"""{site_header(account_menu, index=True, scope=scope)}
<main class="workspace">
  <section class="panel archive-panel" aria-labelledby="archive-title">
    <header class="panel-head"><h2 id="archive-title">{'Matches' if search else 'Index'}</h2>{count}</header>
    {collection_nav(scope, search=search)}
    <div class="archive-scroll" tabindex="0" role="region" aria-label="Archive entries">
      {message}
      <table class="archive-table" style="--post-id-width: {id_width}ch">
        <colgroup><col class="date-column"><col></colgroup>
        <thead><tr><th scope="col">Published</th><th scope="col">Entry</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
  </section>
  <section class="panel map-panel" aria-labelledby="map-title">
    <header class="panel-head">
      <h2 id="map-title">PCA <a class="model-card" href="https://huggingface.co/{quote(model_id, safe='/')}" aria-label="Embedding model card: {escape(model_id)}">{escape(model_id.rsplit('/', 1)[-1])}</a></h2>
      <span class="panel-meta" title="Combined archive input dimensions → displayed dimensions / embedding variance retained">{dimension} → 2 / {variance}</span>
    </header>
    <div class="map-legend"><span class="legend-meditation" aria-hidden="true"></span>meditations <span class="legend-log" aria-hidden="true"></span>logs</div>
    <div class="map-stage">{render_map(entries, projection, codes, selected)}</div>
    <footer class="map-footer"><div class="map-readout"><span class="map-readout-id">—</span><span class="map-readout-title"></span><span class="map-readout-date"></span></div></footer>
  </section>
</main>"""


def entry_content(entry: Entry, code: str, account_menu: str) -> str:
    import markdown

    body = markdown.markdown(entry.body, extensions=["fenced_code", "tables"])
    timestamp = entry.published_iso.replace("T", " ").replace("+00:00", " UTC").replace("Z", " UTC")
    identity = f"{code} · meditation · " if entry.kind == "meditations" else ""
    return f"""{site_header(account_menu, scope=entry.kind)}
<main class="reading-shell">
  <nav class="post-navigation" aria-label="Archive"><a class="back-link" href="{COLLECTIONS[entry.kind]}">← {entry.kind}</a> · <a class="back-link" href="/">all entries</a></nav>
  <article class="article-content">
    <p class="post-meta">{identity}<time datetime="{entry.published_iso}">{timestamp}</time></p>
    <h1>{escape(entry.title)}</h1>{body}
  </article>
</main>"""


def page(title: str, content: str, assets: dict[str, str], *, kind: str, scope: str = "all", search_index: str = "") -> str:
    if kind in {"index", "search"}:
        scripts = f'<script type="module" src="{assets[kind]}"></script>'
        classes = "index-page" + (" search-page" if kind == "search" else "")
    else:
        scripts = """<script>
    window.MathJax = {tex: {inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}};
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-mml-chtml-nofont.js"></script>"""
        if '<code class="language-mermaid">' in content:
            scripts += f'\n  <script type="module" src="{assets["article"]}"></script>'
        classes = "post-page" + (" log-page" if scope == "logs" else "")
    data = f' data-search-index="{search_index}"' if kind == "search" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{assets['style']}">
  {scripts}
</head>
<body class="{classes}" data-kind="{scope}"{data}>
{content}
</body>
</html>
"""


def node_output(script: str, *args: str, source: str | None = None) -> str:
    if shutil.which("node") is None:
        raise RuntimeError("Publishing needs Node.js 24+ and npm ci for search assets.")
    result = subprocess.run(["node", str(ROOT / "scripts" / script), *args], input=source,
                            capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    if result.returncode:
        raise RuntimeError(f"Search asset build failed; run npm ci.\n{result.stderr.strip()}")
    return result.stdout


def build(entries: list[Entry]) -> None:
    spec = load_spec()
    prepared = prepare_entries(entries, spec)
    connection = open_database(DATABASE)
    try:
        connection.execute("BEGIN")
        check_fresh(connection, prepared, spec)
        projection = project(connection, spec["dimension"])
        build_site(entries, connection, prepared, spec, projection)
    finally:
        connection.close()


def build_site(entries: list[Entry], connection: sqlite3.Connection, prepared: list[PreparedEntry], spec: dict, projection: Projection) -> None:
    account_menu = render_account_menu()
    codes = display_ids(entries)
    documents = [{"key": entry.key, "slug": entry.slug, "kind": entry.kind, "title": entry.title,
                  "date": entry.published_iso, "url": entry.url, "postId": codes[entry.key], "blocks": visible_blocks(entry)}
                 for entry in entries]
    payload = node_output("build_search.mjs", source=json.dumps(documents, ensure_ascii=False)).encode("utf-8")
    index_name = f"search-index.{hashlib.sha256(payload).hexdigest()}.json"
    # Stage the complete archive before replacing a preview.
    with TemporaryDirectory(prefix="blog-site-") as directory:
        staged = Path(directory)
        assets = json.loads(node_output("build_assets.mjs", directory))
        (staged / index_name).write_bytes(payload)
        export_public(connection, staged / "blog.sqlite", prepared, spec)
        for scope, url in COLLECTIONS.items():
            destination = staged / url.lstrip("/")
            destination.mkdir(parents=True, exist_ok=True)
            content = render_archive(entries, projection, spec["dimension"], spec["model"], account_menu, codes, scope=scope)
            title = "yet another raj" if scope == "all" else f"{scope.title()} — yet another raj"
            (destination / "index.html").write_text(page(title, content, assets, kind="index", scope=scope), encoding="utf-8")
        destination = staged / "search"
        destination.mkdir()
        content = render_archive(entries, projection, spec["dimension"], spec["model"], account_menu, codes, search=True)
        (destination / "index.html").write_text(page("Search — yet another raj", content, assets, kind="search", search_index=f"/{index_name}"), encoding="utf-8")
        for entry in entries:
            destination = staged / unquote(entry.url.lstrip("/"))
            destination.mkdir(parents=True)
            content = entry_content(entry, codes[entry.key], account_menu)
            (destination / "index.html").write_text(page(entry.title, content, assets, kind="post", scope=entry.kind), encoding="utf-8")
        shutil.copy(ROOT / "CNAME", staged / "CNAME")
        if SITE.exists():
            shutil.rmtree(SITE)
        shutil.copytree(staged, SITE)


def main() -> None:
    try:
        build(read_entries())
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(f"publish: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
