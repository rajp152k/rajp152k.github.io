---
name: ops-log
description: "Create or revise raj's operational logs when requested. Use concise ASD-STE100 prose, source-backed context, and the blog preparation workflow. Keep draft iteration, commit approval, and publication separate."
---

# Operational logs

Create or revise a log only when raj asks. Explain raj's work and intent, not
agent tool output. Refer to raj by name, not as "the user".

## Start

Work in this repository. Read [the cooperation agreement](../../../docs/cooperation.md),
[the writing guide](../../../docs/writing.md), and
[the editorial policy](../../../docs/editorial-policy.md). Inspect Git status and
run `./prepare.sh status`. Preserve unrelated work. Read relevant earlier posts
and the evidence for the work before drafting. Ask raj about missing intent or
unsupported claims. Keep those questions outside the article.

## File format

Use one Markdown file directly in `logs/`, normally `YYYY-MM-DD-topic.md`.
Use only `title` and `date` in YAML front matter. Quote the title safely. Give a
new log a timezone-aware publication timestamp. Preserve its slug and timestamp
when revising it. Put links to earlier posts in the body.

## Body

Use these top-level headings in order:

1. **Abstract:** a brief account of the subject.
2. **Context:** the starting state and the reason for the work.
3. **Named sections:** as many as the subject needs. Explain each material change,
   its reason, and its effect. Choose specific headings.
4. **Conclusion:** the result or expected state. Distinguish completed work from plans.
5. **Past relevant meditations and blogs:** links to existing posts that help the
   reader. If none apply, say so briefly.

Keep review notes, citation questions, approval requests, and draft status outside
the article. Include uncertainty about the work when the reader needs it.

## Language

Use ASD-STE100 Simplified Technical English for new log prose. Use short, direct
sentences, active voice, and one main idea per sentence. Use each term with one
meaning. Define technical terms when needed. Avoid idioms, long noun groups, and
unnecessary detail. Cover material decisions and behavior without a word target
or section limit. Use the correct tense for results and plans.

Use the official rules and controlled dictionary for a compliance review when
available. Plain-language checks alone do not establish ASD-STE100 compliance.
See [the standard](https://www.asd-ste100.org/),
[its scope](https://www.asd-ste100.org/about_STE.html), and
[the official copy request](https://www.asd-ste100.org/STE_downloads.html).

Use Mermaid diagrams, math, or inline SVG only when they make the explanation
clearer or shorter. Keep them in the Markdown file. Give Mermaid diagrams an
accessible title and, when needed, a description. Check the rendered result.

## Prepare and revise

Read the whole draft as a reader. Check names, claims, source passages, and past
links. Apply the editorial policy to terms, introductions, and related reading.
Record each completed review with `./prepare.sh review`; retain open questions.
Run `./prepare.sh build` to update changed embeddings and build the local site.
Use `./prepare.sh preview` to serve it. Check the article, diagrams, links, terms,
and phone layout. Inspect screenshots when a visual check is needed.

Keep iteration local until raj asks for a commit or approves a specific version
for commit. Treat changed `blog.sqlite`, `terms.json`, and `.preparation.json` as
part of the draft. After each prose edit, repeat the affected review stages and
build. Keep meditation edits limited to what raj authorized.

Preserve collection URLs (`/logs/<slug>/` and `/<slug>/`), independent `lx`/`mx`
codes, the shared archive-wide map projection, and collection search behavior.
Check past links against the source posts and the rendered site.

## Commit and publication

After commit approval, run `sh scripts/verify_preparation.sh`. Inspect the diff
and commit the approved log and its required state changes. Keep unrelated work
out of the commit. Report the preview, open questions, and Git state.

Obtain separate approval before merge, push, or publication. `./publish.sh`
requires a clean `master` checkout, runs release checks, and pushes committed
work. It does not stage or commit files. After an approved publication, check
the deployment and the live page.

Ported from raj's dotfiles skill at
`autolith/.config/autolith/skills/ops-log/SKILL.md`. Repository paths and preparation
commands replace the machine-specific workflow in that copy.
