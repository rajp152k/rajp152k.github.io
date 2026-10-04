# /usr/bin/env python3
"""Build the Markdown meditation archive."""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import sys
from html import escape
from urllib.parse import quote

from archive import ROOT, Post, meditations
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
FONT = ROOT / "assets" / "FiraMono-Regular.ttf"
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
  {account_menu}
</header>"""


def post_attributes(published, post_id: str, slug: str) -> str:
    return (
        f'data-post="{escape(slug, quote=True)}" '
        f'data-post-id="{post_id}" '
        f'data-date="{published.isoformat()}"'
    )


def render_map(items: list[Post], projection: Projection, post_ids: dict[str, str]) -> str:
    points = list(projection.points.values())
    if points:
        xs, ys = zip(*points)
        x_low, x_high, y_low, y_high = min(xs), max(xs), min(ys), max(ys)
        x_span, y_span = x_high - x_low, y_high - y_low
        scales = [
            size / span
            for size, span in ((512, x_span), (400, y_span))
            if span > 0
        ]
        scale = min(scales) if scales else 1
        x_center, y_center = (x_low + x_high) / 2, (y_low + y_high) / 2
    else:
        scale, x_center, y_center = 1, 0, 0
    origin_x, origin_y = 320 - x_center * scale, 260 + y_center * scale
    nodes = []
    for published, title, slug, _ in items:
        post_id = post_ids[slug]
        score_x, score_y = projection.points[slug]
        x, y = 320 + (score_x - x_center) * scale, 260 - (score_y - y_center) * scale
        right = x > 320
        label_x, anchor = (x - 16, "end") if right else (x + 16, "start")
        nodes.append(f"""<a class="map-point" href="{quote(slug, safe='')}/" tabindex="0"
    aria-label="{post_id} — {escape(title, quote=True)} — {published.isoformat()}" {post_attributes(published, post_id, slug)}>
  <circle class="map-hit" cx="{x:.3f}" cy="{y:.3f}" r="24"/>
  <circle class="map-halo" cx="{x:.3f}" cy="{y:.3f}" r="14"/>
  <circle class="map-dot" cx="{x:.3f}" cy="{y:.3f}" r="6"/>
  <text class="map-label" x="{label_x:.3f}" y="{y - 16:.3f}" text-anchor="{anchor}">{post_id}</text>
</a>""")
    if not nodes:
        nodes.append('<text class="map-empty" x="320" y="260">Publish a meditation to begin the map.</text>')
    density = " many-points" if len(items) > 12 else ""
    return f"""<svg class="embedding-map{density}" viewBox="0 0 640 520"
    role="group" aria-labelledby="map-title map-description">
  <desc id="map-description">A two-dimensional PCA projection of post embeddings. Each point links to a meditation. Nearby points suggest similar text.</desc>
  <g aria-hidden="true">
    <path class="map-axes" d="M 32 {origin_y:.3f} H 608 M {origin_x:.3f} 32 V 488"/>
    <text class="map-axis-label" x="604" y="{max(44, origin_y - 8):.3f}" text-anchor="end">PC1</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="42">PC2</text>
    <text class="map-axis-label" x="{origin_x + 8:.3f}" y="{origin_y + 16:.3f}">0</text>
  </g>
  {''.join(nodes)}
</svg>"""


def render_index(
    items: list[Post], projection: Projection, dimension: int, model_id: str, account_menu: str
) -> str:
    post_ids = {post[2]: f"x{index:x}" for index, post in enumerate(reversed(items))}
    id_width = len(f"x{max(len(items) - 1, 0):x}")
    rows = "\n".join(
        f'<tr><td class="archive-date"><time datetime="{published.isoformat()}">{published.isoformat()}</time></td>'
        f'<td class="post-cell"><a class="post-link" href="{quote(slug, safe="")}/" '
        f'{post_attributes(published, post_ids[slug], slug)}><span class="post-id">{post_ids[slug]}</span> '
        f'<span>{escape(title)}</span></a></td></tr>'
        for published, title, slug, _ in items
    )
    if not rows:
        rows = '<tr><td colspan="2" class="archive-empty">No meditations published yet.</td></tr>'
    variance = (
        f"{projection.variance:.0%} variance"
        if projection.variance is not None else "zero variance"
    )
    return f"""{site_header(account_menu, index=True)}
<main class="workspace">
  <section class="panel archive-panel" aria-labelledby="archive-title">
    <header class="panel-head">
      <h2 id="archive-title">Index</h2>
      <span class="panel-meta">{len(items)} posts</span>
    </header>
    <div class="archive-scroll" tabindex="0" role="region" aria-label="Meditations">
      <table class="archive-table" style="--post-id-width: {id_width}ch">
        <colgroup><col class="date-column"><col></colgroup>
        <thead><tr><th scope="col">Published</th><th scope="col">Meditation</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </section>
  <section class="panel map-panel" aria-labelledby="map-title">
    <header class="panel-head">
      <h2 id="map-title">PCA <a class="model-card" href="https://huggingface.co/{quote(model_id, safe='/')}" aria-label="Embedding model card: {escape(model_id)}">{escape(model_id.rsplit('/', 1)[-1])}</a></h2>
      <span class="panel-meta" title="Input dimensions → displayed dimensions / embedding variance retained">{dimension} → 2 / {variance}</span>
    </header>
    <div class="map-stage">{render_map(items, projection, post_ids)}</div>
    <footer class="map-footer">
      <div class="map-readout">
        <p class="map-readout-id">—</p>
        <p class="map-readout-date"></p>
      </div>
    </footer>
  </section>
</main>"""


def page(title: str, content: str, *, index: bool = False) -> str:
    prefix = "" if index else "../"
    scripts = (
        '<script defer src="map.js"></script>'
        if index else """<script>
    window.MathJax = {tex: {inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}};
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-mml-chtml-nofont.js"></script>"""
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{prefix}site.css">
  {scripts}
</head>
<body class="{'index-page' if index else 'post-page'}">
{content}
</body>
</html>
"""


def build(items: list[Post]) -> None:
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
    items: list[Post],
    connection: sqlite3.Connection,
    prepared: list[PreparedPost],
    spec: dict,
    projection: Projection,
) -> None:
    import markdown
    account_menu = render_account_menu()

    if SITE.exists():
        try:
            shutil.rmtree(SITE)
        except OSError as error:
            raise RuntimeError(f"could not clear {SITE}") from error
    SITE.mkdir()
    export_public(connection, SITE / "blog.sqlite", prepared, spec)
    index = render_index(items, projection, spec["dimension"], spec["model"], account_menu)
    (SITE / "index.html").write_text(page("yet another raj", index, index=True))

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
        (destination / "index.html").write_text(page(title, content))

    try:
        shutil.copy(FONT, SITE / FONT.name)
        shutil.copy(ROOT / "assets" / "site.css", SITE / "site.css")
        shutil.copy(ROOT / "assets" / "map.js", SITE / "map.js")
        shutil.copy(ROOT / "CNAME", SITE / "CNAME")
    except OSError as error:
        raise RuntimeError("could not copy site assets") from error


def main() -> None:
    try:
        items = meditations()
        if "--readme" in sys.argv:
            update_readme(items)
            return
        build(items)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f"publish: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
