---
schema: 1
kind: post-review
entry: logs/2026-11-06-orchestrating-autolith
cycle: 1
state: curation
post_sha256: c19d9f95a7011f3867aff76f14fa1105a5406a6093aa228347521a83d78884dc
terms:
  - id: T1
    revision: 2
    state: applied
    action: add
    record: t1-hmas
    decision: D1
    applied_at: '2026-11-21T13:08:57Z'
    card:
      name: HMAS
      definition: 'Hierarchical multi-agent systems: systems that organize agents in layers.'
      aliases: [hierarchical multi-agent systems]
      passage: Hierarchical multi-agent systems (HMAS) organize agents in layers.
      introduction: Context section of this log; explain the acronym without implying an implemented system.
      use_scope: This log only. Link the expanded phrase and acronym in Context; keep the paper title citation without a nested term link.
  - id: T2
    revision: 1
    state: proposed
    action: add
    record: t2-peer-discovery
    decision: null
    applied_at: null
    card:
      name: peer discovery
      definition: Finding other running agents and their current communication destinations.
      aliases: []
      passage: Native Lisp peer discovery gives local agents structured session information. They can resolve a current peer without parsing a terminal status report.
      introduction: Use the existing explanatory paragraph in Match the method to the work. No prose change is proposed.
      use_scope: First eligible body use in Orchestrating Autolith only. Local discovery, not remote reachability or permission to act. No other archive matches.
links: []
decisions:
  - id: D1
    actor: raj
    action: approve
    scope: 'T1:r2: definition, aliases, evidence, introduction, and this-log-only uses'
    post_sha256: c19d9f95a7011f3867aff76f14fa1105a5406a6093aa228347521a83d78884dc
    at: '2026-11-21T12:57:02Z'
    evidence: 'review-imports/c190bfe8095e236adca4-33a824290d229925.json; user raj; item logs/2026-11-06-orchestrating-autolith:cycle-1:T1:r2'
    reason: null
transitions: []
blockers: []
release:
  commit: null
  deployed_commit: null
  url: null
  verified_at: null
---

# First term approval batch

## Now

Raj approved T1 revision 2 in Potato. Applied the exact candidate to `terms.json`.
That decision and its provenance are unchanged. Do not queue it again.
The all-log batch adds **T2 revision 1, peer discovery**, for raj's decision.
The [Using Autolith review](../2026-10-07-using-autolith/cycle-1.md) also proposes
VPS and inference with explicit uses in this log. Those two cards appear once
in the shared terms-only session. The post stays in curation.

## Reader review

Read the complete log. It describes a proposed personal multi-agent research
setup and separates local results from untested cross-machine requirements.
The intended reader knows basic programming but may not know agent-system terms.

## T1: HMAS

- Domain: multi-agent systems. The post cites a taxonomy whose title uses
  “Hierarchical Multi-Agent Systems”; this is a domain term, not a name invented
  for raj's setup.
- Registry ID: `hmas` (new record after the reset).
- Name: `HMAS`.
- Exact definition: **Hierarchical multi-agent systems: systems that organize agents in layers.**
- Aliases: `hierarchical multi-agent systems`.
- Reader need: explain the acronym in the Context section without implying that
  raj has already built or tested such a system.
- Exact archive evidence: “Hierarchical multi-agent systems (HMAS) organize agents in layers.”
- Evidence post and proposed introduction:
  [Orchestrating Autolith for a personal laboratory](../../../../logs/2026-11-06-orchestrating-autolith.md).
  Its Context section defines the term. Later sections explain the proposed roles
  and distinguish current local work from remote requirements.
- Use scope: this log only. Both the expanded phrase and acronym occur in its
  Context paragraph. The cited paper title also contains the expanded phrase;
  keep that existing citation as a link, without a nested term link.
  No other archive post contains either spelling in the current source scan.
- Requested approval covers this definition, alias, evidence, introduction, and
  use scope together. Eligibility alone does not approve these details.

## Other candidates

Do not restore product names or local labels merely because they were in the old
registry. Other technical terms need separate proposals. Meditations have no terms.

## Reset decision

Raj requested removal of all old terms and curated post links before this review.
The reset clears nine registry records, 24 related-reading selections, and the
three log reading lists. External citations and meditation prose are preserved.
Old agent receipts are historical and stale, not current approvals.

## Decisions

### D1: T1 revision 2 approved and applied

- Imported [session c190bfe8095e236adca4](../../../../review-imports/c190bfe8095e236adca4-33a824290d229925.json).
  The final response from `raj` is `approve`, with no comment. `changed_sources`
  is empty. The reviewed record hash was
  `02c84477be67762ccb9fdab980d1db50fa1cb8a9611a8e8140872ad0bff53199`;
  the post hash matches the front matter above. Both matched before application.
- The decision time comes from the final approval event in the imported history.
  Earlier selection and comment edits are history, not the final decision.
  Raj gave no final reason.
- Applied only `hmas`: the exact definition, alias, source quote, and introduction
  above. No article prose or curated post links changed.
- Enabled the optional `annotation: first-spelling` setting only for HMAS.
  This marks both approved spellings in Context, with one anchor per term.
  Repeated spellings and the linked paper title are not annotated.
  Other terms default to one annotation per term.
- The registry has no per-post scope filter. Checked all nine archive entries:
  only this log matches. Check this scope again after archive changes.
- Kept both review sessions and their responses. No cleanup or publication.

### Application checks

- Registry validation: one term, one source, one post reference.
- Python: 115 tests passed, including mode validation, both spellings, repeated
  spelling suppression, one anchor and mention, and citation exclusion.
  Search: 11 Node tests passed. Embeddings are fresh for all nine entries.
  `just prepare` passed; it reused all nine embeddings and rebuilt the draft.
- Targeted desktop browser checks passed: both Context references open the exact
  definition; the anchor is unique; the paper citation has no nested annotation;
  the definition page's source and introduction link resolves to this log.
  The phone check passed: the two references are plain text.
- The full browser suite has 9 passes and 14 failures. Its fixtures still expect
  removed terms (`orch`, `autolith`, `simplified-technical-english`) and removed
  curated post references. These same failures occurred before the annotation
  opt-in. Do not restore removed content to satisfy those fixtures.
- The retained old session has 7 files and SHA-256
  `40dce8c22d0ad3fe1b84136a429f6ddb1136e640989fd6487f5edcbba5798618`
  (sorted relative path bytes, then file bytes), equal to its pre-task digest.
- `just check` stops at the existing stale archive reviews. All 18 review stages
  need fresh review; this term decision does not replace them.
- The post remains in `curation`; this batch does not establish a complete
  curation review, commit approval for the post, or publication approval.

## T2: peer discovery

- Proposed registry ID: `peer-discovery`; domain: distributed agent systems.
- Reader need: distinguish finding a peer's destination from proving that a
  remote service is reachable or that an action is allowed.
- Exact definition: **Finding other running agents and their current communication destinations.**
- Aliases: none. Do not match the generic words `peer` or `discovery` alone.
- Exact archive evidence: “Native Lisp peer discovery gives local agents
  structured session information. They can resolve a current peer without
  parsing a terminal status report.” The next sentences limit this result to a
  local destination and deny remote discovery or permission claims.
- Introduction: the existing explanatory paragraph in Match the method to the
  work. It already teaches the proposed meaning. No new prose is needed.
- Complete archive scope: one eligible body occurrence in this log; none in the
  other two logs or six meditations. Use default first-term annotation.
- Requested approval covers this definition, aliases, evidence, introduction,
  and this-log-only use. State is proposed, not approved or applied.

## All-log review coverage, 2026-11-21

Read this whole log again. It separates current local agent work from a proposed
cross-machine system. The intended reader knows basic programming but may not
know agent coordination and transport terms. HMAS already has a scoped decision.
Its definition, source quote, aliases, introduction, post hash, and uses have not
changed. No new HMAS use occurs in the other logs. Preserve D1 and T1:r2.

The all-log review also proposes these uses from the Using Autolith record:

- VPS: two `virtual private server` body occurrences in Context. Mark the first.
- Inference: two body occurrences, in Separate contexts and one task owner and
  Make work resumable across machines. Mark the first. This is model execution,
  not a different logical-deduction meaning. The proposal covers these uses.

No other new term card is needed for this log in this batch:

- Autolith, Paperclip, Hermes, NixOS, ThinkPad, Mac, and Lisp name tools,
  platforms, or a language. Do not restore them as terms merely because named.
- Orch, machine head, project agent, and head are local roles. The post explains
  them; they are not established domain terms simply because repeated here.
- `persistence` is explained as resuming work. Do not create a broad alias for
  that ordinary word. `task owner`, `context`, and `task identity` describe this
  design without needing new glossary entries.
- `rollback`, `transport`, and `cluster` are technical vocabulary, but the current
  sentences only mention them. They do not explain enough to support useful
  definitions. Leave them out of this batch rather than invent archive evidence.
- `restart`, `duplicate delivery`, and `cancellation` are used directly in trial
  requirements. The post distinguishes delivery from completion in plain prose.
  No new term such as idempotency appears or is proposed.
- Reproducible experiments and negative results are described as research
  requirements, not treated as names for a local system.

These are AL's screening choices, not rejection or deferral decisions by raj.
This is a term review, not a completed post-link review. All new candidates wait
for explicit decisions. No registry or article edits were made for this batch.
