---
schema: 1
kind: review-template
entry: null
cycle: 1
state: writing
post_sha256: null
terms: []
links: []
decisions: []
transitions: []
blockers: []
release:
  commit: null
  deployed_commit: null
  url: null
  verified_at: null
---

# Post review template

Copy this file to `docs/reviews/<collection>/<slug>/cycle-1.md`.
Set `kind: post-review`, `entry`, and the real post hash. Replace these instructions
with the review. Use paths relative to the new file when adding Markdown links.
Use the fields and states in `docs/workflow.md` and `docs/curation.md`.

## Now

- State: writing.
- Decision needed: none yet.
- Next action: write the draft.

## Reader review

Purpose, intended reader, assumed knowledge, and open questions.

## Term candidates

One heading per candidate ID. Give the complete proposal and requested decision.
If the list is empty, state why and request confirmation during curation.

## Link candidates

One heading per candidate ID. Include existing links for confirmation and any
proposed changes. Show the placement, target, purpose, and reason.

## Decisions

Summarize raj's decisions for phone reading. Keep the structured decision history
in front matter. Do not substitute this summary for the scoped approval evidence.

## Preview and checks

Preview address, checked source revision, results, and unresolved issues.

## Transition history

Summarize state changes and the next gate. Record exact events in front matter.
