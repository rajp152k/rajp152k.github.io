---
kind: workflow-spec
version: 1
status: proposed
---

# Writing state machine

[Writing desk](README.md) · [Progress](progress.md) · [Curation](curation.md)

Raj owns term, link, commit, and publication approval. This page proposes the exact
state names and record format for our first iteration. Follow the approval gates
now; revise the format with raj as we use it.

## Post states

`writing` → `curation` → `preview` → `commit-approved` → `committed` →
`publish-approved` → `published`

- **writing:** draft or revise the post. Raj writes meditations with `just write`;
  meditations have no terms. AL drafts logs on request and may edit those drafts.
- **curation:** the agent has read the draft and submitted term and link proposals.
  Raj decides which to approve, reject, defer, or return for revision.
- **preview:** curation is resolved and the rendered uses match raj's decisions.
  Reviews and a fresh build are complete. Raj reads the result.
- **commit-approved:** raj has approved this exact preview and source version for
  commit. The agent must still run the full checks.
- **committed:** checks passed and the approved files were committed. Record the SHA.
- **publish-approved:** raj has authorized the exact release revision and any merge
  or push needed. Inspect the whole release, not just this post.
- **published:** deployment succeeded and the live page was checked. Record the URL,
  deployed SHA, and check time. A push alone does not establish this state.

## Transition guards

1. **writing → curation:** record the post hash, complete reader review, and candidate
   batch. Include existing term matches and links. Submit an explicit empty batch
   if none are needed.
2. **curation → preview:** raj has confirmed the batch, including empty batches.
   No item is `proposed`, `revision-requested`, or `stale`. All approved items are
   applied and checked. Rejected or deferred additions and reuses are absent. For
   revision or removal proposals, record raj's decision on the existing use too.
   Check automatic matches and authored links against those decisions. Defer only
   optional items. Obtain approval for any correction needed to produce the agreed
   result. Resolve blockers, record the references review, build, and inspect it.
3. **preview → commit-approved:** record raj's explicit commit approval for the post,
   applied curation, and preview revision. Earlier term approval is insufficient.
4. **commit-approved → committed:** pass `just check`, inspect the diff, and commit
   only the approved files and required records. Failed checks leave the state at
   `commit-approved` with a blocker. Material fixes require a new preview approval.
5. **committed → publish-approved:** record raj's explicit release authorization and
   its SHA. If a merge changes the approved content, return for review. Use clean
   `master` for publication and run release checks there.
6. **publish-approved → published:** after authorized publication, verify deployment
   and the live page. Record a failure as a blocker, not a successful transition.

The agent records factual transitions. Only raj supplies approval events. Keep
commands and state changes separate: `just prepare` does not advance a gate.
Early draft previews are allowed in `writing` and `curation`.

Use Potato for term decisions and log comments. Raj starts the prepared review
with `just review` and tells AL when done. AL imports responses against their
source snapshots before recording or applying decisions. Resolve post-link
questions and final approval in conversation. Browser activity alone does not
advance a post state.

## Revision and return paths

- A prose change returns an unpublished post to `writing`. Re-read the changed
  draft and its context before submitting it again.
- A candidate, source, alias, introduction, link, or affected-use change returns it
  to `curation`. Mark affected decisions `stale`; submit the changed revisions.
- Clear commit and publication approval when their approved content changes. Keep
  earlier decisions in history. Carry forward an unaffected decision only with a
  recorded reason and confirmation that its scope and evidence did not change.
- For a published post, start a new numbered cycle at `writing`. Preserve the prior
  release record. The live version is still the last verified published cycle.
- A blocker is a recorded issue, not a separate state. Name who can resolve it.

## Markdown records

Keep review state in YAML front matter at
`docs/reviews/<collection>/<slug>/cycle-<number>.md`. Start from the
[review template](review-template.md). Keep article metadata separate so the post
hash is independent of state edits. All repository records are public-intended.

Use these fields:

- `schema`: `1`; `kind`: `post-review`; `entry`: `collection/slug`; `cycle`: integer.
- `state`: one post state above; `post_sha256`: SHA-256 of the complete Markdown file.
- `terms`, `links`: candidate records defined in [Curation](curation.md).
- `decisions`: append-only records with `id`, `actor`, `action`, `scope`,
  `post_sha256`, `at` (timezone-aware timestamp), `evidence`, and `reason`.
  Approval records use `actor: raj`. Record the actual message or a stable reference.
  Scope names candidate IDs and revisions, a batch, or an exact commit/preview.
- `transitions`: append-only `from`, `to`, `actor`, `at`, `event`, and `evidence`.
- `blockers`: issue, owner, and resolution needed.
- `release`: `commit`, `deployed_commit`, `url`, and `verified_at`; null until known.

Update a record when work or approval occurs. A typed state without evidence does
not establish approval. Never invent a timestamp, SHA, or decision to fill a field.

## Current enforcement

These Markdown records are maintained by the agent and reviewed by raj. The scripts
currently check `.preparation.json` review freshness, registry integrity, embeddings,
and the build. They do not parse these approval records or enforce these transitions.
`.preparation.json` stores completed review receipts; the Markdown record stores
human decisions. One does not substitute for the other.

The build includes every top-level post in both collections. Front-matter state does
not filter publication. Keep unfinished posts off the release revision. Do not
publish while approvals or archive-wide release checks are unresolved.
