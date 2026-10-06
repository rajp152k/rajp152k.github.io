"""Read the Markdown archive and prepare its visible text for embeddings."""

from __future__ import annotations

import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from xml.etree.ElementTree import Element

ROOT = Path(__file__).resolve().parent.parent
Post = tuple[date, str, str, str]
FRONT_MATTER = re.compile(r"\A---\n(?P<front_matter>.*?)\n---\n", re.DOTALL)


def parse(path: Path) -> Post:
    source = path.read_text(encoding="utf-8")
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
    try:
        published_date = date.fromisoformat(published)
    except ValueError as error:
        raise ValueError(f"{path}: invalid publication date {published!r}") from error
    return published_date, title, path.stem, source[match.end() :].strip()


def meditations(directory: Path = ROOT / "meditations") -> list[Post]:
    return sorted((parse(path) for path in directory.glob("*.md")), reverse=True)


class _VisibleText(HTMLParser):
    BLOCKS = {
        "address", "article", "aside", "blockquote", "dd", "div", "dl", "dt",
        "fieldset", "figcaption", "figure", "footer", "h1", "h2", "h3", "h4",
        "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "section",
        "table", "tr", "ul",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, str]] = []
        self.parts: list[str] = []
        self.kind = "body"
        self.pre = False
        self.code_depth = 0
        self.hidden: str | None = None

    def flush(self) -> None:
        text = "".join(self.parts)
        text = text.strip("\n") if self.pre else text.strip()
        if text:
            self.blocks.append({"kind": self.kind, "text": text})
        self.parts.clear()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.hidden:
            return
        if tag in {"script", "style"}:
            self.hidden = tag
        elif tag == "pre":
            self.flush()
            self.pre = True
            self.kind = "code"
        elif tag in self.BLOCKS:
            self.flush()
            if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                self.kind = "heading"
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "code":
            self.code_depth += 1
        elif tag in {"td", "th"}:
            if self.parts:
                self.parts.append("\t")
        elif tag == "img":
            self.parts.append(dict(attrs).get("alt") or "")

    def handle_endtag(self, tag: str) -> None:
        if self.hidden:
            if tag == self.hidden:
                self.hidden = None
            return
        if tag == "pre":
            self.flush()
            self.pre = False
            self.kind = "body"
        elif tag in self.BLOCKS:
            self.flush()
            self.kind = "body"
        elif tag == "code":
            self.code_depth = max(0, self.code_depth - 1)

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(
                data if self.pre or self.code_depth else re.sub(r"\s+", " ", data)
            )


def visible_blocks(post: Post) -> list[dict[str, str]]:
    import markdown
    from markdown.extensions import Extension
    from markdown.inlinepatterns import InlineProcessor
    from markdown.util import AtomicString

    class MathText(InlineProcessor):
        def handleMatch(self, m, data):
            element = Element("code")
            element.text = AtomicString(m.group(0))
            return element, m.start(0), m.end(0)

    class PreserveMath(Extension):
        def extendMarkdown(self, md):
            # After backticks, before Markdown's backslash escapes and emphasis.
            md.inlinePatterns.register(
                MathText(
                    r"(?<!\\)(?:\$\$[\s\S]*?\$\$|\$(?!\$)(?:\\.|[^$\\])*?\$|"
                    r"\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\])",
                    md,
                ),
                "embedding_math",
                185,
            )

    _, _, _, body = post
    html = markdown.markdown(body, extensions=["fenced_code", "tables", PreserveMath()])
    parser = _VisibleText()
    parser.feed(html)
    parser.close()
    parser.flush()
    return parser.blocks


def prepared_text(post: Post) -> str:
    return "\n\n".join((post[1], *(block["text"] for block in visible_blocks(post))))
