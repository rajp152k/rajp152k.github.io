# /usr/bin/env python3
"""Build the Markdown meditation archive and its lexical search surface."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote

from archive import ROOT, Post, meditations, visible_blocks
from embedding_state import (
    DATABASE,
    PreparedPost,
    check_fresh,
    export_public,
    load_spec,
    open_database,
    prepare_posts,
)
from projection import Projection, project

README = ROOT / "README.md"
SITE = ROOT / "site"
ACCOUNTS = ROOT / "accounts.json"
START = "<!-- meditations:start -->"
END = "<!-- meditations:end -->"


def update_readme(items: list[Post]) -> None:
    table = ["| Date | Meditation |", "| --- | --- |"]
    table.extend(
        f"| {published.isoformat()} | [{title.replace('|', '\\|')}](meditations/{slug}.md) |"
        for published, title, slug, _ in items
    )
    replacement = "\n".join((START, *table, END))
    readme = README.read_text()
    updated, count = re.subn(
        f"{re.escape(START)}.*?{re.escape(END)}", replacement, readme, flags=re.DOTALL
    )
    if count != 1:
        raise ValueError("README.md must contain one meditation index marker pair")
    README.write_text(updated)


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


def site_header(account_menu: str, *, index: bool = False) -> str:
    title_tag = "h1" if index else "span"
    return f"""<header class="site-header">
  <{title_tag} class="site-title"><a class="site-name" href="/" aria-label="Meditations of yet another raj — index">meditations of yet another raj</a></{title_tag}>
  <form class="search-form" role="search" action="/search/" method="get">
    <label for="search-query">search</label>
    <input id="search-query" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="words…" aria-describedby="search-help">
    <button type="submit">go</button>
    <button class="search-clear" type="reset" aria-label="Clear search">clear</button>
    <span class="visually-hidden" id="search-help">All words required. Word prefixes of three or more characters also match. No phrase or operator syntax.</span>
  </form>
  {account_menu}
</header>"""


def post_attributes(published, post_id: str, title: str, slug: str) -> str:
    return (
        f'data-post="{escape(slug, quote=True)}" '
        f'data-post-id="{post_id}" '
        f'data-title="{escape(title, quote=True)}" '
        f'data-date="{published.isoformat()}"'
    )


def render_map(
    items: list[Post], projection: Projection, post_ids: dict[str, str], *, search: bool
) -> str:
    points = list(projection.points.values())
    if points:
        xs, ys = zip(*points)
        x_span, y_span = max(xs) - min(xs), max(ys) - min(ys)
        scales = [size / span for size, span in ((512, x_span), (400, y_span)) if span > 0]
        scale = min(scales) if scales else 1
        x_center, y_center = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    else:
        scale, x_center, y_center = 1, 0, 0
    origin_x, origin_y = 320 - x_center * scale, 260 + y_center * scale
    nodes = []
    for published, title, slug, _ in items:
        post_id = post_ids[slug]
        score_x, score_y = projection.points[slug]
        x, y = 320 + (score_x - x_center) * scale, 260 - (score_y - y_center) * scale
        url = f"/{quote(slug, safe='')}/"
        navigation = 'tabindex="-1" aria-hidden="true"' if search else f'href="{url}" tabindex="0"'
        context = " is-context" if search else ""
        nodes.append(f"""<a class="map-point{context}" {navigation} data-url="{url}"
    aria-label="{post_id} — {escape(title, quote=True)} — {published.isoformat()}" {post_attributes(published, post_id, title, slug)}>
  <circle class="map-hit" cx="{x:.3f}" cy="{y:.3f}" r="24"/>
  <circle class="map-halo" cx="{x:.3f}" cy="{y:.3f}" r="14"/>
  <circle class="map-dot" cx="{x:.3f}" cy="{y:.3f}" r="6"/>
</a>""")
    empty = '<text class="map-empty" x="320" y="260">Publish a meditation to begin the map.</text>' if not nodes else ""
    context_nodes = "".join(nodes) if search else ""
    match_nodes = "" if search else "".join(nodes)
    return f"""<svg class="embedding-map" viewBox="0 0 640 520"
    role="group" aria-labelledby="map-title" aria-describedby="map-description">
  <desc id="map-description">Archive-wide PCA projection of post embeddings. Nearby points suggest similar text. In search, faint points are noninteractive context. Matching points link to posts; hover or focus reveals identity below.</desc>
  <g aria-hidden="true">
    <path class="map-axes" d="M 32 {origin_y:.3f} H 608 M {origin_x:.3f} 32 V 488"/>
    <text class="map-axis-label" x="604" y="{max(44, origin_y - 8):.3f}" text-anchor="end">PC1</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="42">PC2</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="{origin_y + 16:.3f}">0</text>
  </g>
  <g class="map-context">{context_nodes}</g>
  <g class="map-matches">{match_nodes}</g>
  {empty}
</svg>"""


def render_archive(
    items: list[Post], projection: Projection, dimension: int, model_id: str,
    account_menu: str, post_ids: dict[str, str], *, search: bool,
) -> str:
    id_width = len(f"x{max(len(items) - 1, 0):x}")
    rows = []
    for published, title, slug, _ in items:
        hidden = " hidden" if search else ""
        excerpt_id = f"excerpt-{quote(slug, safe='')}"
        excerpt = f'<span class="post-excerpt" id="{excerpt_id}" hidden></span>' if search else ""
        rows.append(
            f'<tr data-post="{escape(slug, quote=True)}"{hidden}><td class="archive-date"><time datetime="{published.isoformat()}">{published.isoformat()}</time></td>'
            f'<td class="post-cell"><a class="post-link" href="/{quote(slug, safe="")}/" '
            f'aria-label="{post_ids[slug]} {escape(title, quote=True)}" '
            f'{post_attributes(published, post_ids[slug], title, slug)}><span class="post-id">{post_ids[slug]}</span> '
            f'<span class="post-title">{escape(title)}</span>{excerpt}</a></td></tr>'
        )
    if not rows and not search:
        rows.append('<tr><td colspan="2" class="archive-empty">No meditations published yet.</td></tr>')
    variance = f"{projection.variance:.0%} variance" if projection.variance is not None else "zero variance"
    heading = "Matches" if search else "Index"
    count = '<span class="panel-meta search-count" role="status" aria-live="polite" aria-atomic="true">Search</span>' if search else f'<span class="panel-meta">{len(items)} posts</span>'
    message = '<p class="search-message" hidden></p><noscript><p class="archive-empty">Search needs JavaScript. <a href="/">Browse the full index</a>.</p></noscript>' if search else ""
    return f"""{site_header(account_menu, index=True)}
<main class="workspace">
  <section class="panel archive-panel" aria-labelledby="archive-title">
    <header class="panel-head"><h2 id="archive-title">{heading}</h2>{count}</header>
    <div class="archive-scroll" tabindex="0" role="region" aria-label="Meditations">
      {message}
      <table class="archive-table" style="--post-id-width: {id_width}ch">
        <colgroup><col class="date-column"><col></colgroup>
        <thead><tr><th scope="col">Published</th><th scope="col">Meditation</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
  </section>
  <section class="panel map-panel" aria-labelledby="map-title">
    <header class="panel-head">
      <h2 id="map-title">PCA <a class="model-card" href="https://huggingface.co/{quote(model_id, safe='/')}" aria-label="Embedding model card: {escape(model_id)}">{escape(model_id.rsplit('/', 1)[-1])}</a></h2>
      <span class="panel-meta" title="Archive-wide input dimensions → displayed dimensions / embedding variance retained">{dimension} → 2 / {variance}</span>
    </header>
    <div class="map-stage">{render_map(items, projection, post_ids, search=search)}</div>
    <footer class="map-footer">
      <div class="map-readout"><span class="map-readout-id">—</span><span class="map-readout-title"></span><span class="map-readout-date"></span></div>
    </footer>
  </section>
</main>"""


def page(
    title: str, content: str, assets: dict[str, str], *, kind: str, search_index: str = ""
) -> str:
    if kind in {"index", "search"}:
        scripts = f'<script type="module" src="{assets[kind]}"></script>'
        classes = "index-page" + (" search-page" if kind == "search" else "")
    else:
        scripts = """<script>
    window.MathJax = {tex: {inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}};
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-mml-chtml-nofont.js"></script>"""
        classes = "post-page"
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
<body class="{classes}"{data}>
{content}
</body>
</html>
"""


def node_output(script: str, *args: str, source: str | None = None) -> str:
    if shutil.which("node") is None:
        raise RuntimeError("Publishing needs Node.js 24+ and npm ci for search assets.")
    result = subprocess.run(
        ["node", str(ROOT / "scripts" / script), *args], input=source,
        capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
    )
    if result.returncode:
        raise RuntimeError(f"Search asset build failed; run npm ci.\n{result.stderr.strip()}")
    return result.stdout


def build(items: list[Post]) -> None:
    if any(post[2] == "search" for post in items):
        raise ValueError("The post slug 'search' is reserved for the search page. Rename meditations/search.md.")
    spec = load_spec()
    prepared = prepare_posts(items, spec)
    connection = open_database(DATABASE)
    try:
        connection.execute("BEGIN")
        check_fresh(connection, prepared, spec)
        projection = project(connection, spec["dimension"])
        build_site(items, connection, prepared, spec, projection)
    finally:
        connection.close()


def build_site(
    items: list[Post], connection: sqlite3.Connection, prepared: list[PreparedPost],
    spec: dict, projection: Projection,
) -> None:
    import markdown

    account_menu = render_account_menu()
    post_ids = {post[2]: f"x{index:x}" for index, post in enumerate(reversed(items))}
    documents = [
        {"slug": slug, "title": title, "date": published.isoformat(),
         "url": f"/{quote(slug, safe='')}/", "postId": post_ids[slug], "blocks": visible_blocks(post)}
        for post in items for published, title, slug, _ in [post]
    ]
    payload = node_output("build_search.mjs", source=json.dumps(documents, ensure_ascii=False)).encode("utf-8")
    index_name = f"search-index.{hashlib.sha256(payload).hexdigest()}.json"

    # Complete dependency/index/bundle work before replacing the previous preview.
    with TemporaryDirectory(prefix="blog-assets-") as directory:
        assets = json.loads(node_output("build_assets.mjs", directory))
        if SITE.exists():
            shutil.rmtree(SITE)
        SITE.mkdir()
        shutil.copytree(Path(directory), SITE, dirs_exist_ok=True)
        (SITE / index_name).write_bytes(payload)
        export_public(connection, SITE / "blog.sqlite", prepared, spec)
        for kind, destination, title in (
            ("index", SITE, "yet another raj"),
            ("search", SITE / "search", "Search — yet another raj"),
        ):
            destination.mkdir(exist_ok=True)
            content = render_archive(
                items, projection, spec["dimension"], spec["model"], account_menu,
                post_ids, search=kind == "search",
            )
            (destination / "index.html").write_text(
                page(title, content, assets, kind=kind, search_index=f"/{index_name}"), encoding="utf-8"
            )
        for published, title, slug, body in items:
            destination = SITE / slug
            destination.mkdir()
            html = markdown.markdown(body, extensions=["fenced_code", "tables"])
            content = f"""{site_header(account_menu)}
<main class="reading-shell">
  <nav class="post-navigation" aria-label="Archive"><a class="back-link" href="/">← index</a></nav>
  <article class="article-content">
    <p class="post-meta"><time datetime="{published.isoformat()}">{published.isoformat()}</time></p>
    <h1>{escape(title)}</h1>{html}
  </article>
</main>"""
            (destination / "index.html").write_text(page(title, content, assets, kind="post"), encoding="utf-8")
        shutil.copy(ROOT / "CNAME", SITE / "CNAME")


def main() -> None:
    try:
        items = meditations()
        if "--readme" in sys.argv:
            update_readme(items)
            return
        build(items)
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(f"publish: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
