---
title: "My Emacs Configuration"
date: 2023-08-17T11:23:10+05:30
categories: ["Configs"]
tags: ["emacs","lisp","emacs-lisp","config","straight.el","general.el","evil","vi","magit","org","org-roam","yaml"]
draft: false
---

**[*As of 0x213B : 2023-08-17 Thu*]**

I use emacs for a lot of my daily tasks and spend majority of my time
in it. This is a review of some significant components of my init.el

---

``` elisp
;keyboard all the way
(menu-bar-mode -1)
(tool-bar-mode -1)
(scroll-bar-mode -1)
```

----


``` elisp
;I don't like distractions
(setq byte-compile-warnings '(cl-functions))
(setq ring-bell-function 'ignore)
(setq visible-bell t)
```

----

I chose the most recently engineered package-management solution when I began with emacs, haven't switched
since and don't think I'll need to. Migrating from vim, I preferred a
configuration file rather than installations via melpa interface.
Also, freezing and thawing is cool : exact reproducibility is guaranteed.
``` elisp
;;BOOTSTRAPPING STRAIGHT.EL (defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name "straight/repos/straight.el/bootstrap.el" user-emacs-directory))
      (bootstrap-version 5))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/raxod502/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))

(straight-use-package 'use-package)
(setq straight-path "~/.emacs.d/straight/")
```
---

Again, I chose the most well-thought out packages when I began two
years ago: I don't particularly know the ins and outs of `general`
but I do know it can do what I wish for elegantly and the proper way

``` elisp
;GENERAL + binding free ups
(use-package general
  :straight t
  :config
  (general-unbind
    "C-M-o" ; free up for org-roam *Notes*
    "C-M-r" ; free up for remote ops
    "C-s" ; for super bindings
	))
```

----

I like being greeted by cultish messages and calls to freedom when I
get to work. Also serves as an index for the most recently and the
most frequently accessed files.

```elisp
;DASHBOARD
(use-package dashboard
  :straight t
  :config
  (dashboard-setup-startup-hook)
  (general-define-key
   "C-c h" (lambda () (interactive)(view-buffer "*dashboard*")))
  (setq
   initial-buffer-choice (lambda () (get-buffer "*dashboard*"))
   dashboard-center-content t
   dashboard-startup-banner 'logo))
```

---

I wouldn't be using emacs if not for this. Modal editing is a must and
not using vi keybindings once you're used to them is an extremely questionable
 way to go about your life.

```elisp
;EVIL ENV
(use-package evil
  :straight t
  :init
  (use-package undo-fu
    :straight t
    :config
    (general-define-key
     :states 'normal
     "u" #'undo-fu-only-undo
     "\C-r" #'undo-fu-only-redo)
    (setq evil-undo-system 'undo-fu))
  (setq
   evil-want-keybinding nil
   evil-want-integration t)
  :config 
  (evil-mode 1))

(use-package evil-collection
  :straight t
  :after evil
  :config
  (evil-collection-init))

(use-package evil-org
  :straight t
  :after org
  :config
  (general-add-hook 'org-mode
		    (list #'evil-org-mode))
  (require 'evil-org-agenda)
  (evil-org-agenda-set-keys))

(use-package evil-surround
  :straight t
  :config
  (global-evil-surround-mode 1))
```

---
Supercharges any lookup and makes any basic operation much more user
friendly.

``` elisp
;HELM
(use-package helm
  :straight t
  :config
  (general-define-key
   "M-x" #'helm-M-x
   "C-h a" #'helm-apropos
   "C-/" #'helm-occur
   "C-x C-f" #'helm-find-files)
  (helm-mode 1))
```
---
Ack'ing large directories and getting referenced instances of all
occurences of a pattern in a matter of seconds is not bad.

```elisp
;PROJECTILE
(use-package projectile
  :init
  :straight t
  :config
  (projectile-mode 1)
  (use-package helm-projectile
    :straight t
    :config
    (general-define-key
     :prefix "C-c p"
     "f f" #'helm-projectile-find-file
     "f d" #'helm-projectile-find-dir
     "a" #'helm-projectile-ack)))
```

----

There's an adage going around since I don't know when: This is the
last file manager you'll ever need.

``` elisp
;FILE MANAGEMENT : DIRED-X
(setq find-file-visit-truename t)
(general-add-hook 'dired-load-hook
		  (list (lambda ()
			  (load "dired-x")
			  ;; Set dired-x global variables here.  For example:
			  ;; (setq dired-guess-shell-gnutar "gtar")
			  ;; (setq dired-x-hands-off-my-keys nil)
			  )))
```

----

Guilty as charged : my emacs isn't vanilla...

``` elisp
;AESTHETICS
(use-package darkroom ;; when reading/writing 
  :straight t)
(use-package nimbus-theme ;; a healthy mix all the shades you need to
  be evil
  :straight t
  :config
  (load-theme 'nimbus t))
(use-package beacon
  :straight t
  :init
  (setq beacon-size 60 
	beacon-blink-when-focused t
	beacon-blink-when-point-moves-vertically 5
	beacon-blink-when-window-changes t
	beacon-color "#4444bb"
	beacon-blink-delay 0.2
	beacon-blink-duration 0.2)
  :config
  (beacon-mode 1))
```

----
Hot-reloads and some buffer space to mess around with new
components I'm testing out.

``` elisp
;QUICK CONFIG
(defun edit-init ()
  (interactive)
  (message (concat "editing user-init-file @ " user-init-file))
  (find-file user-init-file))

(defun open-scratch-space ()
  (interactive)
  (message (concat "opening scratch space @ /mnt/c/Users/Raj Patil/source/scratch" ))
  (find-file "/mnt/c/Users/Raj Patil/source/scratch"))

(general-define-key
 :prefix "C-c"
 "e" #'edit-init
 "s" #'open-scratch-space)
 ```

-----
This makes organizing multiple workspaces and panes easy and you're
missing out on a lot if you don't have sensible tab-management figured out.

``` elisp
;Window management
(use-package window-purpose
  :straight t
  :config
  (purpose-compile-user-configuration)
  (general-define-key
   :prefix "C-c ,"
   "d" #'(lambda ()
	   (interactive)
	   (message "dedicating current window")
	   (set-window-dedicated-p (selected-window) t))
   "u" #'(lambda ()
	   (interactive)
	   (message "undedicating current window")
	   (set-window-dedicated-p (selected-window) nil))))
```
----

The self-documenting editor in action...

``` elisp
;WHICH-KEY
(use-package which-key
  :straight t
  :config
  (which-key-mode)
  (general-define-key "C-h C-k" #'which-key-show-top-level)
  (which-key-setup-side-window-bottom))
```
----

I prefer reading technical texts right within emacs besides my notes..

``` elisp
;PDF INTEROP
(use-package pdf-tools
  :straight (pdf-tools :host github
		       :repo "vedang/pdf-tools")
  :config
  (pdf-loader-install))
```

-----

Magical Git : I haven't used this in a while and mostly use the eshell
interface for basic stuff but I can vouch for the unparalleled
experience it provides in terms of executing even the most complicated
operations with a few chords and strokes. Now that's Magit.  

If you like the the interface in itself and would like to implement a
similar functionality for your extensions, checkout [Transient](https://github.com/magit/transient) or [Hydra](https://github.com/abo-abo/hydra)
``` elisp
;MAGIT
(use-package magit :straight t)
```

-----

Well, enough can't be said about this. All of it can be
[documented](https://orgmode.org/) though........,
[right](https://orgmode.org/worg/)......?  
Do note that you might need to checkout a specific commit of org-mode
if you also wish to use org-roam (some recent releases are breaking
and I personally am not aware of exactly what breaks what stuff..).  

The tag line should be enough to hook you:
> your life in plain text.

If it isn't, you probably are the kind of person that uses the mouse a
tad too much and many programmers - along with me - will be judging
you hard for that.  

Org is an ecosystem in itself and I'm not including my capture
templates, tree manipulators, and babel bindings in here to keep
things concise...

``` elisp
;ORG-OPS
(put 'narrow-to-region 'disabled nil)
(use-package org
  :straight t
  :config
  (general-define-key
   :prefix "C-c"
   "l" #'org-store-link
   "a" #'org-agenda
   "c" #'org-capture
   "!" #'org-time-stamp-inactive)
  (setq org-directory (file-truename "~/source/org/")
	org-default-notes-file (concat org-directory "/gtd/GTD_HQ.org")
	org-startup-with-inline-images t
	org-startup-truncated nil)
  (general-add-hook 'org-mode-hook
		    (list #'toggle-word-wrap
			  #'flyspell-mode
			  #'nlinum-relative-mode))
  (defun update-org-latex-fragments ()
    (org-latex-preview '(64))
    (plist-put org-format-latex-options :scale (* 2 text-scale-mode-amount))
    (org-latex-preview '(16)))
  (general-add-hook 'text-scale-mode-hook
		    (list #'update-org-latex-fragments))
  (setq org-latex-packages-alist '(("margin=2cm" "geometry")))
  (setq org-clock-persist 'history)
  (org-clock-persistence-insinuate)
  (general-define-key
   :prefix "C-c"
   "r" #'org-refile
   "C-x C-g" #'org-clock-goto))
   
```
-----

I've used notion, obsidian, vimwiki, evernote, and anything that was
available before I settled on org-roam (well .., roam research was
paid and I could afford to spend time and effort when I was an
undergrad, but not a subscription). 

``` elisp
;ORG-ROAM

  (use-package org-roam
    :straight (org-roam :host github
			:repo "org-roam/org-roam")
    :config
    (setq org-id-method 'ts)
    (setq org-roam-directory (file-truename "/mnt/c/Users/Raj Patil/source/org/braindump/Content/"))
    (setq org-roam-file-extensions '("org"))
    (org-roam-db-autosync-mode)
    (general-define-key
     :prefix "C-M-o"
     "f" #'org-roam-node-find
     "i" #'org-roam-node-insert
     "c" #'org-roam-capture
     "n h" #'(lambda ()
	          (interactive)
	          (find-file (concat org-roam-directory "index.org")))
     "n t" #'(lambda ()
	          (interactive)
	          (find-file (concat org-roam-directory "todo.org")))
     "d s" #'org-roam-db-sync
     "t a" #'org-roam-tag-add
     "t d" #'org-roam-tag-remove
     "r" #'org-roam-buffer-toggle
     "o c" #'org-id-get-create
     "o s" #'org-id-store-link
     "a a" #'org-roam-alias-add
     "a d" #'org-roam-alias-remove)
    (add-to-list 'display-buffer-alist
		 '(; org-roam buffer toggle config
		   (".org-roam.*"
		    (display-buffer-in-side-window)
		    (window-width . 0.25)
		    (side . left)
		    (slot 0)))))

  (use-package websocket
    :straight t
    :after org-roam)

  (use-package org-roam-ui
    :straight (:host github
		     :repo "org-roam/org-roam-ui"
		     :files ("*.el" "out"))
    :after org-roam
    :config
    (setq org-roam-ui-sync-theme t
	  org-roam-ui-follow t
	  org-roam-ui-update-on-save t
	  org-roam-ui-open-on-start t))
```

-----

You definitely need this.

``` elisp
;YAML
(use-package yaml-mode
  :straight t
  :config
  (add-to-list 'auto-mode-alist '("\\.yml\\'" . yaml-mode)))

```

-----

Life is too short to not try a lisp

``` elisp
;LISP ADD ONS

(use-package smartparens
  :straight t
  :config
  (smartparens-global-mode t))
(use-package rainbow-delimiters
  :straight t
  :config
  (rainbow-delimiters-mode-enable))

;;SLIME
(use-package slime
  :straight t
  :config
  (setq inferior-lisp-program "sbcl"))


;;RACKET

(use-package racket-mode
  :straight t
  :config
  (setq racket-documentation-search-location 'local
	racket-images-inline t)
  (general-add-hook (list 'racket-mode-hook 'racket-repl-mode-hook)
		    (list #'rainbow-delimiters-mode)))

;;ELISP

(general-add-hook 'emacs-lisp-mode-hook
		  (list 'smartparens-mode ;;use (kbd `C-q '`) for single quoting
			'rainbow-delimiters-mode))
```

-----

We all have our moments of self-doubt. Independence is a fabricated notion.

``` elisp
;DICTIONARY
(use-package define-word
  :straight t
  :config
  (general-define-key
   :prefix "C-c"
   "d" #'define-word-at-point
   "D" #'define-word))
```
----

You should blog too.

``` elisp
;BLOG

  (use-package easy-hugo
    :straight t
    :config
    (setq easy-hugo-basedir "/mnt/c/Users/Raj Patil/source/thebitmage.com/")
    (setq easy-hugo-url "https://thebitmage.com")
    (setq easy-hugo-root "/usr/local/bin")
    (defun blog ()
      "Open blogging workspace"
      (interactive)
      (let ((blog-dir "~/links/source/thebitmage.com"))
	(message (concat "opening blogging workspace @ " blog-dir))
	(find-file blog-dir)))
    (defun life-hex-count ()
      "number of days I've been alive"
      (interactive)
      (let* ((birth (date-to-time "2000-05-01 19:30 IST"))
	     (today (date-to-time (format-time-string "%Y-%m-%d %H:%M:%S %Z" (current-time)) ))
	     (diff (float-time (time-subtract today birth))))
	(insert (format "0x%X" (/ diff 86400)))))
    (defun hex-ops ()
      "hexify decimal number at point, invoke life hex count if nil"
      (interactive)
      (defun delete-word-at-point ()
		  (kill-word 1)
		  (backward-kill-word 1))
      (defun valid-number-p (str)
	  "Check if a string is a valid number."
		  (string-match-p "^[+-]?[0-9]*\\.?[0-9]+\\(?:[eE][+-]?[0-9]+\\)?$" str))
      (let ((dec-days (word-at-point)))
	(cond ((null dec-days) (life-hex-count))
	      ((valid-number-p dec-days) (progn
					   (delete-word-at-point)
					   (insert (format " 0x%X " (string-to-number dec-days)))) )
	      (t (message "invalid request; ignoring ...")))))
    (general-define-key
     :prefix "C-c C-h"
     "b" #'easy-hugo-newpost
     "C-b" #'blog
     "C-t" #'hex-ops))
```

---

I've skipped over my LSP setup for all the languages that I use and
the accompanying tooling that goes with it..  

If you made it this far, you probably have too much time on your hands
or are considering shifting your dev environment to emacs. In any
case, I'd say you still have too much time on your hands.  

Do comment on how I'm missing out on some other good stuff that - if I
began using - would make me wonder how was life worth living before I
discovered it...  
