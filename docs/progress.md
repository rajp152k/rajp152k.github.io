---
kind: work-status
state: ui-subtle-motion-publish-approved
updated: 2026-11-23
---

# Progress

[Writing desk](README.md) · [Workflow](workflow.md) · [Curation](curation.md)

## Now

### UI motion refinement

Raj authorized the interface change on `ui/subtle-motion`, based on published
`master` at `3ee3462`. The checked implementation is `fec8a00`.
On 23 November, Raj authorized production publication in conversation:
“alright - take this to production”. This approves the fast-forward to `master`
and push after release checks. Deployment and live checks follow publication.
Controls and map highlights use 100 ms transitions. Inspect and term panels enter
with a 180 ms fade and 3 px travel. Reduced motion gives immediate feedback.
Hover and keyboard focus preview the map label and direct authored references;
the selected Inspect card changes only on selection.

`just check` passed: 132 Python tests, 11 Node tests, 30 Chromium tests, review
freshness, terms, embeddings, build and whitespace checks. Seven new browser
checks cover panel entry, phone touch, hover, keyboard preview, Escape and focus
return, fixed map coordinates, direct references and reduced motion. Desktop,
phone and reduced-motion screenshots were inspected. The local preview on port
8773 was stopped by Raj before publication.

An early test click encountered overlapping SVG hit areas. The test now clicks
the dot center, like the existing phone checks. It also exposed a preview
fallback error after mouse focus; the selected post now takes precedence over
mouse focus when hover ends. Real Tab navigation tests keyboard preview.
Article prose, terms, links, review imports and embeddings are unchanged.

### Blog Update [1] release preparation

The following is the pre-push record for `3ee3462`. Publication later succeeded
for that exact SHA in workflow `44939863525`. The live post and linked pages
matched the checked build; desktop and phone checks passed. Deployment evidence
was reported in conversation, without a separate status-only push.

Raj approved **[Blog Update [1]](../logs/2026-11-21-blog-update-1.md)** and publication
in conversation: “this is good to publish. go ahead and publish - then i sleep for the day”.
The coordinator authorized release preparation and `just publish` from clean `master`
after all checks, without another pre-push exchange. Approved content is `46ed50a`.
The title, 21 November subject date, timestamp, route, term and three links are unchanged.

Stopped only the confirmed final-session Potato server and imported
`f2132a7027bce0dce50c-925014945ee96b2c.json`. Sources match. Native user/navigation
state exists, but there are no saved responses or notes. This is not browser approval;
the conversation approval is separate. All sessions and earlier evidence are preserved.

Read the complete current post and its three post-link targets. Re-read the complete
embedding introduction and approved PCA evidence, then recorded its actual stale
references review. All twenty stages are current. All optional questions are preserved.
Offline preparation reused nine vectors and computed only the new log's vector.
The old database rows, model specification, prose and approved registry are unchanged.

`just check` passed: 132 Python tests, 11 Node tests, 23 Chromium tests, preparation,
terms, embedding freshness, build and whitespace checks. Fresh desktop/phone checks
and image inspection cover both diagrams, exact approved links and the PCA match.
See [release authority and evidence](reviews/blog-update-1-release-2026-11-22.md).
Publication is authorized; deployment and live verification follow the release commit.
No successful deployment is claimed by this pre-push record.

### Completed release

The separately approved release was published at
`f19d221a00462700be3829ac525bb0af2a0e0deb`.
[Workflow 44931985351](https://github.com/rajp152k/rajp152k.github.io/actions/runs/44931985351)
and GitHub Pages deployment succeeded. At 2026-11-21T17:49:56.706523Z, all three
live log pages returned 200 and matched the checked local HTML byte for byte.
See the new evidence report for the deployment record; the earlier
[release record](reviews/release-2026-11-21.md) retains its pre-push evidence.
That release passed all 18 review stages, embedding freshness, 130 Python tests,
11 Node tests, the build, 23 browser tests and whitespace checks. All previous
prose, term records, imports, questions and sessions are preserved in this new task.
Final-session native notes were absent; conversation approval was separate.

### Previous narrator pass
Raj authorized the next pass: “okay - go ahead with the policy updates as well as a rewrite on the logs”.
The canonical [voice policy](writing.md#writing-policy) now names Autolith as narrator:
“I” for its actions, observations, and judgments; “we” for shared work; Raj for his
distinct role. The voice will develop through review, with evidence-based attribution.

All three logs introduce Autolith and use first-person narration where it helps.
**Meditating on logs** distinguishes the author from shared work. **On Autolith**
clarifies the conversational role, writing duties, and assessment of the setup
checks. **A laboratory across machines** separates the narrator from runtime
agents and gives the design judgments a first-person subject. Orch's work keeps
its attribution. Titles, dates, routes, diagrams, and evidence limits are unchanged.

Raj also directed: “do preserve terms and outlinks for now - i don't wish to re-evaluate those”.
Existing curation choices are carried forward for this revision. Terms, registry,
evidence phrases, link text, and destinations are preserved. No candidate votes
are inferred and no term/outlink reconsideration is queued for this prose pass.

Previous narrator Potato session: `fd8ceec61c1ccea15dda`, with three complete frozen
logs, native Notes, and optional whole-log comments. To inspect that historical
batch, use its explicit session ID rather than the current-session pointer.
The [third memo batch](reviews/log-memos-cycle-3-2026-11-21.md) records authority,
edits, hashes, and the curation direction. New cycle-3 records track the current texts.

The [second prose review](reviews/log-memo-feedback-cycle-2-2026-11-21.md) contains
one memo on **Meditating on logs**. It informed this authorized pass. Its native
import and all previous review evidence are preserved.

The study and [complete inventory](reviews/archive-writing-inventory-2026-11-21.md)
cover all 101 Markdown content files in pinned archive commit
`94920842829925836cbc08effa16255ac293832a`: 90 posts and 11 pages. Attribution
boundaries, counterexamples, and individual suggestions are in the review records.

Raj completed the log memo review. Session `62bbaa5280c3a734eaf9` is imported in
[the evidence report](../review-imports/62bbaa5280c3a734eaf9-73a68ec0e64c8b75.json).
It contains 11 memos by `raj`: six for **Two collections, one archive**, four for
**Using Autolith so far**, and one for **Orchestrating Autolith for a personal
laboratory**. There are no replies or whole-log responses; all memo anchors are
null. No source changed before import.

[Full feedback and the proposed edit/policy split](reviews/log-memo-feedback-2026-11-21.md)
are recorded separately from the frozen batch. The native evidence includes
IDs, authors, timestamps, visibility, and all available thread data. The live
server was stopped with SIGINT before import. Session data and prior records are
preserved. This feedback now informs the authorized prose revision and the new memo pass.

### Completed outlink review

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

HMAS, Lisp image T2:r2, and Simplified Technical English T7:r2 were applied at
`c60af1e`. Registry definitions, aliases, and exact evidence quotes are unchanged.
Cycle 2 recorded changed-use scopes as stale. Raj now explicitly directs us to
preserve existing terms and outlinks for this revision without reevaluating them.
Cycle-3 records capture that carry-forward direction; earlier evidence is unchanged.

The [approval import](../review-imports/1c0ce0132fd10a6f26a8-403c434257318011.json)
has no changed sources, comments, or memos. The
[Using Autolith record](reviews/logs/2026-10-07-using-autolith/cycle-1.md)
contains both approvals and applied states. The earlier six rejections and two
revision requests are retained. Rejected terms are absent from the registry.

Selection policy is short and general. Writing docs cover definition references
and revised cards. Review cards and public term pages use the same safe link
renderer. Optional registry `entries` restrict matching to approved posts.
Prior term decisions are preserved as history. Current carry-forward scope is in the cycle-3 records.

## Checks

For the narrator pass: all three posts parse and render through the project
Markdown and article functions. Metadata, exact outgoing link markup, registry
source phrases, and both diagram blocks match the previous revision. Four focused
memo/snapshot/import tests pass. The new session has three full current texts,
native Notes, and an optional comment form, with no responses yet. Import is
pending Raj's review. Editorial receipts are stale; none were refreshed. No diagram
browser checks were repeated because the diagrams did not change. No full build,
broad suites, embedding update, push, or publication was run.

For the previous prose pass: all three posts parse and render through the project Markdown
and article functions. Dates, stable routes, registry source quotes, and strictly
earlier internal-link targets pass. Both Mermaid diagrams render in Chromium;
AL inspected the combined image. Four focused queue/import/snapshot tests pass.
The new session has three exact current snapshots, native memos and only
an optional comment form. Its completed review is imported as described above.
Diff and whitespace checks pass. Reader/references receipts are stale and were not
refreshed. No embedding update, full site build, broad suite, push, or publication
was run. Meditations, registry, old sessions/imports and policy are untouched.

For the second memo import: all four frozen/current sources match. Exact native
evidence equality, SQLite integrity, three full-text items, and byte-identical
idempotent reimport pass. Three focused import/thread/cleanup tests pass. The exact
session server was stopped with SIGINT before import. Prior sessions, imports,
feedback, and the frozen batch are preserved. No browser checks or broad suites ran.

For the policy update: checked local document links and policy anchors, inspected
active policy references for obsolete STE and fixed-heading rules, and reviewed
the scoped diff and whitespace. Posts, registry, receipts, sessions, and imports
are unchanged. No broad suites, browser checks, builds, or publication were run.
Existing receipts need fresh reviews under the changed policy; none were refreshed.

For the archive study: checked source bytes against pinned Git blobs, complete
inventory and batch counts, cited paths, quotations, document links, and diff.
One invalid-UTF-8 source used a documented analysis-only Latin-1 fallback.
A frame's incorrect count was reconciled against its 13 named sources. No archive
code, broad suites, browser tests, builds, push, or publication were run.

For memo import: checked all four frozen source hashes against current files,
all three full log items, exact native evidence equality, SQLite integrity,
idempotent reimport, and 11 complete quoted memo bodies. The 21 direct queue/import
tests pass. No browser tests, builds, or full release suites were run.

For the memo pass: 21 direct queue/import tests pass. Checked the three-item count,
unique IDs, complete current snapshots, source hashes, native memo configuration,
and comment-only form. All 96 prior post, session, import, and registry files match
their pre-task hashes. No browser tests, builds, or full release suites were run.

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

Commit the checked release preparation files and use clean `master`. Report the
complete release scope, commit and checks, then wait for the coordinator's push
go-ahead. After authorized push, verify GitHub Pages deployment, its SHA, and all
three live logs. Do not report publication from a push alone.

The diagram deliberately leaves the blog checkout's host unspecified. It does
not infer a cross-machine topology from the later orchestration proposal.
