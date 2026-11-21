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

Select the first real log and term review batch. AL queues numbered records with
`just queue-review`; raj runs `just review`. Stop the server before importing with
`just import-reviews ID` or removing imported scratch with `just clean-reviews ID`.
See [Writing](writing.md#browser-review) for setup and evidence snapshots.

## Current limits

The scripts do not enforce the new Markdown approval states. We follow the gates
manually. The existing release checks still apply.

The editorial policy changed. Old archive review receipts are stale, and old term
records are not approvals under the new rules. Keep them intact until review with
raj. Release is blocked until the archive checks and approval review are complete.
This does not prevent writing or draft previews.

## Next work

1. Write and curate the selected post in small batches.
2. Keep accepted and rejected examples with raj's reasons in its review record.
3. Review legacy terms and links with raj before a release.
4. Refine the state format through use before implementing automatic enforcement.

## Checks

Integration tests: 109 Python tests passed. The synthetic browser test saved a
term approval and comment, an anchored log issue, and a reply. Import preserved
them; cleanup removed scratch and retained the report. Release checks require
fresh archive reviews; all 18 archive review stages are policy-stale.
No article prose, term records, or editorial receipts have been changed for this
integration. No publication was performed.
