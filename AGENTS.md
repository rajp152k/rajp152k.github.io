# Working on this blog

Start with [docs/README.md](docs/README.md) and [docs/progress.md](docs/progress.md).
Follow [docs/workflow.md](docs/workflow.md) for states and approval gates,
[docs/curation.md](docs/curation.md) for proposals, and
[docs/editorial-policy.md](docs/editorial-policy.md) for selection rules.
Use [docs/writing.md](docs/writing.md) for commands.

Raj approves terms and curated post links, including reuse and changes. Submit
jargon and domain-specific terms, not ordinary phrases given local meaning.
Keep proposals in a Markdown review record under `docs/reviews/`. Apply only raj's
approved candidate revisions to `terms.json` or prose. Existing records and agent
review receipts do not establish approval. Never waive this gate based on past
preferences, a successful build, or general approval of a post.

For preparation, inspect Git status and run `just status`. Read the whole draft,
submit the curation batch, and wait for raj's decisions. Maintain the review's YAML
state and decision history. After approval, apply the changes, record completed
reviews, and run `just prepare`. Early draft previews are allowed. The scripts do
not yet enforce the Markdown approval states.

Meditations are raj's prose and have no terms. Ask before editing them. Create a
log only when requested; AL may edit log drafts during iteration. Load the
repository skill `ops-log` from [.agents/skills/ops-log/SKILL.md](.agents/skills/ops-log/SKILL.md).
If skill discovery is unavailable, read that file directly. Keep prose questions
outside articles. All repository records are public-intended.

Use Potato for term decisions, outlink decisions, no-outlinks-needed results, and log comments. Raj runs `just review`, reviews in
the browser, and tells AL when done. Import responses against the exact reviewed
snapshots. Keep final commit and publication approval in conversation. Maintain records
of actual work and decisions. Update `docs/progress.md` after each review batch,
transition, or blocker. Keep chat updates concise and include detailed evidence
in the review record.

Use `.preparation.json` for completed review receipts and unresolved questions.
Use Markdown front matter for raj's scoped approvals and workflow history.
`docs/archive-review.md` is historical evidence, not current approval. Policy edits
make old receipts stale. Do not refresh them without doing the new reviews.

Keep post iteration local until raj approves a version for commit. After approval,
run `just check`, inspect the diff, and commit only intended
files. For requested repository maintenance, check and commit the work without
including unrelated draft posts. Keep model calls out of builds and CI.

The UX is approved at `8488dd5`; see [docs/lab-journal.md](docs/lab-journal.md).
Change that interaction only when requested or to fix a demonstrated defect.
Obtain separate authority for merge, push, or publication. After authorized
publication, check the deployment and live page before reporting success.
