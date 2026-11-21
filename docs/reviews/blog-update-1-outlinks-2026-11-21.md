---
kind: outlink-review
cycle: 1
revision: 1
state: proposed
posts:
  logs/2026-11-21-blog-update-1: e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d
  meditations/embeddings: 696a62f51d93037f4810f7e69a8fe57972268879d8dc61116fcb23de8e109dc1
  logs/2026-10-06-two-collections-one-archive: 11fc21a7bc1aad602cab08cd50e542278f58c31e9782a2687e297d028fe254e6
  logs/2026-11-06-orchestrating-autolith: e7ec66729f276e421641764175c9faa20a355547bea3a8e83dc3e0ed72a9dae1
links:
- id: L1
  revision: 1
  state: proposed
  action: add
  record: l1
  decision: null
  applied_at: null
  entry: logs/2026-11-21-blog-update-1
  target: meditations/embeddings
  card:
    placement: What arrived with the release
    passage: 'Map positions come from principal component analysis of the post vectors:
      a two-dimensional projection of the whole archive, not a new projection for
      each collection or search.'
    proposed: 'Map positions come from principal component analysis of the [post vectors](/embeddings/):
      a two-dimensional projection of the whole archive, not a new projection for
      each collection or search.'
    purpose: related-reading
    evidence: Use exact reduced SVD, with no per-dimension standardization or whitening.
    reason: Read the original pooling and PCA method and its projection limits rather
      than repeat the equations here.
- id: L2
  revision: 1
  state: proposed
  action: add
  record: l2
  decision: null
  applied_at: null
  entry: logs/2026-11-21-blog-update-1
  target: logs/2026-10-06-two-collections-one-archive
  card:
    placement: Opening
    passage: We wanted a shared laboratory journal without presenting my account as
      his personal prose.
    proposed: We wanted a shared laboratory journal without presenting [my account
      as his personal prose](/logs/2026-10-06-two-collections-one-archive/).
    purpose: related-reading
    evidence: Using “we” need not make my prose his personal writing.
    reason: The revised collections log explains the author distinction that prompted
      this work.
- id: L3
  revision: 1
  state: proposed
  action: add
  record: l3
  decision: null
  applied_at: null
  entry: logs/2026-11-21-blog-update-1
  target: logs/2026-11-06-orchestrating-autolith
  card:
    placement: Reading the logs as writing
    passage: The laboratory account separates removed services from a deployed replacement
      cluster and design requirements from passed remote tests.
    proposed: The [laboratory account](/logs/2026-11-06-orchestrating-autolith/) separates
      removed services from a deployed replacement cluster and design requirements
      from passed remote tests.
    purpose: related-reading
    evidence: We have removed the old services, not established a working cluster.
    reason: Read the concrete distinction between completed local changes and the
      proposed remote laboratory.
no_links: []
---

# Blog Update [1]: proposed outgoing links

All three are unapproved r1 proposals. No authored post links are in the draft yet.
All target posts were read; their dates precede the new log. Full snapshots and exact
source/target evidence will be frozen by the queue. No reverse links.

## L1

Read the original pooling and PCA method and its projection limits rather than repeat the equations here.

Exact proposed text:

Map positions come from principal component analysis of the [post vectors](/embeddings/): a two-dimensional projection of the whole archive, not a new projection for each collection or search.

## L2

The revised collections log explains the author distinction that prompted this work.

Exact proposed text:

We wanted a shared laboratory journal without presenting [my account as his personal prose](/logs/2026-10-06-two-collections-one-archive/).

## L3

Read the concrete distinction between completed local changes and the proposed remote laboratory.

Exact proposed text:

The [laboratory account](/logs/2026-11-06-orchestrating-autolith/) separates removed services from a deployed replacement cluster and design requirements from passed remote tests.
