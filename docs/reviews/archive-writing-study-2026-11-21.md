---
kind: writing-taste-study
state: proposed
source_repository: https://github.com/rajp152k/23-26_archive
source_commit: 94920842829925836cbc08effa16255ac293832a
reviewed: 2026-11-21
---

# Learning from the old archive

## Scope and method

Raj asked for a deep reading before changing writing policy. This study proposes principles. It does not change policy or revise the logs. The [11 current memos](log-memo-feedback-2026-11-21.md) take precedence over historical habits and these interpretations.

The source is [rajp152k/23-26_archive](https://github.com/rajp152k/23-26_archive), pinned at `94920842829925836cbc08effa16255ac293832a`. AL retrieved the named GitHub page and cloned the repository for read-only inspection. No archive code, build, configuration, or dependencies were run. Its one commit does not establish individual revision histories.

The [complete inventory](archive-writing-inventory-2026-11-21.md) lists paths, titles, dates, and character counts for all 101 tracked Markdown content files: 90 post files and 11 ancillary pages. Full bodies, including code and quotations, were supplied to eight bounded RLM analysis frames, not title-only samples. AL also read representative sources directly and checked the quotations used here against the pinned texts.

| Front-matter year | Post files |
| --- | --- |
| 2023 | 25 |
| 2024 | 28 |
| 2025 | 28 |
| 2026 | 9 |

The dated posts span 2023-07-16 through 2026-06-09. These are metadata dates, not proof of first composition. [Reading an Author][reading] preserves a 2022 entry inside a 2023 post and then criticizes it. The 11 ancillary pages have no `date:` field. Some contain dated entries or hexadecimal day counts; they were not assigned invented publication dates. The input totals 282,220 characters, including metadata, code, and borrowed text. This is not an authored-prose word count.

`content/post/aefraisk.md` has invalid UTF-8. Its analysis copy used a Latin-1 fallback. The original bytes were not changed. This limits claims about exact non-ASCII spelling, not coverage of its argument.

### Attribution and limits

Repository membership does not prove that every sentence is Raj's prose:

- [I have a Writing Tutor now ...][tutor] explicitly alternates Raj and ChatGPT. The model's praise, headings, critiques, and proposed rewrite are not Raj's voice. The embedded essay also appears separately; it is not a second independent example.
- [Prompt Crafting Distilled][prompt] mixes first-person exposition, custom instructions, and a labelled ChatGPT response. Separate those sources. Instructions for a model interface do not define article style.
- [Assume Competence][competence] quotes an LLM instruction. Its opening account records a workflow experiment. The quoted instruction is not an instruction for this study or a rule for every audience.
- Both [OSDev introductions][os0] [and study summaries][os1] describe "The creator, Raj" and summarize videos with timestamps. `content/post/pragmatic-opacity.md` uses a similar third-person synopsis. Their prose authorship is not stated. Treat these three summaries as uncertain evidence, not models for repeated third-person references, generic headings, or recap conclusions. Their appearance does not prove AI generation.
- [ThyForce][thyforce] opens with a borrowed Star Wars quotation. Use its engineering explanation as evidence, not the quotation's voice. Apply the same distinction to book excerpts, source notes, code, and attributed quotations elsewhere.
- Shelves, contact pages, video indexes, and the work corpus have reference functions. Sparse video posts give little evidence about sentence rhythm. The `now` and `scroll` pages are logs, not finished essays.

All content bodies were supplied. Linked videos, podcasts, books, external notes, and image contents were not reviewed. This is a source-text study, not a visual review. It does not verify technical, medical, or autobiographical claims or infer personality. Unmarked first-person passages are candidate authored prose, not independently authenticated authorship.

Additional attribution boundaries identified in the full-body analysis:

| Exact archive path | Boundary for style evidence |
| --- | --- |
| `content/post/PICC.md` | Opening epigraph is attributed to Edison; distinguish it from the method essay. |
| `content/post/most-important-book.md` | Opening epigraph is attributed to Socrates. The numbered taxonomy has unspecified provenance. Do not infer generation from a change of register. |
| `content/post/my-emacs-config-0x213B.md` | Org tagline, an existing adage, and code are distinct from commentary. Code authorship is not verified. |
| `content/post/nootropics-init.md` | Opening definition-style quotation is not attributed. Its source is unknown. |
| `content/post/nvim-tmux-docker-python.md` | Definition-style GNU Core Utilities wording has unspecified provenance; distinguish it from the workflow account. |
| `content/post/polymathy.md` | Preserved self-authored material and later commentary surround a definition and quoted sayings. These are not one uniform source. |
| `content/post/programming-pilgrimages.md` | Opening linked quotation is attributed to Linus. |
| `content/post/stuck-island.md` | A saying is presented as heavily paraphrased and of uncertain origin. |
| `content/post/writing setup.md` | Epictetus epigraph precedes first-person reflection. |
| `content/post/practical-nlp-C1-5.md` | An embedded maxim has no established attribution in the report. |
| `content/open-source/index.md` | Attributed saying appears in a link stub. |

These are attribution labels in the texts, not verified historical claims about who first said something. Blockquote markup alone is not external attribution: the about page, `i-know-not` page, `personal-research.md`, and `phrasal-outlines.md` include material presented as the writer's own. `aefraisk.md` and `reading-an-author.md` reproduce earlier self-authored work; retain the older and later voices as separate dated layers. `whitelisting-git.md` acknowledges Stack Overflow for code; that is not evidence of uncertain prose authorship.

### Analysis provenance

Each frame received complete source records with paths and closing markers. The inventory and batch boundaries were generated from the pinned Git tree. Seven batches contain 13 files; the last contains 10.

| Batch | Files supplied / paths enumerated | Persisted trace | Last source |
| --- | --- | --- | --- |
| 1 | 13 / 13 | `G1CcXLs` | `content/post/CLTS/CLTS-0.1.md` |
| 2 | 13 / 13 | `766KaT5` | `content/post/achievements.md` |
| 3 | 13 / 13 | `c59EJAq` | `content/post/diabetic.md` |
| 4 | 13 / 13 | `S6s2a9J` | `content/post/jargon-ai.md` |
| 5 | 13 / 13 | `m2gahzF` | `content/post/nootropics-init.md` |
| 6 | 13 / 13 | `d1rS84w` | `content/post/programming-pilgrimages.md` |
| 7 | 13 / 13 | `G1332Rx` | `content/post/the-home-row.md` |
| 8 | 10 / 10 | `p1qE63P` | `content/search/_index.md` |

Batch 7 incorrectly says "15" in its opening coverage sentence, but enumerates 13 paths and reaches the correct final source. Use 13, checked against the input, not the erroneous total of 103 implied by adding report claims. The eight reports enumerate 101 files with no identified missing body. This establishes supplied and reported coverage, not proof of error-free interpretation of every sentence.

Bounded cross-batch synthesis: `inference:i6EZqQc`. Complete batch outputs are retained outside conversation context in `context:013298dfc9feed1754a9039ae0b17c82473c43279eb095d530b488eba04120ee`. An earlier root synthesis, `inference:y32d6mu`, exhausted its call allowance after a rejected nested model route and slicing errors. It did not produce a validated result and was not used as evidence. No model switch or source changes were needed; the bounded direct synthesis completed.

Explicit drafts, including `generic-polyglotism.md`, `kde-stumpwm.md`, and `tiling-wm-kde.md`, receive less weight as finished-style examples. `content/search/_index.md` has no substantive body. `content/post/how-to-ditch-the-mouse.md` is video-only, and `alias-vi.md` has an image and very little prose. They are included in coverage without being counted as substantive authored essays. No exact count of authenticated authored essays is claimed.

Narrow accuracy and scope review: `inference:J73Ajiq`, against the eight reports and the complete current feedback. It found no material issue. Direct checks matched all 101 source files to their pinned Git blobs, reconciled inventory paths/titles/dates/character counts and all batch boundaries, verified representative quotations, and checked local document links and pinned source references. No browser, build, or broad suite was run.

## Findings

### 1. Titles express an angle, with several valid forms

**Skim, Devour, Feynmanize** compresses a method into three verbs; its body calls the title a mnemonic. **Bells & Whistles** frames an experiment in removing familiar tools. **Blub in the Unix Philosophy** names a change in understanding. **on Naming your Projects** is conversational. **I turned 0x2222 today** uses a personal technical reference that the body explains.

Counterexamples matter: **Common Lisp : The Series - 0.1 : Representing Programs**, **Setting up snapper on Arch**, and book-name reviews serve teaching and retrieval. There is no single requirement for a joke, lowercase title, or cryptic name. In [on Naming your Projects][names], "The more cryptic the better" concerns project names during incubation, not all article titles.

Find the thought or experiment worth naming. Choose a natural phrase, useful reference, or descriptive title according to the piece. The current suggestions "meditating on logs", "autolith'ing", and "on autolith" are examples, not final selections.

### 2. A current practice or problem gives the piece its reason

[Bells & Whistles][bells] begins "I've started spending some time per day" and explains why. [Flexible SWE Experiments][flexible] starts from repeated experimentation before introducing Polylith. [Skim, Devour, Feynmanize][paper] begins with the limit of project-led study. These openings establish a local reason, without a generic history of computing.

Reflection can work this way too. [The Definitive Guide to Books][books] connects reading history, writing, and a particular commitment. Conversely, the short Common Lisp lesson begins with its subject rather than autobiography. The principle is a reason for the piece, not a mandatory personal anecdote.

An archive-layout fact belongs in a log if it helps readers understand why the work matters. The memo does not require deleting implementation facts as a class.

### 3. Confidence and visible revision coexist

[Bells & Whistles][bells] offers a three-part computing model, then says "I would recommend you do not accept that categorization". A broader extension is "a highly experimental thought as of now". [Blub in the Unix Philosophy][unix] describes a changed view, limits a proposed application, and leaves further investigation open.

There are strong recommendations too. The useful pattern is not to hedge every claim. Distinguish observation, interpretation, and planned experiment. In [Reading an Author][reading], later commentary questions earlier ornate phrasing: "yeah, that seems a little overboard now". Keeping that disagreement visible is better evidence of an evolving voice than selecting one old phrase as permanent taste.

A useful technical distinction appears even in the KDE draft: architectural dissatisfaction and operational success are separate claims. It says the setup is not declarative, then "It does work now though" (`content/post/tiling-wm-kde.md`, explicitly a draft). In the next log pass, preserve that distinction between a working result and an unresolved design limitation. More polished success language would lose information.

The archive also contains explicit self-correction about public writing itself. [Here we go again...][setup] says earlier private coinages made the writing less accessible. [Talking About What You Do][talking] interrupts another declaration of plans with "There I go again". Compare this with the earlier book essay's account of public commitments. These are changing judgments, not one permanent preference for announcing plans.

### 4. Shared laboratory voice is a current direction

Clearly first-person archive pieces often use "I". They say what the writer chose, tried, learned, or abandoned. That differs from a narrator repeatedly reporting what "Raj" did. The uncertain OSDev summaries should not determine the house voice.

The current request for "more of a we vibe" supplies the direction for agent-written laboratory logs. It need not be justified by a historical majority of "we". Preserve direct involvement and accountable observations. Name the individual when factual responsibility matters. Do not convert meditations into collective prose.

### 5. Rhythm follows the thought, not a sentence quota

Short sentences often provide a turn or result. Longer sentences carry qualifications and connections. [Flexible SWE Experiments][flexible] places "I haven't had an un-intuitive refactor so far.." after fuller paragraphs about structure. [Knights, Mercenaries and Wizards][minimal] combines short workstation statements with a long, nested account of configuration choices. That permits latitude; it does not make difficult nesting a model to copy.

[Converging Expression][expression] values "the distilled value of the transmission" over exhaustive description. It also admits getting abstract too quickly. Density is not automatically precision. Physical source line breaks are not sentence or paragraph boundaries.

Remove the ASD-STE100 prose constraint when the policy change is authorized. Use coherent thoughts and varied rhythm. Do not replace it with another numeric limit or require long sentences to prove that the old rule is gone.

### 6. Structure depends on genre and scale

There are substantial headings in tutorials and method essays, and connected paragraphs without section hierarchies in short reflections. [ThyForce][thyforce] uses an abstract, design reasons, and a video pointer. [Flexible SWE Experiments][flexible] develops its point without small titled sections. The repeated headings in chronological pages serve a different purpose.

The current objection to "too many short sections" does not require merging tutorials into a wall of prose. Give a section enough substance to form a useful unit of argument, procedure, or reference.

### 7. Technical detail earns space through use

The archive ranges from code-heavy Emacs configuration and Python workflow posts to command notes, book reviews, and reflections. Detailed tutorials and narrow result notes both have a place. In [Knights, Mercenaries and Wizards][minimal], concrete tools identify two work environments and support the point about thinking. In [ThyForce][thyforce], language and architecture choices connect to iteration speed and composition.

Keep commands, conditions, interfaces, and results when they explain or reproduce the experiment. Do not include every captured state merely because it is available. A reflection need not become a setup guide.

### 8. Humour often comes from the subject or self-commentary

The naming post compares fictional mentors before a supervillain aside. The book essay interrupts its expanding sea metaphor and mocks a generic call to action. The milestone title uses hexadecimal age. These are local devices, not a separate layer of stock jokes.

[Teh worth of a workd][free] is an explicit no-backspace exercise. Its typos and "This is enough lexical crime" ending belong to that experiment. They do not justify adding errors to ordinary logs. Casual contractions, parentheses, and unusual vocabulary vary across pieces.

Leave room for a fitting aside. Do not manufacture slang, misspellings, hex labels, metaphors, or jokes as a style recipe.

### 9. Competent readers still need the experiment's context

[Assume Competence][competence] records an experiment with concise, jargon-rich LLM outlines. It argues against unwanted basic explanation in that workflow, not against all explanation. The introductory Common Lisp series and reviews that distinguish revision from first-time learning are counterexamples to a universal expert-only audience.

The self-criticism in [Converging Expression][expression] and [Reading an Author][reading] also warns against unnecessary abstraction. Use the technical term that carries meaning and supply the local context needed to follow it. Reader skill does not waive term or link approval gates.

### 10. Endings may stop at a result or an honest next step

[Blub in the Unix Philosophy][unix] ends its main discussion "Will explore further for a while..". [Skim, Devour, Feynmanize][paper] connects its method to a laboratory aim. [Flexible SWE Experiments][flexible] ends with a finding about structure in throwaway software. None requires repeating the whole piece.

There are conclusions with explicit takeaways, including [Reading an Author][reading]. Tutorial endings can point to resources. The present memo rejects a forced ending that adds nothing. It does not ban conclusions, future work, or a final implication.

### 11. Links and diagrams serve an act of understanding

Links often identify an actual project, book, source, repository, or earlier thought. They are not just a generic reading list. The requested `.files` link is a concrete missing source connection; it belongs in the eventual edit scope, not this study.

A source-text check found Markdown image syntax in five files and a Mermaid mention in [PICC][picc]. The latter discusses charts and graphs as tools for thought; it does not establish a history of rendered Mermaid diagrams. Other markup can also refer to images. Image contents were not inspected, so this study makes no claim about preferred diagram appearance.

The current memo is stronger evidence: add diagrams when they help comprehension, without forcing them. Its computer/topology/human-loop example belongs to the second log. Start from the relationship to explain, then select a suitable format. The archive does not select a mathematical visualization system or require a diagram in every log.

### 12. Several modes persist across time

The early archive includes expansive method essays, book reflections, configuration walkthroughs, and teaching series. Later material includes many compact observations, workflow changes, video pointers, and research notes. [Quick Musings][quick] explicitly proposes short public records of early technical thoughts and a quicker path to publication.

The 2026 pieces remain varied: a Snapper setup note, ThyForce's project abstract, Flexible SWE Experiments' broader method, and Knights, Mercenaries and Wizards' reflection on tooling. This is a change in the mix of forms, not proof of linear progress toward one ideal length or formality. Republishing, linked media, and uncertain summaries limit simple chronological claims.

Use the strengths of a research note without copying scratch-log fragmentation or an early configuration tutorial's length.

## Comparison with all 11 current memos

| Memo | Direct feedback | Proposed response |
| --- | --- | --- |
| First log 1 | Unhelpful archive fact; suggests "meditating on logs" | Start from reader purpose; explore the title, do not treat it as selected. |
| First log 2 | Repeated "raj"; robotic memoir; wants laboratory journal | Use involved reporting, not third-person biography. |
| First log 3 | Too many short sentences; remove ASD-STE100 constraint | Vary rhythm without imposing long sentences. |
| First log 4 | Too many short sections | Match structure to substance; preserve useful tutorial headings. |
| First log 5 | More "we", less separation of raj and agent | Follow current direction while preserving factual attribution. |
| First log 6 | Forced conclusion; review should develop native style | Remove redundancy in the prose pass; refine through review. |
| Second log 1 | Apply first log's general notes | Reuse principles, not its specific cuts or proposed title. |
| Second log 2 | Dry title; try "autolith'ing" or "on autolith"; read old titles | Use the range in the inventory, not one compulsory formula. |
| Second log 3 | Useful unforced diagrams; topology and human-loop example | Design the explanation before choosing a diagram system. |
| Second log 4 | Link `.files` | Concrete source-link edit, not a requirement for more links everywhere. |
| Third log 1 | Apply general feedback; refine and review again | Another review is required after revision. |

## Proposed general writing policy

This is a proposal for approval, not an applied policy change.

1. Write agent-authored logs as a shared laboratory journal. Use "we" where accurate; name an individual when the distinction matters.
2. Begin with the question, friction, experiment, or result that makes the piece worth reading. Connect technical facts to that purpose.
3. Remove the ASD-STE100 prose constraint. Use natural, varied sentences and paragraphs. Prefer precision over exhaustive explanation or ornamental density.
4. Choose a title that names the angle naturally. Use humour or a reference when it fits, and a descriptive title when it serves the reader better.
5. Organize by meaningful units. Use headings, lists, code, and detail to help readers follow or reproduce the work.
6. Assume a capable reader, but supply necessary local context. Keep observations, interpretations, limits, and next tests distinct.
7. Keep links and diagrams useful and specific. Choose a format for the relationship to explain; do not force a diagram or a particular system.
8. End when the piece has done its work. Add a conclusion only if it adds a result, implication, or useful next step. Refine style through actual review.

The next task should separate policy changes from concrete revisions of the three logs. Suggested titles, diagram placement, and material to combine need editorial choices. Meditations, prior term/link approvals, and publication gates are outside this proposal.

## Source references

The inventory links every source at the pinned commit. References below select the main evidence and counterexamples. Paths refer to the old archive, not renamed files in the current blog.

[expression]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/conciser.md
[free]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/free-writing.md
[competence]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/jargon-ai.md
[minimal]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/minimalism.md
[flexible]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/Flexible-SWE-Experiments.md
[reading]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/reading-an-author.md
[paper]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/paper-read-strat.md
[books]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/the-definitive-guide-to-books.md
[bells]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/Bells-and-Whistles.md
[unix]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/Unixier-Unix.md
[names]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/good-names.md
[tutor]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/better-writer.md
[prompt]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/dense-guide-prompt-engineering.md
[os0]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/osdev/0x0.md
[os1]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/osdev/0x1.md
[thyforce]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/ThyForce.md
[quick]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/quickies.md
[picc]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/PICC.md
[setup]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/writing%20setup.md
[talking]: https://github.com/rajp152k/23-26_archive/blob/94920842829925836cbc08effa16255ac293832a/content/post/talking-about-what-you-do.md
