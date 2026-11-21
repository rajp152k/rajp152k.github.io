---
kind: work-status
state: ready-for-review-batch
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

Raj accepted the Potato integration. Version 2.13.1 is installed with uv in
`.venv-review`. Term forms, log notes, snapshot import, and cleanup passed a
synthetic end-to-end test through the running application. No installed package
source was inspected.

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

The first [term proposal](reviews/logs/2026-11-06-orchestrating-autolith/cycle-1.md)
is ready: T1 revision 1, HMAS. Run `just review` and decide that candidate.
Skip the log comment item for now. Stop the server and tell AL when done.
AL will import the response before applying any approved term.

## Current limits

The scripts do not enforce the new Markdown approval states. We follow the gates
manually. The existing release checks still apply.

At raj's request, removed all nine old terms, 24 related-reading selections,
and the three log reading lists. External citations and meditation prose are
unchanged. Old receipts are stale historical records. Release requires fresh
archive reviews and separate approval.

## Next work

1. Complete the first term approval and import cycle with raj.
2. Continue term review in small batches, keeping decisions and reasons.
3. After the approval flow works, write Blog Update [1] as a requested log.
4. Test log comments when reviewing that new article.

## Checks

Integration tests: 109 Python tests passed. The synthetic browser test saved a
term approval and comment, an anchored log issue, and a reply. Import preserved
them; cleanup removed scratch and retained the report. Release checks require
fresh archive reviews; all 18 archive review stages are policy-stale.
The later term reset changes only the registry, curated reading links, and review
records. No publication was performed.
