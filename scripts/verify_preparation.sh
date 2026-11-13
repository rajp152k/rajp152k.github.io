#!/bin/sh
# Final local and CI checks. Requires npm ci and Playwright Chromium.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"
sh scripts/python.sh scripts/prepare.py check
sh scripts/python.sh scripts/terms.py --check
sh scripts/python.sh scripts/embed.py --check
sh scripts/python.sh -m unittest discover -s tests -v
npm test
sh scripts/python.sh scripts/publish.py
npm run test:browser
git diff --check
git diff --cached --check
