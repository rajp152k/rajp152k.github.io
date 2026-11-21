# Term and link curation

[Writing desk](README.md) · [States](workflow.md) · [Editorial policy](editorial-policy.md)

## Candidate selection

1. Read the complete post. Assume a technical audience; omit routine vocabulary.
2. Select a term only when it has a distinct domain meaning and a definition helps
   the reader understand this post. Frequency alone does not qualify it.
3. Prefer a few useful definitions. Make each definition sufficient on its own;
   add a reference when it helps.
4. Check existing records, exact contexts, and use scopes. Propose reuse only when
   meanings agree. Identify missing evidence and important exclusions.
5. Submit a small batch. Raj decides; the agent records and applies the decision.

Meditations have no terms. Use this term process for logs. Eligibility is a
selection judgment, not approval of a definition, aliases, evidence, introduction,
or uses. Submit those details for raj's decision.

## Candidate states

- `proposed`: the agent has submitted a complete candidate revision.
- `revision-requested`: raj requested a change. The agent increments `revision` and
  submits it again as `proposed`.
- `approved`: raj approved the exact candidate revision and use scope.
- `rejected`: raj declined it. Record the reason if given.
- `deferred`: raj chose to omit it from this cycle and revisit it later.
- `applied`: the agent applied the approved revision and checked its uses.
- `stale`: changed inputs invalidate the decision. Submit a new `proposed` revision.

Only raj can approve, reject, defer, or request a revision. The agent can propose,
apply an approved revision, or mark a decision stale. Reopen a rejected or deferred
item only at raj's request or with new evidence; explain why it is back.

## What to submit

Give each item a short ID, such as `T1` or `L1`, unique within the review cycle.
Use headings for items rather than wide tables. Put the decision needed first.

Each `terms` or `links` front-matter entry has `id`, `revision` (integer), `state`,
`action` (`add`, `reuse`, `revise`, or `remove`), `record` (body heading anchor),
`decision` (decision ID or null), and `applied_at` (timestamp or null).
The body under that heading contains the proposal. Increase the revision whenever
that proposal or its evidence changes. Retain old proposals and decisions in Git
and the decision history. A decision must name its candidate revision.

### Term proposal

- Name and domain; why it qualifies as jargon or a domain term.
- Exact proposed definition and aliases.
- Post passage where it would help and the reader need.
- Source passages that support the definition, with post links.
- Proposed introduction and why it teaches the concept.
- Existing registry ID, if any; affected posts and matches, including older posts.
- Requested decision: approve, revise, reject, or defer.

Approve a definition, its aliases, evidence, introduction, and use scope together.
Approval of the word alone is not approval of a definition. Include existing matches
for confirmation. Do not apply a new or revised shared record before approval.

Review term proposals in Potato with their exact candidate revisions and source
snapshots. Use the comment field for reasons and corrections. After raj says the
session is done, AL imports the responses and records the scoped decisions here.
Keep post-link decisions and final approval in conversation.

## Outlink review

Review outgoing post links for every post, including meditations and logs.
Consider only targets published before the source post. An older post was not
written with knowledge of later posts; do not add links that imply that knowledge.

1. Read the source post and consider useful links to earlier posts.
2. Check publication dates for each source and target. If their order is unclear,
   resolve it before proposing the link.
3. Record proposed outlinks, or record that no outlinks are needed. Submit each
   proposal with its purpose and exact placement for raj's decision.
4. Apply approved outgoing links only. Do not calculate inlinks or add reverse
   links to older posts as part of this review.

For the initial archive review, apply the date rule separately to every post.
For later publication reviews, review only the outgoing links of the post being
prepared. Keep decisions in its review record.

### Link proposal

- Source post and exact placement or registry field.
- Target post or passage; use `evidence`, `introduction`, or `related-reading` as
  the purpose.
- Exact link text or field value and the proposed addition, revision, or removal.
- Why this target helps this reader here, after reading the target itself.
- Source and target publication dates, and the effect on the source post and map.

A term proposal may include its evidence and introduction links in the same approval
scope. Use separate `L` items for other links. Avoid making raj approve the same
change twice. Existing authored links can be confirmed as a named batch.

## Apply and inspect

After approval, update only the named records and links. Approval of exact prose
link edits authorizes those edits, not a wider rewrite. Record review receipts only
after the review is done. Build and inspect term matches, definitions, source links,
introductions, and map lines. If an automatic match has the wrong meaning, stop and
propose a correction; do not accept it because a string matched.
Check that rejected or deferred additions and reuses are absent. For a revision
or removal proposal, also record raj's decision on the existing use. An automatic
match or authored link may need a separate approved correction. Keep mismatches
with the agreed result as blockers to the `preview` state. An early draft preview
is allowed with those unresolved uses identified.

## Learn from decisions

Keep individual decisions and reasons in review cards and their records, not in
policy. Change policy only for new general selection principles confirmed by raj.
Selection guidance does not remove the approval gate.

Legacy registry entries and old review receipts are not proof of approval under
this process. Review them with raj in batches; do not delete or approve them silently.
