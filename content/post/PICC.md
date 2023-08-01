---
title: "PICC: pragmatics of intellectual consumption and creation"
date: 2023-08-1T10:40:55+05:30
categories: ["Skills"]
tags: ["incentives","skills","index","speed-reading","touch-typing","efficiency","emacs","vi"]
---

> *There's a better way to do it - Find it.*  
> *Thomas Alva Edison*  

Managing one's intellectual appetite in these times where information
(and - a lot of - noise) on any domain is available effortlessly and
in vast amounts is quite an ordeal. Even though we have superior
tooling and methods at our disposal to plough through these dense
knowledge forests, coming up with the right set of tools for
oneself is a commendable task in itself. In this post, I sketch out
how one could go about making such choices practically, from why you
should bother to what tangible actions you can get started with to set
yourself off on this journey sensibly.

### Pre-requisites

- The following is of no use to you if you aren't a little info-hungry
and are just the "when I cross that bridge" guy : any pursuit today
requires maintaining efficient intellectual pipelines and I hope this
isn't an after-thought for you.
- A welcome plus would be if your eyes twinkle at the idea of
manipulating your notes pretty close to the speed of thought. That would involve the following operations:
- search
- edit (additions/prunes)
- creating linkages
- observing backlinks
- being able to maintain large mental and external caches
relevant to a domain
- training explicitly with these tools with real projects

With that out of the way, ...

## Why bother ..

 .. finding the best tools and methods for your needs when
generic-solutions are good-enough and allow you to get started without
an extensive setup?  

I'd say this is a short term play and doesn't take into account the
future you's convenience. You might get a project's knowledge base
maintained via one set of principles and tools but that's not the only
one you'll do throughout your life. You might wish to port ideas
between projects maintained with different methods or would even like
to maintain generic notes that don't fit any project. It'll be a
large unelegant mess if you don't actively invest some effort into
getting things right before you begin. Although it might slow you down
for the sprint, you'll be better off in the marathon. Efficiency in
the wild isn't about linear progress but phases of waxing and
waning. You might ultimately reach a ceiling that is way beyond your
expectations from when you started out - you'll have your past self's
grit and obsession with productivity to thank for. However, rather
than going all out right away, easing into this idealogy of a
controlled obsession will keep you in the game longer.  

Before proceeding towards the specifics, understanding ... 

## .. When ..

 .. to cash in your profits and cut down on your proverbial "time"
 loss is tricky to figure out - you might fall for the trap that
 sophisticated procrastination is. I personally prefer learning
 aggressively during rests between major projects and then
 incorporating what meta-skills I learned actively into the next
 project. These long consolidation phases really do help with this
 problem and you really know for sure if switching to the "better" now
 would offset the short term demands or not.  
 
## What ..

.. core activities should you focus on when getting started with this
pursuit?  

### Text

Well, text is the common medium that can represent all that we wish
to, with considerable completeness. An image might be better suited to
certain individuals dependent on their work but text is complete and
more potent than images. Relevant charts and graphs can be easily
generated with minimal code and is a more efficient way than picking
up the mouse (eg: mermaid with org-babel).  

Also, I'd suggest sticking to an electronic format for your over-all
store than hand-written notes due to obvious reasons. Quills and
parchments (and derivatives thereof) are romantic, no doubt, but highly impractical.  

### Basic IO

So, for starters, optimizing your interaction with
computers and documents with some core skills like speed reading and
touch typing might be a decent choice. The latter is considerably
easier that the former to maintain which - fortunately or
unfortunately - means that you rent the former skill -> you can lose
it without regular practice and might need considerable effort to be
effortless again. You'll still always be better than if you'd never
picked it up but ..., it feels good to comprehend large sections of
text swiftly.  

I personally invested around 45 mins a day for around 40 days
following the book ["Breakthrough rapid reading" by Peter
Kump](https://www.goodreads.com/book/show/100800.Breakthrough_Rapid_Reading)
around two years ago. I gained an average speedup from 200 wpm to 500
wpm for moderately complex material without sacrificing
comprehension. As of now, without practice, I can lazily achieve 400
wpm simply due to the habits I learned then. When I've slept well and
focus explicitly, I might even clock in a respectable 800 wpm.  

As for touch typing, you can refer any of the numerous online
platforms that ask for around 10 minutes of practice a day for around
a month and you'll be proficient enough that you don't need to carve
out time to directly practice touch typing. This is an important step
as I'll soon be directing you to ditch the mouse and forget that it
exists. You can expect speeds of upto 100 wpm when you've slept well
and testing yourself after months of using the skills in real
projects - you'll never be thinking this fast but it's good to ensure
that this isn't a bottleneck when note-taking/generating drafts.  

### Editing

Now that you don't have to look at the keyboard and are ready to dump
the mouse, I'd highly suggest you learn vi (even if you use vanilla
emacs) and get pretty good at it: vim was my main environment for
around 18 months and I'd recommend you have a few main goals when
learning it:
 - understand the philosophy of modal editing and the incentives for
   the specific binds.
 - understand why you'd like to customize your setup and what are the
   limits of something that looks so basic and is decades old.

Some resources that I used if you'd like to explore it a bit further:
 - a search on how to quit vi
 - the inbuilt help system and vimtutor (`:help  ... <RET>`)
 - https://learnvimscriptthehardway.stevelosh.com/
 
Vi pays off that initial investment in dividends every day till the
day you stop using a computer. I use evil emacs, vim keybindings in
any gui browser I use, within VS code when I need a quick temporary
dev setup for work and the first thing I check for any programmer
oriented tool is if it follows a similar modal philosophy and doesn't
force the mouse on me.  

If you've reached this point, you're already pretty satisfied with
yourself and may consider thinking you've found your sweet comfy
efficiency optimum for eternity. Well .., fortunately .., you
haven't. You might still be relying several distinct pieces of
programs to get stuff done held together with generic glue that isn't
aware of what you're do or is based on assumptions you can't assert
anywhere... This is the time you should start thinking about having a
cohesive ..  

### Ecosystem

Context switching between different tools is a pain and to make the
next leap you need something to be able to bring it all together in a
neat, sophisticated package - a unifying philosophy that just
works. I found my unifying ecosystem 2 years ago with emacs and I've
never regretted that initial lack of productivity incurred when
adapting my way work environment and would never second guess that
choice if I could time travel. This post isn't meant to describe the
tooling in depth but just serve as an index, as a potential
roadmap... With that being said, I will be posting a lot about Emacs
in the future and how I use it - I'll take you as my padawan and be
glad to initiate you to the dark side.  

Now that you're equipped to blaze past all those blogs, papers and the
internet, you should stop and consider ..

## .. Whether ..
	
.. you should be consuming all that you do. Most of the noise (aka
news) is shoved down your throat and isn't a choice. Some primitive
steps you can employ to avoid choking from whatever falls upon your
retina are ear drums:
 - be disciplined in your pursuits : there is a fine line between
   curiosity and being distracted.
 - delegate the work of finding quality content to the wisdom of the
   crowds (stabilize your sources: I use
   <https://news.ycombinator.com/> and RSS(really simple syndication)
   for some specific sources)

# Conclusion

With all that I've indexed, I hope this post inspires you to look at
your consumption/creation pipelines in a new light and sparks the
same enthusiasm I harbor towards regularly sharpening the
proverbial intellectual axe - do chop away : I'd be glad to read
about your epistemological anvils and furnaces.
