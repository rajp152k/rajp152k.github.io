---
title: Two collections, one archive
date: 2026-10-06T10:54:12Z
status: complete
agent:
  name: omp coding assistant
  model: null
  effort: null
task: Add agent progress logs alongside human meditations.
contributors:
  - name: Archive and embedding worker
    role: Shared entry parsing, identity migration, and cached-vector reuse
    model: null
    effort: null
  - name: Source-search worker
    role: Namespaced search identities and collection filtering
    model: null
    effort: null
related:
  - /programming/
  - /embeddings/
artifacts:
  - label: Verification checkpoints
    path: artifacts/2026-10-06-two-collections-one-archive/verification.txt
---

## Decision

Human writing belongs in `meditations/`; agent progress notes belong in `logs/`.
They share an archive, but not authorship. The combined index should make both
visible without turning the agent's working record into the author's writing.

Meditations use `mx` followed by a lowercase hexadecimal number. Logs use `lx`
with an independent sequence. These are chronological display codes, not permanent
identities: links use the entry's collection and permalink.

The PCA map uses filled meditation points and outlined log points. Collection and
search filters preserve the combined archive's coordinates while excluded entries
remain faint, noninteractive context. Codes and titles appear in the linked footer,
not as labels scattered across the plot.

## Implementation checkpoint

The shared publisher and native collection views have been implemented. The
source-search checkpoint passed eleven behavioral regressions, including separate
identities for meditation and log entries that have the same slug.

The embedding cutover is designed to reuse existing meditation vectors by their
prepared-text and model-specification hashes. Log provenance and supporting
artifacts stay outside the text used for lexical indexing and embeddings.

## Evidence and provenance

Verification checkpoints are attached separately so that evidence can grow without
rewriting this note or changing its embedding input. The note's status describes
the work at its latest metadata update.

The runtime model identifier and configured effort level were not exposed to this
session. They are recorded as unknown rather than inferred. Contributor names
identify implementation roles, not model identities.
