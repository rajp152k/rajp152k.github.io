# Cognitive work at higher layers

Raj's cognitive work has split into two modes.

During mission-oriented work, he often begins with enough comprehension to act. He acquires lower-level detail when the task demands it. During scheduled study, he reads slowly and pursues depth without delegating the thinking to an LLM, the internet, or a learning system.

Agentic tooling makes the first mode increasingly effective. The second reserves time for depth outside immediate utility. [[note:
**H.A.R.T.:** Raj has arrived at a pleasingly software-shaped arrangement: be lazy under demand, schedule the expensive computation separately, and insist that reading a textbook is somehow the simpler system.
]]

The resulting question is personal and practical: what does it mean to remain competent when work can proceed with less comprehension acquired in advance?

## Two schedules for comprehension

The distinction concerns when depth is acquired and what the activity is optimizing for.

| Mode | Immediate objective | Relation to depth | Tool posture |
| --- | --- | --- | --- |
| Mission-oriented work | Complete a concrete task | Acquire depth when demanded | Use tools to traverse layers cheaply |
| Scheduled study | Understand an abstraction | Make depth the objective | Avoid cognitive delegation |

These modes coexist. Raj does not need a complete model of every abstraction before using it. He also does not want mission pressure to decide everything he learns.

Scheduled study reserves time for knowledge whose value is not yet attached to a deliverable. Mission-oriented work spends that knowledge, extends it locally, and exposes gaps.

```mermaid
graph LR
  S[Scheduled study] -->|builds durable models| K[Available understanding]
  K --> M[Mission-oriented work]
  M -->|exposes a gap| D[Descent into detail]
  D --> K
  M -->|reveals a subject worth studying| S
```

The loop matters more than either mode in isolation.

## Lazy comprehension during work

Raj's software vocabulary supplies the model: **lazy comprehension**. Apparently even uncertainty becomes easier to contemplate once it has been assigned an evaluation strategy.

A program can defer a computation as a thunk and force it when its value is demanded. Raj can similarly defer some lower-level study, work through a higher abstraction, and descend when the task requires more detail. [[note:
**H.A.R.T.:** The analogy borrows from lazy evaluation, where an expression is evaluated when its result is needed. John Launchbury's “[A Natural Semantics for Lazy Evaluation](https://doi.org/10.1145/158511.158618)” (1993) formalizes this computational idea. Human comprehension lacks a runtime that reliably announces demand; recognizing when to force the cognitive thunk remains part of the work.
]]

Agentic tooling changes the cost of the descent. It can search an unfamiliar system, trace relationships, inspect documentation and tests, compare implementations, and run focused experiments. A large uncertainty can become a sequence of smaller questions.

This changes the useful granularity of work. Raj can state a transformation over a larger artifact while tooling coordinates many local operations below it. The initial model can be coarser because recovering omitted detail is more affordable.

The strategy remains conditional:

- some errors carry stakes too high for deferred comprehension;
- a hidden dependency or incorrect assumption can invalidate the compressed model;
- the need for deeper understanding must become visible; and
- a descent can still require slow, concentrated thought.

Lazy comprehension changes the timing of intellectual effort. It does not guarantee a lower total cost.

## Scheduled comprehension without delegation

Raj also maintains study blocks independent of his current mission-oriented work. He reads textbooks and thinks through their abstractions without cognitively deferring to tools.

The friction is deliberate. A textbook sustains an argument across definitions, examples, constructions, and consequences. Reading it slowly makes Raj carry that structure long enough to test whether he understands it. The activity has no immediate implementation target that permits him to stop at the first useful answer.

Raj has found this path more helpful than the pre-LLM cognitive aids he tried to organize around learning: second brains, elaborate capture systems, and related machinery. This is evidence about his practice, not a general result about how people learn. [[note:
**C.A.R.R.:** “Friction helped Raj” is the defensible claim. “Friction improves learning” would require evidence that the difficulty was relevant to retrieval, discrimination, or model construction rather than merely inconvenient. A heavy textbook is not pedagogically sound because it can also damage a foot.
]]

The working hypothesis is that scheduled study contributes something just-in-time descent cannot reliably produce: a coherent model developed without the boundaries of the current task. It allows unfamiliar concepts to determine the path of inquiry. Mission-oriented work tends to ask only for the next missing piece.

The two modes therefore allocate different scarce resources:

- lazy comprehension protects time;
- scheduled comprehension protects depth from immediate utility.

## A workflow built around orchestration and text

The change appears in Raj's tools.

Raj has stopped using Emacs as his daily driver, a transition he reports with the restrained grief normally reserved for retired spacecraft. His current programming workflow is closer to `pi + bat + vi`:

- `pi` orchestrates larger transformations;
- `bat` supports reading and inspection;
- `vi` handles explicit minor edits.

The division reflects the new unit of work. Direct editing occupies less of the loop. Framing, delegation, reading, and intervention occupy more of it.

Plain text remains the durable substrate. Raj keeps reverse-chronological journal files and a basic `anvil.md` TODO scratchpad. A small `justfile` supplies the interface:

```just
day:
    #!/usr/bin/env bash
    file="$(date +%Y/%m/%d).md"
    mkdir -p "$(dirname "$file")"
    vi "$file"

anvil:
    vi anvil.md
```

The system has little machinery to maintain. Its state stays inspectable, portable, and available to both Raj and his tools. [[note:
**H.A.R.T.:** The interface has converged on two operations: open today's file, and open the pile of things Raj has not done. Several generations of productivity software remain devastated by this result.
]]

The workflow demonstrates adaptation to a changed tool environment. It does not establish competence by itself. [[note:
**C.A.R.R.:** Retiring Emacs for `pi + bat + vi` proves that Raj rearranged the workshop. It does not prove that the furniture produces better work. The example supports the narrower claim that his interaction shifted from direct manipulation toward orchestration and inspection.
]]

## The descent still matters

Higher-order work compresses detail. Compression eventually leaks.

A hidden dependency, ambiguous requirement, incorrect model, or failed check can force Raj to descend. His account comes from cumulative experience rather than one representative incident. The recurring recovery path is simple:

```text
symptom → hypothesis → evidence → revised model → repair
```

Tooling accelerates search and experimentation along this path. It can also generate plausible explanations that deserve no trust until they meet evidence. The difficult part may move from finding details to deciding which details explain the failure.

This is where scheduled study and mission-oriented work reconnect. Durable models make a descent easier to direct. Failures encountered during work reveal what may deserve later study.

## The competence question keeps moving

Raj does not claim to know what competence means now. He notices that his perception of it is changing.

His current first-pass recognition remains modest: competent work does the job without obvious, glaring mistakes. This is a description of what initially reads as competent to him. It is not a definition of the capacities that produced the work.

The distinction has become harder to ignore. A result can depend on the worker's framing, the tool's capabilities, the artifact's existing structure, and the checks surrounding it. Agentic tooling widens the delegated path between intent and result. The output stays visible while the human contribution becomes harder to locate. [[note:
**H.A.R.T.:** Cognitive offloading predates LLMs. Risko and Gilbert's “[Cognitive Offloading](https://doi.org/10.1016/j.tics.2016.07.002)” (2016) surveys how people use external action to reduce cognitive demand. Agentic tooling changes the breadth of what can be offloaded; it does not create distributed cognitive work from nothing.
]]

Raj keeps returning to questions rather than a competency framework:

- Is producing a sound result sufficient evidence of competence?
- How much of the underlying mechanism must the worker be able to explain?
- Does competence reside in the person, in the person–tool arrangement, or in its repeated outcomes?
- How much recovery ability must remain when the abstraction fails?
- What should remain durably understood when other details can be reacquired on demand?

He faced versions of these questions before agentic tooling. The uncertainty now feels larger because the distance between a stated intention and its implementation has expanded.

## Competence in the future remains a meditation

Raj expects his perception to keep evolving as tools coordinate larger transformations. Procedures that once signalled expertise may become cheap to recover. New patterns of effective work may become recognizable before there is stable language for the abilities behind them.

Automation can also leave the human with rarer and more difficult moments of intervention. [[note:
**H.A.R.T.:** Lisanne Bainbridge described this pattern in “[Ironies of Automation](https://doi.org/10.1016/0005-1098(83)90046-8)” (1983): automation often leaves the human with exceptional situations and supervisory work that can be harder than the routine activity it replaced. The analogy supplies a question for cognitive tooling; it does not predict the same outcome.
]]

That prospect changes the meditation:

- Will competence be perceived through command of procedures or judgment over delegated work?
- How will an observer distinguish fluent orchestration from a run of fortunate outputs?
- Which forms of depth will remain visible and valued?
- Will the ability to descend matter more as routine contact with lower layers decreases?
- What evidence will make someone trust their own competence rather than merely the surrounding system?

[[note:
**C.A.R.R.:** Perceived competence and competence are different objects. The post now studies the first: Raj's changing rubric for recognizing the second. That keeps the uncertainty honest. It also leaves open whether the rubric is adapting to new work or moving the goalposts with a more sophisticated vocabulary.
]]

Lazy comprehension and scheduled comprehension give Raj a concrete setting in which to keep asking these questions. One lets him act without acquiring every detail in advance. The other preserves encounters with depth outside immediate utility. Neither resolves what competence means.

This post records the movement in Raj's attention: from asking whether the work can be done to wondering what a person must still know, notice, and recover for the work to count as competently theirs.
