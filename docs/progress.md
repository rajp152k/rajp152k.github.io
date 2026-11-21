---
kind: work-status
state: potato-outlinks-ready
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

The [archive outlink review](reviews/outlinks-2026-11-21.md) covers all nine posts:
three logs and six meditations. Five links to strictly earlier posts are proposed
as L1:r1–L5:r1. Five posts need no outlinks, recorded as N1:r1–N5:r1.
Review all ten cards in Potato with `just review`. Session: `9ea549187a75fbae5e1e`.
There are no existing authored internal post links. External citations are preserved.
The two October 7 posts have unclear relative order; no link between them is proposed.

## Decisions and docs

HMAS, Lisp image T2:r2, and Simplified Technical English T7:r2 are applied
(commit `c60af1e`). Their approved scopes and definitions are unchanged.

The [approval import](../review-imports/1c0ce0132fd10a6f26a8-403c434257318011.json)
has no changed sources, comments, or memos. The
[Using Autolith record](reviews/logs/2026-10-07-using-autolith/cycle-1.md)
contains both approvals and applied states. The earlier six rejections and two
revision requests are retained. Rejected terms are absent from the registry.

Selection policy is short and general. Writing docs cover definition references
and revised cards. Review cards and public term pages use the same safe link
renderer. Optional registry `entries` restrict matching to approved posts.
Article prose, HMAS, prior sessions, and imports are preserved.

## Checks

For this outlink batch: checked dates, target paths, exact source phrases, all nine
source hashes, and the documentation diff. The queue/import code now supports compact outlink and no-link cards.
No article or registry changes.
18 direct queue/import contract tests pass, including link and no-link decisions,
blank responses, dates, hashes, target paths, and escaping.
No browser tests, builds, or full suites were run for this batch.

Earlier term application passed 39 focused tests, registry validation, `just build`,
and generated HTML checks.

## Next

Raj decides the five link revisions and five no-outlinks-needed results in Potato,
then tells AL when the session is done. AL imports and records the scoped decisions. Apply only approved outgoing links afterward. The first log's
[empty term batch](reviews/logs/2026-10-06-two-collections-one-archive/cycle-1.md)
also needs confirmation. Full editorial and publication approvals are separate.
No new log or publication is part of this work.
