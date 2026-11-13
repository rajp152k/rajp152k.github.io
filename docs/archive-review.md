# Archive reader review

Reviewed on 2026-11-12 against archive prose at `181006a`: six meditations and three logs. A second reviewer read every entry in full, including code samples and references, and checked the definitions against `docs/editorial-policy.md`. The preparation receipts identify the reviewed inputs. This is a private editorial record. Review changed entries again through the preparation process.

## Selection decisions

Add a term when a short, context-specific definition resolves a reader's likely gap and an exact source passage supports it. Recurrence is useful evidence, not a requirement. A named tool can need context on its first appearance. Familiar words, incidental names, and passages that already explain their central idea do not need automatic glossary entries.

The registry has nine terms after this review. Four are new: concept tree, PCA, Lem, and Simplified Technical English. Each has exact archive evidence and a chosen introductory post. Related-reading choices and their reasons are recorded below and in `.preparation.json`. A matching mention is not a recommendation.

## Existing definitions

- **Orch:** retain. The November log explicitly assigns cross-project priorities and requests for raj's attention to this agent. Do not infer that it already controls a working remote cluster.
- **Autolith:** retain the definition and October setup log as introduction. That log explains conversation, code, files, processes, and the live Common Lisp image. Remove the Lisp-machine meditation from definition evidence: its product mention supports navigation, not the definition. The meditation still receives a normal term reference.
- **HMAS:** retain. The November log explicitly expands the name and describes layers. The later external-link check confirmed the taxonomy's title, author, and abstract. It did not audit the full paper's claims.
- **machine head:** retain. The November log supports both the machine-local responsibility and the proposed status. Keep the full phrase and plural alias. Do not add `head`, which has other meanings.
- **project agent:** retain. The November log supports project context and resumable work without continuous inference. Keep the full phrase and plural alias, not the generic `agent`.

## Per-entry review

### `meditations/pkm-to-pem`

- **Terms:** no new record. Zettelkasten, knowledge graphs, epistemology, PKM/PEM, and writing to think are candidates, but the post does not provide short, settled definitions for them.
- **Exclusions:** Obsidian, org-roam, Emacs, tmux, Neovim, CLI, NeSy, and LLMs in the draft dumps are incidental examples or occur in code blocks. Do not add records just to annotate the dumps. The book and CognWare link are references, not definitional evidence. Preserve the book attribution as written pending any separate author-approved correction.
- **Reader need:** the meaning of the proposed move from knowledge to epistemological management is the essay's open subject. A glossary definition would falsely settle it. A later authored explanation would be more useful than an inferred label.
- **Related reading:** `meditations/studying` shows a concrete concept-outline method; `meditations/laboratory` sets out the broader research space. These later posts are follow-up reading, not sources for what the earlier author intended.
- **Question:** should PKM/PEM become stable names for raj's methods, or remain exploratory title language? Optional; omit definitions until clarified.

### `meditations/programming`

- **Terms:** no new record. HCI is expanded inline. Lisp, Emacs, s-expressions, agentic programming, and deromanticizing were reviewed.
- **Exclusions:** the essay concerns changing motivation and interaction with a computer. It does not define Lisp or s-expressions. Do not turn `deromanticizing` into a shared technical concept from this personal description. L-theanine and hobbies are incidental, not reader prerequisites.
- **Related reading:** `meditations/the-lisp-machine` is a later return to Lisp; `meditations/laboratory` develops the ambition for personal work; `meditations/pkm-to-pem` explains the writing approach.
- **Questions:** none needed for preparation.

### `meditations/studying`

- **Terms:** add **concept tree**. The post defines a tree of concepts and constituent sub-concepts, followed by a context-aware pass. Its own entry is the introduction and source.
- **Aliases:** keep only the full phrase. Do not alias `outline`, `tree`, or `project outline`; these could mark unrelated structures.
- **Exclusions:** org mode and Markdown name possible working formats, not necessary definitions. The prose already explains nodes, leaves, deadlines, and study order. Do not replace that central explanation with panel summaries.
- **Related reading:** `meditations/pkm-to-pem` gives the writing and knowledge-management context. `meditations/laboratory` gives a later research setting.
- **Questions:** none.

### `meditations/embeddings`

- **Terms:** add **PCA**, with `principal components` as the only alias. Scope its definition to the centered post-vector map and the projection-fidelity limit stated here. This entry is the introduction and source. The opening pipeline gives a short route into the detailed mathematics.
- **Exclusions:** do not define all embeddings as this site's weighted, normalized post vector. The prospective embedding use in `meditations/pkm-to-pem` is broader. Chunking, normalization, token weighting, and retained variance receive direct explanation here. SVD, cosine similarity, and whitening may warrant a future mathematical primer, but this post does not supply standalone definitions. The later link check retrieved the model card. External pages are not saved term evidence under the current schema.
- **Related reading:** `logs/2026-10-06-two-collections-one-archive` explains the shared archive; `logs/2026-10-07-using-autolith` records a local setup of this workflow.
- **Reader need:** a short general embedding explanation would help a reader without ML background. It needs an authored passage or an approved evidence-source extension, not an unsupported registry definition.
- **Question:** is that general mathematical introduction wanted? Optional; does not block the existing technical post.
- **Workflow note:** the Usage Flow records an older command sequence. Use the current README and preparation command for present work. Any revision to this meditation requires raj's approval.

### `meditations/laboratory`

- **Terms:** no new record. Personal research lab, personal science, and computational epistemology were reviewed.
- **Exclusions:** `laboratory` is the essay's central framing and already receives context. Computational epistemology is a domain the author is still exploring; the one-line mention does not define his meaning. Archetypes and music are incidental. The lost personal-science article cannot be treated as a known source.
- **Related reading:** `meditations/pkm-to-pem` explains the writing experiment; `meditations/studying` gives a practical study method; `logs/2026-11-06-orchestrating-autolith` describes a later concrete application of the laboratory idea.
- **Question:** if computational epistemology becomes a recurring term, ask for the intended scope and a supporting explanation. Omit it for now.

### `meditations/the-lisp-machine`

- **Terms:** reuse **Autolith** and add the new **Lem** reference. Choose the October setup log as the introduction for both because it explains their roles, rather than merely naming them.
- **Evidence:** Lem's ncurses build, Lisp editing, Vim bindings, and terminal role are explicit in the setup log. The meditation independently records the choice of Lem but is not needed as additional definition evidence.
- **Exclusions:** Fedora, VPS specifications, hardware fields, vulnerabilities, and command output are setup detail. Code blocks do not receive annotations. Do not define a historical `Lisp machine` from a metaphorical title and a contemporary setup record. Do not add `lisp` as an alias for Autolith.
- **Related reading:** `logs/2026-10-07-using-autolith` supplies concrete setup details; `meditations/programming` supplies the earlier motivation; the November orchestration log is a later development.
- **Questions:** none.

### `logs/2026-10-06-two-collections-one-archive`

- **Terms:** no new record. The log itself clearly explains meditation authorship, requested agent logs, shared search, and source labels.
- **Exclusions:** do not create global `log`, `agent`, `archive`, or `meditation` aliases. These are familiar words with broader uses elsewhere. `mx` and `lx` are explained inline and in a diagram. They do not need a separate definition page.
- **Related reading:** retain the existing links to `meditations/programming` and `meditations/embeddings`. The October setup log is useful later reading about the authoring rules in use.
- **Questions:** none.

### `logs/2026-10-07-using-autolith`

- **Terms:** retain **Autolith**; add **Lem** and **Simplified Technical English**. This entry is the introduction and evidence for all three.
- **Aliases:** `Simple Technical English` is a documented wording variant of the log style. The definition describes the local writing rule, not a claim of formal ASD-STE100 compliance. Do not add `STE`, which does not occur here and can be ambiguous.
- **Exclusions:** ops-log and OMP identify the prior workflow but lack enough source explanation for useful records. Emacs, Vim, Stow, dotfiles, forks, origin/upstream, Node.js, and Python are contextual setup details. Their names alone do not justify a glossary.
- **Related reading:** retain the existing links to the Lisp-machine meditation and the collections log. `meditations/embeddings` adds technical detail on the blog build; the November orchestration log is a later design, not evidence that this October setup already included it.
- **Questions:** none.

### `logs/2026-11-06-orchestrating-autolith`

- **Terms:** retain **Orch**, **Autolith**, **HMAS**, **machine head**, and **project agent**. This is the introduction for all except Autolith. Inspect the proposed/implemented distinction when reusing their definitions.
- **Exclusions:** Paperclip and Hermes are retired alternatives in this account, not active reader prerequisites. NixOS and ThinkPad identify hosts. Task ownership, retries, acknowledgement, transport, recovery, and cancellation are explained in the design prose; no separate local meanings need records. Do not broaden machine head to `head` or project agent to `agent`.
- **References:** keep the existing taxonomy link. Its presence does not verify the external paper or the proposed remote system.
- **Related reading:** retain Laboratory for the research purpose and the Lisp-machine meditation for personal motivation. Recommend the October setup log for concrete Autolith background. Exclude Project Outlines: its study method does not directly explain the coordination design.
- **Questions:** none.

## Follow-up decisions

Three optional editorial questions remain: the intended PKM/PEM meanings, a general embedding primer, and the intended scope of computational epistemology. They do not prevent preview or release of the current archive. Do not invent definitions while waiting for answers.

Before adding external term evidence, decide how to save and validate it. The current schema accepts exact passages from archive entries only. The external-link check below records retrieval and citation context separately from definition evidence.

Related-reading recommendations are saved in `.preparation.json`, not inserted into meditation prose. Each references receipt records its reason. Later posts are follow-up reading, not evidence of earlier intent. All nine entries have reader and references receipts; the three optional questions above are recorded with their respective entries.

## External-link check

Checked on 2026-11-13 by retrieving the cited pages. Checked destination identity
and citation context, not every claim in the linked work.

| Archive URL | Result |
| --- | --- |
| https://arxiv.org/abs/2508.12683 | Retrieved Moore's HMAS taxonomy title, author, and abstract. These match the November log's citation. |
| https://huggingface.co/Alibaba-NLP/gte-modernbert-base | Retrieved the named model card. It describes a text-embedding model with 768 output dimensions. |
| https://github.com/lambda-symbolics/autolith | Retrieved the Autolith repository. Its description identifies a self-modifiable Lisp AI agent. |
| https://fedoraproject.org/ | Retrieved the Fedora project site. This is a HOME_URL in recorded os-release output, not article evidence. |
| https://docs.fedoraproject.org/en-US/fedora/f44/ | Returned a relocation notice to https://docs.fedoraproject.org/en-US/fedora-user-docs/. Retrieved that destination; it is now general Fedora user documentation. Preserve the original URL in historical command output. |
| https://ask.fedoraproject.org/ | Resolved to the Ask Fedora support category on Fedora Discussion. This is a SUPPORT_URL in recorded command output. |
| https://bugzilla.redhat.com/ | Retrieved the Red Hat Bugzilla page. This is a BUG_REPORT_URL in recorded command output. |
| https://www.youtube.com/@CognWare | Retrieval identified the title as cognware industries. The response did not expose video content, so the channel's individual claims and videos were not verified. |

The three citation destinations and the channel identity fit their local use.
The four Fedora URLs occur inside a historical code block. No article or command
output was changed. Access and content can change; check cited pages again when
revising a claim that depends on them. Network retrieval is an agent review step,
not a site-build or CI requirement.
