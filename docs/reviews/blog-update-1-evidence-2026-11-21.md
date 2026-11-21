# Blog Update [1]: evidence and review handoff

## Scope

Requested new log: `logs/2026-11-21-blog-update-1.md`, titled exactly
**Blog Update [1]**. This is a draft for review, not publication.
Draft SHA-256: `e7200d5b526b2dba7c6930cfe79e8b1b0a959897381e982652c0127dd482623d`.
Branch: `draft/blog-update-1-2026-11-21`, based on published `f19d221`.

The coordinator explicitly requested a scoped branch checkpoint commit. This is
not Raj's final approval of the post, curation, merge, push, or publication.
Workflow state is `curation`. The existing eighteen editorial receipts are
preserved; only a completed reader review for the new draft is added.

## Coverage and sources

| Draft subject | Primary evidence and limits |
| --- | --- |
| Earlier work shipped today | Git range `ebcb94b..f19d221` contains 33 commits. `181006a` added terms/panels on 11 November; `95dc0c0`, `36ef581`, `575b4e5`, and `8488dd5` record 13 November layout, palette, relationships, and approved Inspect interaction. `docs/lab-journal.md` describes current behavior. These are not claimed as implementations made today. |
| Projection, similarity, references | `meditations/embeddings.md` describes cached vectors and centered PCA. `docs/lab-journal.md` separates projected position, authored reference lines, and full-vector cosine neighbours. Filters do not refit the archive projection. |
| Curation and review tools made today | `f77efc5`, `f530ca7`, `fde3868`, `f068f6c`, and `c60af1e`; `docs/curation.md`, `docs/editorial-policy.md`, current `terms.json`, and the cycle-1 review records. Compact cards, expandable evidence, per-entry scopes, and safe definition links are distinct from the older public interface. |
| Actual term decisions | `af17af8`, `63c8d2a`, `c60af1e` and their tracked imports: six rejections, two requests for revised definitions, then exact revised-card approvals. Three final registry records. No old rejected candidate is reopened by this draft. |
| Actual outgoing-link decisions | `docs/reviews/outlinks-2026-11-21.md` and import `9ea549187a75fbae5e1e-4441fb6b796e5891.json`: ten approved cards, five additions across four posts and five no-link results. No reverse links or guessed same-day order. |
| Archive study and first prose feedback | `docs/reviews/log-memo-feedback-2026-11-21.md`, `archive-writing-study-2026-11-21.md`, and `archive-writing-inventory-2026-11-21.md`. Eleven native memos; pinned archive `94920842829925836cbc08effa16255ac293832a`; 101 Markdown files, 90 posts and 11 pages, read in eight bounded body-study batches. Coverage is not an attribution or perfect-interpretation guarantee. |
| Prose and narrator changes | `971cf2f`, `27754ed`, `0cea7c0`, `1261f7e`; canonical `docs/writing.md`; first and second feedback reports and cycle-3 memo batch. Second review has one memo, not three approvals. Blog prose policy changed, not the runtime setting. Final terms/outlinks were carried forward under explicit direction. |
| Release blockers and checks | `docs/reviews/release-2026-11-21.md`, `release-editorial-2026-11-21.md`, and `f19d221`: expired authentication during an optional model-file check; pinned-cache offline retry; three changed embeddings, nine fresh entries; three stale test files repaired; 130 Python, 11 Node, 23 browser tests passed. No approved production prose or term record changed for the test repair. |
| Publication | Exact SHA `f19d221a00462700be3829ac525bb0af2a0e0deb`; [workflow 44931985351](https://github.com/rajp152k/rajp152k.github.io/actions/runs/44931985351), both validation/build and deployment successful. GitHub Pages deployment `7967067568` records the same SHA and success. At 2026-11-21T17:49:56.706523Z, all three live log pages returned 200 and matched the checked local HTML byte for byte. This evidence was recorded after the release record's pre-push state. |

The published prose of all nine earlier entries is unchanged by this task.
Potato.nvim is separate and incomplete. It is not part of this article or task.
No conversation fact remains missing for this draft's stated claims.

## Review session

Session: `6a7d77d92e6e51fd9e14`.
Service: **http://127.0.0.1:8769/**, bound to loopback only.
The server was started with:

```sh
just review --session 6a7d77d92e6e51fd9e14 --port 8769
```

The dedicated background service is execution
`L3h41nW`. Keep it running for review. No pre-existing listener was stopped. Existing
session folders, imports, and native evidence were not removed or modified.
An initial batch, `4598f1432af24f843c32`, is also preserved. Its server was stopped after confirming no native activity. A whitespace check found one extra blank line at the end of the outlink record; I removed it and froze this replacement batch. The post and candidate text are unchanged. The current-session pointer now selects this new session. Always use its explicit
ID and port if restarting it. Plain `just review` uses the current session on its
default port, 8768.

The frozen batch has five items:

1. T1:r1: principal component analysis, a new-post-only definition proposal.
2. Complete **Blog Update [1]** text, with native Notes and an optional general comment.
3. L1:r1: the original vector/projection method in **Blog Update [0]**.
4. L2:r1: the authorship distinction in **Meditating on logs**.
5. L3:r1: completed changes versus proposed cluster work in **A laboratory across machines**.

The draft contains no applied outgoing post links. The three link cards are
proposals. The term registry is unchanged. Full source/target snapshots and the
term evidence are frozen; no candidate votes or native memos are fabricated.

### For Raj

1. Open http://127.0.0.1:8769/. Enter `raj` in the username field and select **Continue**.
2. Read T1:r1. Select approve, request changes, reject, or defer. Use its comment field for the reason or exact correction.
3. Read the complete log item. Open **Notes**, quote a passage or name a section, write feedback, and select **Add note**. Add more notes or replies as needed. Use the general comment field for whole-post feedback. A decision on the log item is not commit or publication approval.
4. Review L1:r1–L3:r1. Open the evidence sections when needed and decide each exact proposal.
5. Tell AL when done. Leave final commit and publication approval in conversation.

After Raj finishes, AL must confirm and stop this exact server with SIGINT before
import. Then run:

```sh
just import-reviews 6a7d77d92e6e51fd9e14
```

Read all native decisions, comments, memos, and thread rows. Check the frozen and
current source hashes before applying any decision. Preserve the session and
all earlier data for this review cycle. Do not clean merely because an import
exists. If there is no saved evidence, report that fact rather than creating an
approval. Refine the draft from the actual feedback and queue new revisions for
changed candidates or sources.

## Checks performed for this draft

- Read AGENTS, writing/curation/workflow/editorial/cooperation policies, and the repository ops-log instructions.
- Ran `just status` before drafting: all eighteen prior stages were current.
- Read the full draft and source/target posts; reviewed the historical evidence. Two independent read-only reviews checked the older/today distinction and release claims. Corrected the expired-authentication wording and the collective-pronoun sentence.
- Recorded only the new draft's completed reader stage with `just record-review`. Its reference stage is pending; all old stages and questions are preserved.
- Ran the two focused review test modules: **21/21 passed**. No release suite was run.
- Queued the real batch with both review records and `--source meditations/embeddings.md`. Queue validation checked exact source hashes, passages, target paths, and strictly earlier target dates.
- Verified five unique items, byte-exact complete log text, current hashes for every frozen source, native Notes enabled, password-free username login, and no user saves created during checks.
- Confirmed the review service returns HTTP 200 with the correct session ID and listens only on `127.0.0.1:8769`.
- Confirmed earlier memo-session manifests remain present. No synthetic login, vote, memo, import, or editorial approval was created.
- Ran `scripts/terms.py --check`: three valid records, ten entries, and no matched terms in the new log. Prior eligible matches are unchanged.
- Compared every previously tracked article and import, the term registry, embedding database, writing policy, and AGENTS against `f19d221`: byte-identical. Compared preparation JSON after removing the new reader entry: all earlier receipts and questions are identical.
- Ran `just status` after preparation: all eighteen old stages current; the new reader stage current and references pending. Verified all queued candidates are still proposed with null decisions and no applied prose links.

This review uses the complete frozen text in Potato. No embedding refresh, site
build, or visual browser check is claimed for the new draft. `blog.sqlite` and
`terms.json` are unchanged. Those checks and curation application can follow the
user's refinement pass. This branch must not be merged or published by this task.
