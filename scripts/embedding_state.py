"""Current, reproducible embedding state; Markdown is the source of truth."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sqlite3
import struct
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote

from archive import ROOT, Post, prepared_text

DATABASE = ROOT / "blog.sqlite"
SPEC_PATH = ROOT / "embedding.json"
_FIELDS = {
    "model", "revision", "dimension", "preprocessing", "max_words", "max_tokens",
    "prefix", "pooling", "aggregation", "normalize", "precision", "backend",
}
_POLICIES = {
    "preprocessing": "markdown-text-v1",
    "pooling": "model",
    "aggregation": "token-weighted-normalized-mean-v1",
    "normalize": True,
    "precision": "float32",
    "backend": "torch",
}
_COLUMNS = {
    "model_specs": ("tag", "specification"),
    "archive": ("id", "model_tag"),
    "posts": ("slug", "title", "published_date", "text_hash", "embedding_key", "model_tag", "embedding"),
}
_SCHEMA = (
    "CREATE TABLE model_specs (tag TEXT PRIMARY KEY, specification TEXT NOT NULL) WITHOUT ROWID",
    "CREATE TABLE archive (id INTEGER PRIMARY KEY CHECK (id = 1), model_tag TEXT NOT NULL REFERENCES model_specs(tag))",
    "CREATE TABLE posts (slug TEXT PRIMARY KEY, title TEXT NOT NULL, published_date TEXT NOT NULL, text_hash TEXT NOT NULL, embedding_key TEXT NOT NULL, model_tag TEXT NOT NULL REFERENCES model_specs(tag), embedding BLOB NOT NULL) WITHOUT ROWID",
)
_REBUILD = "Run python3 scripts/embed.py to update the derived state."


@dataclass(frozen=True)
class PreparedPost:
    slug: str
    title: str
    published_date: str
    text: str
    text_hash: str
    embedding_key: str


@dataclass(frozen=True)
class _State:
    specs: dict[str, str]
    metadata: dict[int, str]
    posts: dict[str, tuple[str, str, str, str, str, bytes]]


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _validate_spec(spec: dict) -> None:
    if not isinstance(spec, dict) or set(spec) != _FIELDS:
        actual = set(spec) if isinstance(spec, dict) else set()
        missing = ", ".join(sorted(_FIELDS - actual)) or "none"
        extra = ", ".join(sorted(str(key) for key in actual - _FIELDS)) or "none"
        raise ValueError(f"Embedding specification must contain exactly the supported fields (missing: {missing}; extra: {extra}).")
    if not isinstance(spec["model"], str) or not spec["model"].strip():
        raise ValueError("Embedding model must be a nonempty model ID.")
    if not isinstance(spec["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", spec["revision"]):
        raise ValueError("Embedding revision must be a pinned, lowercase 40-character commit SHA, not a branch or tag.")
    for field in ("dimension", "max_words", "max_tokens"):
        if type(spec[field]) is not int or spec[field] <= 0:
            raise ValueError(f"Embedding {field} must be a positive integer.")
    if not isinstance(spec["prefix"], str):
        raise ValueError("Embedding prefix must be a string.")
    for field, expected in _POLICIES.items():
        if type(spec[field]) is not type(expected) or spec[field] != expected:
            raise ValueError(f"Unsupported embedding {field}={spec[field]!r}; only {expected!r} is implemented.")


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate embedding specification field {key!r}.")
        result[key] = value
    return result


def load_spec(path: Path = SPEC_PATH) -> dict:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        _validate_spec(spec)
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f"Could not load embedding specification {path}: {error}") from error
    return spec


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def model_tag(spec: dict) -> str:
    _validate_spec(spec)
    return "sha256:" + _sha256(_canonical(spec))


def _embedding_key(text: str, spec: dict) -> str:
    return _sha256(_canonical({"specification": spec, "text": text}))


def prepare_posts(posts: list[Post], spec: dict) -> list[PreparedPost]:
    _validate_spec(spec)
    result = []
    slugs = set()
    for published, title, slug, body in posts:
        if slug in slugs:
            raise ValueError(f"Duplicate post slug {slug!r}; the archive must have unique slugs.")
        slugs.add(slug)
        text = prepared_text((published, title, slug, body))
        result.append(PreparedPost(slug, title, published.isoformat(), text, _sha256(text), _embedding_key(text, spec)))
    return result


def _validate_prepared(prepared: list[PreparedPost], spec: dict) -> None:
    _validate_spec(spec)
    slugs = set()
    for post in prepared:
        if post.slug in slugs:
            raise ValueError(f"Duplicate prepared post slug {post.slug!r}.")
        slugs.add(post.slug)
        if post.text_hash != _sha256(post.text) or post.embedding_key != _embedding_key(post.text, spec):
            raise ValueError(f"Prepared hashes for {post.slug!r} do not match its text and specification; use prepare_posts.")
        try:
            canonical_date = date.fromisoformat(post.published_date).isoformat()
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid prepared publication date for {post.slug!r}.") from error
        if canonical_date != post.published_date:
            raise ValueError(f"Prepared publication date for {post.slug!r} must be ISO YYYY-MM-DD.")


def _validate_schema(connection: sqlite3.Connection) -> None:
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")}
    if version != 1 or not set(_COLUMNS).issubset(tables):
        raise ValueError("Unsupported embedding database schema; remove this derived database and rebuild it. " + _REBUILD)
    for table, expected in _COLUMNS.items():
        columns = tuple(row[1] for row in connection.execute(f"PRAGMA table_info({table})"))
        if columns != expected:
            raise ValueError(f"Invalid embedding database table {table!r}; remove this derived database and rebuild it. " + _REBUILD)


def open_database(path: Path = DATABASE, *, writable: bool = False) -> sqlite3.Connection:
    path = Path(path).expanduser().resolve()
    connection = None
    try:
        if writable:
            connection = sqlite3.connect(path)
        else:
            connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        journal = connection.execute("PRAGMA journal_mode").fetchone()[0]
        if journal != "delete":
            raise ValueError(f"Embedding database {path} must use the DELETE rollback journal, not {journal!r}; remove this derived database and rebuild it. " + _REBUILD)
        objects = connection.execute("SELECT name FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'").fetchall()
        version = connection.execute("PRAGMA user_version").fetchone()[0]
        if writable and not objects and version == 0:
            connection.execute("BEGIN IMMEDIATE")
            for statement in _SCHEMA:
                connection.execute(statement)
            connection.execute("PRAGMA user_version = 1")
            connection.commit()
        _validate_schema(connection)
        return connection
    except (sqlite3.Error, ValueError) as error:
        if connection is not None:
            connection.close()
        raise ValueError(f"Could not open embedding database {path}: {error} {_REBUILD}") from error


def _read_state(connection: sqlite3.Connection) -> _State:
    _validate_schema(connection)
    return _State(
        {row[0]: row[1] for row in connection.execute("SELECT tag, specification FROM model_specs")},
        {row[0]: row[1] for row in connection.execute("SELECT id, model_tag FROM archive")},
        {row[0]: (row[1], row[2], row[3], row[4], row[5], row[6]) for row in connection.execute("SELECT slug, title, published_date, text_hash, embedding_key, model_tag, embedding FROM posts")},
    )


def _validate_vector(vector: bytes, dimension: int, description: str) -> None:
    if not isinstance(vector, bytes) or len(vector) != dimension * 4:
        raise ValueError(f"{description}: expected {dimension * 4} bytes of little-endian float32 data.")
    values = tuple(value[0] for value in struct.iter_unpack("<f", vector))
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"{description}: vector contains NaN or infinite values.")
    norm = math.sqrt(math.fsum(value * value for value in values))
    if abs(norm - 1.0) > 1e-4:
        raise ValueError(f"{description}: vector must have unit L2 norm (found {norm:.8g}).")


def _cached_vector(state: _State, post: PreparedPost, spec: dict, tag: str, canonical: str) -> bytes | None:
    if state.specs.get(tag) != canonical:
        return None
    expected = (post.text_hash, post.embedding_key, tag)
    cached = state.posts.get(post.slug)
    if cached is not None and cached[2:5] == expected:
        try:
            _validate_vector(cached[5], spec["dimension"], f"Cached embedding for {post.slug!r}")
        except ValueError:
            return None
        return cached[5]
    # Keys exclude slugs and dates, allowing metadata updates and renames to reuse vectors.
    for cached in state.posts.values():
        if cached[2:5] != expected:
            continue
        try:
            _validate_vector(cached[5], spec["dimension"], f"Cached embedding for {post.slug!r}")
        except ValueError:
            continue
        return cached[5]
    return None


def pending_posts(connection: sqlite3.Connection, prepared: list[PreparedPost], spec: dict) -> list[PreparedPost]:
    _validate_prepared(prepared, spec)
    tag, canonical = model_tag(spec), _canonical(spec)
    try:
        state = _read_state(connection)
        return [post for post in prepared if _cached_vector(state, post, spec, tag, canonical) is None]
    except sqlite3.Error as error:
        raise ValueError(f"Could not inspect embedding database: {error}. Remove a corrupt derived database and rebuild it. {_REBUILD}") from error


def _freshness_errors(state: _State, prepared: list[PreparedPost], spec: dict) -> list[str]:
    tag, canonical = model_tag(spec), _canonical(spec)
    issues = []
    if state.specs != {tag: canonical}:
        issues.append("model specification metadata is missing, mismatched, or historical")
    if state.metadata != {1: tag}:
        issues.append("archive model tag is missing or mismatched")
    expected_slugs = {post.slug for post in prepared}
    if set(state.posts) - expected_slugs:
        issues.append("deleted posts remain in the database")
    for post in prepared:
        expected = (post.title, post.published_date, post.text_hash, post.embedding_key, tag)
        cached = state.posts.get(post.slug)
        if cached is None:
            issues.append(f"missing post/embedding {post.slug!r}")
            continue
        if cached[:5] != expected:
            issues.append(f"stale metadata/text/specification for {post.slug!r}")
        try:
            _validate_vector(cached[5], spec["dimension"], f"Embedding for {post.slug!r}")
        except ValueError as error:
            issues.append(str(error))
    return issues


def check_fresh(connection: sqlite3.Connection, prepared: list[PreparedPost], spec: dict) -> None:
    _validate_prepared(prepared, spec)
    try:
        state = _read_state(connection)
        issues = _freshness_errors(state, prepared, spec)
        for table in ("posts", "archive"):
            if connection.execute(f"PRAGMA foreign_key_check({table})").fetchone() is not None:
                issues.append(f"database references in {table!r} are corrupt")
    except sqlite3.Error as error:
        raise ValueError(f"Could not check embedding database: {error}. Remove a corrupt derived database and rebuild it. {_REBUILD}") from error
    if issues:
        detail = "; ".join(issues[:12])
        if len(issues) > 12:
            detail += f"; and {len(issues) - 12} more problems"
        raise ValueError(f"Embedding state is not fresh: {detail}. {_REBUILD}")


def _desired_state(state: _State, prepared: list[PreparedPost], spec: dict, vectors: dict[str, bytes]) -> _State:
    tag, canonical = model_tag(spec), _canonical(spec)
    slugs = {post.slug for post in prepared}
    if set(vectors) - slugs:
        raise ValueError("New vectors include slugs not present in the current archive.")
    for slug, vector in vectors.items():
        _validate_vector(vector, spec["dimension"], f"New embedding for {slug!r}")
    by_key = {}
    posts = {}
    for post in prepared:
        vector = _cached_vector(state, post, spec, tag, canonical)
        if vector is None:
            vector = vectors.get(post.slug)
        if vector is None:
            vector = by_key.get(post.embedding_key)
        if vector is None:
            raise ValueError(f"Missing new embedding for {post.slug!r}; compute all pending vectors before synchronizing. {_REBUILD}")
        vector = by_key.setdefault(post.embedding_key, vector)
        posts[post.slug] = (post.title, post.published_date, post.text_hash, post.embedding_key, tag, vector)
    return _State({tag: canonical}, {1: tag}, posts)


def synchronize(connection: sqlite3.Connection, prepared: list[PreparedPost], spec: dict, vectors: dict[str, bytes]) -> None:
    _validate_prepared(prepared, spec)
    if connection.in_transaction:
        raise ValueError("Synchronization must own its transaction; finish the existing database transaction first.")
    try:
        before = _read_state(connection)
        desired = _desired_state(before, prepared, spec, vectors)
        if before == desired:
            return
        connection.execute("BEGIN IMMEDIATE")
        # Re-read after acquiring the write lock; update only differing rows.
        before = _read_state(connection)
        for tag, specification in desired.specs.items():
            if before.specs.get(tag) != specification:
                connection.execute("INSERT INTO model_specs VALUES (?, ?) ON CONFLICT(tag) DO UPDATE SET specification = excluded.specification", (tag, specification))
        for slug, values in desired.posts.items():
            if before.posts.get(slug) != values:
                connection.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(slug) DO UPDATE SET title = excluded.title, published_date = excluded.published_date, text_hash = excluded.text_hash, embedding_key = excluded.embedding_key, model_tag = excluded.model_tag, embedding = excluded.embedding", (slug, *values))
        connection.executemany("DELETE FROM posts WHERE slug = ?", ((slug,) for slug in sorted(set(before.posts) - set(desired.posts))))
        for identifier, tag in desired.metadata.items():
            if before.metadata.get(identifier) != tag:
                connection.execute("INSERT INTO archive VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET model_tag = excluded.model_tag", (identifier, tag))
        connection.execute("DELETE FROM archive WHERE id != 1")
        connection.execute("DELETE FROM model_specs WHERE tag NOT IN (SELECT model_tag FROM posts UNION SELECT model_tag FROM archive)")
        connection.commit()
    except sqlite3.Error as error:
        try:
            if connection.in_transaction:
                connection.rollback()
        except sqlite3.Error as rollback_error:
            raise ValueError(f"Could not synchronize embedding database ({error}); rollback also failed ({rollback_error}). Close the database and inspect/rebuild its derived state.") from error
        raise ValueError(f"Could not synchronize embedding database: {error}; no partial update was committed. {_REBUILD}") from error
    except BaseException:
        if connection.in_transaction:
            connection.rollback()
        raise


def export_public(connection: sqlite3.Connection, destination: Path, prepared: list[PreparedPost], spec: dict) -> None:
    destination = Path(destination).expanduser().resolve()
    temporary = None
    public = None
    owns_transaction = False
    try:
        for database in connection.execute("PRAGMA database_list"):
            source = database[2]
            if source and (destination == Path(source).resolve() or (destination.exists() and os.path.samefile(source, destination))):
                raise ValueError("Public export destination must not replace the local embedding database.")
        if not connection.in_transaction:
            connection.execute("BEGIN")
            owns_transaction = True
        check_fresh(connection, prepared, spec)
        state = _read_state(connection)
        descriptor, filename = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".sqlite", dir=destination.parent)
        os.close(descriptor)
        temporary = Path(filename)
        public = sqlite3.connect(temporary)
        public.execute("PRAGMA foreign_keys = ON")
        public.execute("PRAGMA journal_mode = DELETE")
        public.execute("BEGIN")
        public.execute("CREATE TABLE model (tag TEXT PRIMARY KEY, model_id TEXT NOT NULL, revision TEXT NOT NULL, dimension INTEGER NOT NULL, dtype TEXT NOT NULL) WITHOUT ROWID")
        public.execute("CREATE TABLE posts (slug TEXT PRIMARY KEY, title TEXT NOT NULL, published_date TEXT NOT NULL, url TEXT NOT NULL, model_tag TEXT NOT NULL REFERENCES model(tag), embedding BLOB NOT NULL) WITHOUT ROWID")
        public.execute("PRAGMA user_version = 1")
        tag = model_tag(spec)
        public.execute("INSERT INTO model VALUES (?, ?, ?, ?, ?)", (tag, spec["model"], spec["revision"], spec["dimension"], "<f4"))
        public.executemany(
            "INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)",
            ((post.slug, post.title, post.published_date, f"/{quote(post.slug, safe='')}/", tag, state.posts[post.slug][5]) for post in prepared),
        )
        public.commit()
        public.close()
        public = None
        temporary.chmod(0o644)
        os.replace(temporary, destination)
        temporary = None
    except (OSError, sqlite3.Error) as error:
        raise ValueError(f"Could not create public embedding database {destination}: {error}; the previous public artifact was not replaced.") from error
    finally:
        if public is not None:
            public.close()
        if temporary is not None:
            temporary.unlink(missing_ok=True)
            Path(str(temporary) + "-journal").unlink(missing_ok=True)
        if owns_transaction:
            connection.rollback()
