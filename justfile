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

# Record a completed review: ENTRY --stage STAGE --note "...".
review +args:
    ./prepare.sh review "$@"

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
