---
title: "The Home Row"
date: 2025-07-23T10:17:53+05:30
categories: ["Configs"]
tags: ["emacs","evil","vim","peeve","mood"]
---

Getting a little pedantic with my doom configs[^1] these days..  

``` elisp
(defmacro generate-bindable-lambda (&rest body)
  `#'(lambda ()
       (interactive)
       ,@body))

;; .. the home row ..
(map! :map evil-normal-state-map
      "C-M-i p" (generate-bindable-lambda (insert "+"))
      "C-M-i n" (generate-bindable-lambda (insert "-"))
      "C-M-i u" (generate-bindable-lambda (insert "_"))
      "C-M-i e" (generate-bindable-lambda (insert "=")))
```

Maybe I should consider buying foot pedals..,  and eye trackers (3 screens at the moment ) ..,  and setting up an array of interface sensors to truly begin exploiting emacs..,
to the point of conducting an orchestra of text buffers.., somewhat musically (/ whimsically?)..

[^1]: https://github.com/rajp152k/.dotfiles/blob/master/doom/.config/doom/config.el
