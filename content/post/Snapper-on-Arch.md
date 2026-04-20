---
title: "Setting up snapper on Arch"
date: 2026-04-20T18:42:10+05:30
categories: ["Tooling"]
tags: ["arch","opensuse", "tumbleweed","snapshots","btrfs","bed rock linux", "linux"]
---

had thinkpad to spare; old opensuse tumbleweed; snapper on btrfs was convenient post mess ups.

don't like distrohopping, like rolling releases, like docs, like snapper - installed arch (arch wiki's great), will hijack with bedrock linux [^1] some day.

installed with minimal defaults first(systemd-boot instead of grub), later decided to setup snapper : an involved process: crude state transitions as follows:
 - systemd-boot + UKI -> grub + initramfs 
   - grub-btrfs convenience
   - readily shows snapper snapshots
 - setup pacman (pre and post mutation, temporal) snapper snapshot creation and cleanup hooks
 
been my DD for a while now : sway + waybar, wayland, gcc emacs, tmux, some handrolled CSS, a bunch of TUIs: been fun

BedRock Linux Hijack soon

[^1]: https://bedrocklinux.org/
