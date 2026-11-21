---
kind: log-memo-review
cycle: 2
state: ready
posts:
  logs/2026-10-06-two-collections-one-archive: 1b1c95a9b6a32b63b7bd684470459b23ea7aa7e6dd42936d63423f1cd3eec200
  logs/2026-10-07-using-autolith: b3d81fa47b9ed73ac396a678bd59b213b7248d69110009a46a9fc6b00f6eb912
  logs/2026-11-06-orchestrating-autolith: 51d10ec537eedb0fe5aa429a50158ae92f7adc8426b4e9078da8ec122ce6f505
---

# Revised logs: second prose pass

Raj authorized revision: “alright revise the logs and then i'll do a review pass again”.
Read the three complete frozen texts in Potato. Add native **Notes**, quoting the
passage or naming the section. The whole-log comment field is optional. This
session has no candidate approval form.

## Revisions

- **Meditating on logs:** start with the authorship problem, explain the shared
  archive through retrieval, and combine the short sections. Remove the repeated
  conclusion. Preserve the author distinction, map labels, and review gates.
- **On Autolith:** start with the setup practice, group configuration and workflow
  details, add Raj's supplied `.files` link, and show the human review loop in a
  Mermaid diagram. Only the Fedora exploration host is identified; the blog
  checkout's host is unspecified. Preserve the limits of the embedding checks.
  Describe the original STE rule as history, rather than as current prose policy.
- **A laboratory across machines:** start with task ownership across machines,
  combine the account into three sections, and distinguish completed service
  removal and local messaging from the proposed remote system and tests.

The [11 imported memos](log-memo-feedback-2026-11-21.md),
[archive study](archive-writing-study-2026-11-21.md), and canonical
[writing policy](../writing.md#writing-policy), commit `971cf2f`, guided this pass.
Titles are choices for this revision, not new naming rules. Routes and dates are
unchanged. Meditations, registry definitions, and old review evidence are untouched.

## Approval scope

All three posts return to **writing**. Earlier exact-revision approvals and
editorial receipts do not approve these texts. Reader and references receipts
were already stale after policy changes and remain stale; none were refreshed.
The new per-post cycle-2 records identify the current hashes and stale scopes.

- First log: the old no-outlinks-needed result described an earlier text. The new
  text has no post links; reconfirm that result for this revision.
- Second log: preserve `/embeddings/` and the first log's stable route. The latter's
  title changed, and both links have new surrounding prose or placement. Renew
  exact link approval. The Lisp-image evidence sentence is unchanged. The STE
  evidence sentence is now a quotation of the old rule, with explicitly historical
  scope. The registry is unchanged; renewed term-use/evidence approval is needed
  before treating either use as currently approved. No new definitions were added.
- Third log: preserve `/laboratory/`, now in the opening. Renew exact placement
  approval. The HMAS evidence sentence is unchanged, but its surrounding passage
  changed; renew the term-use scope. No previously rejected term was added.
- The `.files` external source link was explicitly requested in Raj's memo. It is
  not a new curated archive-post link.

Earlier cycle-1 records, frozen sessions, imports, and decisions are historical
evidence. This memo session collects writing feedback only. It does not renew
curation decisions, approve release, or authorize publication.

## Open and import

Queue with `just queue-review docs/reviews/log-memos-cycle-2-2026-11-21.md`.
Run `just review` to open the newly selected session at http://127.0.0.1:8768/.
Tell AL when done. Stop the server before `just import-reviews ID`; read native
notes and comments against these frozen texts and inspect changed-source flags.
Preserve all previous sessions and imports.
