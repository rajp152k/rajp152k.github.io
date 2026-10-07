---
title: Using Autolith so far
date: 2026-10-07T03:52:29Z
---

# Abstract

raj has started to use Autolith for local setup and blog work. This log records the Lisp environment, shared settings, development checkout, and writing workflow established so far.

# Context

raj spent about half a day exploring Autolith on a Fedora VPS. Autolith runs in a live Common Lisp image. It provides a place to work with code, files, and processes through conversation.

raj's meditation, "the lisp machine," records the personal reason for this work. raj wants to return to Lisp and develop side projects. This log records the concrete setup and its current limits.

# A Lisp environment on the VPS

raj chose the ncurses build of Lem instead of Emacs for Lisp editing. The Lem setup includes Vim bindings. Shared settings live in the dotfiles repository and load from a Common Lisp init file.

This provides a terminal editor beside Autolith. The editor settings can be installed again without copying local history or generated files.

# Shared Autolith settings

raj added an Autolith package to the dotfiles repository. Its init file sets the model, reasoning effort, reasoning traces, and Simple Technical English. A separate local init file can supply machine-specific settings.

The shared package records the intended setup. Credentials, conversations, caches, and other runtime state stay outside that package. This separates portable configuration from the state of one machine.

# A separate development checkout

raj created a fork of Autolith and a local development checkout. The checkout has raj's fork as its origin and the original project as its upstream.

The development checkout is separate from the installed Autolith release. It is also separate from private changes to the running image. This gives raj a place for future source changes without treating local setup as a change to the project. This log does not record a new Autolith source feature.

# Preparing the blog for local work

raj used Autolith to prepare the blog's local embedding and build environment. The setup uses a separate Python environment for inference and Node.js for the site assets. Local checks covered embedding freshness, the site build, and the Python and JavaScript tests.

Markdown is the source of each post. The embedding updater stores archive state in blog.sqlite. The site builder produces the local site, search index, and shared map.

During the setup checks, existing entries reused their stored vectors. Those checks verified the local workflow, but did not exercise a new model download or new inference.

# Bringing the log rules into Autolith

raj already used the ops-log skill in OMP to write operational logs. Before installing that skill in Autolith, raj asked for a review of the skill and the blog workflow.

The Autolith version keeps the same writing rules. Logs explain raj's work and intent. They use title and date front matter, an Abstract, Context, named sections, a Conclusion, and links to relevant past posts. New prose uses Simplified Technical English. Short sentences must still contain the material decisions and results.

The skill also tells Autolith where to start: the local blog checkout. Autolith must read the current README, check existing posts, preserve unrelated changes, and verify the local preview.

# Installing the skill as a regular file

The installed skill is a regular-file copy inside Autolith's configuration directory. The dotfiles package excludes skills from Stow and documents the copy step. Autolith lists ops-log in its skill catalog.

After a change to the tracked skill, the installed copy needs an update.

# Review before commit and publication

raj keeps personal meditations separate from agent-written logs. Both collections use the same archive, search, and map. A log does not authorize an edit to raj's meditation prose.

A request for a draft starts local iteration. Autolith updates the embedding state and builds a preview for review. A revision does not approve a commit. A commit request does not approve a push or publication.

The copied skill records these boundaries. This draft is the first local log written with that Autolith setup.

# Conclusion

raj now has a local Lisp editor, shared Autolith settings, a separate development checkout, and a working blog setup. Autolith can use the existing operational log rules when raj requests a record of work.

This is an initial setup, not a report of completed side projects or new Autolith features. raj can refine the workflow through further use. The current log is a local draft for review.

# Past relevant meditations and blogs

- [the lisp machine](/the-lisp-machine/): raj's account of exploring Autolith and preparing the VPS for Lisp work.
- [Two collections, one archive](/logs/2026-10-06-two-collections-one-archive/): the separation between personal meditations and requested agent logs.
