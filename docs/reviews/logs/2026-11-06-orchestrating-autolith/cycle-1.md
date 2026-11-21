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
    state: proposed
    action: add
    record: t1-hmas
    decision: null
    applied_at: null
    card:
      name: HMAS
      definition: 'Hierarchical multi-agent systems: systems that organize agents in layers.'
      aliases: [hierarchical multi-agent systems]
      passage: Hierarchical multi-agent systems (HMAS) organize agents in layers.
      introduction: Context section of this log; explain the acronym without implying an implemented system.
      use_scope: This log only. Link the expanded phrase and acronym in Context; keep the paper title citation without a nested term link.
links: []
decisions: []
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

Approve, request changes, reject, or defer T1 revision 2 in Potato.
This is one candidate to test the approval flow, not a complete archive review.
The terms-only session has no log comment item. Memo testing and Blog Update [1] come later.

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

Awaiting raj's response. No candidate has been approved or applied.
