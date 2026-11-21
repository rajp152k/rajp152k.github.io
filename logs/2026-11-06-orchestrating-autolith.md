---
title: Orchestrating Autolith for a personal laboratory
date: 2026-11-06T10:17:50+05:30
---

# Abstract

raj is experimenting with personal swarms of agents. He wants persistent project contexts, direct communication between agents, and clear control over work across machines. He is moving toward Autolith after trying a mixed set of agent systems.

Local agents already communicate and keep separate contexts. The proposed cross-machine system still needs trials. Its purpose is to support a personal computer science laboratory, with reproducible experiments, useful records, blogs, and eventually papers.

# Context

raj read David J. Moore's [A Taxonomy of Hierarchical Multi-Agent Systems: Design Patterns, Coordination Mechanisms, and Industrial Applications](https://arxiv.org/abs/2508.12683). Hierarchical multi-agent systems (HMAS) organize agents in layers. He is considering how to apply those ideas to personal work.

He tried Paperclip on a NixOS virtual private server, Hermes on a ThinkPad, and Autolith on a Mac. He now prefers Autolith heads across machines instead of this mixed setup. A head is the agent responsible for execution and resources on one machine.

Orch verified removal of the Paperclip and Hermes services from their active system configurations. The former services and endpoints are inactive. Data and rollback state were retained. The running and boot system profiles match on both machines, but reboot behavior was not tested.

The ThinkPad already had Autolith before this change. No replacement Autolith was installed on the virtual private server. The proposed organization of machine heads still needs implementation and tests. Removing the old services does not establish a working cluster.

# Separate contexts and one task owner

Persistent project agents keep the context for their own projects. They can communicate directly instead of requiring raj to repeat each report. Persistence means that an agent can resume its work. It does not require continuous inference.

Orch is the coordinating agent. It handles priorities across projects and requests for raj's attention. Machine heads manage local execution and resource conflicts. Project agents retain domain knowledge. One agent must own each task, even when other agents contribute.

raj is considering a shallow hierarchy. For example, Orch could also act as the Mac head at first. Adding machines should not require adding layers of coordination to every small task.

The current local workflow already includes separate project contexts and direct agent messages. Extending that workflow across machines needs separate transport, recovery, and permission checks. Local success does not prove remote readiness.

# Match the method to the work

Use direct tools for small, exact tasks. A command, file read, or calculation often needs no additional agent.

For independent work, use low-effort workers for clear, bounded tasks with explicit checks. Use medium-effort workers for implementation, debugging, unclear scope, or failed checks. Keep the main coordinator at medium effort unless raj chooses otherwise.

The reason is practical: delegation adds context transfer and review. Use it when independent work can improve the result or reduce elapsed time. More agents do not, by themselves, produce better research. More machines also do not multiply a shared provider quota.

Native Lisp peer discovery gives local agents structured session information. They can resolve a current peer without parsing a terminal status report. This identifies a local destination. It does not establish remote discovery or grant permission to act.

Shared files also do not prove shared runtime state. Two agents can read the same configuration while running different loaded definitions. Changes need an appropriate reload and a check of the active state.

# Make work resumable across machines

The proposed system needs a record for each task. That record should identify the objective, owner, machine, workspace, input revisions, permitted actions, budget, output location, and completion check.

Keep task identity separate from a running process. After a restart, an agent should recover its commitments and next permitted step. It should inspect existing jobs before starting replacements. An inactive agent context should use no inference budget.

Delivery, acceptance, execution, and verified completion are different states. A sent message is not proof that work finished. Keep results until the receiving agent acknowledges them.

Disconnects make retries difficult. If a reply is missing, inspect the actual state before repeating an action with side effects. Identify duplicate requests and bound the number of retries. For cancellation, check that the underlying jobs and child agents stopped.

These are requirements for the cross-machine design. They are not claims that remote recovery and cancellation have passed tests.

# Evaluate research, not agent activity

The long-term goal is a personal computer science laboratory. The cluster is one application within it. More messages or completed subtasks are weak evidence of research progress.

For an investigation, retain the question, code and input versions, environment, configuration, measurements, and uncertainty. Preserve negative results. Separate exploration from reproduction and review. A model's claim is not a measurement.

A useful first remote trial would produce a read-only artifact that another agent can check independently. Later trials should cover disconnects, duplicate delivery, restart, and cancellation. An isolated write task needs its own permission. Complete a real investigation before expanding the system.

Research output should pass verification before it reaches the blog or a paper.

# Conclusion

raj has chosen a direction: persistent Autolith agents with separate project contexts, direct communication, and a shallow structure for coordination. The local workflow provides a starting point. The proposed cross-machine system still needs verified transport, bounded tasks, recovery tests, and a first reproducible investigation.
