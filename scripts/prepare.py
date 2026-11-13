"""Track editorial reviews and run the deterministic preparation stages.

A receipt records a review of specific inputs. It is not a semantic proof.
The state file is versioned but is never included in the public site.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from functools import partial

import markdown

from archive import ROOT, read_entries
from terms import load_terms, transform_html

STATE = ROOT / ".preparation.json"
POLICY = ROOT / "docs/editorial-policy.md"
STAGES = ("reader", "references")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def draft(entry):
    # Dates affect embeddings/metadata, not the meaning reviewed here.
    return digest({"title": entry.title, "body": entry.body})


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate preparation field {key!r}.")
        result[key] = value
    return result


def text(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def load_state(path=STATE):
    if not path.exists():
        return {"version": 1, "posts": {}}
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if (not isinstance(data, dict) or set(data) != {"version", "posts"}
            or type(data["version"]) is not int or data["version"] != 1
            or not isinstance(data["posts"], dict)):
        raise ValueError("Preparation state requires version 1 and a posts object.")
    for key, stages in data["posts"].items():
        if not text(key) or not isinstance(stages, dict) or set(stages) - set(STAGES):
            raise ValueError(f"Invalid preparation stages for {key!r}.")
        for receipt in stages.values():
            fields = {"inputs", "note", "decisions", "related", "questions", "blocking_questions"}
            if not isinstance(receipt, dict) or set(receipt) != fields or not text(receipt["note"]):
                raise ValueError(f"Invalid preparation receipt for {key}.")
            inputs = receipt["inputs"]
            if not isinstance(inputs, dict) or not inputs or any(
                    not text(name) or not isinstance(value, str) or len(value) != 64
                    or any(c not in "0123456789abcdef" for c in value)
                    for name, value in inputs.items()):
                raise ValueError(f"Invalid preparation input hashes for {key}.")
            for field in fields - {"inputs", "note"}:
                values = receipt[field]
                if not isinstance(values, list) or any(not text(v) for v in values) or len(values) != len(set(values)):
                    raise ValueError(f"Invalid preparation {field} for {key}.")
    return data


def save_state(data, path=STATE):
    """Replace state only after a complete write on the same filesystem."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, indent=2, sort_keys=True, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class Preparation:
    def __init__(self, entries, registry, policy):
        self.entries = {entry.key: entry for entry in entries}
        self.registry = registry
        self.policy = digest(policy)
        self.matches = {}
        for entry in entries:
            html = markdown.markdown(entry.body, extensions=["fenced_code", "tables"])
            self.matches[entry.key] = {match.term_id for match in transform_html(html, registry).mentions}

    def inputs(self, key, stage, related=()):
        entry = self.entries[key]
        result = {"draft": draft(entry), "policy": self.policy,
                  "stage": digest({"stage": stage, "version": 1})}
        if stage == "references":
            for term in self.registry.terms:
                if (term.id in self.matches[key] or term.introduction == key
                        or any(source.entry == key for source in term.sources)):
                    result[f"term:{term.id}"] = digest(asdict(term))
                    # Review a changed source context even if the exact quote survives.
                    dependencies = {source.entry for source in term.sources} | {term.introduction}
                    for source in sorted(dependencies):
                        result[f"source:{source}"] = draft(self.entries[source])
            for other in related:
                result[f"related:{other}"] = draft(self.entries[other]) if other in self.entries else digest(None)
        return result

    def stage_status(self, key, stage, receipt):
        if receipt is None:
            return "pending", ["no review"]
        current = self.inputs(key, stage, receipt["related"])
        changed = sorted(name for name in current.keys() | receipt["inputs"].keys()
                         if current.get(name) != receipt["inputs"].get(name))
        missing = [other for other in receipt["related"] if other not in self.entries]
        if changed or missing:
            return "stale", changed + [f"missing related post:{other}" for other in missing]
        if receipt["blocking_questions"]:
            return "blocked", receipt["blocking_questions"]
        return "current", []

    def report(self, state):
        posts = {}
        for key in sorted(self.entries):
            saved = state["posts"].get(key, {})
            posts[key] = {}
            for stage in STAGES:
                receipt = saved.get(stage)
                status, reasons = self.stage_status(key, stage, receipt)
                posts[key][stage] = {"status": status, "reasons": reasons,
                                     "questions": receipt["questions"] if receipt else []}
        removed = sorted(set(state["posts"]) - set(self.entries))
        ready = not removed and all(item["status"] == "current" for stages in posts.values() for item in stages.values())
        return {"ready": ready, "posts": posts, "removed": removed}

    def review(self, state, key, stage, note, decisions=(), related=(), questions=(), blocking_questions=()):
        if key not in self.entries:
            raise ValueError(f"Unknown post {key!r}; use its collection/slug key.")
        if stage not in STAGES or not text(note):
            raise ValueError("A valid stage and a nonempty review note are required.")
        if any(other not in self.entries or other == key for other in related):
            raise ValueError("Related posts must exist and differ from the reviewed post.")
        if stage == "reader" and related:
            raise ValueError("Record related reading in the references stage.")
        if stage == "references":
            reader = state["posts"].get(key, {}).get("reader")
            if self.stage_status(key, "reader", reader)[0] != "current":
                raise ValueError("Complete the current reader review before reviewing references.")
        lists = {"decisions": list(decisions), "related": list(related), "questions": list(questions),
                 "blocking_questions": list(blocking_questions)}
        for field, values in lists.items():
            if any(not text(value) for value in values) or len(values) != len(set(values)):
                raise ValueError(f"Review {field} must contain unique, nonempty text.")
        state["posts"].setdefault(key, {})[stage] = {
            "inputs": self.inputs(key, stage, related), "note": note, **lists,
        }


def print_report(report):
    for key, stages in report["posts"].items():
        print(key)
        for stage, item in stages.items():
            details = "; ".join(item["reasons"])
            print(f"  {stage}: {item['status']}" + (f" ({details})" if details else ""))
            for question in item["questions"]:
                print(f"    question: {question}")
    for key in report["removed"]:
        print(f"Removed post receipt: {key}; run ./prepare.sh prune after checking the deletion.")
    print("Editorial reviews are current." if report["ready"] else "Editorial work is pending; draft preview is available.")


def run_stage(script):
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status", help="show pending work without changing records")
    status.add_argument("--json", action="store_true")
    sub.add_parser("check", help="require current editorial reviews for release")
    sub.add_parser("build", help="update embeddings and build a draft; do not mark reviews complete")
    preview = sub.add_parser("preview", help="prepare a draft and serve it on loopback")
    preview.add_argument("--port", type=int, default=8765)
    review = sub.add_parser("review", help="record an editorial review that you have performed")
    review.add_argument("key")
    review.add_argument("--stage", choices=STAGES, required=True)
    review.add_argument("--note", required=True)
    for option in ("decision", "related", "question", "blocking-question"):
        review.add_argument(f"--{option}", action="append", default=[])
    sub.add_parser("prune", help="remove receipts for deleted posts")
    args = parser.parse_args(argv)
    try:
        entries = read_entries()
        preparation = Preparation(entries, load_terms(entries), POLICY.read_text(encoding="utf-8"))
        state = load_state()
        if args.command == "review":
            preparation.review(state, args.key, args.stage, args.note, args.decision, args.related,
                               args.question, args.blocking_question)
            save_state(state)
        elif args.command == "prune":
            state["posts"] = {key: value for key, value in state["posts"].items() if key in preparation.entries}
            save_state(state)
        report = preparation.report(state)
        if args.command == "status" and args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print_report(report)
        if args.command == "check" and not report["ready"]:
            return 1
        if args.command in {"build", "preview"}:
            sys.stdout.flush()
            run_stage("embed.py")
            run_stage("publish.py")
        if args.command == "preview":
            handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
            with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
                print(f"Preview: http://127.0.0.1:{server.server_port}/ (Ctrl-C to stop)", flush=True)
                server.serve_forever()
        return 0
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"prepare: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
