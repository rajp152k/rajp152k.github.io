---
title: "Contextual .gitignores"
date: 2025-01-09T09:01:27+05:30
categories: [""]
tags: [""]
draft: true
---

A while ago, I had a strong desire to partition some of my professional work logs into mutually exclusive git repositories: Blacklists and Whitelists flipped in the one another.  

I was aware that the `.gitignore` could ignore stuff; today I found out that I can also whitelist stuff via that.  

checkout [^1] [this stackoverflow question]( https://stackoverflow.com/questions/9162919/whitelisting-and-subdirectories-in-git)  


So if the first `.gitignore` looks like  

```
asdf-pattern 
more-asdf
some-absolute-asdf
dir-asdf/
```

the second one would look like:

```
# blacklist everything first
*

# unignore the directories to capture nested existences
!*/

# then your usual unignores
!asdf-pattern
!more-asdf
!some-absoluete-asdf
!dir-asdf/
```

What I wonder now is if git would allow for a branch-contextual .gitignore (named with certain protocols) so that I don't have to maintain two different repositories altogether.  

Maybe I should consider creating a pull request sometime down the line...  

The generic desire I take away from this is to have contextual gitignores.  
