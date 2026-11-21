set positional-arguments

# List available commands.
default:
    @just --list

# Create a meditation and open Neovim.
write title:
    ./write.sh "$1"

# Update embeddings and build the site.
prepare:
    ./prepare.sh build

# Prepare and serve a preview; optional arguments: --port 8766.
preview *args:
    ./prepare.sh preview "$@"

# Show current, pending, stale, and blocked reviews.
status:
    ./prepare.sh status

# Install the pinned browser review tool in its own uv environment.
setup-review:
    uv venv --python 3.12 .venv-review
    uv pip install --python .venv-review/bin/python -r requirements-review.txt

# Freeze exact Markdown review records and post snapshots.
queue-review +records:
    sh scripts/python.sh scripts/review.py queue "$@"

# Start/resume Potato; legacy ENTRY --stage arguments record a review receipt.
review *args:
    if [ "$#" -gt 0 ] && [ "${1#--}" = "$1" ]; then ./prepare.sh review "$@"; else sh scripts/python.sh scripts/review.py serve "$@"; fi

# Record a completed editorial review receipt.
record-review +args:
    ./prepare.sh review "$@"

# Import native annotations and memos into a durable report.
import-reviews session:
    sh scripts/python.sh scripts/review.py import "$1"

# Remove only a scratch session whose current responses were imported.
clean-reviews session:
    sh scripts/python.sh scripts/review.py clean "$1"

# Check editorial review freshness and term records.
review-check:
    ./prepare.sh check

# Remove review records for intentionally deleted posts.
prune:
    ./prepare.sh prune

# Run all release checks, including browser tests.
check:
    sh scripts/verify_preparation.sh

# Publish approved commits from a clean master checkout.
publish:
    ./publish.sh

# Update embeddings only.
embed:
    sh scripts/python.sh scripts/embed.py

# Build only, without updating embeddings.
build:
    sh scripts/python.sh scripts/publish.py

# Compatibility alias for the former embed/build/serve sequence.
e2e: preview
