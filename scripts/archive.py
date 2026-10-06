"""Read the Markdown archive and prepare its visible text for embeddings."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.etree.ElementTree import Element

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = re.compile(r"\A---\n(?P<front_matter>.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class Artifact:
    label: str
    url: str
    source: Path | None


@dataclass(frozen=True)
class Entry:
    kind: str
    slug: str
    title: str
    published: date | datetime
    body: str
    metadata: dict = field(default_factory=dict)
    artifacts: tuple[Artifact, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in {"meditations", "logs"}:
            raise ValueError(f"Unknown archive source kind {self.kind!r}.")
        reserved = {"meditations": {"search", "logs", "meditations"}, "logs": {"artifacts"}}
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


def _url(value: object, description: str, *, external: bool = False) -> str:
    value = _text(value, description)
    parsed = urlsplit(value)
    if external:
        valid = parsed.scheme == "https" and bool(parsed.netloc)
    else:
        valid = (parsed.scheme in {"https", "http"} and bool(parsed.netloc)) or (
            value.startswith("/") and not value.startswith("//") and not parsed.scheme
        )
    if not valid or any(character.isspace() for character in value):
        raise ValueError(f"{description} must be {'an explicit HTTPS' if external else 'a web or root-relative'} URL.")
    return value


def _record(value: object, description: str, *, contributor: bool = False) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{description} must be a structured record.")
    fields = ("name", "provider", "model", "effort", "role") if contributor else ("name", "provider", "model", "effort")
    return {
        key: None if key in {"model", "effort"} and value[key] is None else _text(value[key], f"{description}.{key}")
        for key in fields if key in value
    }


def _metadata(fields: dict) -> dict:
    status = fields.get("status")
    if not isinstance(status, str) or status not in {"in-progress", "blocked", "complete"}:
        raise ValueError("log status must be in-progress, blocked, or complete.")
    result = {"status": status}
    if "agent" in fields:
        result["agent"] = _record(fields["agent"], "agent")
    if "task" in fields:
        result["task"] = _text(fields["task"], "task")
    if "related" in fields:
        if not isinstance(fields["related"], list):
            raise ValueError("related must be a list of URLs.")
        result["related"] = [_url(value, "related link") for value in fields["related"]]
    if "contributors" in fields:
        if not isinstance(fields["contributors"], list):
            raise ValueError("contributors must be a list of structured records.")
        result["contributors"] = [_record(value, "contributor", contributor=True) for value in fields["contributors"]]
    return result


def _artifacts(value: object, path: Path) -> tuple[Artifact, ...]:
    if not isinstance(value, list):
        raise ValueError("artifacts must be a list of label and path or URL records.")
    result = []
    logs_root = path.parent.resolve()
    artifacts_root = (logs_root / "artifacts").resolve()
    for record in value:
        if not isinstance(record, dict) or ("path" in record) == ("url" in record):
            raise ValueError("Each artifact requires a label and exactly one path or URL.")
        label = _text(record.get("label"), "artifact label")
        if "url" in record:
            result.append(Artifact(label, _url(record["url"], "artifact URL", external=True), None))
            continue
        relative = _text(record["path"], "artifact path")
        parts = relative.split("/")
        if len(parts) < 3 or parts[:2] != ["artifacts", path.stem] or any(part in {"", ".", ".."} for part in parts):
            raise ValueError(f"Artifact path {relative!r} must be relative to logs as artifacts/{path.stem}/... without traversal.")
        source = (logs_root / relative).resolve()
        if (not artifacts_root.is_relative_to(logs_root) or not source.is_relative_to(artifacts_root)
                or not source.is_relative_to(logs_root) or not source.is_file()):
            raise ValueError(f"Artifact path {relative!r} must be an existing regular file safely inside logs/artifacts.")
        url = "/logs/artifacts/" + quote("/".join(parts[1:]), safe="/")
        result.append(Artifact(label, url, source))
    return tuple(result)


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
        metadata = _metadata(fields) if kind == "logs" else {}
        artifacts = _artifacts(fields.get("artifacts", []), path) if kind == "logs" else ()
        return Entry(kind, path.stem, title, published, source[match.end() :].strip(), metadata, artifacts)
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
