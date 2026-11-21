---
kind: work-status
state: outlinks-applied
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

Raj approved all ten r1 cards in Potato session `9ea549187a75fbae5e1e`.
The [archive outlink review](reviews/outlinks-2026-11-21.md) records five applied
outgoing links and five confirmed no-outlinks-needed results across all nine posts.
The [import report](../review-imports/9ea549187a75fbae5e1e-4441fb6b796e5891.json)
has no changed sources, blank decisions, comments, or memos. All source hashes and
exact candidate revisions matched before application.

The five links change four posts. External citations and captured command output
are preserved. No reverse links or links between the ambiguously ordered October 7
posts were added. The term registry and prior sessions/imports are unchanged.

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
HMAS and prior term decisions are unchanged.

## Checks

For this outlink application: checked the import against all ten exact reviewed
cards, all nine post hashes, and the review record hash. Checked the five applied
replacements, earlier target dates, target routes, unchanged no-link posts, and
preserved Markdown hard breaks. The final article text matches the reviewed
snapshots plus only those five approved link additions.
18 direct queue/import contract tests pass. Diff inspection and a whitespace check
that allows the existing Markdown hard breaks pass.
No browser tests, builds, or full release suites were run.

Earlier term application passed 39 focused tests, registry validation, `just build`,
and generated HTML checks.

## Next

This outlink batch is complete. The first log's
[empty term batch](reviews/logs/2026-10-06-two-collections-one-archive/cycle-1.md)
also needs confirmation. Full editorial and publication approvals are separate.
No new log or publication is part of this work.
