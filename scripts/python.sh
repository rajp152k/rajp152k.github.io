#!/bin/sh
# Run project Python with one interpreter selection rule.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -n "${PYTHON:-}" ]; then
    exec "$PYTHON" "$@"
elif [ -x "$root/.venv-embed/bin/python" ]; then
    exec "$root/.venv-embed/bin/python" "$@"
elif [ -x "$root/.venv/bin/python" ]; then
    exec "$root/.venv/bin/python" "$@"
else
    exec python3 "$@"
fi
