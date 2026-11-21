---
schema: 1
kind: post-review
entry: logs/2026-11-21-blog-update-1
cycle: 1
state: writing
post_sha256: e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d
terms:
- id: T1
  revision: 1
  state: applied
  action: add
  record: t1-principal-component-analysis
  decision: raj-t1-r1
  applied_at: '2026-11-21T18:35:22Z'
  card:
    name: Principal component analysis
    definition: A linear projection of centered data onto orthogonal directions of
      greatest variance.
    aliases:
    - PCA
    passage: 'Map positions come from principal component analysis of the post vectors:
      a two-dimensional projection of the whole archive, not a new projection for
      each collection or search.'
    introduction: Use meditations/embeddings as the mathematical introduction. Keep
      the new log passage unchanged; show the proposed definition through the term
      surface only after approval.
    use_scope: First eligible principal component analysis or PCA body mention in
      logs/2026-11-21-blog-update-1 only. No meditation annotations, other post uses,
      or changes to the three existing registry records.
links: []
decisions:
- id: raj-t1-r1
  actor: raj
  action: approve
  scope: T1:r1 definition, alias, evidence, introduction and new-log-only use
  post_sha256: e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d
  at: '2026-11-21T18:35:22Z'
  evidence: review-imports/6a7d77d92e6e51fd9e14-de90af940de0f7a7.json
  reason: Imported exact candidate approval; time records AL's observation, not browser submission.
transitions:
- from: curation
  to: writing
  actor: autolith
  at: '2026-11-21T18:35:22Z'
  event: Imported requested prose changes; applied approved curation independently.
  evidence: review-imports/6a7d77d92e6e51fd9e14-de90af940de0f7a7.json
blockers:
- issue: Revised complete prose needs Raj's review.
  owner: raj
  resolution: Read the new exact-source whole-log session and add native Notes.
release:
  commit: null
  deployed_commit: null
  url: null
  verified_at: null
---

# Blog Update [1]: draft review

## Now

The first batch is imported. Raj approved T1:r1 and L1:r1–L3:r1, requested prose
changes, and left six native memos. Approved curation is applied. The log returns
to `writing` for revision. See [exact feedback and dispositions](../../blog-update-1-feedback-cycle-1-2026-11-22.md).

The original reviewed hash and exact card below identify the approval snapshot.
The next memo batch records the revised hash; it does not reopen unaffected cards.

Draft checkpoint only, on `draft/blog-update-1-2026-11-21`. No final commit,
merge, push, or publication approval. The coordinator requested a scoped branch
checkpoint to hand off this review. That does not advance the post's workflow
state to `committed`. Published content remains at `f19d221`.

Read the revised full post in the next memo-only log item. Use Notes for passage
comments or general feedback. The candidate votes are already imported and applied.
Existing sessions and all earlier review evidence are preserved.

## Initial reader review (before Raj's feedback)

Purpose: explain the blog work performed on 21 November and the older work shipped
with it, including how user feedback changed the writing and how publication was
verified. Audience: capable technical readers who need local context, not a tool
transcript. Full draft read against the canonical writing policy. It distinguishes
projection, similarity, and authored links; author decisions, native notes, and
agent receipts; observed release checks and remote-system design claims.

The draft ends at verified deployment, without a forced conclusion. No diagram is
needed to repeat the interface mechanics or the already published setup diagram.
The draft has no authored links yet; the separate outlink batch proposes three.
No existing registry term has an eligible match in this draft under its current
scope. No term record or old post is changed. Final curation and reference-stage
completion await Raj's decisions.

## T1 Principal component analysis

Decision requested: approve, request changes, reject, or defer T1:r1, including its
exact definition, alias, evidence, introduction, and new-post-only use scope.

This is a statistical term with a specific domain meaning, not an ordinary phrase
assigned local meaning. It helps explain why a map has projection loss and why its
positions differ from full-vector similarity and authored link edges. Existing
registry has no PCA record. Rejected embedding, inference, and other old candidates
are not reopened. Product names, checks, and local workflow labels need no glossary.

Proposed archive evidence: `meditations/embeddings`, Blog Update [0], dated
2026-10-03. Exact passages:

> Use exact reduced SVD, with no per-dimension standardization or whitening.

> Refit PCA on each build, so positions can change.

The surrounding centered matrix and SVD equations specify the projection. Read the
complete target in the frozen evidence. Proposed introduction:
`meditations/embeddings`. The definition explains the term without following a link.
No new evidence quote or introduction is applied to the registry before approval.
The full T1 card in front matter is the proposed revision. Only the new log is an
annotation target; all existing posts and three term records are excluded.

## Link candidates

See `docs/reviews/blog-update-1-outlinks-2026-11-21.md` for L1:r1–L3:r1. These are
proposals, not existing approved links. They cover the mathematical method,
authorship distinction, and the laboratory account's evidence limits. All targets
are strictly earlier than this new log. No reverse links or edits to old posts.

## Decisions

T1:r1 approved and applied with only the new log in annotation scope. L1:r1–L3:r1
approved and applied in the separate outlink record. Whole-log native label:
`request changes`; general comment: “check notes and refine”. The six exact memos
and the reason for carrying the unchanged candidate scopes forward are in the
feedback report. No final prose, commit, or publication approval is inferred.

## Preview and checks

See the evidence report. The complete post in Potato is the draft review surface.
No embedding refresh or broad release suite is needed for this first review.
No final reference receipt is recorded while curation is unresolved.
