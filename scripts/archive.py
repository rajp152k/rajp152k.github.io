"""Read the Markdown archive and prepare its visible text for embeddings."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from xml.etree.ElementTree import Element

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = re.compile(r"\A---\n(?P<front_matter>.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class Entry:
    kind: str
    slug: str
    title: str
    published: date | datetime
    body: str

    def __post_init__(self) -> None:
        if self.kind not in {"meditations", "logs"}:
            raise ValueError(f"Unknown archive source kind {self.kind!r}.")
        reserved = {"meditations": {"search", "logs", "meditations"}, "logs": set()}
        if not self.slug or "/" in self.slug or self.slug in reserved[self.kind]:
            raise ValueError(f"Reserved or invalid {self.kind} slug {self.slug!r}.")
        if self.kind == "meditations":
            if not isinstance(self.published, date) or isinstance(self.published, datetime):
                raise ValueError("Meditations require a publication date, not a timestamp.")
        elif not isinstance(self.published, datetime) or self.published.utcoffset() is None:
            raise ValueError("Logs require a timezone-aware publication timestamp.")

    @property
    def key(self) -> str:
        return f"{self.kind}/{self.slug}"

    @property
    def url(self) -> str:
        prefix = "/logs/" if self.kind == "logs" else "/"
        return f"{prefix}{quote(self.slug, safe='')}/"

    @property
    def published_iso(self) -> str:
        if isinstance(self.published, datetime):
            return self.published.astimezone(timezone.utc).isoformat()
        return self.published.isoformat()

    @property
    def date_label(self) -> str:
        return self.published_iso[:10]

    @property
    def sort_key(self) -> tuple[datetime, str, str]:
        published = self.published
        if isinstance(published, datetime):
            instant = published.astimezone(timezone.utc)
        else:
            instant = datetime.combine(published, time.min, tzinfo=timezone.utc)
        return instant, self.title, self.key


class _FrontMatterLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in result
            except TypeError as error:
                raise yaml.constructor.ConstructorError(
                    None, None, "front matter keys must be scalar", key_node.start_mark,
                ) from error
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate front matter key {key!r}", key_node.start_mark,
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def _text(value: object, description: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{description} must be nonempty text.")
    return value.strip()


def parse(path: Path, kind: str) -> Entry:
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(source)
    if match is None:
        raise ValueError(f"{path}: missing front matter")
    try:
        fields = yaml.load(match.group("front_matter"), Loader=_FrontMatterLoader)
        if not isinstance(fields, dict):
            raise ValueError("front matter must be a mapping.")
        title = _text(fields.get("title"), "title")
        published = fields.get("date")
        if isinstance(published, str):
            published = datetime.fromisoformat(published) if kind == "logs" else date.fromisoformat(published)
        if not isinstance(published, date):
            raise ValueError("date must be a publication date or timestamp.")
        return Entry(kind, path.stem, title, published, source[match.end() :].strip())
    except (ValueError, yaml.YAMLError) as error:
        raise ValueError(f"{path}: {error}") from error


def read_entries(meditations_dir: Path = ROOT / "meditations", logs_dir: Path = ROOT / "logs") -> list[Entry]:
    meditations_dir, logs_dir = Path(meditations_dir), Path(logs_dir)
    if not meditations_dir.is_dir():
        raise ValueError(f"Meditation directory {meditations_dir} does not exist or is not a directory.")
    if logs_dir.exists() and not logs_dir.is_dir():
        raise ValueError(f"Log directory {logs_dir} is not a directory.")
    entries = [parse(path, "meditations") for path in meditations_dir.glob("*.md")]
    if logs_dir.is_dir():
        entries.extend(parse(path, "logs") for path in logs_dir.glob("*.md"))
    return sorted(entries, key=lambda entry: entry.sort_key, reverse=True)


def display_ids(entries: list[Entry]) -> dict[str, str]:
    counts = {"meditations": 0, "logs": 0}
    prefixes = {"meditations": "mx", "logs": "lx"}
    result = {}
    for entry in sorted(entries, key=lambda entry: entry.sort_key):
        result[entry.key] = f"{prefixes[entry.kind]}{counts[entry.kind]:x}"
        counts[entry.kind] += 1
    return result


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


def visible_blocks(entry: Entry) -> list[dict[str, str]]:
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

    html = markdown.markdown(entry.body, extensions=["fenced_code", "tables", PreserveMath()])
    parser = _VisibleText()
    parser.feed(html)
    parser.close()
    parser.flush()
    return parser.blocks


def prepared_text(entry: Entry) -> str:
    return "\n\n".join((entry.title, *(block["text"] for block in visible_blocks(entry))))
