---
schema: 1
kind: post-review
entry: logs/2026-11-21-blog-update-1
cycle: 1
state: curation
post_sha256: e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d
terms:
- id: T1
  revision: 1
  state: proposed
  action: add
  record: t1-principal-component-analysis
  decision: null
  applied_at: null
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
decisions: []
transitions: []
blockers:
- issue: Term and outlink candidate decisions and prose review are pending.
  owner: raj
  resolution: Review the exact frozen revisions in Potato; tell AL when done.
release:
  commit: null
  deployed_commit: null
  url: null
  verified_at: null
---

# Blog Update [1]: draft review

## Now

Draft checkpoint only, on `draft/blog-update-1-2026-11-21`. No final commit,
merge, push, or publication approval. The coordinator requested a scoped branch
checkpoint to hand off this review. That does not advance the post's workflow
state to `committed`. Published content remains at `f19d221`.

Read the full post in the log item. Use Notes for specific passages or general
comments. Each term and outlink card needs its own decision. No responses or
memos have been invented. Existing sessions and all earlier review evidence are
preserved. Review access and checks are in the evidence report.

## Reader review

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

None. Blank browser fields and agent review notes are not decisions.

## Preview and checks

See the evidence report. The complete post in Potato is the draft review surface.
No embedding refresh or broad release suite is needed for this first review.
No final reference receipt is recorded while curation is unresolved.
