#!/bin/sh
# Publish reviewed, committed work after explicit approval.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$root"
if [ "$(git branch --show-current)" != master ]; then
    printf '%s\n' 'publish: use the approved master branch.' >&2
    exit 1
fi
if [ -n "$(git status --porcelain)" ]; then
    printf '%s\n' 'publish: inspect and commit intended changes first.' >&2
    exit 1
fi
sh scripts/verify_preparation.sh
if [ -n "$(git status --porcelain)" ]; then
    printf '%s\n' 'publish: checks changed files; inspect them before publishing.' >&2
    exit 1
fi
git push
