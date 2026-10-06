#!/usr/bin/env bash
set -euo pipefail

if (($# == 0)); then
  printf 'usage: %s "title"\n' "$0" >&2
  exit 1
fi

title="$*"
slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/^-//; s/-$//')"

if [[ -z "$slug" ]]; then
  printf 'title must contain a letter or number\n' >&2
  exit 1
fi

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
file="$root/meditations/$slug.md"

if [[ -e "$file" ]]; then
  printf 'meditation already exists: %s\n' "$file" >&2
  exit 1
fi

quoted_title="$(python3 -c 'import json, sys; print(json.dumps(sys.argv[1], ensure_ascii=False))' "$title")"
printf -- '---\ntitle: %s\ndate: %s\n---\n\n' "$quoted_title" "$(date +%F)" >"$file"
exec nvim "$file"
