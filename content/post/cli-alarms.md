---
title: "A CLI Timer to save your soul"
date: 2024-09-26T11:26:45+05:30
categories: ["Tooling"]
tags: ["bash","cli","timer","linux","morse","sos","alarm"]
---

This is how I time my workblocks these days...  

### Prerequisites

 - ALSA : https://wiki.archlinux.org/title/Advanced_Linux_Sound_Architecture
 
 
### Functions

``` 
single_beep() {
( \speaker-test --frequency $1 --test sine )&
pid=$!
\sleep  0.${2}s
\kill -9 $pid
}

morse(){
for i in {1..3};
do
        single_beep 400 $1
        \sleep 0.${2}s
done
}

sos() {
    morse 200 500
    morse 400 500
    morse 200 500
}

timer() {
    \sleep $1 && sos &
}
```


### Usage

The above can be sourced in your shell rc.  
I store it in a `.bash_funcs` where I have all my functions and source them in the end of my rc as `source ~/.bash_funcs`.


``` 
timer <seconds to sleep before the alarm>
```

### Known Bugs

If you happen interrupt (`C-c`) a single_beep when it is in the sleeping stage, the sine test will not be killed and continue to ring.  
In such a case `ps aux | grep speaker-test | awk  '{print $2}' | xargs kill -9 `  would save your soul.

PS: I would recommend you to let it ring.  

