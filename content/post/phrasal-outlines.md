---
title: "Jargony Outlines"
date: 2025-04-17T06:36:56+05:30
categories: ["Writing"]
tags: ["jargon","outline","org","lisp","fun","not-drunk","distributed","termite","scheme"]
---

## Context

> been reading more papers  
> notes by jargony outlines  
> no unnecessary words  


> if can express  
> few words  
> you get it  
> get it?  
 
 
> concise, practical  
> flowy, comprehensible  
> jargon is fun  
   
   
> in org-roam  
> links when depth  
> more speed  
> good  
   
  
> all left  
> tech haikus  
> challenge  
> someday  
  
  
> until then  
 
## [Enjoy instance](https://github.com/rajp152k/buffer/blob/master/20250416130434-termite_distributed_lisp.org)

 - for [this](http://www.european-lisp-workshop.org/archives/05.germain.pdf)

``` org
#+title: Termite: A Lisp for Distributed Computing

* Outline
** Isolated Sequential Processes
*** Memory Space Isolation
*** Node and Process Identifiers
*** Process Spawning
** Sending and Receiving messages
*** Process Mailbox
*** [[id:b2ce2739-98c4-4ff0-931c-3a836686bf55][Async]] Message Sends
*** Sync Message Recvs
*** spawn and send sample

#+begin_src lisp
(let ((me (self)))
  (spawn
   (! me "hello, world.")))

(?)
#+end_src

 - ! : async send mesg
 - ? : sync (blocking) recv mesg

** Failure
*** Hardware Unreliability
 - the "real world" or the "physical"
 - [[id:a4fd4495-8068-4824-8629-e5b2e5cdb906][send and pray]]

*** Sends : Unreliable Operations

** Peripheral Aspects
*** Serialization
 - [[id:d45dae92-5148-4220-b8dd-e4da80674053][Data]]
 - [[id:5344927b-c263-48d0-bb1e-c234af8fe694][Closures]]
 - [[id:d41dc898-8776-47bb-a88d-bc143250799f][Continuations]]
**** Non-Serializables -> Addressable Proxies
 - ports -> open files -> processes -> pids
 - processes as pids
*** [[id:efba8f9b-a5df-4212-94c9-230bef916b5c][Immutability]]
*** Suspended Processes as State
*** [[id:34df7d47-1f78-4acf-8dd7-9c03e04e4a9d][Exception Handling]]
**** Dyamically scoped handlers
 - choose : handle or raise again
 - when raise:
   - encapsulating handler invoked
 - Cross Process Exception Transfers upon deaths
   - "send and pray" applies here as well
   - cross process exception raises upon receives

**** Process relations
 - supervisor - worker (two way death effects : work doesn't matter if not supervised)
 - monitor - worker (one way death effect : worker doesn't care if monitor dies)

*** Connecting Nodes
 - Unique identifiers for each node
   - (IP#:port)
   - node references contain these
     - gen with make-node

*** [[id:19079639-be92-46cf-82c5-3d81c935705c][Remote Procedure Calls]]
*** [[id:f6111cb3-60df-422e-aca3-c4cb1b5cbb2a][Process Migration]]
 - Serialize a Continuation
 - send and pray
** Language Overview
*** Making a server
   #+begin_src scheme
(define pong-server
    (spawn
     (let loop ()
          (let ((msg (?)))
            (if (and (list? msg)
                     (= (length msg) 2)
                     (pid? (car msg))
                     (eq? (cadr msg) 'ping))
                (let ((from (car msg)))
                  (! from 'pong)
                  (loop))
                (loop))))))

(! pong-server (list (self) 'ping))     ;; -> send 'ping

(?) ;; -> 'pong
   #+end_src
*** predicate + pattern matches
   #+begin_src scheme
(define better-pong-server
  (spawn
   (let loop ()
     (recv
      ((from 'ping)                     ;pattern to match
       (where (pid? from))              ;additional conditions
       (! from 'pong)))                 ;action
     (loop))))
   #+end_src
*** timeouts
#+begin_src scheme
(recv
 (pattern-match-form predicate-filter-form action-form)
 (after timeout-duration (raise 'timeout)))
#+end_src
*** Remote Procedure Calls
 - !? from the client (sync sends and recvs) -> not just a !

   #+begin_src scheme
(define rpc-server
  (spawn
   (let loop ()
     (recv
      ((from tag ('proc-tag arg))
       (! from (list tag ((fetch-corresponding-proc 'proc-tag) arg))))
      (loop)))))

(let ((tag (make-tag)))
  (! rpc-server (list (self) tag (list 'add 1 2)))

  (recv
   ;; check for same tag from ret
   ((tag result) result)                ;; yields 3
   ))

;; !? -> send and recv like above
;; !? handles tag management -> no explicit need
(!? rpc-server (list 'add 1 2 ))   ;; yields 3
   #+end_src

*** Mutability
 - simulate via let loops
   #+begin_src scheme
(define (make-cell init-content)
  (spawn
   (let loop ((content init-content))
     (recv

      ((from tag 'get)
       (! from (list tag content))
       (loop content))

      (('set! new-content)
       (loop new-content))))))

(define (cell-get cell)
  (!? cell 'get))

(define (cell-set! cell val)
  (! cell (list 'set! val)))
   #+end_src

*** Exception Handling
 - raise -> catch & handle
 - handlers are dynamically scoped
 - (catch dealer ..body) : implements dealer for raises and doesn't continue
 - (handle dealer ..body) : implements dealer for raises and continues exec

   #+begin_src scheme

(catch
  (lambda (exc) exc)
  (some-work) ;; is done
  (raise 'err) ;; returns 'err from here
  (some-more-work) ;; isn't exec'd
  (yield-final-val)) ;; control doesn't reach here

(handle
  (lambda (exc) exc)
  (some-work) ;; is done
  (raise 'err) ;; this form returns err but exec continues
  (some-more-work) ;; is exec'd
  (yield-final-val)) ;; final yield val from here

   #+end_src

 - for interprocess exc transfers, need to use a spawn-link

   #+begin_src scheme
(catch
 (lambda (exc) (list 'transfer-will-fail exc))
 (spawn (raise 'err)) ;; isn't handled cause no interprocess link
 (? 1 'ok) ;; timed receive will fail -> way to sleep
 (some-work)) ;; is exec'd cause spawn raises right away

(catch
  (lambda (exc) (list 'transfer-succeeds exc) )
  (spawn-link (raise 'err)) ;; caught and parent catch yields (list 'transfer-succeeds 'err)
  (? 1 'ok) ;; sleep
  (some-work)) ;; isn't exec'd
   #+end_src



*** Process Migration
 - node references as IP:ports needed
   #+begin_src scheme

(define migrating
  (spawn (let loop ()
           (recv ((from tag 'where)
                  (! from (list tag (current-node))))
                 (('migrate to)
                  (migrate to))))))

(define this (current-node))
(define that (make-node "<that's domain>" <thats port>))

(!? migrating 'where)                   ; spawned on this - yields this
(! migrating (list 'migrate that))      ; init's migration to that
(!? migrating 'where)                   ; yields that
(! migrating (list 'migrate this))      ; migrate back to this
(!? migrating 'where)                   ; back on this
   #+end_src
*** Remote Spawns
 - migrate after spawn

   #+begin_src scheme
(define node (make-node "domain.com" <port>))

(let ((this (self)))
  (spawn
   (migrate node)                       ; migrate the spawn
   (! this (list 'from node))))

(?)                                     ; recv `(from ,node)
   #+end_src

*** [[id:d41dc898-8776-47bb-a88d-bc143250799f][Continuations]]
**** [[id:7922a2b7-534f-454f-8c11-59b4322a1b00][process cloning]]

   #+begin_src scheme
(define original
  (spawn
   (let loop ()
     (recv
      ((from tag 'clone)
       (call/cc
        (lambda (clone)
          (! from (list tag (lambda ()
                              (clone #t))))))))
     (loop))))

(define clone (spawn ((!? original 'clone))))
   #+end_src

**** Dynamic code updates

 - need an update message handler in the server

#+begin_src scheme
(define server
  (spawn
   (let loop ()
     (recv
      (('update k)
       (k #t))
      ((from tag 'ping)
       (! from (list tag 'not-pong))))  ;;bug
     (loop))))

(define new-server
  (spawn
   (let loop ()
     (recv
      (('update k)
       (k #t))

      ((from tag 'clone)
       (call/cc
        (lambda s (k)
                (! from (list tag k)))))

      ((from tag 'ping)
       ( from (list tag 'pong))))
     (loop))))

(!? server 'ping)                       ;; not-pong

(let ((replacement (!? new-server 'clone)))
  (! server (list 'update replacement)))

(!? server 'ping)                       ;; pong
#+end_src

* Application Instances
** [[id:0d7c2dea-a250-4380-b826-ad4d2547d8d6][Load Balancing]]
 - meters for per node load
 - supervisor to collate metrics from meters

   #+begin_src scheme(define (start-meter supervisor)
  (let loop ()
    (! supervisor
       (list 'load-report
             self
             (local-loadavg)))          ;; send avg load
    (recv (after 1 'ok))                ;; sleep for a sec
    (loop)))
   #+end_src

 - supervisor maintains a node load map and responds with lowest load node when requested

   #+begin_src scheme
(define (meter-supervisor meter-list)
  (let loop ((meters (make-dict)))
    (recv

     (('load-report from load)
      (loop (dict-set meters from load)))

     ((from tag 'average-load)
      (let ((avg-load (find-avg (dict->list meters))))
        (! from (list tag avg-load)))
      (loop dict))

     ((from tag 'minimum-load)
      (let ((min (find-min (dict->list meters))))
        (! from (list tag (pid-node (car min)))))
      (loop dict)))))


(define (min-load-node supervisor)
  (!? supervisor 'minimum-load))

(define (avg-load supervisor)
  (!? supervisor 'average-load))

(define (start-meter-supervisor)
  (spawn
   (let ((supervisor (self)))
     (meter-supervisor
      (map (lambda (node)
              (spawn
               (migrate node)
               (start-meter supervisor)))
            ,*node-list*)))))


(define (start-work-dispatcher load-server)
  (spawn
   (let loop ()
     (recv
      ((from tag ('dispatch thunk))
       (let ((min-loaded-node
              (minimum-load load-server)))
         (spawn
          (migrate min-loaded-node)
          (! from (list tag (thunk))))))
      (loop)))))

()
(define (dispatch dispatcher thunk)
  (?! dispatcher (list 'dispatch thunk)))
   #+end_src

** Abstracting [[id:618d0535-411d-4c36-b176-84413ec8bfc1][Concurrency]]
 - modifying a generic server with classes of functionalities
 - plugins to management, core compute and other needs

#+begin_src scheme
(define key/value-generic-server-plugin
  (make-generic-server-plugin
   (lambda ()                           ;INIT
     (print "Key-Value server starting")
     (make-dict))

   (lambda (term from state)            ;CALL
     (match term
       (('store key val)
        (dict-set! state key val)
        (list 'reply 'ok state))

       (('lookup key)
        (list 'reply (dict-ref state key) state))))

   (lambda (term state)                 ;CAST (state shifts)
     (match term
       (('stop (list 'stop 'normal state)))))

   (lambda (reason state)               ;TERMINATE
     (print "Key Value Server Terminating"))))

(define (kv:start)
  (generic-server-start-link
   key/value-generic-server-plugin))

(define (kv:stop server)
  (generic-server-cast server 'stop))

(define (kv:store server key val)
  (generic-server-call server (list 'store key val)))

(define (kv:lookup server key )
  (generic-server-call server (list 'lookup key)))

#+end_src

** [[id:20240519T162542.805560][Fault Tolerence]]
 - restarts by a supervisor when needed

   #+begin_src scheme
(define (start-pong-server)
  (let loop ()
    (recv
     ((from tag 'crash)
      (! from (list tag (/ 1 0))))
     ((from tag 'ping)
      (! from (list tag 'pong))))
    (loop)))

(define robust-pong-server
  (spawn-thunk-supervised start-pong-server))

   #+end_src

* Implementation
- over Gambit-scheme (gambit c): https://www.gambitscheme.org/4.3.0/manual/

* Paper
 -  http://www.european-lisp-workshop.org/archives/05.germain.pdf
```
