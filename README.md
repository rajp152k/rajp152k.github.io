# meditations of yet another raj


## Writing and publishing

Posts live in `meditations/` as Markdown with `title` and `date` front matter.
Create one with `./write.sh "Title"`; Markdown remains the source of truth.

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
| New post, title change, or changed prepared body text | Yes | Only missing/changed posts |
| Date-only correction, unchanged-content rename, or deleted post | Yes | None; synchronize metadata/reuse vectors |
| Model/revision, chunking, preprocessing, or aggregation policy | Yes | Re-embed the archive |
| CSS, map interaction, HTML layout, PCA presentation, or README | No | None |
| Nothing changed | Optional | None; unchanged state is a no-op |

The updater hashes the prepared title/body and complete embedding specification.
Formatting-only edits that leave prepared text unchanged reuse the vector.
Nothing runs automatically while writing: run the updater once a post is ready.
CI **never** computes embeddings or downloads a model.

### Preview and publish

After writing, revising, renaming, or deleting posts:

```sh
.venv-embed/bin/python scripts/embed.py
.venv-embed/bin/python scripts/publish.py
```

The second command builds `site/`, including the PCA map and public SQLite
snapshot. For a local preview:

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

A freshness check, the regression suite, and a site build need only
`requirements.txt`; model inference additionally needs `requirements-embed.txt`.

### GitHub CI and deployment

The [Publish workflow](https://github.com/rajp152k/rajp152k.github.io/actions/workflows/publish.yml)
uses Python 3.13 and only `requirements.txt` to:

1. Check that the committed `blog.sqlite` matches the current posts and policy.
2. Run deterministic state/export and PCA geometry regressions.
3. Generate the HTML, local assets, PCA map, and allowlisted public database.
4. Upload `site/` and deploy GitHub Pages at <https://yetanotherraj.com/>.

Pull requests targeting `master` run validation and build, **not deployment**.
Pushes to `master` deploy when posts, scripts, assets, requirements, embedding
configuration/database, tests, the workflow, or `CNAME` change. README-only edits
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
- `posts`: title/date metadata, text and embedding hashes, and the vector.

Inference finishes before a write transaction begins. Synchronization is atomic,
and publishing opens the database read-only and refuses missing, stale, or
invalid vectors before clearing an existing site build.

SQLite state is a binary Git artifact: inspect it with SQLite rather than relying
on readable diffs, and avoid concurrent branch edits to it. It is derived data and
can be regenerated from the Markdown and pinned configuration.

For isolated archives or experiments, the embed command also accepts
`--posts PATH`, `--database PATH`, and `--spec PATH`.

## Homepage and PCA map

The homepage uses a compact, fixed-viewport split layout: an independently
scrolling chronological table on the left and an embeddings panel on the right.
Table headings stay visible while the rows scroll. On narrow screens, the panels
stack within the same fixed shell; the compact ID/date readout stays on one line.
Article pages share the Fira Mono, green-on-black treatment but retain normal
reading scroll.

The palette follows the local tmux, Neovim, and Ghostty themes: pure black
(`#000000`), primary green (`#00ff00`), secondary green (`#00b300`), subdued
separators (`#006600`), and bright green/white for active targets. There are no
logos, decorative taglines, shadows, or promotional footers. Space is reserved
for the post list, coordinate diagram, projection statistics, and ID/date
readout.

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

Posts have zero-based, lowercase hexadecimal display IDs: `x0`, `x1`, …, `xe`,
`xf`, `x10`, …, assigned from oldest to newest in the archive's chronological
order. The newest post has the highest ID. The index pairs IDs with full titles;
PCA labels and hover/focus readouts use only IDs and dates, with full titles
retained in accessible link labels rather than native hover tooltips.

IDs are derived presentation indexes, not stored identities or permalinks:
backdated insertions, deletions, or changes to archive ordering can renumber them.
Hovering or focusing either view still highlights the corresponding entry in
both views. Each point is a native post link, so navigation
still works without JavaScript. The homepage loads only local assets: it does
not fetch the SQLite file, run an embedding model, or require a charting framework.

`assets/site.css` controls the shared visual treatment; `assets/map.js` adds
progressive cross-highlighting. Publishing now needs NumPy in addition to
Markdown, both pinned in `requirements.txt`; inference dependencies remain
separate. The public SQLite schema is unchanged.

## Public SQLite artifact

Every site build creates a fresh, allowlisted `site/blog.sqlite`, available as
`/blog.sqlite` after deployment. It is **not** a copy of the working database:
internal hashes, complete specifications, bodies, unrelated local tables, and
deleted records are excluded.

The public schema has `PRAGMA user_version = 1`:

| Table | Columns |
| --- | --- |
| `model` | `tag`, `model_id`, `revision`, `dimension`, `dtype` |
| `posts` | `slug`, `title`, `published_date`, `url`, `model_tag`, `embedding` |

`posts.model_tag` references `model.tag`. Dates use ISO `YYYY-MM-DD`; URLs are
root-relative. `model.dtype` is `<f4`: each embedding BLOB contains
`dimension` little-endian float32 values, normalized to unit L2 length.

```sh
sqlite3 site/blog.sqlite \
  'SELECT slug, title, length(embedding) AS vector_bytes FROM posts;'
```

This is a downloadable data artifact, not a search endpoint. No SQLite download
link is shown in the rendered pages. The artifact remains available at its
explicit URL; the website does not automatically download it, and no browser
SQLite runtime is included.

## Verification

Run deterministic state, integrity, text-preparation, export, and PCA geometry regressions:

```sh
.venv-embed/bin/python -m unittest discover -s tests -v
```

Real-model and tokenizer smoke scenarios were exercised separately: initial
embedding, offline no-op, metadata changes, one-post edits/additions, policy
invalidation, deletion/empty archives, and lossless word/token-bounded chunks.
