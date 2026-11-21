---
name: ops-log
description: "Create or revise raj's operational logs when requested. Follow the canonical blog writing policy and source-backed preparation workflow. Keep draft iteration, commit approval, and publication separate."
---

# Operational logs

Create or revise a log only when raj asks. Follow the canonical
[writing policy](../../../docs/writing.md#writing-policy) for voice and prose.

## Start

Work in this repository. Read [the cooperation agreement](../../../docs/cooperation.md),
[the writing guide](../../../docs/writing.md), and
[the editorial policy](../../../docs/editorial-policy.md). Inspect Git status and
run `just status`. Preserve unrelated work. Read relevant earlier posts
and the evidence for the work before drafting. Ask raj about missing intent or
unsupported claims. Keep those questions outside the article.
Follow the [state machine](../../../docs/workflow.md). Keep this log's workflow
state in a separate Markdown review record under `docs/reviews/` and update
[Progress](../../../docs/progress.md) after each batch or state change.

## File format

Use one Markdown file directly in `logs/`, normally `YYYY-MM-DD-topic.md`.
Use only `title` and `date` in YAML front matter. Quote the title safely. Give a
new log a timezone-aware publication timestamp. Preserve its slug and timestamp
when revising it. Put links to earlier posts in the body.

## Body

Choose sections for the account under the [writing policy](../../../docs/writing.md#writing-policy).
There is no required heading sequence. Place approved earlier-post links where
useful; a separate related-reading section is optional.

Keep review notes, citation questions, approval requests, and draft status outside
the article. Include uncertainty about the work when the reader needs it.

## Language

Use the canonical [writing policy](../../../docs/writing.md#writing-policy).
Keep prose rules there rather than maintaining a second style guide here.

Use Mermaid diagrams, math, or inline SVG only when they make the explanation
clearer or shorter. Keep them in the Markdown file. Give Mermaid diagrams an
accessible title and, when needed, a description. Check the rendered result.

## Prepare and revise

Read the whole draft as a reader. Submit jargon and domain-specific term candidates
and post-link proposals under the [curation rules](../../../docs/curation.md).
Raj approves exact term and post-link revisions, including reuse, removal, and
no-outlinks-needed results. Use Potato for these decisions and log memos. Keep
unapproved proposals in the review page; apply only approved revisions to the log
and registry. Record decisions against the reviewed snapshots in review front
matter. Record completed agent stages with `just record-review`; this is not approval.
Run `just prepare` to update changed embeddings and build the local site.
Use `just preview` to serve it. Check the article, diagrams, links, terms,
and phone layout. Inspect screenshots when a visual check is needed.

Keep iteration local until raj asks for a commit or approves a specific version
for commit. Treat changed `blog.sqlite`, `terms.json`, and `.preparation.json` as
part of the draft. After edits, mark affected decisions stale, repeat the affected
reviews and raj's approvals, and build. Keep meditation edits within permission.

Preserve collection URLs (`/logs/<slug>/` and `/<slug>/`), independent `lx`/`mx`
codes, the shared archive-wide map projection, and collection search behavior.
Check past links against the source posts and the rendered site.

## Commit and publication

After commit approval, run `just check`. Inspect the diff
and commit the approved log and its required state changes. Keep unrelated work
out of the commit. Report the preview, open questions, and Git state.

Obtain separate approval before merge, push, or publication. `just publish`
requires a clean `master` checkout, runs release checks, and pushes committed
work. It does not stage or commit files. After an approved publication, check
the deployment and the live page.

Ported from raj's dotfiles skill at
`autolith/.config/autolith/skills/ops-log/SKILL.md`. Repository paths and preparation
commands replace the machine-specific workflow in that copy.
