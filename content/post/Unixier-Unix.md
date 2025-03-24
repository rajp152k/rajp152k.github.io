---
title: "Blub in the Unix Philosophy"
date: 2025-03-24T15:18:39+05:30
categories: ["Tooling"]
tags: ["operating systems","blub","microessays","unix","linux","plan9","virtualization","distributed"]
---

I've always maintained a philosophical appetite for the tooling that I use.  

One of the core tenets of the Unix Philosophy[^1] is that everything is a file...  

Plan9[^2] has caught my eye due to its more homogenous design than the usual unix you're used to.  

The footnoted-paper (~pre-mature book) is somewhat unhinged and doesn't shy away from taking a jab at the Unix ecosystem and design.  

Apart from the several points the author makes, what stands out the most for me is the idea of _everything_ truly being a file: in hindsight, Unix only realizes a fraction of the principle.  

A year ago, I wouldn't have explicilty realized that Unix needed evolution, but I now understand there's a whole bunch of unrealized potential in this space.  

I personally am interested in investigating virualization capabilities (can it replace a hypervisor for larger cloud workloads?) via Plan 9 but couldn't find explicit literature right away: a natural trajectory of engineering this from the already provisioned namespacing does arise.  

I understand that this will not be production grade due to the philosophical and design differences between the underlying virtualizer (Plan9) and what the demand is rich for (the Unices), but this could potentially fork into a niche of distributed virtualization.  

Will explore further for a while..  

> PS : Do checkout the [Blub Paradox](https://en.wikipedia.org/wiki/Paul_Graham_(programmer)#The_Blub_paradox)

[^1]:https://en.wikipedia.org/wiki/Unix_philosophy

[^2]: checkout the [papershelf](/papershelf) [entry on 0x2384](http://9p.io/sources/contrib/uriel/mirror/9book.pdf)
