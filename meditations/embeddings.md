---
title: Blog Update [0]
date: 2026-10-03
---

Previously, the blog was only a collection of posts in a table.  

I've setup a pipeline to sort of visualize semantics now: 
- first generate embeddings based on a change hash (post + embedding model tag) i.e. recompute only for recent delta
- store those in sqlite
- compute principal components and build the map(an svg).


## Math

Each post's title and visible Markdown text are split into non-overlapping chunks of at most 512 whitespace-delimited words and 2,048 model tokens (including special tokens), without truncation. The pinned [gte-modernbert-base](https://huggingface.co/Alibaba-NLP/gte-modernbert-base) model and its own pooling produce a 768-dimensional vector $e_{ic}$ for chunk $c$ of post $i$.

Normalize each chunk, average by its actual input-token count $t_{ic}$, then normalize the post:

$$
u_{ic} = \frac{e_{ic}}{\lVert e_{ic}\rVert_2},
\qquad m_i = \frac{\sum_c t_{ic}u_{ic}}{\sum_c t_{ic}},
\qquad v_i = \frac{m_i}{\lVert m_i\rVert_2}.
$$

Token weighting prevents a short final chunk from counting as much as a full chunk. One vector per post necessarily compresses its mixture of topics. Unit normalization relates Euclidean distance to cosine similarity:

$$
\lVert v_i-v_j\rVert_2^2 = 2(1-v_i^\top v_j).
$$

For $n\ge1$ posts, stack $v_i^\top$ as rows of $X\in\mathbb{R}^{n\times768}$, ordered by slug. Store vectors as float32; compute centered PCA in float64, subtracting the first row before the mean to preserve small differences:

$$
\mu = \frac{1}{n}\sum_i v_i,
\qquad C = X-\mathbf{1}\mu^\top,
\qquad C = U\Sigma V^\top.
$$

Use exact reduced SVD, with no per-dimension standardization or whitening. For $k=\min(2,n-1)$, the map coordinates are $Y=C V_k=U_k\Sigma_k$; missing coordinates are zero. Fix each component's sign so its largest-magnitude loading is positive. Use the same display scale on both axes.

The retained-variance fraction is:

$$
R = \frac{\sum_{r=1}^{k}\sigma_r^2}{\sum_r\sigma_r^2}.
$$

The heading displays $100R$ rounded to a whole percent. Three centered vectors span at most two dimensions, so two components retain all their variance. This measures projection fidelity, not semantic accuracy; with more posts, 2D distances can lose information. With no variation, the ratio is undefined and points coincide; an empty archive has no points. Refit PCA on each build, so positions can change.

## Usage Flow

1. Create a post with `./write.sh "Title"` and edit its Markdown in `meditations/`.
2. When ready, run `.venv-embed/bin/python scripts/embed.py`. SHA-256 keys cover the prepared title/body and complete pinned embedding specification. Only missing/changed vectors require inference; model/policy changes invalidate the archive. Date corrections, unchanged-content renames, and deletions synchronize without inference. Metadata and vectors are committed atomically to `blog.sqlite`.
3. Optionally preview: `.venv-embed/bin/python scripts/publish.py` builds `site/`; `.venv-embed/bin/python -m http.server 8765 --directory site` serves it locally.
4. Run `./publish.sh` on `master`: it checks freshness, then stages, commits, and pushes the posts and working database. Styling-only changes need no embedding update.
5. GitHub CI installs only publishing dependencies, checks committed embedding freshness, runs regressions, refits PCA, and builds HTML/SVG plus a fresh public SQLite snapshot. It uploads `site/` and deploys GitHub Pages to `yetanotherraj.com`. CI never runs embedding inference; stale state blocks deployment. Pull requests validate/build but do not deploy.
