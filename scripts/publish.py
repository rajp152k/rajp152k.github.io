# /usr/bin/env python3
"""Build the Markdown meditation archive."""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDITATIONS = ROOT / "meditations"
README = ROOT / "README.md"
SITE = ROOT / "site"
FONT = ROOT / "assets" / "VT323-Regular.ttf"
START = "<!-- meditations:start -->"
END = "<!-- meditations:end -->"
FRONT_MATTER = re.compile(r"\A---\n(?P<front_matter>.*?)\n---\n", re.DOTALL)

CSS = """
@font-face { font-family: VT323; src: url("/VT323-Regular.ttf") format("truetype"); font-display: swap; }
:root { color-scheme: dark; font-family: VT323, ui-monospace, monospace; background: #000; color: #00ff00; }
body { max-width: 44rem; margin: 4rem auto; padding: 0 1rem; line-height: 1.35; font-size: 1.35rem; }
a { color: #39ff14; } a:hover { background: #00ff00; color: #000; text-decoration: none; }
::selection { background: #00b300; color: #000; } pre { overflow-x: auto; padding: 1rem; border: 1px solid #006600; } code { font: inherit; }
table { border-collapse: collapse; width: 100%; } th, td { border-bottom: 1px solid #006600; padding: .5rem 0; text-align: left; } th + th, td + td { border-left: 1px solid #006600; padding-left: .75rem; }
""".strip()


def parse(path: Path) -> tuple[date, str, str, str]:
    source = path.read_text()
    match = FRONT_MATTER.match(source)
    if match is None:
        raise ValueError(f"{path}: missing front matter")

    fields = dict(
        line.split(":", 1)
        for line in match.group("front_matter").splitlines()
        if ":" in line
    )
    title = fields.get("title", "").strip()
    published = fields.get("date", "").strip()
    if not title or not published:
        raise ValueError(f"{path}: front matter requires title and date")

    return (
        date.fromisoformat(published),
        title,
        path.stem,
        source[match.end() :].strip(),
    )


def meditations() -> list[tuple[date, str, str, str]]:
    return sorted((parse(path) for path in MEDITATIONS.glob("*.md")), reverse=True)


def update_readme(items: list[tuple[date, str, str, str]]) -> None:
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


def page(title: str, content: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)}</title>
  <style>{CSS}</style>
  <script>
    window.MathJax = {{tex: {{inlineMath: [['$', '$']], displayMath: [['$$', '$$']]}}}};
  </script>
  <script async src=\"https://cdn.jsdelivr.net/npm/mathjax@4.1.3/tex-mml-chtml-nofont.js\"></script>
</head>
<body>
{content}
</body>
</html>
"""


def build(items: list[tuple[date, str, str, str]]) -> None:
    import markdown  # pyright: ignore[reportMissingModuleSource]

    if SITE.exists():
        try:
            shutil.rmtree(SITE)
        except OSError as error:
            raise RuntimeError(f"could not clear {SITE}") from error
    SITE.mkdir()
    rows = "\n".join(
        f'<tr><td>{published.isoformat()}</td><td><a href="{slug}/">{escape(title)}</a></td></tr>'
        for published, title, slug, _ in items
    )
    index = f"<h1>meditations of yet another raj</h1><table><thead><tr><th>Date</th><th>Meditation</th></tr></thead><tbody>{rows}</tbody></table>"
    (SITE / "index.html").write_text(page("yet another raj", index))

    for _, title, slug, body in items:
        destination = SITE / slug
        destination.mkdir()
        html = markdown.markdown(body, extensions=["fenced_code", "tables"])
        content = f'<p><a href="/">← index</a></p><article><h1>{escape(title)}</h1>{html}</article>'
        (destination / "index.html").write_text(page(title, content))

    try:
        shutil.copy(FONT, SITE / FONT.name)
        shutil.copy(ROOT / "CNAME", SITE / "CNAME")
    except OSError as error:
        raise RuntimeError("could not copy site assets") from error


def main() -> None:
    items = meditations()
    if "--readme" in sys.argv:
        update_readme(items)
        return
    build(items)


if __name__ == "__main__":
    main()
