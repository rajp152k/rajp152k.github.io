"""Prepare immutable Potato sessions and import their native review evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VERSION = "2.13.1"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def inside(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes project: {name}")
    return path


def snapshot(root: Path, name: str, sources: dict) -> str:
    data = inside(root, name).read_bytes()
    sources[name] = {"sha256": digest(data), "text": data.decode("utf-8")}
    return data.decode("utf-8")


def term_card(term: dict, item_id: str, evidence: list[tuple[str, str]]) -> str:
    """Render escaped candidate details with full snapshots closed by default."""
    card = term.get("card", {})
    fields = (("definition", "Definition"), ("aliases", "Aliases"),
              ("passage", "Exact passage"), ("introduction", "Introduction"),
              ("use_scope", "Use scope"))
    for key in ("name", *(key for key, _ in fields)):
        if key not in card or not isinstance(card[key], (str, list)):
            raise ValueError(f"Missing or invalid term card field {key}: {item_id}")
    def escape(value: object) -> str:
        return html.escape(str(value), quote=True)
    rows = []
    for key, label in fields:
        value = card.get(key, "Not specified")
        if isinstance(value, list):
            value = ", ".join(value) or "None"
        rows.append(f"<tr><th style='text-align:left;vertical-align:top;padding:4px 16px 4px 0'>{label}</th>"
                    f"<td style='padding:4px 0'>{escape(value)}</td></tr>")
    details = "".join(f"<details><summary>{escape(label)}</summary>"
                      f"<pre style='white-space:pre-wrap'>{escape(text)}</pre></details>"
                      for label, text in evidence)
    return (f"<div><small>{escape(item_id)}</small><h3>{escape(card['name'])}</h3>"
            f"<table>{''.join(rows)}</table>"
            "<p>Approve these exact details and use scope.</p>" + details + "</div>")


def prepare(root: Path, records: list[str], extra_sources: tuple[str, ...] | list[str] = (),
            *, terms_only: bool = False) -> Path:
    """Freeze complete records, posts, and named evidence. IDs include their scope."""
    sources, items = {}, []
    for name in extra_sources:
        snapshot(root, name, sources)
    for name in records:
        text = snapshot(root, name, sources)
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            raise ValueError(f"Missing YAML front matter: {name}")
        meta = yaml.safe_load(match[1])
        entry, cycle = meta["entry"], meta["cycle"]
        if meta.get("kind") != "post-review" or not isinstance(cycle, int):
            raise ValueError(f"Not a numbered post-review: {name}")
        if not entry.startswith(("logs/", "meditations/")):
            raise ValueError(f"Unknown entry: {entry}")
        post_name = f"{entry}.md"
        post = snapshot(root, post_name, sources)
        if meta.get("post_sha256") != sources[post_name]["sha256"]:
            raise ValueError(f"Review post hash is stale: {name}")
        terms = meta.get("terms", [])
        if terms and entry.startswith("meditations/"):
            raise ValueError("Meditations have no terms")
        for term in terms:
            if term["state"] != "proposed":
                continue
            revision = term["revision"]
            if not isinstance(revision, int) or revision < 1:
                raise ValueError("Candidate revision must be a positive integer")
            item_id = f"{entry}:cycle-{cycle}:{term['id']}:r{revision}"
            items.append({"id": item_id, "kind": "term", "entry": entry,
                          "candidate": term["id"], "revision": revision,
                          "record": name, "post": post_name,
                          "text": term_card(term, item_id, [("Full review record", text),
                              ("Full post snapshot", post)] + [(f"Evidence: {source}", sources[source]["text"])
                                                             for source in extra_sources])})
        if entry.startswith("logs/") and not terms_only:
            items.append({"id": f"{entry}:cycle-{cycle}:log", "kind": "log",
                          "entry": entry, "record": name, "post": post_name,
                          "text": post})
    if not items:
        raise ValueError("No proposed terms or logs to review")
    if len({item["id"] for item in items}) != len(items):
        raise ValueError("Duplicate candidate or log IDs")
    payload = {"schema": 2, "presentation": "term-card-v1", "potato_version": VERSION,
               "sources": sources, "items": items, "terms_only": terms_only}
    session_id = digest(json.dumps(payload, sort_keys=True).encode())[:20]
    session = root / ".reviews" / session_id
    if session.exists():
        if json.loads((session / "manifest.json").read_text()) != payload:
            raise ValueError("Existing session manifest differs")
        (root / ".reviews/current").write_text(session_id + "\n")
        return session
    session.mkdir(parents=True)
    dump(session / "manifest.json", payload)
    dump(session / "data.json", [{"id": i["id"],
                                 "card_html": i["text"] if i["kind"] == "term" else "",
                                 "text": i["text"] if i["kind"] == "log" else ""} for i in items])
    config = {"annotation_task_name": f"Blog review {session_id}",
              "task_dir": str(session.resolve()), "data_files": ["data.json"],
              "item_properties": {"id_key": "id", "text_key": "text"},
              "instance_display": {"fields": [{"key": "card_html", "type": "html"}] +
                                     ([] if terms_only else [{"key": "text", "type": "text"}])},
              "output_annotation_dir": "annotation_output", "export_annotation_format": "jsonl",
              "require_password": False, "annotation_ui": {"memos": True, "visibility": "shared"},
              "annotation_schemes": [
                  {"annotation_type": "radio", "name": "decision",
                   "description": "Decision for this candidate" if terms_only else "Term decision only. Leave blank for log comments.",
                   "labels": ["approve", "request changes", "reject", "defer"]},
                  {"annotation_type": "text", "name": "comment", "description": "Reasons and corrections"}]}
    (session / "config.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
    (root / ".reviews/current").write_text(session_id + "\n")
    return session


def native_evidence(session: Path) -> dict:
    """Read user saves and database rows, including memo replies and issue state."""
    users = {}
    for path in sorted((session / "annotation_output").glob("*/user_state.json")):
        if path.is_symlink():
            raise ValueError("Refusing symlinked user state")
        users[path.parent.name] = json.loads(path.read_text())
    memos, threads = [], []
    database = session / "project.sqlite"
    if database.exists():
        with sqlite3.connect(f"file:{database.resolve()}?mode=ro", uri=True) as db:
            db.row_factory = sqlite3.Row
            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not {"memos", "memo_threads"} <= tables:
                raise ValueError("Potato memo tables are missing; check installed version")
            memos = [dict(row) for row in db.execute("SELECT * FROM memos ORDER BY id")]
            threads = [dict(row) for row in db.execute("SELECT * FROM memo_threads ORDER BY memo_id")]
    return {"users": users, "memos": memos, "memo_threads": threads}


def responses(manifest: dict, evidence: dict) -> list[dict]:
    items = {item["id"]: item for item in manifest["items"]}
    result = []
    for user, state in evidence["users"].items():
        for item_id, labels in state.get("instance_id_to_label_to_value", {}).items():
            if item_id not in items:
                raise ValueError(f"Unknown annotation instance: {item_id}")
            decision, comment = None, None
            for label, value in labels:
                if label["schema"] == "decision" and value:
                    if label["name"] not in {"approve", "request changes", "reject", "defer"}:
                        raise ValueError(f"Unknown decision: {label['name']}")
                    if decision is not None:
                        raise ValueError(f"Multiple decisions for {item_id}")
                    decision = label["name"]
                elif label["schema"] == "comment":
                    comment = value
            result.append({"user": user, "item_id": item_id, "kind": items[item_id]["kind"],
                           "decision": decision if items[item_id]["kind"] == "term" else None,
                           "comment": comment})
    return result


def import_session(root: Path, session: Path) -> Path:
    manifest = json.loads((session / "manifest.json").read_text())
    for name, source in manifest["sources"].items():
        if digest(source["text"].encode()) != source["sha256"]:
            raise ValueError(f"Corrupt snapshot: {name}")
    changed = [name for name, source in manifest["sources"].items()
               if not inside(root, name).exists() or digest(inside(root, name).read_bytes()) != source["sha256"]]
    evidence = native_evidence(session)
    known = {item["id"] for item in manifest["items"]}
    for memo in evidence["memos"]:
        if memo["instance_id"] not in known:
            raise ValueError(f"Unknown memo instance: {memo['instance_id']}")
    if not evidence["users"] and not evidence["memos"]:
        raise ValueError("No saved annotations or memos to import")
    report = {"schema": 1, "session": session.name, "manifest": manifest,
              "changed_sources": changed, "responses": responses(manifest, evidence), "evidence": evidence}
    report_hash = digest(json.dumps(report, sort_keys=True).encode())
    output = root / "review-imports" / f"{session.name}-{report_hash[:16]}.json"
    output.parent.mkdir(exist_ok=True)
    if output.exists():
        if json.loads(output.read_text()) != report:
            raise ValueError("Existing import report differs")
    else:
        dump(output, report)
    dump(session / "imported.json", {"report": str(output.relative_to(root)), "sha256": digest(output.read_bytes()),
                                     "evidence_sha256": digest(json.dumps(evidence, sort_keys=True).encode())})
    return output


def clean(root: Path, session: Path) -> None:
    if session.is_symlink() or session.parent.resolve() != (root / ".reviews").resolve():
        raise ValueError("Refusing to clean outside review scratch")
    marker = json.loads((session / "imported.json").read_text())
    report = inside(root, marker["report"])
    if digest(report.read_bytes()) != marker["sha256"]:
        raise ValueError("Import report is missing or changed")
    evidence_hash = digest(json.dumps(native_evidence(session), sort_keys=True).encode())
    if evidence_hash != marker["evidence_sha256"]:
        raise ValueError("New responses exist; import again before cleaning")
    shutil.rmtree(session)
    current = root / ".reviews/current"
    if current.exists() and current.read_text().strip() == session.name:
        current.unlink()


def select_session(root: Path, session_id: str | None = None) -> Path:
    """Prefer an explicit ID, then the last queued session, then a sole session."""
    scratch = root / ".reviews"
    current = scratch / "current"
    if session_id is None and current.exists():
        session_id = current.read_text().strip()
    if session_id is None:
        sessions = sorted(scratch.glob("*/manifest.json"))
        if len(sessions) != 1:
            raise ValueError("Queue a session with just queue-review, or pass --session ID")
        session_id = sessions[0].parent.name
    if not re.fullmatch(r"[0-9a-f]{20}", session_id):
        raise ValueError("Invalid review session ID")
    session = inside(scratch, session_id)
    if not (session / "manifest.json").is_file():
        raise ValueError("Review session is missing; queue it again or pass --session ID")
    return session


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    queue = sub.add_parser("queue", help="Freeze numbered Markdown review records")
    queue.add_argument("--source", action="append", default=[], help="Also freeze a local evidence source")
    queue.add_argument("--terms-only", action="store_true", help="Queue term decisions without log memo items")
    queue.add_argument("records", nargs="+")
    serve = sub.add_parser("serve", help="Start or resume one prepared session on localhost")
    serve.add_argument("--session")
    serve.add_argument("--port", type=int, default=8768)
    for command in ("import", "clean"):
        sub.add_parser(command).add_argument("session")
    args = parser.parse_args()
    try:
        if args.command == "queue":
            print(prepare(ROOT, args.records, args.source, terms_only=args.terms_only).relative_to(ROOT))
        elif args.command == "serve":
            session = select_session(ROOT, args.session)
            python = ROOT / ".venv-review/bin/python"
            version = subprocess.check_output([str(python), "-m", "potato", "--version"], text=True)
            if VERSION not in version:
                raise ValueError(f"Expected Potato {VERSION}; run just setup-review")
            subprocess.run([str(python), "-m", "potato", "start", str(session / "config.yaml"),
                            "--host", "127.0.0.1", "-p", str(args.port)], check=True)
        else:
            session = inside(ROOT / ".reviews", args.session)
            if args.command == "import":
                print(import_session(ROOT, session).relative_to(ROOT))
            else:
                clean(ROOT, session)
    except (ValueError, KeyError, OSError, sqlite3.Error, subprocess.CalledProcessError) as error:
        parser.exit(1, f"review: {error}\n")


if __name__ == "__main__":
    main()
