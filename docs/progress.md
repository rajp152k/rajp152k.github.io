---
kind: work-status
state: revised-terms-awaiting-approval
updated: 2026-11-21
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

Run `just review` for session `1c0ce0132fd10a6f26a8`: **two revised term cards**,
Lisp image T2:r2 and Simplified Technical English T7:r2. Both are proposed,
not approved or created. Each definition includes the reference raj requested.
HMAS T1:r2 is the one applied term.

## Current work

Imported [raj's eight responses](../review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json)
with no changed sources. Recorded six rejections and two revision requests in
[Using Autolith](reviews/logs/2026-10-07-using-autolith/cycle-1.md) and
[Orchestrating Autolith](reviews/logs/2026-11-06-orchestrating-autolith/cycle-1.md).
Rejected candidates are not queued again. The first log has no candidates;
its [empty batch](reviews/logs/2026-10-06-two-collections-one-archive/cycle-1.md)
awaits confirmation in conversation.

The two revised cards keep their previous meanings, introductions, aliases,
and uses. They add the Stack Overflow reference and the official ASD-STE100
Issue 9 reference. The official site offers the original specification by
request. No meditation annotations or article edits are proposed by this revision.
Prior sessions, responses, and HMAS approval provenance are retained.

Selection guidance now assumes a technical audience, omits routine vocabulary,
and favors a few useful, sufficient definitions. Specific decisions are in the
review records, not policy. Raj still approves exact revisions and use scopes.

## Next

1. Review the two revised cards. A revision request is not approval.
2. After approval, apply only the named changes and check their exact uses.
   Public term pages need clickable definition references before application;
   the review cards support them now. The registry has no per-post filter;
   verify the two exact-name scopes before applying.
3. Write Blog Update [1] only when requested. Commit and publish separately.

## Checks and limits

13 review tests pass, including safe clickable definition references. Data checks
verify the two proposed r2 items, frozen source hashes, and no selected decisions.
No browser checks or full release suite were run for this revision.

Earlier work passed 117 Python tests and eight native Potato card checks.
Known release blockers are unchanged: 18 stale archive review stages and
14 browser failures with removed-term and removed-link fixtures. No publication.
