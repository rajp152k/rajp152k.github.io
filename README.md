# meditations of yet another raj

Source for <https://yetanotherraj.com/>. Markdown is the source of truth:

- `meditations/`: raj's writing, published at `/<slug>/`.
- `logs/`: requested operational logs, published at `/logs/<slug>/`.

Every top-level Markdown post in both collections enters the build. Preview can
include unfinished work; `draft` metadata and future dates do not exclude posts.

## Guides

- [Cooperation](docs/cooperation.md): ownership, draft agreement, commit and publication approval.
- [Writing](docs/writing.md): create, review, prepare, and preview a post.
- [Editorial policy](docs/editorial-policy.md): reader, terms, and references review.
- [Ops-log skill](.agents/skills/ops-log/SKILL.md): operational-log structure and prose.
- [Lab journal](docs/lab-journal.md): approved interface and interactions.
- [Build reference](docs/build.md): embeddings, data, rendering, tests, and deployment.

## Local setup

Install Node.js 24+ and [uv](https://docs.astral.sh/uv/). For local authoring,
create a separate Python 3.12 environment and install the pinned dependencies:

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

Run these from the repository root. Follow the [writing guide](docs/writing.md)
for review stages and the [cooperation guide](docs/cooperation.md) for approvals.

| Task | Command |
| --- | --- |
| Start a meditation | `./write.sh "Title"` |
| Check review status | `./prepare.sh status` |
| Prepare and preview | `./prepare.sh preview` |
| Prepare without serving | `./prepare.sh build` |
| Run release checks | `sh scripts/verify_preparation.sh` |
| Publish approved commits | `./publish.sh` |

Open <http://127.0.0.1:8765/> for preview; stop with Ctrl-C. Preparation updates
embeddings and builds the site. Builds do not perform editorial reviews.
`publish.sh` requires clean `master`, runs release checks, then runs `git push`.
It does not stage files or create commits.
