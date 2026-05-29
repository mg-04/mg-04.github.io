---
title: Operating Systems I
permalink: /courses/os
---


Here are my OS notes:
1. [Systems Programming](/articles/os/1-asp) (see [ASP Notes](/courses/asp))
2. [Scheduling](/articles/os/2-sched)
3. [Memory Management](/articles/os/3-mm)
4. [Disk and IO](/articles/os/4-io)

These notes were not taken in any careful or organized manner, because:
1. The slide format makes it incredibly difficult to **distill** and **coalesce** the key concepts real-time
2. There are plenty of great material on *specific* topics, see [below](#resources)
3. Most of my comprehension happens during late-night debugging, instead of deliberate note-taking.

Some of the homework/recitation notes are omitted, as they lead directly to solutions.

## Delivery
If you take OS with Kostis (or descendants of his version), you are in a challenging state. Personally, I don't like using **slides** to deliver the Columbia OS curriculum

Systems are best understood as an unbroken, continuous **stream** of concepts. Slides fundamentally **constrain** knowledge within artificial rectangular boundaries, leading to problems such as:
- Filler text and verbose background info simply to pad the dead space of a slide template.
- Squeezing multiple text/diagrams/schematics of a complex topic onto a single slide
- Incomplete/segmented code snippets on multiple slides
- Poor portability (you can't cleanly copy code in a slide layout)

These characteristics make learning difficult, for both students and instructors
- There are also debates on logistics and grading, which merit their own discussion...

## Resources
I recommend referencing **Jae**'s OS [course page](https://cs4118.github.io/www/2023-1/) from Spring 2023, the good old days! (It's publicly accessible via Jae's [homepage](https://www.cs.columbia.edu/~jae/))

Here are also some *very* useful guides written by former Head TA [**Alex Jiakai Xu**](https://alex-xjk.github.io/), previously posted on EdStem. 
- [Pipes](https://alex-xjk.github.io/post/connect2/)
- [Kernel task_struct](https://alex-xjk.github.io/post/taskstruct/)
- [HW5 Scheduler](https://alex-xjk.github.io/post/scheduler/)
- [HW7 EZFS](https://alex-xjk.github.io/post/tiny-afs/)

You can check out more awesome articles in his [GitHub page](https://alex-xjk.github.io/post/)

Here's a scheduler state diagram I made when reviewing for the finals
![](/articles/s26/os/img/sched_states.jpg)
- **Green**: normal pick -- run -- preempt -- put loop
- **Red**: wait -- sleep -- wakeup routine
- **Yellow**: load balancing (between 2 CPU/runqueues)
- **Blue**: task switching schedule classes