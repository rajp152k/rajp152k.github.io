---
schema: 1
kind: post-review
entry: logs/2026-10-07-using-autolith
cycle: 1
state: curation
post_sha256: 0054f49ad70df541e9934ec66af9b8416b5cd88a116748ae41b7d6a3c82bd62c
terms:
  - id: T1
    revision: 1
    state: rejected
    action: add
    record: t1-vps
    decision: D1
    applied_at: null
    card:
      name: VPS
      definition: 'Virtual private server: a virtual machine with reserved resources on a shared physical server.'
      aliases: [virtual private server]
      passage: raj spent about half a day exploring Autolith on a Fedora VPS.
      introduction: 'After that sentence in Context, add: A virtual private server (VPS) is a virtual machine with reserved resources on a shared physical server.'
      use_scope: First eligible body use in Using Autolith and Orchestrating Autolith. Skip headings and all meditations. No other logs match.
  - id: T2
    revision: 2
    state: proposed
    action: add
    record: t2-lisp-image
    decision: null
    applied_at: null
    card:
      name: Lisp image
      definition: 'A Lisp environment with its loaded program code and runtime data. See [What is a Lisp image?](https://stackoverflow.com/questions/480083/what-is-a-lisp-image).'
      aliases: [Common Lisp image]
      passage: Autolith runs in a live Common Lisp image.
      introduction: 'After that sentence in Context, add: A Lisp image is an environment with its loaded program code and runtime data.'
      use_scope: First eligible body use in Using Autolith only. Do not match the bare word image or add uses to other posts.
  - id: T3
    revision: 1
    state: rejected
    action: add
    record: t3-fork
    decision: D3
    applied_at: null
    card:
      name: fork
      definition: A separate copy of a project's repository for independent development.
      aliases: []
      passage: raj created a fork of Autolith and a local development checkout.
      introduction: 'After that sentence in A separate development checkout, add: A fork is a separate copy of a project’s repository for independent development.'
      use_scope: First eligible body use in Using Autolith only. Exclude the fork mention in Project Outlines and all other meditations.
  - id: T4
    revision: 1
    state: rejected
    action: add
    record: t4-text-embedding
    decision: D4
    applied_at: null
    card:
      name: text embedding
      definition: A numerical vector that represents text so that texts can be compared.
      aliases: [embedding, embeddings, text embeddings]
      passage: raj used Autolith to prepare the blog's local embedding and build environment.
      introduction: 'After that sentence in Preparing the blog for local work, add: A text embedding is a numerical vector that represents text so that texts can be compared.'
      use_scope: First eligible body use in Using Autolith only. Blog Update [0] is evidence, not an annotation target. Exclude all meditations.
  - id: T5
    revision: 1
    state: rejected
    action: add
    record: t5-inference
    decision: D5
    applied_at: null
    card:
      name: inference
      definition: Running a trained machine-learning model to produce an output from an input.
      aliases: []
      passage: The setup uses a separate Python environment for inference and Node.js for the site assets.
      introduction: 'After that sentence in Preparing the blog for local work, add: Inference runs a trained machine-learning model to produce an output from an input.'
      use_scope: First eligible body use in Using Autolith and Orchestrating Autolith. Covers embedding and agent model execution, not logical deduction. Exclude all meditations.
  - id: T6
    revision: 1
    state: rejected
    action: add
    record: t6-front-matter
    decision: D6
    applied_at: null
    card:
      name: front matter
      definition: Metadata at the start of a document, before its main text.
      aliases: []
      passage: They use title and date front matter, an Abstract, Context, named sections, a Conclusion, and links to relevant past posts.
      introduction: 'After that sentence in Bringing the log rules into Autolith, add: Front matter is metadata at the start of a document, before its main text.'
      use_scope: First eligible body use in Using Autolith only. Metadata blocks are not term uses. No other archive body contains this phrase.
  - id: T7
    revision: 2
    state: proposed
    action: add
    record: t7-simplified-technical-english
    decision: null
    applied_at: null
    card:
      name: Simplified Technical English
      definition: 'A controlled form of English with writing rules and a dictionary for technical documentation. See [ASD-STE100, Issue 9 (January 2025)](https://asd-ste100.org/STE_downloads.html), the original specification (free copy by request).'
      aliases: []
      passage: New prose uses Simplified Technical English.
      introduction: 'After that sentence in Bringing the log rules into Autolith, add: Simplified Technical English is a controlled form of English with writing rules and a dictionary for technical documentation.'
      use_scope: First eligible body use of this exact name in Using Autolith only. Do not alias Simple Technical English or claim formal compliance.
links: []
decisions:
  - id: D1
    actor: raj
    action: reject
    scope: 'T1:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T1:r1
    reason: 'too simple - my audience knows this sort of stuff already - they''re techincal folks '
  - id: D7
    actor: raj
    action: request changes
    scope: 'T7:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T7:r1
    reason: 'should have a link to the original doc in the definition - asd-ste-100 one '
  - id: D6
    actor: raj
    action: reject
    scope: 'T6:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T6:r1
    reason: 'not jargon, too simple '
  - id: D2
    actor: raj
    action: request changes
    scope: 'T2:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T2:r1
    reason: 'have a link to this https://stackoverflow.com/questions/480083/what-is-a-lisp-image in the definition '
  - id: D3
    actor: raj
    action: reject
    scope: 'T3:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T3:r1
    reason: null
  - id: D4
    actor: raj
    action: reject
    scope: 'T4:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T4:r1
    reason: null
  - id: D5
    actor: raj
    action: reject
    scope: 'T5:r1: exact reviewed candidate and uses'
    evidence: review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json; user raj; item logs/2026-10-07-using-autolith:cycle-1:T5:r1
    reason: null
transitions: []
blockers: []
release:
  commit: null
  deployed_commit: null
  url: null
  verified_at: null
---

# Term review: Using Autolith so far

## Now

Raj rejected T1, T3, T4, T5, and T6 revision 1. He requested reference links
for T2 and T7. Only **T2:r2 and T7:r2** are proposed now. Their definitions add
the requested links; introductions, aliases, passages, and uses are unchanged.
No new registry or prose changes are approved or applied.

## Reader review

Read the whole log on 2026-11-21. It records an initial local Lisp and blog setup,
not completed side projects or a new Autolith feature. The intended reader knows
basic programming but may not know Lisp runtime concepts, model execution, or
the difference between a repository fork and an installed release.

The original seven proposals addressed those gaps and the post format.
Raj rejected five as recorded below; only two revised cards are pending. This is not a glossary
of every implementation detail. Domain evidence and its limits are in the
[frozen evidence notes](../../term-domain-evidence.md).

## Evidence and introductions

The card's Exact passage is an exact quote from the current post. It establishes
where the reader meets the term. Some passages do not explain the full meaning.
For each candidate, the Introduction field gives one exact proposed sentence.
After approval, insert it at that location and use that exact new sentence as
definition evidence in the registry. Do not quote it as existing archive prose.
The external references in the evidence notes support the proposed meanings.

All new records would use the default `annotation: first-term`. Mark only the
first eligible body occurrence per approved post. Repeated mentions remain
plain text. Existing links, headings, quotations, and code are excluded. These
are proposed use scopes, not a change to current matching or approval policy.

## T1: VPS

- Original proposal registry ID: `vps`; domain: server virtualization.
- Reader need: expand the acronym and explain the machine used for the setup.
- Current evidence: the Context sentence in the card. The AWS definition supplies
  the virtualization meaning that this sentence does not explain.
- Scope: this log, Context (one body `VPS`); Orchestrating Autolith, Context
  (`virtual private server` twice, mark the first only).
- Exclude the heading “A Lisp environment on the VPS”. Also exclude the `vps`
  mention in the meditation “the lisp machine”. No other archive matches.
- Introduction: use the exact sentence and placement in the card. It expands the
  acronym in this log. This proposal also covers the later log's matching use.

## T2: Lisp image

Revision 2 adds the requested [Stack Overflow reference](https://stackoverflow.com/questions/480083/what-is-a-lisp-image)
to the definition. Rainer Joswig explains saved functions, values, and symbols
and restarting from a saved image. Retrieved through web search; direct retrieval
returned HTTP 403. The short definition still describes the live environment.


- Original proposal registry ID: `lisp-image`; domain: Lisp runtime systems.
- Reader need: distinguish a running environment from a checkout or installation.
- Current evidence: “Autolith runs in a live Common Lisp image.” The later
  paragraph distinguishes private changes to the running image from source work.
- Domain support: SBCL's documented global process state and core-image saving.
  The definition does not promise that every resource can be saved and resumed.
- Scope: only this log's Context phrase `Common Lisp image`. No other archive
  body matches either exact spelling. Do not use the broad alias `image`.

## T3: fork

- Original proposal registry ID: `fork`; domain: source-code collaboration.
- Reader need: distinguish raj's independent repository from a local checkout,
  branch, and upstream project.
- Current evidence: the card sentence and “The checkout has raj's fork as its
  origin and the original project as its upstream.” GitHub documents the general
  meaning; the current archive only gives the concrete relationship.
- Scope: two body occurrences in this log's A separate development checkout
  paragraph; mark the first. The one mention in Project Outlines is excluded
  because it is a meditation. No other exact matches.

## T4: text embedding

- Original proposal registry ID: `text-embedding`; domain: machine-learning text representation.
- Reader need: connect the embedding updater to its stored numerical vectors.
- Current evidence: the card sentence and “During the setup checks, existing
  entries reused their stored vectors.”
- Definition evidence: [Blog Update [0], Math](../../../../meditations/embeddings.md)
  explains model-produced chunk vectors, normalization, and distances. It is
  evidence only; its prose and term state do not change.
- Scope: this log's Preparing the blog for local work section: two `embedding`
  occurrences in its opening paragraph and one in the paragraph beginning
  `Markdown is the source`; also the Review before commit and publication
  paragraph beginning `A request for a draft` (one). Mark the first only.
- Exclude all matching text in Blog Update [0] and Personal (Knowledge ->
  Epistemological) Management. No other log matches these spellings.

## T5: inference

- Original proposal registry ID: `inference`; domain: machine learning.
- Reader need: distinguish model execution from reusing saved vectors, and from
  keeping an agent's state without running its model.
- Current evidence: the card sentence and the setup-check paragraph about no new
  inference. The AWS deployment guide explains the general model-use meaning.
- Scope: two body occurrences in this log (Preparing the blog for local work);
  two in Orchestrating Autolith (Separate contexts and one task owner; Make work
  resumable across machines). Mark the first eligible body occurrence per log.
- Exclude the three occurrences in Blog Update [0]. No other archive matches.
  The second log's `inference budget` means a budget for model execution, not a
  new meaning or an approval for a remote system.

## T6: front matter

- Original proposal registry ID: `front-matter`; domain: document and static-site formats.
- Reader need: distinguish the title/date metadata block from the article body.
- Current evidence: the card sentence, plus title/date blocks in all three logs.
  Jekyll documents the established term; this blog does not use Jekyll.
- Scope: one body occurrence, in this log only. The first log describes the same
  placement without this phrase; do not introduce a new use there.

## T7: Simplified Technical English

Revision 2 adds [ASD-STE100 Issue 9, January 2025](https://asd-ste100.org/STE_downloads.html)
to the definition. The official page offers a free copy of the original
specification by request. No direct specification PDF was retrieved.


- Original proposal registry ID: `simplified-technical-english`; domain: technical writing.
- Reader need: distinguish the named controlled language from a general request
  for short or simple prose.
- Current evidence: the card sentence and “Short sentences must still contain
  the material decisions and results.” The ASD source establishes the writing
  rules and controlled dictionary.
- Scope: one exact-name body occurrence, in this log only. `Simple Technical
  English` in Shared Autolith settings is different wording. It is not an alias
  in this proposal; leave it unchanged and raise any correction separately.
- A term card does not establish compliance with ASD-STE100.

## Other screened terms

Do not restore Autolith, Lem, Emacs, Fedora, Vim, Python, Node.js, Markdown,
SQLite, Stow, OMP, or ops-log merely because they are named products, languages,
formats, or local skill labels. This batch explains the concepts necessary to
read the account. `origin` and `upstream` are useful Git vocabulary, but the
existing sentence already explains which repository plays each role. `checkout`,
`init file`, `dotfiles`, `cache`, and `runtime state` are not separate cards in
this batch. Reconsider them if raj identifies a reader gap. This is screening by
AL, not a rejection or deferral decision by raj.

## Archive scope and decisions

Scanned all three logs and all six meditations for every proposed spelling.
Meditation matches are listed above only to prevent accidental annotation.
No new use of HMAS occurs. Its applied T1:r2 and approval provenance in the
orchestration review are unchanged.

Raj rejected VPS and inference, including their proposed uses in the later log. No post-link changes are
proposed. Existing archive review receipts remain stale; this preparation is not
a completed references review, post commit approval, or publication approval.

## Imported all-log decisions

Source: [cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json](../../../../review-imports/cdb5159a86f2dc71b13c-56ec7e34f4daeb94.json).
`changed_sources` is empty. These are raj's final responses to revision 1.
Revision requests do not approve revision 2. The frozen import retains each
original card and its source snapshots.

- D1, T1:r1: **reject**. Raj: "too simple - my audience knows this sort of stuff already - they're techincal folks "
- D7, T7:r1: **request changes**. Raj: "should have a link to the original doc in the definition - asd-ste-100 one "
- D6, T6:r1: **reject**. Raj: "not jargon, too simple "
- D2, T2:r1: **request changes**. Raj: "have a link to this https://stackoverflow.com/questions/480083/what-is-a-lisp-image in the definition "
- D3, T3:r1: **reject**. No reason supplied.
- D4, T4:r1: **reject**. No reason supplied.
- D5, T5:r1: **reject**. No reason supplied.
