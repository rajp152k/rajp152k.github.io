---
title: "Python like a Spartan"
date: 2024-01-18T12:15:48+05:30
categories: ["Tooling"]
tags: ["tmux","nvim","emacs","GNU","utils"]
---

I'm an AI Research Engineer and that involves messing around a little
with python. I've spent the past 4 years perfecting a disciplined,
minimal, but enabling setup.

This is a tour of my trusty set of tools, in the hopes that it will help
you find the same CLI zen that I've been enjoying for a while now.  

## Tmux : towards an Eternal Shell

![tmux](https://ik.imagekit.io/rajp152k/rpdev/setup/tmux.png)

I start my work sessions off by ssh'ing into my remote compute
cluster.  

I Don't type in my passwords all the time and prefer being a little lazy.
So, `sshpass`(stores credentials) and an aliased bash script do the job reliably.

##### *~/remote/dev.sh*

``` bash
#!/bin/bash

sshpass -f ~/remote/dev_pass.txt \
	ssh -t -L 8000:localhost:8000 -p 5522 \
	<username>@<IP> \
	'tmux attach -t hq || tmux new -s hq'
```

Tunnel forwarding comes in handy when you want to use web based
applications or want to run an HTTP server on a whim. You may
additionally range over multiple ports using a bash loop in case you
need to use multiple utilities (Jupyter on one, MkDocs on another for
instance).  

Lastly, don't just drop into the naked shell but into a tmux
session. The command above first attempts to attach to a tmux session
named "hq". Failure results in the creation of such a tmux
server. Success short-circuits the latter's execution and you're into
whatever you were last working on.  

Finally, just dump in a bunch of aliases direct into whatever cluster
you want to, in a jiffy.  

##### *~/.bashrc

```bash
alias dev="~/remote/dev.sh"
alias avx="~/remote/avx.sh"
alias avx_prod="~/remote/avx_prod.sh"
alias avx_resch="~/remote/avx_research.sh"
```


## Edit like you mean it

![vim](https://ik.imagekit.io/rajp152k/rpdev/setup/vim.png)

I've used my fair share of editors to finally have a favourite when it
comes to working remotely and getting to business as soon as
possible.  

For personal projects, I use evil gccemacs and won't ever
stop doing so. However, for remote work, nothing beats the sleekness
of [vim](https://github.com/rajp152k/.cfg-nvim)(using neovim, to be specific)

![emacs](https://ik.imagekit.io/rajp152k/rpdev/setup/emacs.png)

[Emacs](https://github.com/rajp152k/emacs-configs) with tramp mode just doesn't cut it (I haven't tried running CLI
emacs remotely because my keybindings are a little too crazy for a
terminal emulator to manage correctly).  

To summarize, emacs is the souped up tank and neovim + tmux makes for
the vagabond-warrior-way to get on with your job surgically.  

Given we're pretending to be spartans, Neovim + Tmux it is.  

Btw, going minimal doesn't mean you're going unprepared and
compromised. Neovim is relatively minimal to Emacs but it gets the
job done and a whole lot more.  

Moreover, my experience with one enhances my workflow in the
other (I use evil emacs and nvim with Neogit (Neovim's Magit), for
instance (one of several)).  

Also .., don't even think of VS code, just don't...  

## Contain your Enthusiasm

Working on multiple projects might call for working on the same libraries
with different versions. This may be handled easily if you're working
on in a uniform tooling ecosystem like python libraries (check out
[micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) -> that's pretty spartanish) but throw in other
dependencies that a polyglotic application might ask for and you'll quickly
realize the nightmare you've signed up for.  

So.., check out [docker](https://www.docker.com/) and how containers help segregate your mess.  

# Miscellaneous

I also use several utilities that aren't particularly a part of
any specific umbrella of a tool.  

### A Simple HTTP server

```
python -m http.server <port>
```


![python http server](https://ik.imagekit.io/rajp152k/rpdev/setup/emacs.png)

That exposes your current filesystem and has been a convenient tool
when I want to share files across my research cluster on muliple
virtual machines.  

You may just `wget` the specific file from the server or browse the 
directory listing using `lynx`. I'd recommend you reserve this method
for smaller files that you'd like to be accessible across
your cluster.  `rsync` or `scp` are the usual alternatives
otherwise. Of course you could always just access that in a "normal"
browser if you want to access these on your GUI host.  

I personally prefer documenting my code and my thought process the
same time I'm building something so I'd rather fire up a auto documentation
tool that helps me write stuff down in markdown : I use
[mkdocs](https://www.mkdocs.org/) and given that I'm using tmux, my
documented approaches and thought processes are always accessible
over my `IP:port` on the research cluster. So that is also how I
provide context to my team-mates about what I'm up to.  

### GNU coreutils

 The GNU Core Utilities are the basic file, shell and text manipulation utilities of the GNU operating system. These are the core utilities which are expected to exist on every operating system. 

for instance, to quickly check the number of entities in a parent entity I'd use an enlister, piped into the line count variant
of wc.

```
cat records.csv | wc -l
tree cats-and-dogs-directory | wc -l
```

There are some days when I need to manipulate a file in a very old
docker container that doesn't have vim. sed does come in handy such
days and has saved me quite some time, numerous times.

```
sed -i '/good_sentinels/s/42/1729/' your_file.txt
```

Say there's a zombie process lying around
that might need a quick kill: grep and awk
then come in handy :

```
ps aux | grep 'Z' | awk '{print $2}' | xargs kill -9
```

This is just scraping the surface with what you can do with the core
utils. Considering the powerful interface capabilities of these with
vim and you've got yourself an enviable setup running at a fraction of
the compute of what your run of the mill IDE does.  

Farewell, for now, and good luck sharpening your technical repertoire...

> Tools don't make the Trader, but ..., they kinda do...  
> -- I made that up

### P.S.

I side with evil gccemacs in the editor wars...
