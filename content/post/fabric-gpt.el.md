---
title: "I wrote an Emacs Package"
date: 2025-03-16T19:10:48+05:30
categories: ["Tooling"]
tags: ["emacs","automation","fabric","llm","package","lisp","elisp","open-source","software","alacritty","tmux","eshell","tooling","cli","programming","microessays"]
---

Fabric[^1] is a collection of crowd-sourced prompts, exposed via a CLI tool. I used it for a while some time ago but never fully exploited it because I prefer Emacs.  

Eshell buffers are an option, but I am principled in my tool usage and prefer to delegate longer-running CLI tasks to a combination of Alacritty and Tmux.  

Maintaining my Emacs shell usage to ephemeral popups feels natural.  

Gptel[^2] is a versatile LLM client that integrates smoothly into my workflow (buffer/text manipulation and management) without disrupting my thought flow.  

I wanted Fabric's crowd-sourced prompts and patterns to be accessible via Gptel, so I wrote my first Emacs package: https://github.com/rajp152k/fabric-gpt.el.

I often write Elisp for configuration upkeep but needed to explore more to develop a package. I will refine it as new opportunities arise through usage experience.  

Hitting `spc i g f f` launches an M-x style fuzzy complete for the pattern I want to work with, and an LLM request is dispatched with the context preceding the cursor in the current buffer.  

It has made my life a little simpler.  

Check out my [.dotfiles](https://github.com/rajp152k/.dotfiles) for further insights into my Emacs configuration.

[^1]: https://github.com/danielmiessler/fabric
[^2]: https://github.com/karthink/gptel
