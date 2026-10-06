# meditations of yet another raj


## Writing and publishing

Human writing lives in `meditations/`; agent operational logs live in `logs/`. Both are
Markdown with YAML front matter. Create a meditation with `./write.sh "Title"`; the
command quotes titles safely and opens the file in Neovim. Agents write logs, not
meditation prose, unless explicitly asked to edit it. Markdown remains the source of truth.

Create logs only when requested. Use **Abstract**, **Context**, only the necessary
named sections, **Conclusion**, and **Past relevant meditations and blogs**. Explain
the work and its purpose in ASD-STE100, not as a report of agent tool calls.

### Local embedding setup

Inference uses Python 3.12 and a separate environment so publishing does not need
PyTorch. With [uv](https://docs.astral.sh/uv/) installed, create the environment
once, then install the pinned dependencies:

```sh
uv venv --python 3.12 .venv-embed
uv pip install --python .venv-embed/bin/python -r requirements-embed.txt
```

Leave an existing `.venv` alone. If `.venv-embed` already exists, skip its creation.
The first embedding update downloads the pinned model into the local Hugging Face
cache; subsequent updates can run offline.

### When to run embeddings

Run the updater after changing Markdown posts or the embedding policy, before
publishing. It synchronizes metadata and deletions as well as computing vectors:

| Change | Run `scripts/embed.py`? | Inference |
| --- | --- | --- |
| New meditation/log, title change, or changed prepared body text | Yes | Only missing/changed entries |
| Date-only correction, unchanged-content rename, namespace migration, or deleted entry | Yes | None; synchronize metadata/reuse vectors |
| Model/revision, chunking, preprocessing, or aggregation policy | Yes | Re-embed the archive |
| CSS, account-menu data/icons, map interaction, search logic, HTML layout, PCA presentation, or README | No | None |
| Nothing changed | Optional | None; unchanged state is a no-op |

The updater hashes the prepared title/body and complete embedding specification.
Formatting-only edits that leave prepared text unchanged reuse the vector.
Nothing runs automatically while writing: run the updater once a post is ready.
CI **never** computes embeddings or downloads a model.

### Preview and publish

Install Node.js 24+ and the pinned search/build dependencies once (or after changing
`package-lock.json`):

```sh
npm ci
```

After writing, revising, renaming, or deleting posts:

```sh
.venv-embed/bin/python scripts/embed.py
.venv-embed/bin/python scripts/publish.py
```

The second command builds `site/`, including the PCA map, lexical index, hashed
local assets, and public SQLite snapshot. For a local preview:

```sh
.venv-embed/bin/python -m http.server 8765 --directory site
```

Open <http://localhost:8765/>. For styling-only changes, skip the embed command
and just rebuild. Stop the preview server with Ctrl-C.

Review the changes, then commit and push:

```sh
./publish.sh
```

This checks freshness **before staging anything**, then stages all non-ignored
changes, commits, and pushes. It uses `.venv-embed/bin/python` if present, then
`.venv/bin/python`, then `python3`; override it with
`PYTHON=/path/to/python ./publish.sh` if needed. It does not run inference: a
stale-state error means run the updater locally, then publish again.

Commit `blog.sqlite` together with the post/configuration changes that produced
it. Do not commit `site/`, virtual environments, model weights, or SQLite journal,
WAL, and SHM files.

To check freshness without changing the database or loading the model:

```sh
.venv-embed/bin/python scripts/embed.py --check
```

A freshness check and the Python regression suite need only `requirements.txt`.
A site build also needs Node.js and `npm ci`; model inference additionally needs
`requirements-embed.txt`. Do not commit `node_modules/`.

### GitHub CI and deployment

The [Publish workflow](https://github.com/rajp152k/rajp152k.github.io/actions/workflows/publish.yml)
uses Python 3.13 with `requirements.txt`, Node.js 24, and `npm ci` to:

1. Check that the committed `blog.sqlite` matches the current posts and policy.
2. Run deterministic state/export, PCA geometry, and lexical-search regressions.
3. Generate the HTML, bundled assets, lexical index, PCA map, and allowlisted public database.
4. Upload `site/` and deploy GitHub Pages at <https://yetanotherraj.com/>.

Pull requests targeting `master` run validation and build, **not deployment**.
Pushes to `master` deploy when posts, scripts, assets, requirements, embedding
configuration/database, `logs/**`, authoring command, npm manifests, `accounts.json`, tests, the workflow, or `CNAME` change. README-only edits
do not trigger deployment. To republish unchanged content, use **Actions →
Publish → Run workflow** with branch `master`, or:

```sh
gh workflow run publish.yml --ref master
gh run list --workflow publish.yml --branch master --limit 5
gh run watch --exit-status
```

Select the relevant run when prompted. A successful push alone is not proof of
publication: wait for the **Deploy GitHub Pages** job to succeed, then open the
live domain and check the new post/layout. If validation fails, read the failing
step, fix/update state locally, and push the corrected posts and database;
the previous live site remains available.

## Embedding state

`embedding.json` pins
[`Alibaba-NLP/gte-modernbert-base`](https://huggingface.co/Alibaba-NLP/gte-modernbert-base)
to revision `e7f32e3c00f91d699e8c43b53106206bcc72bb22`. It produces 768-dimensional
vectors using the model's own pooling implementation.

Prepared input is the title followed by visible Markdown text. It preserves
headings, lists, code, mathematical notation, and paragraph boundaries while
excluding comments, script/style content, and link destinations.
The publication date is not part of the prepared text. Entry keys are
namespaced (`meditations/<slug>` or `logs/<slug>`); the namespace cutover reuses
unchanged vectors by prepared-text/model hashes rather than recomputing them.

Chunks contain at most **512 whitespace-delimited words** and **2,048 model
tokens**, including any input prefix and special tokens. Paragraph/sentence
boundaries are preferred when they do not make chunks unnecessarily small.
Oversized sentences or code are split using original character offsets, with
no overlap, omitted text, or silent truncation.

Chunk vectors are L2-normalized, averaged with actual input-token counts as
weights, then normalized again. Vectors are stored as little-endian float32.
CPU is the default; `--device mps` requests Apple GPU execution, and
`--device auto` chooses MPS when available. An unavailable explicitly requested
MPS device fails rather than silently switching backends.

### Recomputing only when necessary

Each post's embedding key is SHA-256 over its prepared text and the complete
embedding specification. The model tag is SHA-256 over the specification alone.
The specification includes the pinned model revision, text-preparation version,
chunk limits, input prefix, pooling, aggregation, normalization, and precision.

- New or substantively edited posts are embedded.
- Changing the model/revision or embedding policy invalidates the archive.
- Date-only corrections and unchanged-content renames reuse vectors.
- Deleted posts are removed without inference.
- Exact no-ops do not import inference libraries or modify the database.

Date, slug, and website styling are not embedding inputs. When changing the
text-preparation or aggregation implementation, update its named policy version
in both the implementation and `embedding.json`.

`blog.sqlite` stores the current state, not edit history:

- `model_specs`: the model tag and complete specification.
- `archive`: the active model tag, including for an empty archive.
- `posts`: namespaced entry keys in the physical `slug` column, title/date metadata,
  text and embedding hashes, and the vector.

Inference finishes before a write transaction begins. Synchronization is atomic,
and publishing opens the database read-only and refuses missing, stale, or
invalid vectors before clearing an existing site build.

SQLite state is a binary Git artifact: inspect it with SQLite rather than relying
on readable diffs, and avoid concurrent branch edits to it. It is derived data and
can be regenerated from the Markdown and pinned configuration.

For isolated archives or experiments, the embed command also accepts
`--posts PATH` (meditation directory), `--logs PATH`, `--database PATH`, and `--spec PATH`.
The default updater reads both collections. A missing logs directory is an empty collection.

## Account menu

The top-right header menu appears on the index, search page, and every post. Its initial
GitHub, Goodreads, and X destinations come from the profiles linked on the
[nilenso author page](https://nilenso.com/people/raj-patil/).

Edit `accounts.json`, an ordered array of entries:

```json
{
  "label": "GitHub",
  "url": "https://github.com/rajp152k",
  "icon": "github"
}
```

`label` supplies the accessible link name and hover hint, `url` the destination,
and `icon` the basename of a local `assets/icons/<icon>.svg`. Array order controls
menu order. The publisher reads the configuration once per build and embeds the
SVGs directly into each page; visitors fetch neither the JSON nor remote icons.
Links work without JavaScript. Icons are neon green, with brighter green on
hover/focus; on narrow screens the title wraps while the menu stays at the right.

SVG paths are vendored from Simple Icons 13.13.0 under
[CC0](https://cdn.jsdelivr.net/npm/simple-icons@13.13.0/LICENSE.md).
Account-data and icon changes trigger Pages CI without embedding inference.

## Homepage and PCA map

The homepage uses a compact, fixed-viewport split layout: an independently
scrolling chronological table on the left and an embeddings panel on the right.
Table headings stay visible while the rows scroll. On narrow screens, the panels
stack within the same fixed shell; the compact ID/title/date readout stays on one line.
Article pages share the Fira Mono, green-on-black treatment but retain normal
reading scroll.
The homepage is the combined chronological index. Native links select all entries
(`/`), meditations (`/meditations/`), or logs (`/logs/`), including without JavaScript.
The table and map keep their cross-highlighting; excluded source points are faint,
noninteractive context. Every view uses the same combined projection. Adding logs
can move the PCA coordinates or make its principal components log-dominated; source
filtering does not recompute the projection.

The palette follows the local tmux, Neovim, and Ghostty themes: pure black
(`#000000`), primary green (`#00ff00`), secondary green (`#00b300`), subdued
separators (`#006600`), and bright green/white for active targets. There are no
logos, decorative taglines, shadows, or promotional footers. Space is reserved
for the post list, coordinate diagram, projection statistics, and ID/title/date
readout.

Violet (`#a878e8`) is limited to the model-card link, active point ring, and
matching row marker. The active row uses a near-black violet tint (`#150d20`);
its text and point stay white. Frames, axes, ordinary points, headings, body text,
keyboard focus outlines, and text selection retain their green treatment.

During publishing, `scripts/projection.py` reads the validated SQLite vectors and
uses NumPy's exact centered SVD to project them into two principal components.
There is no feature standardization or whitening. The SVG uses a single scale
for both axes so the display does not stretch distances independently.
The displayed PC1/PC2 axes intersect at zero PCA scores, rather than the center
of the panel's bounding box.

Coordinates are derived on each build, not saved as embedding state. They can
move as posts are added or revised. The retained-variance caption measures
projection fidelity, not semantic accuracy; with three posts, two components can
retain all centered variance. Empty, single-post, and identical-vector archives
are handled without inventing separation.
The PCA heading includes a small link to the configured embedding model's Hugging
Face model card; its label and URL come from `embedding.json`.

Meditations have `mx0`, `mx1`, …, `mxf`, `mx10`, … display codes; logs have
`lx0`, `lx1`, …, `lxf`, `lx10`, … . Each collection has its own zero-based lowercase
hexadecimal sequence, assigned chronologically from oldest to newest. Adding a log
does not renumber meditations. Filled circles are meditations, outlined circles are
logs; a compact legend explains the shapes. The index pairs codes with full titles.
PCA points have no visible labels. The footer shows ID, full title, and date on
hover or focus; accessible point links retain the title without native hover tooltips.

IDs are derived presentation indexes, not stored identities or permalinks:
backdated insertions, deletions, or changes to archive ordering can renumber them.
Hovering or focusing either view still highlights the corresponding entry in
both views. Each point is a native post link, so navigation
still works without JavaScript. The homepage loads only local assets: it does
not fetch the SQLite file, run an embedding model, or require a charting framework.

`assets/site.css` controls the shared visual treatment; `assets/map.js` supplies
the linked-view interaction shared by `assets/index.js` and `assets/search.js`.
Publishing uses pinned Markdown/NumPy/PyYAML from `requirements.txt` and MiniSearch/esbuild
from `package-lock.json`; inference dependencies remain separate.

## Operational logs

Keep each log in one Markdown file directly in `logs/`. Use only title and date
in front matter:

```yaml
title: Two collections, one archive
date: 2026-10-06T10:54:12Z
```

The current publisher requires a timezone-aware log date. Log pages show the title,
date, and body. Do not add agent metadata, status, contributors, or raw artifacts.
Put relevant links to past meditations and blogs in the body, not in metadata.
No per-entry directories are needed.

Use these top-level Markdown headings in order:

- **Abstract:** a brief account of the log.
- **Context:** the starting state and the reason for the work.
- **Named sections:** a dynamic number of sections that connect the whole story. Keep material decisions, changes, and resulting behavior.
- **Conclusion:** the result or expected new state. Distinguish plans from completed work.
- **Past relevant meditations and blogs:** links to relevant existing posts.

Refer to the author as **raj**, not “the user.” Keep the wording concise without
removing useful detail about the work, interface, routes, or data flow.

Draft iteration and commit are separate steps. During iteration, edit and preview
locally; do not stage, commit, push, or publish. Commit an agreed version only when
raj explicitly asks. Push or publish only with separate approval. Do not use
`publish.sh` for a commit-only request: it stages all non-ignored files and pushes.

Use [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) for log
prose. Use short sentences and consistent terms. The official standard has writing
rules and a controlled dictionary; AI output alone does not prove compliance.
[Request the official Issue 9 copy](https://www.asd-ste100.org/STE_downloads.html)
for a complete dictionary review. Use Mermaid diagrams or math only when they
make the information clearer. Prefer an inline SVG for an accurate UI wireframe.

### Mermaid diagrams

Write a diagram in a fenced `mermaid` block. Include an accessible title and, when
needed, a description:

````markdown
```mermaid
flowchart LR
  accTitle: Draft review
  accDescr: raj reviews a local draft before a separate commit request.
  Draft --> Preview --> Review
  Review -->|Revise| Draft
  Review -->|Explicit request| Commit
```
````

The build bundles pinned Mermaid locally into hashed ES modules. Only articles
with Mermaid blocks load the diagram entry; diagram modules load as needed.
Diagrams use the site colors and font. Strict security disables diagram links
and HTML labels. An invalid diagram keeps its source and shows an error; later
diagrams still render. With JavaScript disabled, the source remains readable.
No artifact files or per-log directories are needed.

Log URLs remain `/logs/<slug>/`; meditation URLs remain `/<slug>/`. Archive codes,
source filters, and the combined PCA map are unchanged. Meditation slugs `search`,
`logs`, and `meditations` are reserved. Duplicate YAML keys and malformed dates
are rejected. The site is staged before it replaces the previous preview.

## Lexical search

Every page has a native GET form targeting `/search/?q=…`. At widths of at least
900px it sits between the site name and account icons, separated by vertical rules;
on narrow screens it moves below them. Searches respect the selected collection.

The static search page uses MiniSearch 7.2.0 with AND matching across title, headings,
and body, weighted **5 / 2 / 1**. Headings and titles are not duplicated into body.
Tokens use Unicode NFKC and lowercase, preserve internal apostrophes and `C++`/`C#`,
and split punctuation, hyphens, and underscores. Terms of at least three Unicode
codepoints also match word prefixes. There is no stemming, fuzzy matching, phrase
syntax, or operator language. Score ties use newest date, then binary namespaced key order.

Results highlight complete matching tokens and show one block-bounded excerpt of
up to 220 codepoints plus ellipses, preferring distinct term coverage, exact matches,
then the earliest block/window. Title-only matches use the opening body block.
Text extraction is shared with embedding preparation without changing embedding inputs.
The collection selector is separate from query syntax and persists as
`kind=all|meditations|logs` in search URLs. Empty queries list that collection without
fetching the index. The shared payload uses schema version 2 and namespaced keys,
so equal slugs in different collections do not collide. Only the title and visible
Markdown headings and body text enter the lexical fields.

Only matching rows remain in the table. Nonmatching map points stay at their
archive-wide coordinates and become faint, noninteractive context; IDs, axes,
scale, and retained variance do not change with the query. Live edits are debounced
and replace the current URL rather than creating a history entry for each edit.
Native post links preserve modified clicks, and Back restores query, result scroll,
and the activated post. IME composition is respected. With a usable viewport below
480px the search page allows document scrolling as well as result scrolling.

The publisher builds a content-addressed `search-index.<sha256>.json` and hashed
JavaScript, CSS, and font assets before replacing the previous preview. The search
page fetches the index only for searchable input and rejects incompatible payloads.
Homepage and article pages do not fetch it or the SQLite artifact. Search requires
JavaScript; without it, the search page links to the fully usable archive. Loading,
empty, no-match, punctuation-only, and unavailable-index states are explicit.

## Public SQLite artifact

Every site build creates a fresh, allowlisted `site/blog.sqlite`, available as
`/blog.sqlite` after deployment. It is **not** a copy of the working database:
internal hashes, complete specifications, bodies, unrelated local tables, and
deleted records are excluded.

The public schema has `PRAGMA user_version = 2`:

| Table | Columns |
| --- | --- |
| `model` | `tag`, `model_id`, `revision`, `dimension`, `dtype` |
| `posts` | `entry_key`, `kind`, `slug`, `title`, `published_date`, `url`, `model_tag`, `embedding` |

`entry_key` is the namespaced primary key; `kind` is `meditations` or `logs`, and
`slug` is the leaf slug. `posts.model_tag` references `model.tag`. Meditation dates
use ISO `YYYY-MM-DD`; log timestamps use canonical UTC ISO datetime. URLs are
root-relative. `model.dtype` is `<f4`: each embedding BLOB contains
`dimension` little-endian float32 values, normalized to unit L2 length.

```sh
sqlite3 site/blog.sqlite \
  'SELECT entry_key, kind, title, length(embedding) AS vector_bytes FROM posts;'
```

This is a downloadable data artifact, not a search endpoint. No SQLite download
link is shown in the rendered pages. The artifact remains available at its
explicit URL; the website does not automatically download it, and no browser
SQLite runtime is included.

## Verification

Run deterministic state, integrity, front-matter boundaries, text-preparation, export, PCA geometry, and lexical-search regressions:

```sh
.venv-embed/bin/python -m unittest discover -s tests -v
npm test
```

Real-model and tokenizer smoke scenarios were exercised separately: initial
embedding, offline no-op, metadata changes, one-post edits/additions, policy
invalidation, deletion/empty archives, and lossless word/token-bounded chunks.
