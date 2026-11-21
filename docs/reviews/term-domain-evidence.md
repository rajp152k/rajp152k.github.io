# Domain evidence for the all-log term batch

Retrieved on 2026-11-21. These notes support the proposed meanings. They do not
establish raj's approval. The session freezes this file and the complete logs.
Short quotations below are from the named pages. Other descriptions are summaries.

## Lisp image

[SBCL manual, Saving a Core Image](https://www.sbcl.org/manual/#Saving-a-Core-Image):
“SBCL has the ability to save its state as a file for later execution.”
A saved core can restart the Lisp process with its global state. The proposed
term covers the running Lisp environment in the log, not a disk image or a claim
that every thread and resource can be saved. The log's separate development
checkout and private changes to the running image establish the local context.

## Virtual private server

[AWS, What is a VPS?](https://aws.amazon.com/what-is/vps/), main definition:
a VPS has reserved resources within a physical server shared with other users.
The two logs name the Fedora VPS and the NixOS virtual private server. Neither
current passage explains virtualization; the proposal includes an exact short
explanation to add only after approval.

## Fork

[GitHub, Forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks):
“Forks are repositories that start as copies of another repository”.
The source repository is the upstream repository. A fork is a separate
repository, not a branch or merely a local checkout. The archive passage names
raj's fork, origin, and upstream; it does not define the general concept.

## Inference

[AWS, Deploy models for inference](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html):
“predictions, or inferences, from your trained machine learning models”.
The proposed meaning is model execution that produces outputs. It covers the
embedding model in the setup log and model use by agents in the orchestration
log. It does not mean logical deduction or model training.

## Front matter

[Jekyll, Front Matter](https://jekyllrb.com/docs/front-matter/):
“valid YAML set between triple-dashed lines”.
This documents established static-site terminology. This blog has its own
builder; the proposal makes no claim that it uses Jekyll. The source files and
the setup log show title and date before the article body.

## Simplified Technical English

[ASD, About ASD-STE100](https://www.asd-ste100.org/about_STE.html):
“The STE standard consists of a set of writing rules and a controlled dictionary.”
This is a named controlled language for technical documentation. A preference
for short sentences alone does not establish compliance. The proposal does not
claim that raj or AL completed a formal compliance review.

## Text embedding

Archive evidence is in [Blog Update [0]](../../meditations/embeddings.md), Math:
“The pinned [gte-modernbert-base](https://huggingface.co/Alibaba-NLP/gte-modernbert-base) model and its own pooling produce a 768-dimensional vector $e_{ic}$ for chunk $c$ of post $i$.”
The following normalization and distance equations explain how the vectors
support comparison. This meditation is evidence only. No term annotation or
prose edit is proposed for any meditation.

## Peer discovery

The orchestration log directly explains the use: local agents obtain structured
session information and resolve a current peer's destination. The proposed
meaning is limited to finding peers and their communication destinations. It
does not imply remote discovery, authentication, or permission to execute work.

## Evidence and application limits

Some existing passages establish use but do not explain the whole definition.
Those candidates include an exact proposed introduction sentence. If approved,
apply that sentence before using it as a registry source quote. Do not present a
proposed sentence as a quotation from the current archive. Registry evidence can
also retain the existing passages where they support the same meaning.

The current registry has no per-post annotation filter. Several proposed names
also occur in meditations. Do not apply these candidates with unrestricted
matching. Enforce the approved log-only scopes before applying them. This batch
changes neither registry records nor article prose.
