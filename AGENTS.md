# AGENTS.md

Guidance for writing and editing posts in this repository.

## Voice and structure

- Work in outlines first. Do not start with prose; start with the knowledge structure.
- Be concise: prefer short sections, direct claims, and concrete examples.
- Write with a mathematical and computer-science mindset: define terms, expose structure, model mechanisms, and state invariants.
- Treat posts as cumulative knowledge and engineering experience, not as opinion logs.
- The objective is to become a better presenter of information, knowledge, and wisdom; not merely to document words.
- Prefer observations, models, measurements, implementations, and falsifiable claims over taste or commentary.
- Write for clarity before completeness; add depth only where it changes understanding.
- Prefer precise wording over rhetorical flourish.
- Use a direct voice. Avoid stylistic elevation, ambiguity, and ornamental phrasing.
- Do not use rhetorical contrast patterns such as “not only … but also …”, “the point is not … but …”, or “not X, rather Y”. State the positive claim directly.
- Keep conceptual language plain. Do not make an idea sound deeper by changing the style around it.
- Keep introductions short. Get to the core idea quickly.
- End with practical implications, open questions, or a compact summary.

## Explanatory style

- Give every post a higher-order structure: objective, context, model, mechanism, example, implications, and links to related knowledge.
- Make the reader's path explicit. Each section should answer why it exists and what it unlocks next.
- Use Mermaid diagrams extensively when they can clarify structure, flow, trade-offs, causality, state machines, timelines, dependencies, or feedback loops.
- Always look for diagram opportunities before finalizing a post.
- Prefer Mermaid over external images. Do not add external image dependencies unless explicitly requested.
- When useful, include the mathematical foundations of the concept being discussed:
  - define variables and assumptions;
  - show the minimal model, equation, recurrence, graph, type, grammar, or algorithm;
  - identify invariants, complexity, constraints, and failure modes;
  - explain what the model captures and what it ignores;
  - avoid unnecessary formalism.
- Use assistive diagrams, charts, tables, and mathematical equations whenever they improve compression, comparison, or recall.
- When making foundational claims, cite fundamental literature wherever possible: papers, books, specifications, standards, primary documentation, or historically important implementations.
- Prefer citations that anchor concepts, not citations used as decoration.
- When discussing software, prefer concrete artifacts: types, interfaces, state machines, data flow, build graphs, protocols, tests, and source-level behavior.

## Cross-linking, continuity, and compounding

- Optimize for a higher-order incentive: each post should increase the future value of the whole knowledge base.
- Before writing or editing a post, scan `content/posts/` for related past posts.
- Suggest internal links to relevant posts where they strengthen the reader's path.
- When a new post changes, contradicts, refines, or depends on an older post, mention that relationship explicitly.
- Treat the site as a growing knowledge base: reuse definitions, refine models, and avoid re-explaining concepts inconsistently.
- Watch for philosophical fallacies or weak reasoning both within the current post and across related posts. Flag them and suggest updates to older posts when needed.

## Reasoning standards

- Distinguish observation, inference, speculation, prescription, and implementation detail.
- Do not document opinions as endpoints. If an opinion appears, convert it into assumptions, criteria, trade-offs, or a testable claim.
- Identify hidden assumptions, false dichotomies, category errors, circular reasoning, motte-and-bailey shifts, equivocation, survivorship bias, and overgeneralization.
- Prefer charitable revisions over adversarial critique.
- If a claim is broad, either narrow it or support it.

## Ontologies and annotations

- Start documenting ontologies over time: core entities, relationships, constraints, processes, and vocabularies that recur across posts.
- When a post introduces durable terminology, define it clearly and consider whether it belongs in a future ontology note or index.
- Prefer ontology entries that are operational: include examples, non-examples, relationships, and how the concept is used in engineering work.
- Keep ontologies revisable. If a later post improves a concept, suggest updating the older definition.
- Use annotations for side knowledge: citations, historical notes, definitions, caveats, related mathematical ideas, and links to prior posts.
- Add annotation notes when a claim would benefit from a reference to fundamental literature.
- Use annotations to keep the main text concise while preserving rigor.

## Writing workflow

1. Draft an outline before prose.
2. State the objective and reader payoff.
3. Identify the core entities, relationships, and mechanisms.
4. Decide where diagrams, charts, equations, examples, citations, annotations, or code make the structure clearer.
5. Write the smallest prose needed to connect the structure.
6. Review for compounding value: links, ontology candidates, reusable definitions, and future engineering lessons.

## Collaboration workflow

- Write and edit in alternation.
- The assistant makes a pass; the author then edits, comments, corrects incentives, and adjusts direction.
- Later assistant passes should refine the author's changes instead of overwriting them.
- Treat author comments as source material for the next structural pass.
- Preserve the evolving intent across passes.

## Post format

Posts live under:

```txt
content/posts/<slug>/
  post.json
  canvas.md
```

Use `canvas.md` for the post body. Keep metadata in `post.json` consistent with the title and slug.

## Pre-publication checklist

- Was an outline created before prose?
- Is the higher-order purpose of the post clear?
- Is the central claim stated plainly?
- Are key terms defined precisely?
- Can a Mermaid diagram, chart, or table make the concept easier to understand?
- Is there a useful mathematical, algorithmic, or CS model to include?
- Are equations useful for compression or precision?
- Are citations to fundamental literature included wherever possible?
- Are annotations used for citations, caveats, side definitions, or historical context?
- Are invariants, constraints, complexity, or failure modes relevant?
- Are related past posts linked?
- Does this post refine or add to an ontology?
- Are any fallacies, contradictions, unsupported claims, or unexamined opinions present?
- Are external images avoided?
- Is the post concise?
