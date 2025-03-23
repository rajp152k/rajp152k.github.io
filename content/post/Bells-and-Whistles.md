---
title: "Bells & Whistles"
date: 2025-03-23T14:18:07+05:30
categories: ["Tooling"]
tags: ["microessays", "compute", "network", "storage", "abstraction", "turing","lambda", "RAM", "lisp","orchestration", "Unix","BSD","Linux","Plan9","distributed","infrastructure","electrons","waves","descartes","fallacy","superhero","suits","info","man","state","software","hardware","systems","thinking","recursion","abstraction"]
---

I've started spending some time per day without the usual modern software engineering tooling (LLMs, the Internet, etc) to explicitly maintain my cyber-deduction skills (in the context of Unix-based systems (BSDs, Linux, yet to explore Plan9), mostly because they power the majority of the global compute infrastructure).

It's fun: init your journey with a `man man` (I'm an `info info` guy myself) and be extremely skeptical of your usual modus operandi, ditching all assumptions and tumbling down the rabbit hole.  

Things really start picking up when you begin thinking about the neatly tucked away manipulation and conveyance of state, orchestrated by your operating system. I prefer breaking down any computing abstraction into interactions of three abstract systems rather than one of more theoretically foundational models (Turing machines (The RAM model) and Lambda Calculus (The Lisps) being the two I'm aware of):  
 - Processing(core and facilitative)  
 - Persistence (varying temporal granularity)  
 - Communications/Interfaces (internal and exposed)  
 
I would recommend you do not accept that categorization (also seen in the wild, more explicitly realized as Compute, Storage and Networking) right away and instead work towards your own understanding by observing and messing around.  

This helped me understand hardware better and that each constituent (seemingly responsible for one[^1] specific task) of the parent abstraction can be further broken down into a combination of those three:
 - CPUs employ registers, caches and need to facilitate inter-core task orchestration  
 - NICs need buffers, protocol encoders/decoders to handle coms
 - SSDs orchestrate concurrent IO, detect and repair corruptions, collaborate redundancy  

This is just one class[^2] of personal insights I've developed by deliberately giving up on the "superhero suits" that are easily available to the usual software engineer today. Going down the local hood of your own computer will also help you understand the global distributed infrastructure as a unit (thank abstractual recursion again) with ease.  

Eventually, I've begun doing this intuitively for any "novel" computing abstraction that I encounter and have been grasping the crux faster than usual.  

I might even be little ambitious and claim that this will help you not fall for a descartes' fallacy[^3] and claim that the boundaries that we draw between hardware and software are fairly fluid.

[^1]: I'm trying to be familiar with the examples

[^2]: I've lately been tempted to apply parallels of this to organisms, organizations and the global network formed by their interactions as well but that is a highly experimental thought as of now. A more generic tooling (systems thinking) would be better suited but I like being capable of different tints to my shades based on the mood I'm in.

[^3]: https://en.wikipedia.org/wiki/Descartes'_Error
