---
title: "Doom Emacs config'd for Python"
date: 2024-09-19T15:10:44+05:30
categories: ["Python"]
tags: ["conda","python","mamba","emacs","doom","lsp-mode","pyright","language-server-protocol","lsp","miniforge","org-babel","org","conda",]
---


Alter your doom block in init.el:
``` elisp
(doom! 
    ...
    :lang 
    (python +lsp +pyright +conda)
    ...)
```

I recommend pyright, is snappier than pyls..

you'll also need lsp enabled in your tools, I also have `+peek`

``` elisp
(doom! 
    ...
    :tools
    (lsp +peek)
    ...)
```

for more info, hit `<space> h d m lsp<CR>`

Alter your config.el (I use miniforge to get mamba and conda):

```elisp
                                        ; Conda
(use-package! conda
  :config
  (setq conda-anaconda-home (expand-file-name  "~/mambaforge"))
  (conda-env-initialize-interactive-shells)
  (conda-env-initialize-eshell)
  (conda-env-autoactivate-mode t)
  (add-hook 'find-file-hook (lambda () (when (bound-and-true-p conda-project-env-path)
                                    (conda-env-activate-for-buffer)))))
```


Once that's done, hit `<space> h r r` and your ready to go.

Activate the env your working on `M-x conda-env-activate ...` and can get on with the usuals ..

for more info checkout the local docs for `:lang python` (hit `<space> h d m python <CR>` and it should pop up) ..


If any jargon is too jargony, google a little and you should be fine.  

The setup works great, would recommend using the repl here and an org-babel based literate programming setup instead of juptyer notebooks.

