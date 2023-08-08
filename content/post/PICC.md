---
title: "PICC: pragmatics of intellectual consumption and creation"
date: 2023-08-01T10:40:55+05:30
categories: ["Skills"]
tags: ["incentives","skills","index","speed-reading","touch-typing","efficiency","emacs","vi"]
---

> *There's a better way to do it - Find it.*  
> *Thomas Alva Edison*  

Managing one's intellectual appetite in these times of information
(and noise) excess is quite an ordeal. Given superior
tooling and methods to plough through dense
knowledge forests, coming up with the right set of tools for
oneself is still a commendable task. In this post, I sketch out
how one could go about making such choices practically, from why you
should bother, to what tangible actions you can get started with.

### Pre-requisites

The following is of no use to you if you aren't a little info-hungry
and are just the "when I cross that bridge" guy : any pursuit today
requires maintaining efficient intellectual pipelines and I hope this
isn't an after-thought for you.

With that out of the way, ...

## Why bother ..

 .. finding the best tools and methods for your needs when
generic-solutions are good-enough and allow you to get started without
an extensive setup?  

I'd say this is a short term play and doesn't take into account the
future you's convenience. You might get a project's knowledge base
maintained via one set of principles but that's not the only
one you'll do throughout your life. You might wish to port ideas
between projects maintained with different methods or would even like
to maintain generic notes that don't fit any project. It'll be a
large unelegant mess if you don't actively invest some effort into
getting things right before you begin. Although it might slow you down
for the sprint, you'll be better off in the marathon. Efficiency in
the wild isn't about linear progress but phases of waxing and
waning. You might ultimately reach a ceiling that is way beyond your
expectations from when you started out. You'll have your past self's
grit and obsession with productivity to thank for then. However, rather
than going all out right away, easing into this idealogy of a
controlled obsession will keep you in the game longer.  

Before proceeding towards the specifics, understanding ... 

## .. When ..

 .. to cash in your profits and cut down on your proverbial "time"
 loss is tricky to figure out - you might fall for the trap that
 sophisticated procrastination is. I personally prefer learning
 aggressively during rests between major projects and then
 incorporating what meta-skills I learned actively into the next
 project. These intermittent consolidation phases give me a break from
 what would otherwise be a pretty boring and unidimensional intellectual life.
 
## What ..

.. core activities should you focus on when getting started with this
pursuit?  

### Text

Well, text is the common medium that can represent all that we wish
to, with considerable completeness. An image might be better suited to
certain individuals dependent on their work but text is complete and
more potent than images. Relevant charts and graphs can be easily
generated with minimal code which is more efficient than touching
the mouse (eg: mermaid with org-babel).  

I'd suggest being digital all the way for your over-all
store than having some hand-written notes due to obvious reasons. Quills and
parchments (and derivatives thereof) are romantic, no doubt, but
highly impractical. When completely digital, you have the opportunity
of setting up custom pipelines and triggers between tools if you wish
to be a little more serious in this endeavor.

### Basic IO

On the context of digitizing your knowledge forest, optimizing your interaction with
computers and documents with some meta skills like speed reading (for
screens and not just books) and touch typing might be a decent
choice.  

I personally invested around 45 mins a day for 40 days
following the book ["Breakthrough rapid reading" by Peter
Kump](https://www.goodreads.com/book/show/100800.Breakthrough_Rapid_Reading)
around two years ago. I sped up from 200 wpm to 500
wpm for moderately complex material without sacrificing
comprehension. As of now, without practice, I can lazily achieve 400
wpm simply due to the habits I learned then. When I've slept well and
focus explicitly, I might even clock in a respectable 800 wpm.  

As for touch typing, you may refer any one online
platform that demands a relatively measly 10 minutes of practice a day for around
a month : from this point forth, you'll be proficient enough at this point that you don't
need to explicitly carve out time to practice touch typing. This is an important step
as you'd definitely be ditching the mouse soon, given you like
speed. You can expect speeds of upto 100 wpm when cognitively fresh.
You'll probably never be thinking this fast when programming.  

Albeit, It's good to ensure that you aren't IO bound when
note-taking/generating drafts when reading technically dense
material.

### Editing

Now that you love keyboards and text, I'd suggest you learn vi
(even if you use vanilla emacs) and get pretty good at it: vim was my
main dev and intellectual ecosystem (with the unix utilities) for
around 18 months and I'd recommend you have a few main goals when
doing so:
 - understand the philosophy of modal editing and the semantics for
   specific binds (most of them are pretty intuitive).
 - understand why you'd like to customize your setup and what are the
   limits of something that looks so basic and is decades old (I was
   personally amazed initially as to why ancient software (without
   extreme philosophical upgrades) is still in
   active use and development today (referring to vim and emacs)).

Some resources that I used if you'd like to explore this a bit further:
 - a search on how to quit vi
 - the inbuilt help system and vimtutor (`:help  ... <RET>`)
 - https://learnvimscriptthehardway.stevelosh.com/
 
Vi pays off that initial investment in dividends every day till the
day you stop using a computer. I use evil emacs, vim keybindings in
my gui browsers, within VS code when I need a quick temporary
dev setup for work and the first thing I check for any programmer
oriented tool is if it follows a similar modal philosophy and doesn't
force the mouse on me.  

If you've reached this point, you're already pretty satisfied with
yourself and may consider thinking you've found your sweet comfy
efficiency optimum for eternity. Well .., fortunately .., you
haven't. You might still be relying several distinct pieces of
programs to get stuff done, held together with generic glue that isn't
aware of what you're doing or is based on assumptions you explicitly assert
anywhere... This is the time you should start thinking about having a
cohesive ...   

### Ecosystem

Context switching between different tools is a pain and for the
next big leap, you need something to be able to bring it all together in a
neat, sophisticated package - a unifying philosophy that doesn't just
works - it hypnotizes you into its doctrines. I found my unifying
ecosystem 2 years ago with emacs and I've never regretted that initial
lack of productivity incurred when porting my work environment from
vim.  

This post isn't meant to describe the
tooling in depth but just serve as an index, as a potential
roadmap...  

With that being said, I will be posting a lot about Emacs
in the future and how I use it - I'll take you as my padawan and be
glad to initiate you to the dark side.  

Now that you're equipped to blaze past all those blogs, papers and the
internet, you should stop and consider ..

## .. Whether ..
	
.. you should be consuming all that you do. Most of the noise (aka
news) is shoved down your throat and isn't a choice. Some primitive
steps you can employ to avoid choking from whatever falls upon your
retina and ear drums:
 - be disciplined in your pursuits : there is a fine line between
   curiosity and being distracted -> I struggle with this from time to
   time and have only recently grasped what balance is.
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
