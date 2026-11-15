---
kind: work-status
state: awaiting-review
updated: 2026-11-15
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

We are defining the writing process. No post has been selected for this session's
first writing cycle. The workflow and record format are version 1, ready for raj's
review. This page tracks the work; its state is not a post publication state.

## Confirmed by raj

- Raj approves terms throughout the process.
- Submit jargon and domain-specific terms, not ordinary phrases given local meaning.
- Gate term curation and post linking with raj in the loop.
- Use explicit states and transitions. Keep the working documents under `docs/`.
- Use short chat updates and readable documents for phone review.

## Ready to review

- [Post states and transition guards](workflow.md).
- [Candidate states and approval scope](curation.md).
- [Markdown front-matter template](review-template.md).

Next decisions: refine these state names or use them for the first post; name the
post or writing topic. The agent will then link its review record here.

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

## Checks for this documentation pass

- Parsed 15 Markdown documents and their YAML; checked 76 local links.
- Passed 102 Python tests.
- `just review-check` reports all 18 stages stale because the policy changed.
- A separate design review found two guard gaps. The draft now blocks transition
  on pending revisions and requires rendered uses to match raj's decisions.

No article prose or term records were changed for this documentation pass. No
publication was performed.
