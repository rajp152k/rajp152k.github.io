# List available blog commands.
default:
  @just --list

# Install lockfile-pinned dependencies.
install:
  npm ci

# Build with the pinned SSG dependency.
build:
  npm run blog:build

# Run the development server with the pinned SSG dependency.
dev:
  npm run blog:dev

# Build and prepare the GitHub Pages output.
check:
  npm run blog:check

# Create a curated canvas post.
new title:
  npm run blog:new -- {{quote(title)}}

# Create a meditation.
meditation title:
  npm run blog:new:meditation -- {{quote(title)}}

# Refresh templates from the pinned SSG dependency.
sync:
  npm run blog:sync-templates

# Refresh templates from the sibling SSG checkout.
sync-local:
  npm run blog:sync-templates:local
