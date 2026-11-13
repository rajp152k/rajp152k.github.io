#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -eq 0 ]; then
    set -- build
fi
exec sh "$root/scripts/python.sh" "$root/scripts/prepare.py" "$@"
