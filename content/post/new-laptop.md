---
title: "Thinkpad X13 Gen 4 AMD Ryzen Pro 7840U & Workflow Review"
date: 2024-06-06T17:17:59+05:30
categories: ["tooling"]
tags: ["emacs","doom","fedora","thinkpad","amd","ryzen","lenovo","linux","gnu","vim","alacritty","firefox","spotify","network","hardware"]
---

I recently shifted my operations to a thinkpad x13g4amd (Ryzen 7840U + 780M Radeon) and am using this transfer as an opportunity to realize and improve my work related habits.  

## GNU/Linux

All of my pipelines are based around Linux and the core GNU utils. I had to use windows for a while due to org-wide constraints but I've recently been given the signal to shift to linux.  

I rarely used any windows native tools for my workflows and there was always a layer of linux emulation/virtualization (wsl, scoop, and the likes) upon which I conducted my usual operations. Given I use Debian at home, a non native linux experience was frustrating at best and depressing at worst. No more, do I have to confine myself.  

## Fedora/Doom-gccEmacs

Initially I entertained (read "failed installation due to hardware incompatibilities" (kernel panics)) the thought of Qubes for a while but running a hypervisor given I already am ssh'ing into multiple virtual machines seemed to be an unnecessary overhead.  

Dropping that idea, I turned to Fedora, thanks to a [description that couldn't be ignored](https://www.reddit.com/r/Fedora/comments/r70j4d/why_you_should_use_fedora/).  

Initial perspectives: just the sweet spot between bleeding edge and hammer stable. I've broken Arch before and do continue to use Debian to date so I do appreciate the consumer market that Fedora is going for.

The only issue (feature not bug) you might need to explicitly take care of in the latest distribution (I'm on Fedora 40 workstation) is [to disable MAC Address Randomization](https://fedoraproject.org/wiki/Changes/StableSSIDMACAddress) (good for security, but useful corporate networks that whitelist addresses).

It's not perfect but it does come ~95% of the way there. You might have to fix some drivers manually and will regularly experience the joy of fixing a new issue from time to time. So far the only major irk is the Quectel EM05G WWAN module not working post the first suspension of your system. After a reboot, you might need to [manually unlock](https://foundata.com/en/blog/2024/quectel-em05-g-thinkpad-t14-gen4-fedora-linux/) the module.

I do use a window manager for my home setup (i3wm) but am going for K DE Plasma 6 with this one (not a fan of the default Gnome DE) while I'm transferring my workflows into CLI based routines.  

Honestly I don't think I'll be shifting to i3wm anytime soon as I do spend most of my time in emacs and firefox, the former of which is a good operating system in itself.

On that note, I recently shifting from vanilla Emacs to Doom and have been enjoying the defaults while not being blindsided to what's under the hood (been using vanilla for 3+ years now, and used vim for 18 months before that (cumulative 5)).  

It's been 3 days into Doom and I appreciate the convenience and the power (recommend you use vim and emacs separately for a considerable duration before skipping to doom) - I don't experience any trade-offs yet.  


## Hardware

This is my first (of many definitely (going to have a thinkpad shelf I bet)) Thinkpad(s) and now I understand what they're all about.  

I'm using a smaller model (<14 inches) for portability (so that I can write anywhere) and a battery (52.5 WHr) life optimized build (opted for a low power 400 nit screen) with the AMD Ryzen Pro 7840U : and it's definitely not a disappointment - upon normal usage from my standards (spotify, emacs, alacritty, firefox), it estimates around 13 hours of usage, and that is nice.  

The keyboard is just the right snappy and is fun to type with. I don't use the touchpad much and am not experienced in what makes a good touchpad so all I can say is there's nothing that disappoints me about it.  

It does catch on fingerprints fairly easily and you might need some time adjusting to it. I, however, am not of the mind that a scratch ruins the build but rather see them as trophies, so what's a temporary smudge anyway.  

## Thoughts

Good stuff.., will enjoy work more henceforth - you definitely can't be sad when you get to spend your days in emacs.  
