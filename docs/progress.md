---
kind: work-status
state: all-log-term-review-ready
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

Term review for all three logs is ready in Potato session `cdb5159a86f2dc71b13c`.
The session contains eight proposed cards and no selected decisions. Run
`just review` to review them. Meditations are excluded.

## Confirmed by raj

- Raj approves terms throughout the process.
- Submit jargon and domain-specific terms, not ordinary phrases given local meaning.
- Gate term curation and post linking with raj in the loop.
- Use explicit states and transitions. Keep the working documents under `docs/`.
- Raj writes meditations with `just write "Title"`; meditations have no terms.
- AL drafts logs and may edit log drafts during iteration.
- Use Potato for term decisions and passage comments on logs. Raj runs
  `just review`, works in the browser, and tells AL when done.
- Keep post-link decisions and final approval in conversation.
- Keep repository records public-intended and use dedicated critical review sessions.

## Current work

The three log batches contain 0, 7, and 1 new term cards, in date order:

- [Two collections, one archive](reviews/logs/2026-10-06-two-collections-one-archive/cycle-1.md): no candidates. Raj must confirm this empty batch in conversation.
- [Using Autolith](reviews/logs/2026-10-07-using-autolith/cycle-1.md): VPS, Lisp image, fork, text embedding, inference, front matter, and Simplified Technical English.
- [Orchestrating Autolith](reviews/logs/2026-11-06-orchestrating-autolith/cycle-1.md): peer discovery. The VPS and inference cards also propose uses in this log.

Each card includes its passage, definition, aliases, introduction, and proposed
archive scope. The session also contains frozen records, posts, and
[domain evidence](reviews/term-domain-evidence.md). The embeddings meditation
is evidence only, not a review target.

Raj's applied HMAS T1:r2 decision and its
[import evidence](../review-imports/c190bfe8095e236adca4-33a824290d229925.json)
are unchanged. The session does not ask for this decision again. Prior sessions
and responses are retained. No new term or prose change has been applied.

## Current limits

The scripts do not enforce the new Markdown approval states. We follow the gates
manually. The existing release checks still apply.

The term registry has no per-post filter. Enforce the proposed log-only scopes
before applying affected candidates. Do not add meditation matches.

At raj's request, removed all nine old terms, 24 related-reading selections,
and the three log reading lists. External citations and meditation prose are
unchanged. Old receipts are stale historical records. Release requires fresh
archive reviews and separate approval.

## Next work

1. Review the eight cards in Potato and confirm the empty first batch in conversation. Import decisions, then enforce approved scopes before applying terms.
2. Update browser fixtures that still expect the removed terms and post links.
3. Wait for the next request before writing Blog Update [1].
4. Test log comments when reviewing that new article.

## Checks

117 Python tests pass. Native Potato browser checks covered all eight cards:
four unselected decisions per card, closed evidence sections, and readable
card layouts. No decisions were submitted during these checks.

Earlier checks passed 11 Node search tests, registry validation (one term,
one source, one post reference), and `just prepare` with all nine embeddings
reused. Both HMAS spellings opened the approved definition on desktop;
the phone references were plain text. The paper citation was unchanged.

The full browser suite has 9 passes and 14 failures. Its fixtures expect removed
terms and curated post references. `just check` stops at the existing stale
archive reviews: all 18 stages need fresh review. The scoped term decision does
not replace them. No publication was performed.
