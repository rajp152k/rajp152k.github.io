# Working together

## Who does what

| Work | Raj | Agent |
| --- | --- | --- |
| Meditations | Write the prose; decide its meaning | Read, ask questions, suggest edits; change prose only with permission |
| Logs | Request the subject; confirm intent and results | Draft and revise with the [ops-log skill](../.agents/skills/ops-log/SKILL.md) |
| Terms and sources | Resolve unclear meaning | Check evidence; maintain definitions, source passages, and reading choices |
| Preparation | Review the preview | Review the draft, update records and embeddings, build, and test |
| Commit | Approve a specific post version for commit | Check and commit that version with its required state |
| Publication | Approve merge, push, or publication separately | Run release checks and verify the deployment and live page |

## The normal exchange

1. Write a meditation with `./write.sh "Title"`, or ask for a log about specific work.
2. Ask to prepare it. The agent follows the [writing workflow](writing.md) without
   asking you to name each stage. It reads the whole post, checks terms and sources,
   records reviews, updates embeddings, and builds a local preview.
3. Discuss the preview and questions. The agent repeats only the affected work
   after a revision. Drafts and previews stay local until commit approval.
4. Approve a version for commit. The agent runs the complete checks, inspects the
   diff, and commits the post and required records. Approval to commit is separate
   from approval to publish.
5. Approve publication when ready. The agent checks the deployment and the live post.

Use the same preparation steps for a new post and an edited post. Keep log slugs
and publication timestamps stable when revising them.

## Decisions and handoff

Keep intent questions and proposed prose changes outside the article. The agent
handles clear supporting records without asking for each edit. Record unresolved
questions and their effect on release in `.preparation.json`. Follow the
[editorial policy](editorial-policy.md) to decide which questions block review.

Keep the handoff short: changed posts, preview address or build result, open
questions, check results, and whether the work is local, committed, or published.
Name the next decision needed from raj. A successful build is not prose approval.

The UX was approved at `8488dd5`: select a map circle, inspect the card below the
map, then follow its title. Change that interaction only when requested or when
fixing a demonstrated defect. See [the interface notes](lab-journal.md).

For repository maintenance, the agent may update scripts, tests, and supporting
docs and commit the requested work after checks. That does not authorize changes
to article prose or publication. Preserve unrelated work and keep maintenance
commits separate from draft posts.
