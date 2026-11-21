"""Prepare immutable Potato sessions and import their native review evidence."""

from __future__ import annotations

import argparse
import hashlib
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


def prepare(root: Path, records: list[str], extra_sources: tuple[str, ...] | list[str] = ()) -> Path:
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
                          "text": f"TERM DECISION: {item_id}\n\nReview the exact candidate named above in this complete review record. Approval covers its exact details and use scope. Eligibility alone does not approve those details.\n\n{text}\n\nPOST SNAPSHOT\n\n{post}"})
        if entry.startswith("logs/"):
            items.append({"id": f"{entry}:cycle-{cycle}:log", "kind": "log",
                          "entry": entry, "record": name, "post": post_name,
                          "text": post})
    if not items:
        raise ValueError("No proposed terms or logs to review")
    if len({item["id"] for item in items}) != len(items):
        raise ValueError("Duplicate candidate or log IDs")
    for item in items:
        if item["kind"] == "term":
            for name in extra_sources:
                item["text"] += f"\n\nEVIDENCE SNAPSHOT: {name}\n\n{sources[name]['text']}"
    payload = {"schema": 1, "potato_version": VERSION, "sources": sources, "items": items}
    session_id = digest(json.dumps(payload, sort_keys=True).encode())[:20]
    session = root / ".reviews" / session_id
    if session.exists():
        if json.loads((session / "manifest.json").read_text()) != payload:
            raise ValueError("Existing session manifest differs")
        return session
    session.mkdir(parents=True)
    dump(session / "manifest.json", payload)
    dump(session / "data.json", [{"id": i["id"], "text": i["text"]} for i in items])
    config = {"annotation_task_name": f"Blog review {session_id}",
              "task_dir": str(session.resolve()), "data_files": ["data.json"],
              "item_properties": {"id_key": "id", "text_key": "text"},
              "output_annotation_dir": "annotation_output", "export_annotation_format": "jsonl",
              "require_password": False, "annotation_ui": {"memos": True, "visibility": "shared"},
              "annotation_schemes": [
                  {"annotation_type": "radio", "name": "decision",
                   "description": "Term decision only. Leave blank for log comments.",
                   "labels": ["approve", "request changes", "reject", "defer"]},
                  {"annotation_type": "text", "name": "comment", "description": "Reasons and corrections"}]}
    (session / "config.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    queue = sub.add_parser("queue", help="Freeze numbered Markdown review records")
    queue.add_argument("--source", action="append", default=[], help="Also freeze a local evidence source")
    queue.add_argument("records", nargs="+")
    serve = sub.add_parser("serve", help="Start or resume one prepared session on localhost")
    serve.add_argument("--session")
    serve.add_argument("--port", type=int, default=8768)
    for command in ("import", "clean"):
        sub.add_parser(command).add_argument("session")
    args = parser.parse_args()
    try:
        if args.command == "queue":
            print(prepare(ROOT, args.records, args.source).relative_to(ROOT))
        elif args.command == "serve":
            sessions = sorted((ROOT / ".reviews").glob("*/manifest.json"))
            if args.session:
                session = inside(ROOT / ".reviews", args.session)
            elif len(sessions) == 1:
                session = sessions[0].parent
            else:
                raise ValueError("Prepare one session with just queue-review, or pass --session ID")
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
