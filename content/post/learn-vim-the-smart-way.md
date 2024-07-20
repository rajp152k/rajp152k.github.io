---
title: "Learn Vim the smart way"
date: 2023-10-20T19:18:08+05:30
categories: ["Book"]
tags: ["microessays","emacs","vim","text","macros","registers","book","efficiency","productivity","tmux","unix","maturity","evil"]
draft: false
---

I've been building up my vimrc again because emacs' tramp mode just
wasn't cutting it when it came to speed for my remote work
environments.  

I've been a vim user for around 4 years now and having read some books
partially and sampling a lot of blogs and conference recordings over
this span, I decided I should commit and formally invest into a
definitive resource to get me upto speed and beyond.  

I'd began [Learn vim the hard
way](https://learnvimscriptthehardway.stevelosh.com/) before I shifted
to emacs fulltime but I decided emacs lisp was much better than
learning vimscript for a longer time horizon.  

I definitely am not leaving emacs anytime soon. All my writing and
personal projects will be hosted by evil gccemacs and will only be
using vanilla vim + tmux setup for python, shell and relevant data
science oriented utilities on my remote setup.  

So, Given my hyper-enthusiastic personality when it comes to reading
everything before I begin with something : I decided to read the book
[Learn vim the smart way](https://leanpub.com/learnvim).  

I learned a lot in [4 dense
days](https://buffer.thebitmage.com/20231017105418-vim.html) (everything
before 0x217B (inclusive) pertains to comments in the book) and was
blown away by some pretty neat peculiarities as well.  

I would say that all the CLI interaction made me reminisce about my
sophomore year in university when I was in awe of the terminal and
first began blogging in a minimal setup with markdown files via jekyll
in vim: this was a few months before the pandemic I believe. Blogging
and the terminal is what kept me intellectually ticking.  

Emacs did come in later on because I considered my options to upgrade
my productivity:
 - learn a whole bunch of unix utilities to fully exploit vim (command
   mode, etc)
 - learn one unified software that can do everything and more
 
Plus, the affinity of the parenthesis made it pretty easy to choose.  

Getting back to the point, I've setup a minimal [dot file](https://buffer.thebitmage.com/20231020193344-vimrc.html) right now
that allows me get things done without much overheads.  

I don't particularly miss being out of emacs, I consider I'm mature
enough now (I would definitely throw a tantrum a couple years ago) to
not associate work with the tool but just get things done.  

I mean, I still do use evil emacs and learning about the core of vim
more would still level up my editing game, so its not really a
equal comparison. Emacs still does encompass everything.  

For instance, just one of the many new things I realized from this
productivity fiasco (exaggerating) is that vim macros and registers
are just different interpretations of the same underlying data
structure.  

Macros are code and Registers are the source of fetching instructions
of that code.  

The craziest thing I've done recently is write a contorted recursive macro
by debugging it by printing it as contents of a register and yanking
the updates, post editing into the same variable to test it out as a macro again,
only to repeat until success.  

Need I say more..., the day I started out editing text in VS code in
freshman year, I never thought I'd be able to be so lazy in the
future when it comes to manipulating programs: thanks to the book, I'm
thinking much more and moving much less than I used to 4 days ago.
