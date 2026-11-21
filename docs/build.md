# Build reference

See [local setup](../README.md#local-setup) for dependencies,
[writing](writing.md) for preparation stages, and [cooperation](cooperation.md)
for approval boundaries. Run commands below from the repository root.

## Inputs and generated state

The archive reads every top-level `*.md` file in `meditations/` and `logs/`.
There is no draft or future-date exclusion. Meditation routes are `/<slug>/`;
log routes are `/logs/<slug>/`. Meditation slugs `search`, `logs`, `meditations`,
and `terms` are reserved. Duplicate YAML keys and malformed dates fail validation.
Log dates require a timezone. See the [ops-log skill](../.agents/skills/ops-log/SKILL.md)
for log front matter and prose.

| File | Purpose |
| --- | --- |
| `embedding.json` | Pinned model and text/embedding policy |
| `blog.sqlite` | Current local embedding state |
| `terms.json` | Definitions, aliases, sources, and further reading |
| `.preparation.json` | Internal editorial reviews and questions |
| `accounts.json` | Ordered account links and local image references |
| `site/` | Generated site, assets, search index, and public database |

The build validates saved state and generates output in a staging directory
before replacing the local preview. Builds use saved reviews and term records;
they do not perform editorial review or model inference. Preparation runs the
embedding updater before the build. CI checks committed embeddings without
loading a model.

## Embeddings and cache

`embedding.json` pins
[`Alibaba-NLP/gte-modernbert-base`](https://huggingface.co/Alibaba-NLP/gte-modernbert-base)
to revision `e7f32e3c00f91d699e8c43b53106206bcc72bb22`. The model produces
768-dimensional vectors with its own pooling implementation. The first update
downloads the pinned model into the local Hugging Face cache. Later updates can
run offline with that cache.

Prepared input is the title followed by visible Markdown text. It preserves
headings, lists, code, mathematical notation, and paragraph boundaries. It omits
comments, script/style content, and link destinations. Dates are not input text.
Entry keys use `meditations/<slug>` or `logs/<slug>`. Namespace migrations reuse
unchanged vectors by prepared-text and model hashes.

Chunks contain at most **512 whitespace-delimited words** and **2,048 model
tokens**, including any input prefix and special tokens. Chunking prefers
paragraph and sentence boundaries unless these make chunks unnecessarily small.
Oversized sentences and code split at original character offsets, without
overlap, omitted text, or silent truncation.

Chunk vectors are L2-normalized, averaged with actual input-token counts as
weights, then normalized again. Storage uses little-endian float32. CPU is the
default. `--device mps` requests Apple GPU execution; `--device auto` selects MPS
when available. An explicit unavailable MPS device causes failure.

### Update rules

| Change | Run updater? | Inference |
| --- | --- | --- |
| New post, changed title, or changed prepared body | Yes | Missing or changed entries |
| Date correction, unchanged-content rename, namespace migration, deletion | Yes | None; synchronize metadata and reuse vectors |
| Model, revision, chunking, preprocessing, or aggregation policy | Yes | Entire archive |
| CSS, accounts/icons, map, search, HTML layout, PCA presentation, documentation | No | None |
| No change | Optional | None; no-op |

Run the updater directly when needed:

```sh
sh scripts/python.sh scripts/embed.py
```

Each embedding key is SHA-256 over the prepared text and complete embedding
specification. The model tag hashes the specification alone. It includes the
pinned revision, text-preparation version, chunk limits, input prefix, pooling,
aggregation, normalization, and precision. Formatting-only edits reuse vectors
when prepared text is unchanged. Exact no-ops neither import inference libraries
nor modify the database.

When changing text preparation or aggregation, update its named policy version
in both the implementation and `embedding.json`. The updater accepts `--posts PATH`
for meditations, `--logs PATH`, `--database PATH`, and `--spec PATH` for isolated
archives. Defaults read both collections; a missing logs directory is empty.

### Working database

`blog.sqlite` stores current state rather than edit history:

- `model_specs`: model tag and complete specification.
- `archive`: active model tag, including for an empty archive.
- `posts`: namespaced entry keys in the physical `slug` column, title/date
  metadata, text and embedding hashes, and vectors.

Inference finishes before the write transaction starts. Synchronization is
atomic. The site builder opens the database read-only and rejects missing,
stale, or invalid vectors before replacing the previous preview.

Inspect binary changes with SQLite. Avoid concurrent branch edits to this file.
Regenerate it from Markdown and the pinned configuration when needed.

## Rendering and assets

Build dependencies are pinned in `requirements.txt` and `package-lock.json`.
Python handles Markdown, YAML, and NumPy projection. esbuild bundles local assets;
MiniSearch supplies lexical search. Inference dependencies are separate.

`assets/site.css` defines the shared style. `assets/map.js` supplies linked-view
behavior for `assets/index.js` and `assets/search.js`. See the
[lab journal](lab-journal.md) for approved layout, inspection, keyboard, touch,
and reference-panel interactions.

### PCA projection

`scripts/projection.py` uses NumPy's exact centered SVD on validated SQLite
vectors. There is no feature standardization or whitening. The SVG uses one
scale for both axes; PC1 and PC2 intersect at zero PCA scores.

Coordinates are generated on each build, not saved in embedding state. They can
move as posts change. All collection and search views use the combined archive
projection. Filtering does not recompute coordinates, axes, scale, or variance.
Added logs can move points or dominate principal components.

Retained variance measures projection fidelity, not semantic accuracy. Two
components can retain all centered variance for three posts. Empty, single-post,
and identical-vector archives do not receive invented separation. The model-card
link label and URL come from `embedding.json`.

Meditation display codes are `mx0`, `mx1`, …, `mxf`, `mx10`, …; log codes are
`lx0`, `lx1`, …, `lxf`, `lx10`, … . Each collection has a separate zero-based,
lowercase hexadecimal sequence, assigned oldest first. Adding a log does not
renumber meditations. Backdated insertions, deletions, and ordering changes can
renumber codes. Codes are presentation indexes, not stored identities or URLs.
The homepage uses local assets without a chart framework, model execution, or
SQLite download.

### Accounts

Edit `accounts.json`, an ordered array. For an SVG icon, use:

```json
{"label": "GitHub", "url": "https://github.com/rajp152k", "icon": "github"}
```

`label` supplies the accessible name and hover hint; `url` is the destination.
`icon` names `assets/icons/<icon>.svg`. Channel entries use `image` to name a
local file in `assets/channels/`, such as `bitmage.png`. See
[channel provenance](../assets/channels/README.md) for the transparent logos.
Array order controls menu order. During a build, SVGs are embedded in each page;
visitors fetch neither account JSON nor remote icons. Links work without JavaScript.

The initial GitHub, Goodreads, and X destinations came from the
[nilenso author page](https://nilenso.com/people/raj-patil/). SVG paths are from
Simple Icons 13.13.0 under [CC0](https://cdn.jsdelivr.net/npm/simple-icons@13.13.0/LICENSE.md).
Account and icon changes trigger Pages CI without embedding inference.

### Mermaid

Use a fenced `mermaid` block. Supply an accessible title and, when needed, a
description:

```text
flowchart LR
  accTitle: Build stages
  accDescr: Validate saved state, build the site, then check the output.
  Validate --> Build --> Check
```

Pinned Mermaid is bundled locally into hashed ES modules. Only articles with
Mermaid blocks load the diagram entry; other diagram modules load as needed.
Diagrams use site colors and font. Strict security disables diagram links and
HTML labels. Invalid diagrams show their source and an error without stopping
later diagrams. With JavaScript disabled, readers see the source.

## Lexical search

Every page has a native GET form for `/search/?q=…`. The collection parameter is
`kind=all|meditations|logs`, separate from query syntax. Empty queries list the
selected collection without fetching the index.

MiniSearch 7.2.0 uses AND matching across title, headings, and body with weights
**5 / 2 / 1**. Titles and headings are not duplicated into body text. Tokens use
Unicode NFKC and lowercase, preserve internal apostrophes and `C++`/`C#`, and split
punctuation, hyphens, and underscores. Terms of at least three Unicode codepoints
also match prefixes. Search has no stemming, fuzzy matching, phrase syntax, or
operator language. Score ties use newest date, then binary namespaced-key order.

Results highlight whole matching tokens. Each excerpt stays within one block,
uses at most 220 codepoints plus ellipses, and prefers distinct term coverage,
exact matches, then the earliest block/window. Title-only matches use the first
body block. Text extraction is shared with embedding preparation; search does
not alter embedding inputs. Only titles and visible Markdown headings and body
enter lexical fields. Payload schema 2 uses namespaced keys to avoid collisions.

Only matches appear as table rows. Nonmatches keep their archive-wide map
coordinates as faint, noninteractive context. Live query edits are debounced and
replace the URL. Modified link clicks work; Back restores query, result scroll,
and the activated post. Input respects IME composition.

The build creates `search-index.<sha256>.json` and hashed JavaScript, CSS, and
font assets. Search fetches the index only for searchable input and rejects
incompatible payloads. Homepage and article pages fetch neither this index nor
SQLite. Without JavaScript, readers can follow the search page's archive link.
The page distinguishes loading, empty query, no matches, punctuation-only input,
and an unavailable index.

## Terms and references

`terms.json` contains definitions and aliases. See the
[editorial policy](editorial-policy.md) for selection rules and the initial
[archive review](archive-review.md) for inclusion and exclusion decisions.
Generate a deterministic mention report with:

```sh
sh scripts/python.sh scripts/terms.py --json
```

The build validates records and marks the first eligible mention per term per
post. A term can set optional `annotation` to `first-term` (the default) or
`first-spelling`. Use `first-spelling` only when the approved scope needs the
first occurrence of the name and each alias. Case and whitespace differences
count as the same spelling. Each term has one anchor and one post reference,
even when it has several marked spellings.

Matching skips existing links, headings, code, and quotations; it uses whole
words, ignores case, and prefers the longest alias. Generated spans do not
change Markdown source. Search and embeddings use the original post. `/terms/`
and `/terms/<id>/` are navigation pages, not archive entries.

The registry has no per-post scope filter. Check the complete mention report
against the approved scope before committing a term and after archive edits.

Record validation failure stops the build before preview replacement. Builds use
saved records without model calls. Term-only changes need no embedding update.
See the [lab journal](lab-journal.md) for reference-panel behavior.

## Public SQLite artifact

Each build creates an allowlisted `site/blog.sqlite`, available at `/blog.sqlite`
after deployment. It is a fresh export, not a copy of the working database.
It excludes internal hashes, complete specifications, bodies, unrelated local
tables, and deleted records.

The public schema has `PRAGMA user_version = 2`:

| Table | Columns |
| --- | --- |
| `model` | `tag`, `model_id`, `revision`, `dimension`, `dtype` |
| `posts` | `entry_key`, `kind`, `slug`, `title`, `published_date`, `url`, `model_tag`, `embedding` |

`entry_key` is the namespaced primary key. `kind` is `meditations` or `logs`;
`slug` is the leaf slug. `posts.model_tag` references `model.tag`. Meditation
dates use `YYYY-MM-DD`; log timestamps use canonical UTC ISO datetime. URLs are
root-relative. `model.dtype` is `<f4`; each BLOB holds `dimension` little-endian
float32 values with unit L2 length.

```sh
sqlite3 site/blog.sqlite \
  'SELECT entry_key, kind, title, length(embedding) AS vector_bytes FROM posts;'
```

This is a downloadable artifact, not a search endpoint. Pages have no SQLite
link or automatic download, and include no browser SQLite runtime.

## Technical checks

Run the full release check after setup:

```sh
just check
```

It requires current editorial reviews and committed embedding state, runs Python
and lexical-search tests, builds the site, and runs Chromium browser tests. It
performs no inference. CI runs the underlying `scripts/verify_preparation.sh` script.

For focused checks:

```sh
sh scripts/python.sh -m unittest discover -s tests -v
npm test
# After a site build:
npm run test:browser
```

Tests cover state integrity, front-matter boundaries, text preparation, export,
PCA geometry, terms, preparation, search, and browser interaction. Browser checks
include desktop, keyboard, phone, touch, and JavaScript-disabled reading.
Screenshots and reports are ignored local files under `test-results/`.

Separate real-model/tokenizer smoke checks have covered initial embedding,
offline no-op, metadata changes, post edits/additions, policy invalidation,
deletion, empty archives, and lossless word/token-bounded chunks.

## CI and deployment

The [Publish workflow](https://github.com/rajp152k/rajp152k.github.io/actions/workflows/publish.yml)
uses Python 3.13 with `requirements.txt`, Node.js 24, `npm ci`, and Chromium.
It validates editorial reviews and fresh embeddings, runs the release checks,
then uploads `site/`. It never downloads a model or computes embeddings.

Pull requests targeting `master` validate and build without deployment. Pushes
to `master` deploy when paths listed in
[the workflow](../.github/workflows/publish.yml) change. These include site inputs,
authoring scripts, review state, editorial policy, tests, and the workflow itself.
README-only edits do not trigger deployment. Deployment uses GitHub Pages at
<https://yetanotherraj.com/>.

`publish.sh` requires a clean `master` checkout, runs the release checks, checks
cleanliness again, then runs `git push`. It neither stages files nor makes commits.
Use the [cooperation guide](cooperation.md) for publication authority.

After approval to redeploy unchanged content, select **Actions → Publish → Run
workflow** on `master`, or run:

```sh
gh workflow run publish.yml --ref master
gh run list --workflow publish.yml --branch master --limit 5
gh run watch --exit-status
```

Select the relevant run when prompted. Wait for **Deploy GitHub Pages** to
succeed, then inspect the live domain and affected page. A successful push alone
is not evidence of publication. For validation failure, inspect the failed step
and correct the source or saved state locally before another approved release.
