# meditations of yet another raj

Source for <https://yetanotherraj.com/>. Markdown is the source of truth:

- `meditations/`: raj's writing, published at `/<slug>/`.
- `logs/`: requested operational logs, published at `/logs/<slug>/`.

Every top-level Markdown post in both collections enters the build. Preview can
include unfinished work; `draft` metadata and future dates do not exclude posts.

## How to write and publish

After the one-time setup below, use this flow for new posts and revisions.

1. **Write.** Run `just write "Title"` from the repository root to create a
   meditation and open it in Neovim. Write and save your draft in
   `meditations/<slug>.md`. For an existing post, edit its Markdown file.
   For a log, ask the agent: “Write a log about [work], covering [scope].”
   The agent drafts it in `logs/` with the repository's ops-log skill.
2. **Ask for preparation.** Say “Prepare `meditations/<slug>.md` for review.”
   The agent reads the whole draft, reviews the intended reader, checks terms,
   sources, introductions, and related posts, and records the results. It asks
   about unclear meaning outside the article and requests permission before
   changing meditation prose. It then updates changed embeddings, builds the
   site, and starts a local preview. You do not need to request each stage.
3. **Read and revise.** Open the preview at <http://127.0.0.1:8765/>. Check the
   post and discuss any questions. Edit your meditation or request log changes,
   then ask the agent to prepare it again. The agent repeats affected reviews
   and rebuilds the preview. Saving a file does not start these steps.
4. **Approve a commit.** Say “Commit this version.” The agent runs the release
   checks, reviews the diff, and commits the post with its term records, review
   records, and embedding database changes. You can preview unfinished work;
   release checks require current reviews across the archive.
5. **Approve publication separately.** When ready, authorize publication and
   any required merge or push. The agent uses a clean `master` checkout, runs
   `just publish`, and checks the deployment and live page. Every post on that
   revision is included, so keep unrelated unfinished drafts off it.

The agent maintains `terms.json`, `.preparation.json`, and `blog.sqlite` as part
of preparation. In the build, it generates article pages, term pages, search,
the archive map, and the public database under `site/`. Review and approval are
human/agent work; running a build alone does not perform an editorial review.

For a preview without an agent, run `just preview` and open the address
above. After edits, run `just prepare` in another terminal, then refresh
the browser. Preview builds once; it does not watch files. Stop it with Ctrl-C.
See [Writing](docs/writing.md) for the complete review commands.

## Guides

- [Cooperation](docs/cooperation.md): ownership, draft agreement, commit and publication approval.
- [Writing](docs/writing.md): create, review, prepare, and preview a post.
- [Editorial policy](docs/editorial-policy.md): reader, terms, and references review.
- [Ops-log skill](.agents/skills/ops-log/SKILL.md): operational-log structure and prose.
- [Lab journal](docs/lab-journal.md): approved interface and interactions.
- [Build reference](docs/build.md): embeddings, data, rendering, tests, and deployment.

## Local setup

Install [just](https://just.systems/), Node.js 24+, and [uv](https://docs.astral.sh/uv/).
On macOS, install just with `brew install just`. For local authoring, create a
separate Python 3.12 environment and install the pinned dependencies:

```sh
uv venv --python 3.12 .venv-embed
uv pip install --python .venv-embed/bin/python -r requirements-embed.txt
npm ci
npx playwright install chromium
```

Skip environment creation if `.venv-embed` already exists. Leave any existing
`.venv` alone. `requirements-embed.txt` includes the build dependencies plus
inference libraries. For checks and builds alone, install `requirements.txt`
instead; no PyTorch or model download is needed.

Shell commands select `.venv-embed/bin/python`, then `.venv/bin/python`, then
`python3`. Set `PYTHON=/path/to/python` to override this choice. The first
embedding update downloads the pinned model into the local Hugging Face cache;
later updates can run offline. Keep `site/`, environments, `node_modules/`, and
model files local.

## Daily commands

Run `just` to list commands. Use these from the repository root or a subdirectory.
Follow the [writing guide](docs/writing.md) for review stages and the
[cooperation guide](docs/cooperation.md) for approvals.

| Task | Command |
| --- | --- |
| Start a meditation | `just write "Title"` |
| Check review status | `just status` |
| Prepare and preview | `just preview` |
| Preview on another port | `just preview --port 8766` |
| Prepare without serving | `just prepare` |
| Record a completed review | `just review ENTRY --stage reader --note "Review notes"` |
| Check editorial reviews | `just review-check` |
| Remove records for deleted posts | `just prune` |
| Run release checks | `just check` |
| Publish approved commits | `just publish` |

Open <http://127.0.0.1:8765/> for preview; stop with Ctrl-C. Preparation updates
embeddings and builds the site. Builds do not perform editorial reviews.
`just publish` requires clean `master`, runs release checks, then runs `git push`.
It does not stage files or create commits. For focused work, use `just embed` to
update embeddings only or `just build` to build without updating embeddings.
