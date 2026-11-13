# Writing and preparation

## Daily use

Write a meditation with `./write.sh "Title"`. Ask the agent to prepare the post.
The agent handles all stages below. Discuss open questions, review the preview,
and approve publication separately.

Run `npm ci` after dependency changes. Use the Python environment setup in README.
For browser checks, install Chromium once with `npx playwright install chromium`.

| Command | Result |
| --- | --- |
| `./prepare.sh status` | Show current, pending, stale, and blocked reviews |
| `./prepare.sh` or `./prepare.sh build` | Show review status, update embeddings, build a draft |
| `./prepare.sh preview` | Build, then serve site/ at http://127.0.0.1:8765/ |
| `./prepare.sh preview --port 8766` | Use another local port |
| `./prepare.sh check` | Require current editorial reviews and valid term records |
| `sh scripts/verify_preparation.sh` | Run the complete release checks |

Stop the preview with Ctrl-C. Builds and previews permit pending editorial work.
A failed embedding update stops preparation before the site build. Invalid term
records or reserved anchor collisions stop preparation before either command.
A styling-only preview can use `sh scripts/python.sh scripts/publish.py` without
updating embeddings. An unchanged embedding update is a no-op.

## Agent stages

1. **Read.** Read the complete draft and the editorial policy. Identify its purpose,
   intended reader, assumed knowledge, source links, and questions. Record the
   reader review.
2. **Review terms and references.** Read source contexts and useful related posts.
   Reuse, add, revise, or exclude term candidates. Check the effect on older posts.
   Choose introductory posts for reader value. Record decisions, reading choices,
   and questions. Follow docs/editorial-policy.md.
3. **Prepare.** Run `./prepare.sh build`. This updates changed embeddings and builds
   HTML, term pages, search, the map, and the public database. Check the preview,
   including terms, links, keyboard use, desktop layout, and phone reading.
4. **Revise.** After edits, run status. Repeat the affected editorial stages and
   prepare again. Keep questions outside the article.
5. **Check.** Run the complete release checks. Inspect the diff and commit the
   intended source, registry, review state, and embedding database changes.
6. **Publish with approval.** Obtain raj's publication approval. On a clean master
   checkout, `./publish.sh` runs release checks and pushes committed work. It does
   not stage files or create a commit. Verify the deployment and live page.

The agent maintains records. Raj decides uncertain meaning and approves prose
changes and publication. A post can pass review without any terms.

## Record a review

Only record a stage after performing it. Use a collection/slug entry key.
The references stage requires a current, unblocked reader review.

```sh
./prepare.sh review meditations/studying --stage reader \
  --note "Read the draft for readers planning self-study; the concept-tree example explains the central method."
./prepare.sh review meditations/studying --stage references \
  --note "Checked the concept-tree definition, evidence, and introductory post." \
  --decision "Keep outline out of aliases because it has a broader meaning." \
  --related meditations/pkm-to-pem
```

Repeat `--decision`, `--related`, `--question`, or `--blocking-question` as needed.
Use the note and decisions to explain why selected related reading helps.
Related-reading choices are internal editorial records; they do not insert links
into article prose. Term cards separately show introductions and matched mentions.

Optional questions are visible in status and permit release checks. Blocking
questions prevent a current stage. After resolving one, record a new review with
its answer in the note or decisions. Each review replaces that stage's previous
note, decisions, reading choices, and questions; include any questions still open.

After an intentional deletion, run `./prepare.sh prune` to remove its receipts.
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
