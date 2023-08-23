---
title: "My Creation and Publishing Pipeline"
date: 2023-08-23T18:13:15+05:30
categories: ["Writing"]
tags: ["youtube","emacs","org-roam","github-actions","writing","ideas,"systems","org-mode","markdown","git","org-roam-ui","hugo"]
draft: false
---

This is an auxilliary post collating resources for the recent video I
posted ...

{{< youtube "dKU_mNaEo1g" >}}  

## The Pipeline 

1. All the ideas, resources that I want to process, any miscellaneous
   questions I have, are fed into the input-queue in the buffer 
2. All the manipulation takes place in these buffers - they're
   org-files and I use org-roam to maintain the connections
3. whenever a node set ripens and is worth sharing, I write a
   post or publish a video.
4. It can go both ways : I can force a set into maturity if I wish to
   publish something specific or I may chance upon a concept when
   observing connections.
   
## Observations 

I use [org-roam-ui](https://github.com/org-roam/org-roam-ui) to
visualize the buffer and check for linkages that might result in
something useful. I also want to publish this graph (demonstrated in
video) but there's no explicit solution for that yet and I'm planning
to build one myself with rust and webassembly as a compilation
target. 

## Publishing

The buffer is a collection of org-files and is published via
[maker2413/OrgRoamPublish](https://github.com/marketplace/actions/org-roam-publish). Check
out the exact process at this similar [brain
dump](https://notes.ethancpost.com/?stack=%2Fhow_this_website_is_made.html).  

The main blog is published via [hugo](https://gohugo.io/) and is
deployed via [github
pages](https://github.com/rajp152k/rajp152k.github.io).  

Both, the buffer and the main blog, are published via github actions
that are triggered when I push to their respective repositories.  

Youtube is something I'm figuring out my style with and don't exactly
have formal systems yet to produce consistent output. I hope to
converge on a system upon multiple iterations (think at least 20).  

## Concluding ...

The video does give you a quick overview of the pipeline which I hope
inspires you to start creating content - given that I'm trying to
highlight how convenient it is to automate stuff and get in the flow
of publishing posts/videos once you have your basics set up.   

Do let me know if you see any improvements, conceptual upgrades, or
notice any inefficiencies with this pipeline in the comments below...  
