# Writing and preparation

## Daily use

Write a meditation with `just write "Title"`, or ask the agent to write a log.
Ask for preparation, decide the term and link candidates, then read the preview.
Approve commit and publication separately. Follow the [state machine](workflow.md)
and open [Progress](progress.md) for the current review and next decision.

Saving Markdown does not start a build or a review. Run the commands below, or
ask the agent to complete the preparation workflow.

Run `npm ci` after dependency changes. Use the Python environment setup in README.
For browser checks, install Chromium once with `npx playwright install chromium`.

| Command | Result |
| --- | --- |
| `just status` | Show current, pending, stale, and blocked reviews |
| `just prepare` | Show review status, update embeddings, build a draft |
| `just preview` | Build, then serve site/ at http://127.0.0.1:8765/ |
| `just preview --port 8766` | Use another local port |
| `just review-check` | Require current editorial reviews and valid term records |
| `just check` | Run the complete release checks |

Stop the preview with Ctrl-C. Preview builds once, then serves `site/`; it does
not watch files. After edits, run `just status`, repeat affected reviews,
and run `just prepare` in another terminal. Refresh the browser.

Builds and previews permit pending editorial work. A failed embedding update
stops preparation before the site build. Invalid term records or reserved anchor
collisions stop preparation before either command. For a styling-only preview,
use `just build` without updating embeddings.
An unchanged embedding update is a no-op.

## Start a post

| Collection | Authoring | File and date | Public URL |
| --- | --- | --- | --- |
| Meditation | Raj writes; the agent edits prose only with permission | `meditations/<slug>.md`; `date: YYYY-MM-DD` | `/<slug>/` |
| Log | The agent drafts only when requested, using [ops-log](../.agents/skills/ops-log/SKILL.md) | `logs/YYYY-MM-DD-topic.md`; timezone-aware timestamp | `/logs/<slug>/` |

Use `title` and `date` in YAML front matter. Keep each post directly in its
collection directory. For a log, preserve its slug and publication timestamp on
revision. For a meditation, `just write` quotes the title, sets today's date, and
opens Neovim. Use a different title if its slug is `search`, `logs`, `meditations`,
or `terms`; those routes are reserved.

Keep workflow state and human decisions in a separate Markdown review record under
`docs/reviews/`, using the [template](review-template.md). Its YAML front matter
tracks the post state; it is not publication metadata. The scripts do not enforce
these human approval fields yet.

The release includes **every top-level Markdown post** in both collections on
the release revision. A future date or `draft: true` does not exclude a file.
Keep unrelated unfinished posts off that revision. A local preview may include
them, but release checks require current reviews for the whole archive.

## Agent stages

1. **Read.** Read the complete draft and the editorial policy. Identify its purpose,
   intended reader, assumed knowledge, source links, and questions. Record the
   reader review.
2. **Submit curation.** Propose jargon and domain-specific terms and useful post
   links under the [curation rules](curation.md). Include existing matches and links.
   Raj decides the candidate revisions. Record those decisions before applying any
   registry or link changes. Then complete the references review.
3. **Prepare.** Run `just prepare`. This updates changed embeddings and builds
   HTML, term pages, search, the map, and the public database. Check the preview,
   including terms, links, keyboard use, desktop layout, and phone reading.
4. **Revise.** After edits, run status. Mark affected decisions stale, repeat affected
   reviews and raj's approvals, and prepare again. Keep questions outside the article.
5. **Check and commit with approval.** After raj approves a specific version for
   commit, run the complete release checks. Inspect the diff and commit the
   intended source, registry, review state, and embedding database changes.
6. **Publish with approval.** Obtain separate publication approval. After any
   approved merge, use a clean `master` checkout. Run `just publish` to run release
   checks and push committed work. It does not stage files or create a commit.
   Verify the deployment and live page.

The agent maintains records. Raj approves terms, links, prose changes, commit, and
publication. Submit a no-term or no-link result for confirmation too.

## What preparation changes

| Input or stage | Result |
| --- | --- |
| Reader and references reviews | Current-input review records, decisions, and questions in `.preparation.json` |
| Raj-approved term decisions | Definitions, exact source passages, aliases, and introductions in `terms.json` |
| Embedding update | Metadata and changed vectors in `blog.sqlite`; reuse unchanged vectors |
| Site build | Article HTML, terms and source links, search index, shared PCA map, post-reference lines, and public SQLite export in `site/` |
| Local preview | Serve the generated site at the reported loopback address |

Keep Markdown, changed records, and `blog.sqlite` together for an approved post
commit. Keep `site/`, environments, dependencies, and model caches local.
Related-reading review records do not insert links into prose. The map's reference
lines come from links in the posts; nearest-post scores come from embeddings.
See [build reference](build.md) for the implementation and CI details.

## Record a review

Only record a stage after performing it. Use a collection/slug entry key.
The references stage requires a current, unblocked reader review.
Record the references receipt after raj's curation decisions and the actual review.
These commands record agent work, not human approval. The example below assumes
raj has already approved the named term and related-reading scope.

```sh
just review meditations/studying --stage reader \
  --note "Read the draft for readers planning self-study; the concept-tree example explains the central method."
just review meditations/studying --stage references \
  --note "Checked the concept-tree definition, evidence, and introductory post." \
  --decision "Keep outline out of aliases because it has a broader meaning." \
  --related meditations/pkm-to-pem
```

Repeat `--decision`, `--related`, `--question`, or `--blocking-question` as needed.
Use the note and decisions to explain why selected related reading helps.
Related-reading choices are internal editorial records; they do not insert links
into article prose. Term cards separately show introductions and matched mentions.

The current scripts permit optional questions and block on blocking questions.
That behavior is separate from approval: keep a proposed item out of applied
changes until raj decides it. Resolve blockers and record a new review with the
answer. Each review replaces that stage's previous notes, so retain open questions.

After an intentional deletion, run `just prune` to remove its receipts.
Fix any term sources, introductions, or reading choices that point to the deleted
post. Renamed posts have new keys and require a review under those keys.

## Review freshness

`.preparation.json` is internal, versioned state. It is excluded from generated
HTML, search, embeddings, and the public database.

- New posts need reader and references reviews.
- Title or body changes invalidate both stages for that post.
- Relevant definitions, aliases, introductions, source contexts, and selected
  reading changes invalidate affected references reviews.
- Newly matching terms also invalidate the affected references reviews.
- Editorial policy changes invalidate both stages across the archive.
- Dates, CSS, layout, unrelated registry terms, and this command guide do not
  invalidate editorial reviews. Other build and embedding checks still apply.

Status reports which inputs changed. It does not perform a review or record one.
The receipt hashes establish which inputs were reviewed, not editorial quality.
Builds and CI make no model calls. CI runs the same release script as local work.
Preparation receipts do not replace approval of the final preview.

## Maintenance effort

Review changed material and its dependencies, not the whole archive on every
post. Keep useful exclusion reasons. Run the stages on the next real post before
adding more workflow features. Assess preparation time, questions asked, repeated
work, and corrections after preview. There is no measured time estimate yet.
