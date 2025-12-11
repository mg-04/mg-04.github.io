---
title: "4321 Adder"
permalink: /articles/vlsi/adder
---

Now comes the first real task of 4321: adder

A few points:
- Use a bit pitch width of 2.1 um!!! You will know why.
- For the purpose of this final project, use ripple carry, since it's only 8-bits. You can show off with a more complex carry structure, but they won't help you much in pre-sim, and *definitely* won' help you in post-sim. 
{: .notice--info}

As we covered in class, and adder has two parts:

# Design
![this](https://www.eecs.umich.edu/courses/eecs427/w07/lecture8.pdf)

# Sample Carry Circuit Walkthrough

I would recommend **deleting** all transistors you are not planning to use, to avoid obstructing the real DRC errors

# Our Adder

Below is our adder from a few months ago. It is less optimal, but fine.


# Misc
We didn't follow the design rules before, and it sucked that we have to re-layout