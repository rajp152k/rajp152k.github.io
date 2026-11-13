# Lab journal interface

Use green for primary text and the outer frame. Use violet for secondary
structure, source markers, and selection. The palette follows Raj's Bit-Mage
Ghostty, Neovim, and tmux configurations. Keep article text sharp. Apply a small
glow only to the active map point.

## Two relationships in one map

Position represents the archive-wide PCA projection of post embeddings. The
header gives input dimensions and retained variance. Read the method note below
the map for the projection limits.

A dim violet line represents an authored link from one post to another. The
build reads links from article bodies before term enhancement. It resolves
relative paths and URLs on the CNAME host, and keeps the first reference per
directed post pair. The active arrow points to the referenced post.

Choose a post with **Inspect** to see its references, backlinks, and three
nearest posts. Reference entries include a quoted passage and a link to its
source anchor. Nearest-post scores are cosine similarities computed from the
full embedding vectors. The scores use the whole archive, including posts
outside the selected collection or search results. Zero vectors have no
similarity results. Equal scores sort by post key.

Post IDs, source counts, numbered source lists, and section permalinks provide
stable navigation. Post reference sections are available without JavaScript.
On small screens, inspection expands the page so the map and notes have room.
Use the themed **Inspect** menu with a pointer, touch, or keyboard. Use Up/Down,
Home/End, or type part of a title to browse. Press Enter or Space to select.
Press Escape to close the menu, then Escape again to clear inspection. Use
**clear** to clear inspection directly. Press Tab to leave the menu.

## Channel links

`accounts.json` lists the social and YouTube links. The two channel images are
local assets. See `assets/channels/README.md` for their sources.

## Checks

Run `sh scripts/verify_preparation.sh` for the full check. The relationship
unit tests cover URL resolution, passage anchors, deduplication, and cosine
scores. The lab browser tests cover inspection, search filtering, map endpoints,
source navigation, reduced motion, mobile layouts, channel images, and article
links without JavaScript.
