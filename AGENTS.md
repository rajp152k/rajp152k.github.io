# Working on this blog

Read [docs/cooperation.md](docs/cooperation.md) for ownership and approval boundaries.
Follow [docs/writing.md](docs/writing.md) for commands and stages, and
[docs/editorial-policy.md](docs/editorial-policy.md) for review decisions.

For a request to prepare a post, inspect Git status and run `./prepare.sh status`.
Read each affected draft in full. Complete reader and references reviews,
maintain `terms.json`, update only affected review records, and run
`./prepare.sh build`. Report the preview and open questions. Handle these stages
without asking raj to name each one.

Meditations are raj's prose. Ask before editing them. Create or revise a log only
when requested; load the repository skill `ops-log` from
[.agents/skills/ops-log/SKILL.md](.agents/skills/ops-log/SKILL.md). If skill discovery
is unavailable, read that file directly. Keep prose questions outside articles.
Maintain clear supporting records yourself and record only reviews actually done.

Use `.preparation.json` for current reviews, decisions, reading choices, and
questions. It is committed internal state, excluded from the public site.
`docs/archive-review.md` is the initial review, not the current status.

Keep post iteration local until raj approves a version for commit. After approval,
run `sh scripts/verify_preparation.sh`, inspect the diff, and commit only intended
files. For requested repository maintenance, check and commit the work without
including unrelated draft posts. Keep model calls out of builds and CI.

The UX is approved at `8488dd5`; see [docs/lab-journal.md](docs/lab-journal.md).
Change that interaction only when requested or to fix a demonstrated defect.
Obtain separate authority for merge, push, or publication. After authorized
publication, check the deployment and live page before reporting success.
