"""Compact outlink and explicit no-outlinks cards for Potato."""
from datetime import date, datetime
import html
import re
from urllib.parse import quote

import yaml


def post_date(text: str):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("Missing post publication metadata")
    value = yaml.safe_load(match[1])["date"]
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00")) if "T" in value else date.fromisoformat(value)
    if not isinstance(value, date) or isinstance(value, datetime) and value.tzinfo is None:
        raise ValueError("Publication date must be a date or timezone-aware timestamp")
    return value


def earlier(target, source) -> bool:
    """Same-day order is known only when both posts have timestamps."""
    if isinstance(target, datetime) and isinstance(source, datetime):
        return target < source
    return (target.date() if isinstance(target, datetime) else target) < (source.date() if isinstance(source, datetime) else source)


def outlink_items(meta: dict, name: str, record: str, sources: dict, freeze) -> list[dict]:
    """Validate the batch, then freeze exact source and target details in each card."""
    posts = {}
    for entry, expected_hash in meta["posts"].items():
        if not entry.startswith(("logs/", "meditations/")) or len(entry.split("/")) != 2:
            raise ValueError(f"Unknown post entry: {entry}")
        path = f"{entry}.md"
        text = freeze(path)
        if sources[path]["sha256"] != expected_hash:
            raise ValueError(f"Review post hash is stale: {path}")
        posts[entry] = (text, post_date(text))
    cycle = meta["cycle"]
    if not isinstance(cycle, int) or cycle < 1:
        raise ValueError("Review cycle must be a positive integer")
    items = []
    for kind, candidates in (("link", meta.get("links", [])), ("no-links", meta.get("no_links", []))):
        for candidate in candidates:
            if candidate["state"] != "proposed":
                continue
            revision = candidate["revision"]
            if not isinstance(revision, int) or revision < 1:
                raise ValueError("Candidate revision must be a positive integer")
            entry = candidate["entry"]
            post, published = posts[entry]
            card = candidate["card"]
            fields = ["placement", "passage", "proposed", "purpose", "reason"]
            if kind == "link":
                fields += ["evidence"]
            if any(not isinstance(card.get(key), str) or not card[key].strip() for key in fields):
                raise ValueError("Missing or invalid outlink card field")
            if card["passage"] not in post:
                raise ValueError(f"Source passage is missing: {entry}")
            rows = [("Source", entry), ("Source publication", published.isoformat())]
            evidence = [("Full review record", record), ("Full source post", post)]
            if kind == "link":
                target = candidate["target"]
                target_post, target_date = posts[target]
                if not earlier(target_date, published):
                    raise ValueError(f"Target must be strictly earlier: {target}")
                if card["evidence"] not in target_post:
                    raise ValueError(f"Target evidence is missing: {target}")
                prefix = "/logs/" if target.startswith("logs/") else "/"
                url = prefix + quote(target.split("/")[1], safe="") + "/"
                if f"]({url})" not in card["proposed"]:
                    raise ValueError(f"Proposed link must use target path: {url}")
                rows += [("Target", target), ("Target publication", target_date.isoformat())]
                evidence.append(("Full target post", target_post))
            else:
                rows += [("Target", "None. Confirm no outlinks are needed.")]
            rows += [(key.replace("_", " ").title(), card[key]) for key in fields]
            rows += [("Rule", "Link only to strictly earlier published posts. Do not infer same-day order or add reverse links.")]
            item_id = f"{entry}:cycle-{cycle}:{candidate['id']}:r{revision}"
            esc = lambda value: html.escape(str(value), quote=True)
            table = "".join(f"<tr><th style='text-align:left;vertical-align:top;padding:4px 16px 4px 0'>{esc(label)}</th><td>{esc(value)}</td></tr>" for label, value in rows)
            details = "".join(f"<details><summary>{esc(label)}</summary><pre style='white-space:pre-wrap'>{esc(text)}</pre></details>" for label, text in evidence)
            rendered = (f"<div><small>{esc(item_id)}</small><h3>{'Outlink proposal' if kind == 'link' else 'No outlinks needed'}</h3>"
                        f"<table>{table}</table><p>Approve this exact revision only. A blank decision is not approval.</p>{details}</div>")
            items.append({"id": item_id, "kind": kind, "entry": entry,
                          "candidate": candidate["id"], "revision": revision,
                          "record": name, "post": f"{entry}.md", "text": rendered})
    return items
