---
kind: release-record
state: publish-approved
approved_content_commit: 46ed50a03a71545c8dbfeb6c61b54caa40dbccca
session: f2132a7027bce0dce50c
---

# Blog Update [1] release, 22 November 2026

## Authority and exact scope

Raj approved the current post and publication in conversation:

> this is good to publish. go ahead and publish - then i sleep for the day

The coordinator `@blog-progress-recap` relayed this approval in conversation
`d130d358-975d-492e-b059-68707bbab79b`, authorized release preparation, a move to
clean `master`, and `just publish` after all checks pass. No additional pre-push
exchange is required. This approval includes the current prose and the required
release commit. It is separate from Potato evidence and earlier candidate votes.

Approved content is `46ed50a03a71545c8dbfeb6c61b54caa40dbccca`. The complete post
SHA-256 is `89c322f93719ad13810067dcba8757dfeb6cd06d4d683cf29c1f947ed7a1ddd9`.
The title, 21 November subject date, publication timestamp and route are unchanged.
T1:r1 and L1:r1–L3:r1 retain their exact imported approvals. No prose, term,
source passage, introduction, annotation scope or outgoing link is changed here.

## Actual final-session evidence

Confirmed HTTP session ID and PID 7631's exact Potato config for
`f2132a7027bce0dce50c` on loopback port 8769. Sent SIGINT only to that process.
Confirmed the listener had stopped, then ran:

```sh
just import-reviews f2132a7027bce0dce50c
```

Import: [f2132a7027bce0dce50c-925014945ee96b2c.json](../../review-imports/f2132a7027bce0dce50c-925014945ee96b2c.json).
All frozen sources match (`changed_sources: []`). There are no saved responses,
labels, spans, memos or memo threads. Native user/navigation state for `raj`
exists. This is not a saved approval or a completed browser review. There is no
feedback that conflicts with the separate conversation approval. All old imports
and session data are preserved.

## Editorial review and preparation

Read the complete approved post again, including the snapshot key, Mermaid flow,
source attribution and account of the previous release. Read the complete three
post-link targets. The authorship link explains the narrator distinction; the
mathematical introduction explains the vectors and projection; the laboratory
account distinguishes design requirements from passed remote trials. All three
are earlier posts. The nine-point figure is explicitly historical and excludes
this new log; its layout must not be replaced by the new ten-post projection.

Only `meditations/embeddings` references were stale. Read its complete equations,
variance caveats and usage steps, and the current PCA card. Centering and exact
reduced SVD without whitening support the approved greatest-variance definition.
Both saved quotes are exact and supported by their context. Introduction and
evidence are in this meditation; annotation scope is only the new log. The
meditation has no annotations and keeps its approved no-outlinks result. Recorded
the actual references review with `just record-review`. Kept all optional questions,
including its dated description of `publish.sh`. Did not edit meditation prose.
All twenty reader/reference stages are current; no blocking question is present.

Ran `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 just prepare` with the existing pinned
model cache. CPU inference encoded six chunks for one new entry and reused nine
embeddings. The database retains every old row and the exact model/archive state;
only `logs/2026-11-21-blog-update-1` is new. The model specification is unchanged.
The fresh build contains ten entries. All prose and `terms.json` are byte-identical
to the approved content commit. Only the stale references receipt changed; all
other receipts and questions are preserved.

## Checks before publication

`just check` passed: current preparation, four valid term records, embedding
freshness, 132 Python tests, 11 Node tests, the build, 23 Chromium tests, and both
working-tree and index whitespace checks. No production or test repair was needed.

Additional fresh-build checks pass at 1440 and 390 pixels: Mermaid renders without
fallback, all nine snapshot points and five reference arrows are present, the
three approved post links and both external links are present, one PCA reference
is present, and no page errors or horizontal overflow occur. Inspected both map
and Mermaid screenshots with `fs.view-image`. Phone diagram labels are small;
the explanatory text and complete map key are readable. Two initial ad hoc checks
used incorrect CSS selectors; reading the generated markup and renderer resolved
those checks without a site change. Screenshots are local under
`.reviews/blog-update-1-release-render/`.

The outgoing release includes the two approved draft checkpoints and this scoped
preparation commit. Fetched `origin/master` is still
`f19d221a00462700be3829ac525bb0af2a0e0deb`. Inspect the whole outgoing diff before
commit and publication. Generated site output, local environments, review scratch
state and screenshots are excluded from Git. Unrelated potato.nvim work is outside
this release.

## Deployment verification

Publication is authorized but has not yet occurred at this record's commit.
Run `just publish` from clean `master`; it repeats the full release checks before
pushing. Confirm the workflow and Pages deployment for the exact pushed SHA, then
compare the live post HTML with the checked build and inspect its map, Mermaid,
term and links. Report those results in conversation. Do not make another public
push only to update this status record.
