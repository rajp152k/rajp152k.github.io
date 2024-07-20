---
title: "Reading an Author"
date: 2023-09-06T16:46:47+05:30
categories: ["Anecdote"]
tags: ["nietzsche","book","philosophy","author","cycle","past","anecdote","rumi","himalayas","passion","ambition"]
draft: false
---

Do note that this is an old post (from my last archived blog) that I'm
refactoring : more on that [here](https://thebitmage.com/post/refactoring-old-works/)

# The Unaltered Entry

## [2022-02-01 Tue 10:11] - 7946

I, hitherto, have been reading books as a single unit of intellectual
conveyance. However, that strategy doesn't work for all the
works. Some authors have their writings crisply intertwined with
their other writings. 

Approaching a single book as a part of a larger intellectual
conveyance is more efficient in the longer term if one intends to read
all the work of a particular author. Consequently, grouping these
reads together has also been somewhat interesting lately.

The first author that I'm reading adhering to this strategy is
Nietzsche. 
On the road to "Thus Spake Zarathustra", I've already read "Beyond
Good and Evil", "Twilight of the Idols", and presently consuming
"Human, all too Human". The next milestones will be "Genealogy of
Morals", "The Antichrist", "The Gay Science". Then I'll move on to
his reflective works: the "Ecce Homo" and the posthumous "The Will to
Power" (not exactly reflective, but will be using his notebooks to
derive reflective insights). Finally, all this will be put to use for
the better understanding of his "Thus Spake Zarathustra". Definitely
expecting to grasp him much better than if all this was consumed sparsely.
This is one reading cycle: will be revisiting the main works again
over the duration of my life.

# The Commentary

- Okay, I actually did end up reading those works in that order up
  until "The Will to Power".
  - It was a slog and worth it.
  - It led to some intricate discussions with an individual I met on
    trek in the himalayas a year ago -> I was 22 and he was probably
    in his 40s so there was some life experience at play as well in
    our conversations.
  - It's rare to find other individuals that are philosophically
    inclined these days and are willing to put in the work to read
    books and actually contemplate upon what they read.
  - we had several insightful heated discussions but yeah, what led to that is
    the fact that we both personally chose to read such books.
  - as a parting note, he recommended I read up on Rumi - the poet.
	- I did put that in my queue and decided I'll get to that when I
      finish the Nietzschean reading cycle.
	  
But ...  

- stuff rolled downhill post that trek (literally and figuratively) in
  all aspects and I never got around to finishing the will to power
  and getting on "Thus Spake Zarathustra" (I'd already secured the "Thus Spoke Syphilis" variant)
- that led to a huge break in my intellectual pursuits (~10 months)
  and I only recently began caring about piecing my life back together.
- I began working out and reading again a couple of months ago,
  writing again a month after that and socially reconnecting with my
  friends a little while after that.
- All I can say is that it'd been a stagnant year and the temporal river's
  begun flowing smoothly again fairly recently.
  - that's a little too many adverbs at once.
- anyway, one such friend of mine brought up the topic of Nietzsche a
  couple of days ago and that induced this huge recall spree of my
  past and my plans.
- so, I've finally decided to put an end to my first reading cycle of
  Nietzsche and "Thus Spake Zarathustra" has been my bed time read
  since yesterday.

## Conclusion

What I would like you to take away from this anecdote is:
 - read good books
 - have good friends that read good books
 - blog, to log your prominent thoughts over time
 - stay true to your promises
 - it's never too late for you to revive your ambition and
   passion, irrespective of what life has dumped on you

---

### Meta Commentary

- Those were the times when I used to index my days in decimal and
would manually keep a count of the same
- That was also a time when I was critical of timestamping whatever I
wrote down : these specifically are org-style timestamps (`C-u C-c C-!`)
- as of now, I use an elisp function that does the counting and
handles similar utilities.
- stylistically speaking, there does seem to be an unecessary tinge of
  complexity and I don't particularly recall forcing that.
  - guess that was just a phase..
  - words did flow off my fingers pretty fluidly those days...
  - good times ...
- addressing the "intellectual conveyance"... 
  - yeah, that seems a little overboard now
- Being able to criticize your past works rather than revering them is
  a sign of progress I guess.

#### Appendix

 - the utility function that I use for hexifying my stream timestamps
``` elisp
    (defun life-hex-count ()
      "number of days I've been alive"
      (interactive)
      (let* ((birth (date-to-time "2000-05-01 19:30 IST"))
	     (today (date-to-time (format-time-string "%Y-%m-%d %H:%M:%S %Z" (current-time)) ))
	     (diff (float-time (time-subtract today birth))))
	(insert (format "0x%X" (/ diff 86400)))))

    (defun hex-ops ()
      "hexify decimal number at point, invoke life hex at count if nil"
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
```

 - I had a log about all these books with reviews in my old good reads
   stream 
   - But...., I was decided to delete that account for reasons I can't
     reason for as of now.
 - well, fresh starts aren't that bad after all 
   - there's no intellectual baggage, and I don't care what others
     think of what I read now..
 - Good reads isn't just another biblio-social media for me and serves
   merely as an index now -> now that's what I call progress.
