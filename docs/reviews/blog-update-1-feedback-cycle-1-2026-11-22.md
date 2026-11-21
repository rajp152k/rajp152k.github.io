# Blog Update [1]: first feedback and revision

## Imported evidence

Subject date: 21 November 2026. Revision date: 22 November 2026.
Session: `6a7d77d92e6e51fd9e14`.
[Durable native import](../../review-imports/6a7d77d92e6e51fd9e14-de90af940de0f7a7.json).
Reviewed post SHA-256: `e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d`.

AL confirmed the loopback listener, PID 19946, the exact Potato config path,
and the served session ID. AL stopped that server with SIGINT before running
`just import-reviews 6a7d77d92e6e51fd9e14`. Its execution `L3h41nW`
completed successfully. No other listener was stopped. `changed_sources` is empty.
Frozen inputs, native session data, imports, and older sessions are preserved.

Raj approved T1:r1 and L1:r1–L3:r1 without candidate comments. The normalized
whole-log response has no decision and says **“check notes and refine”**.
The native label under `evidence.users.raj.instance_id_to_label_to_value`
records **`request changes`** for the whole log. This is a request to revise,
not approval of the prose, final commit, or publication.

There are six native memos, all by `raj`, all `private`, all with null anchors.
Their creation and update times are equal. The import preserves these times,
IDs, bodies, visibility, and source text. `memo_threads` is empty. Native span,
phase/page, room-provenance, link, and event fields contain no additional feedback.
The quoted text below is exact, including typing errors. AL used the wording and
frozen article for context and did not invent passage offsets.

## Exact memos and disposition

### Opening context

Memo `07c2aecda81b4acda9f12b3ccc0d0cce`, timestamp `1795284843.4626079`:

> no context in the first line itself - what even is a working map ? i don't recall it well - how will a foreign reader of first time relate. we should be this mystic.

Replaced the first line with an explanation of the blog's article points,
text-derived positions, and reference lines. It now introduces the subject to a
first-time reader. The request for context is clear despite the last sentence's
typing error. AL did not treat that error as a request to add obscure language.

### Explanatory map snapshot

Memo `c63947daed0249de8d47d96119c8cda1`, timestamp `1795284962.4910269`:

> we could paste the current svg as a snapshot here with popups /hovers that are curated towards explanation instead of being the navigation that they are in the index.

Add a fixed SVG from the actual current nine-post layout, with explanatory hover
text and a visible accessible text equivalent. Label its date and nine-post scope;
exclude this unembedded draft. Preserve the public index's navigation interaction.
The coordinator confirmed this interpretation and required rendered inspection.
Snapshot provenance and final rendering checks are recorded below when complete.

### Potato source link

Memo `48a0c626487c43caa82607d5e0ea43a1`, timestamp `1795284976.4988632`:

> we should have a link to potato annotation tool

Linked the first Potato mention to `https://github.com/davidjurgens/potato`.
The installed package metadata names that source repository; AL also retrieved
its page and confirmed the annotation-tool identity. This is Raj's requested
external source link, not a new curated archive-post candidate.

### Old archive link

Memo `9253d4c08af5455bbeb64d1982014eef`, timestamp `1795285091.289072`:

> old archive link instead of the commit hash

Replaced the raw hash in article prose with an **old archive** link to the pinned
GitHub tree. The link keeps the exact studied revision without making readers
interpret an isolated hash. The pinned hash and inventory are in the study record.

### Archive analysis method

Memo `98187ebb9c624351ac33e9c1c5097a85`, timestamp `1795285285.9379818`:

> could say that we used an rlm infer map followed by a reduce for the larger scan of the old archive.

Added the map-and-reduce method: eight bounded recursive-language-model
inferences over complete body batches, then a separate synthesis. The study's
batch trace table and `inference:i6EZqQc` support this account. The prose describes
the decomposition, not an unverified claim that a particular `rlm.map` tool call
ran. It also preserves direct passage checks and attribution limits.

### Review diagram and collaboration

Memo `4baf2a437f274ba1a9b6e0d16138171a`, timestamp `1795285587.1878421`:

> we can have a mermaid diagram around reviews flow . term election and approval, outlink reviews, and finally the notes flow for generic comments. we should say this is our own evals setup to converge to a collaboration style over time.

Added a Mermaid diagram with accessible title and description. Its branches show
term selection, earlier-post link proposals, and full-log Notes/general comments;
then native import, approved curation, prose revision, and renewed review. A text
explanation states the same flow. The prose names this our evaluation setup for
developing collaboration through actual responses, without claiming a validated
quality score. Final commit and publication approval are separate.

## Candidate disposition

- **T1:r1:** approved. Added `principal-component-analysis` with the exact reviewed
  name, definition, alias `PCA`, two archive evidence passages, introduction
  `meditations/embeddings`, and only the new log as eligible use. Existing three
  term records are unchanged. The approved passage's visible wording is unchanged.
- **L1:r1:** approved. Applied the exact **post vectors** link to `/embeddings/`.
- **L2:r1:** approved. Applied the exact **my account as his personal prose** link
  to `/logs/2026-10-06-two-collections-one-archive/`.
- **L3:r1:** approved. Applied the exact **laboratory account** link to
  `/logs/2026-11-06-orchestrating-autolith/`.

All three proposed replacement sentences are present verbatim. Their targets,
link text, purpose, surrounding claims, and date order are unchanged. The two
requested external links add no reverse archive links. No other approved term
scope or link passage changes. The next pass therefore needs the complete revised
log, not another vote on these unaffected exact candidates. General post approval
is still pending. No new general writing-policy rule is inferred from this pass.

## Approved schema correction

The first term check exposed an invalid coupling: `entries` controlled automatic
matches but also had to contain every evidence source and the introduction.
Adding `meditations/embeddings` would have expanded the approved annotation scope.
AL stopped and raised this conflict. The coordinator approved separating evidence
validation from annotation scope, with focused checks and the contract update.

Removed only that subset requirement in `scripts/terms.py`. Known-entry checks,
exact source quotes, unique scope keys, and all other validation remain in place.
Updated `docs/build.md`. Tests cover evidence and introduction outside scope,
unknown sources and introductions, stale quotes, and matching only the named log.
The initial new test fixtures used plain dates for logs; AL corrected them to
required timezone-aware timestamps. All final tests pass. The registry does not
include the evidence meditation in annotation `entries`.

## Verification and next review

Current article SHA-256:
`89c322f93719ad13810067dcba8757dfeb6cd06d4d683cf29c1f947ed7a1ddd9`.
Title, route, and 21 November publication timestamp are unchanged.

- 27 term tests, 2 term-page tests, and 21 review tests pass: 50 focused tests.
- Term validation: 4 records, 10 entries, 3 post references. PCA has exactly one
  eligible match, in this new log. The three earlier registry records are equal
  to their previous versions. All three approved link sentences are verbatim.
- Existing posts, old imports, and `blog.sqlite` are byte-identical to checkpoint
  `ed2c9a2`. Existing eighteen editorial receipts and questions are preserved.
- New reader and reference receipts record actual work on this log. The embedding
  meditation's old reference receipt is now stale because it is evidence for the
  new term. It was not refreshed without a separate completed review.
- Snapshot fragment: `assets/figures/blog-update-1-map-snapshot.html`, SHA-256
  `725079562c3b161a3fefdddee065d89f97eb7dbfe7d13b5ed1ebbc9d9689effc`.
  Its source hashes identify the existing nine-post build and database. All nine
  coordinates and five directed endpoints match that build. The article contains
  the complete literal fragment. SVG XML and unique IDs were checked.
- Browser checks at 900px and 390px verified nine explanatory point titles, five
  reference titles, actual hover targets, all nine text-key rows, no navigation
  links or scripts in the figure, and no page overflow. Primary and independent
  reviewer viewed both screenshots with `fs.view-image`. Phone labels are small;
  the expandable text key is readable. Accessibility output includes scope/date,
  the projection/reference distinction, nine post titles and all five arrows.
  Native operating-system tooltip pixels were not inspected.
- Mermaid rendered on desktop and phone with its accessible title and description,
  no fallback, no page errors, and no page overflow. Primary inspected the renders.
  Checks also found exactly one PCA annotation and all three approved body links.
- Independent read-only editorial review found no material issue in the six memo
  dispositions, prose claims, dates, policy, or carried candidate scopes.

Local render evidence: `test-results/map-snapshot/{900,390}.png` and corresponding
accessibility text; `.reviews/blog-update-1-render/mermaid-{1440,390}.png` and
`article-{1440,390}.png`. These are ignored local artifacts. The isolated preview
uses the real Markdown renderer, term transform, article template and bundled
assets. It does not claim a fresh archive build or new embeddings.

### Next review

[Exact-source second memo batch](blog-update-1-memos-cycle-2-2026-11-22.md).
Session: `f2132a7027bce0dce50c`.
Potato: **http://127.0.0.1:8769/**.
Rendered article: **http://127.0.0.1:8771/**.

One complete log item, native Notes, optional general comment, no candidate votes.
All frozen hashes and the complete item text match current files. HTTP 200 and
served session ID verified. Loopback-only listener: PID 7631, execution `T1XJesf`
(job `exec:96`). Isolated preview execution: `n1xYqPb` (job `exec:90`).

Open Potato, enter `raj`, select Continue, and read the complete log. Open Notes,
quote a passage or name a section, then select Add note. Tell AL when done.
After checking ownership, stop that exact server with SIGINT before
`just import-reviews f2132a7027bce0dce50c`. Read all comments, memos, threads and
source flags against these snapshots. Preserve sessions and imports.

The draft is at `writing`. The coordinator authorized this scoped branch
iteration checkpoint, not final workflow commit approval. No embedding inference,
full release suite, merge, push or publication occurred. The current review
requests no policy change and no new term/link decisions.
