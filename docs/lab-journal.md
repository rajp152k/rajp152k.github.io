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

Click or tap a map circle to open its **Inspect** card below the map. The card
shows the post title, date, and opening excerpt. Follow the title to read the
post. Select another circle to update the card. Expand **References and similarity**
to see references, backlinks, and three nearest posts. Reference entries include
a quoted passage and a link to its source anchor. Nearest-post scores are cosine
similarities computed from the full embedding vectors. The scores use the whole archive, including posts
outside the selected collection or search results. Zero vectors have no
similarity results. Equal scores sort by post key.

Post IDs, source counts, numbered source lists, and section permalinks provide
stable navigation. Post reference sections are available without JavaScript.
On small screens, inspection expands the page so the map and notes have room.
With a keyboard, use Tab to focus a circle. Press Enter or Space to inspect it
and move focus to the card title. Press Enter again to read the post. Press
Escape or use **clear** to close the card and return focus to the selected circle.
Without JavaScript, follow the circle link directly to the post.

## Channel links

`accounts.json` lists the social and YouTube links. The two channel images are
local assets. See `assets/channels/README.md` for their sources.

## Checks

Run `just check` for the full check. The relationship
unit tests cover URL resolution, passage anchors, deduplication, and cosine
scores. The lab browser tests cover inspection, search filtering, map endpoints,
source navigation, reduced motion, mobile layouts, channel images, and article
links without JavaScript.
