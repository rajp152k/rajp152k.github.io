#!/usr/bin/env python3
"""Generate the meditation index in README.md."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDITATIONS = ROOT / "meditations"
README = ROOT / "README.md"
START = "<!-- meditations:start -->"
END = "<!-- meditations:end -->"
FRONT_MATTER = re.compile(r"\A---\n(?P<front_matter>.*?)\n---\n", re.DOTALL)


def meditation_row(path: Path) -> tuple[date, str, str]:
    match = FRONT_MATTER.match(path.read_text())
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

    return date.fromisoformat(published), title, path.name


def index() -> str:
    rows = sorted((meditation_row(path) for path in MEDITATIONS.glob("*.md")), reverse=True)
    table = ["| Date | Meditation |", "| --- | --- |"]
    table.extend(f"| {published.isoformat()} | [{title}](meditations/{filename}) |" for published, title, filename in rows)
    return "\n".join((START, *table, END))


def main() -> None:
    readme = README.read_text()
    replacement = index()
    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    updated, count = pattern.subn(replacement, readme)
    if count != 1:
        raise ValueError("README.md must contain one meditation index marker pair")

    if "--check" in sys.argv:
        if updated != readme:
            raise SystemExit("README.md is stale; run scripts/generate_readme.py")
        return

    README.write_text(updated)


if __name__ == "__main__":
    main()
