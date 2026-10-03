#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${PYTHON:-}" ]]; then
  python="$PYTHON"
elif [[ -x "$root/.venv-embed/bin/python" ]]; then
  python="$root/.venv-embed/bin/python"
elif [[ -x "$root/.venv/bin/python" ]]; then
  python="$root/.venv/bin/python"
else
  python=python3
fi
"$python" "$root/scripts/embed.py" --check

git -C "$root" add .
git -C "$root" commit -m "publish"
git -C "$root" push
