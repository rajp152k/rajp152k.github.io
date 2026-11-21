---
kind: work-status
state: first-term-applied
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

Raj approved HMAS, T1 revision 2, in Potato. Imported the response from session
`c190bfe8095e236adca4` with no changed sources. Applied its exact definition,
alias, source passage, and introduction to `terms.json`.

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

The first [term decision](reviews/logs/2026-11-06-orchestrating-autolith/cycle-1.md)
is recorded with its [import evidence](../review-imports/c190bfe8095e236adca4-33a824290d229925.json).
The scope is this log only. Both review sessions and their responses are retained.
The article remains in curation. Full archive review and publication need separate work.

## Current limits

The scripts do not enforce the new Markdown approval states. We follow the gates
manually. The existing release checks still apply.

At raj's request, removed all nine old terms, 24 related-reading selections,
and the three log reading lists. External citations and meditation prose are
unchanged. Old receipts are stale historical records. Release requires fresh
archive reviews and separate approval.

## Next work

1. Continue term review in small batches, keeping decisions and reasons.
2. Update browser fixtures that still expect the removed terms and post links.
3. Wait for the next request before writing Blog Update [1].
4. Test log comments when reviewing that new article.

## Checks

115 Python tests and 11 Node search tests pass. Registry validation reports one
term, one source, and one post reference. `just prepare` passed and reused all
nine embeddings. Both HMAS spellings open the approved definition on desktop;
the phone references are plain text. The paper citation is unchanged.

The full browser suite has 9 passes and 14 failures. Its fixtures expect removed
terms and curated post references. `just check` stops at the existing stale
archive reviews: all 18 stages need fresh review. The scoped term decision does
not replace them. No publication was performed.
