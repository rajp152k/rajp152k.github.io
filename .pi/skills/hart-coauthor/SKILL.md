---
name: hart-coauthor
description: Co-author blog posts with Raj using the H.A.R.T. workflow. Use when outlining, drafting, editing, reviewing, annotating, researching, or improving collaboration habits for posts and pages in this repository.
---

# H.A.R.T. co-authoring

Read the repository `AGENTS.md` first. It is the constitution. This skill supplies the operating workflow.

## Select the mode

Infer the mode from Raj's request. If unclear, ask which pass is needed.

### Frame

1. Scan `content/posts/` and `content/pages/` for related material.
2. State the objective, reader payoff, and central claim.
3. Name core entities, relations, mechanisms, and assumptions.
4. Draft the reader path as an outline.
5. Identify diagram, equation, citation, annotation, and ontology opportunities.
6. Stop at structure when Raj has requested an outline pass.

### Draft

1. Treat the current outline and Raj's latest edits as authoritative.
2. Write the smallest coherent prose that connects the structure.
3. Use objective third person by default; use attributed first person under the voice rules in `AGENTS.md`.
4. Add H.A.R.T. annotations only when they add provenance, critique, history, useful humor, or a distinct editorial observation.
5. Ground mathematical and computer-science models in the mechanism being explained.
6. Prefer one focused diagram over several overlapping diagrams.

### Curate

1. Read Raj's edits before changing prose.
2. Identify which incentive, claim, term, or structure changed.
3. Preserve deletions. Do not restore superseded material.
4. Refine around Raj's wording without silently replacing his meaning.
5. Keep unresolved disagreement visible as a question, assumption, or attributed annotation.

### Review

Use [references/review.md](references/review.md).

### Compound

1. Suggest internal links that improve the reader path.
2. Identify reusable definitions and ontology terms.
3. Note where this post refines or contradicts earlier posts.
4. Suggest precise updates to older material.
5. Separate durable knowledge from implementation history.

### Improve H.A.R.T.

Run this only when Raj explicitly asks H.A.R.T. to improve, learn, update habits, or reflect on the collaboration.

Use [references/improvement.md](references/improvement.md). Review the current session and recent file changes, then update [references/learned-habits.md](references/learned-habits.md). Promote a habit into `AGENTS.md` only when it is durable, general across posts, and approved or clearly requested by Raj.

## Build verification

After modifying publishable content, run:

```bash
npm run blog:build:local
```

Use the dependency build when validating the pinned production SSG:

```bash
npm run blog:build
```
