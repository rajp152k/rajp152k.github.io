# Working together

## Who does what

| Work | Raj | Agent |
| --- | --- | --- |
| Meditations | Write the prose; decide its meaning | Read, ask questions, suggest edits; change prose only with permission |
| Logs | Request the subject; confirm intent and results | Draft and revise with the [ops-log skill](../.agents/skills/ops-log/SKILL.md) |
| Terms and post links | Approve, reject, defer, or request revisions | Propose candidates and evidence; apply only approved revisions |
| Preparation | Review the preview | Review the draft, update records and embeddings, build, and test |
| Commit | Approve a specific post version for commit | Check and commit that version with its required state |
| Publication | Approve merge, push, or publication separately | Run release checks and verify the deployment and live page |

## The normal exchange

1. Write a meditation with `just write "Title"`, or ask for a log about specific work.
   Meditations have no terms. AL may edit log drafts during iteration.
2. Ask to prepare it. AL reads the whole post and prepares the review material.
   Follow the [state machine](workflow.md).
3. Run `just review`. Decide term and outlink proposals, including no-outlinks-needed results, and add log comments in
   Potato. Tell AL when you are done. AL imports responses, records scoped
   decisions, and applies approved changes. Keep final approval in conversation.
4. Read the preview and revise. Use dedicated review sessions to examine ideas,
   evidence, and writing. Repeat affected reviews and approvals after changes.
5. Approve a specific version for commit in conversation. AL checks and commits
   that version with its records. Approval to commit does not authorize publication.
6. Approve publication separately. AL verifies deployment and the live page.

Use the same preparation steps for a new post and an edited post. Keep log slugs
and publication timestamps stable when revising them.

## Decisions and handoff

Keep intent questions and proposals outside articles. The agent maintains the
Markdown review state and `.preparation.json` receipts. Raj owns approval of terms
and curated post links; the agent cannot approve them as routine record maintenance.
See [Curation](curation.md) for evidence and decision scope.

Read [Progress](progress.md) on the Markdown server for the current work and next
decision. The agent updates it after batches, transitions, and blockers. Keep chat
updates short: state, changes, decision needed, and the review link. Record raj's
reasons to improve later proposals; keep the approval gate through that learning.

The UX was approved at `8488dd5`: select a map circle, inspect the card below the
map, then follow its title. Change that interaction only when requested or when
fixing a demonstrated defect. See [the interface notes](lab-journal.md).

For repository maintenance, the agent may update scripts, tests, and supporting
docs and commit the requested work after checks. That does not authorize changes
to article prose or publication. Preserve unrelated work and keep maintenance
commits separate from draft posts.
