---
title: "Flexible SWE Experiments"
date: 2026-05-18T06:03:19+05:30
categories: ["SWE"]
tags: ["swe","polylith","architecture","tooling","organization","experiment","strategy","flexibility", "legos","monorepo","structure","code", "microessays"]
---

From time to time, I pick up a long running swe experiment : one where I choose to iteratively explore a domain by playing around with the ecosystem and tooling available. This is such a common occurence now that I've begun implicitly templatizing this process.  

Surf a little, and this pops up: [polylith](https://polylith.gitbook.io/polylith) : an optimal (at a first glance and first use and consequent uses and reglances and meditations as well) way of separating concerns in a monorepo, while allowing for rapid experimentation.  

"Legos", is the analogy offered by the docs where in your functional abstractions are wrapped in thin interfaces (therefore easily swappable) and multiple deployment recipes calling upon these former bricks. Sticking to certain namespacing and structuring practices enable usage of meta-tooling that allow for capturing the state of your software at a moment.  

The idea evolved from [clojure](https://cljdoc.org/d/polylith/clj-poly/) but usable anywhere: it's just an idea.  

As for the nature of the experiments themselves: they span along dimensions of being ephemeral/long-running, domain specific/higher order, personally optimized/ conventional UX focused,  seeded with firm intent right way/ purely exploratory and with the intent of figuring the next class of experiments out.  

I haven't had an un-intuitive refactor so far..  

There's a lot of literature on building good software compared to building throw aways; there's a lot of value to maintaining structure with your throw aways, is my recent finding.  
