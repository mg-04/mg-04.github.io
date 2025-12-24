---
title: "VLSI Mini Processor"
permalink: /articles/vlsi
---

{% include toc %}




In this set of articles, I will walk through the **essentials of the 4321 design project**, so you can achieve an A-tier even you are completely new to layout (like I was). It will be a *huge* learning curve, and that's exactly the point. 

Think of this layout project as a process of **successive approximation** (Shepard’s favorite exam technique): make an initial attempt, realize how bad it is, learn new lessons, refine it, and repeat. 

This guide is meant to help you along that gradient so you can converge faster, avoiding many of the traps and misjudgments we fell early on, and focusing on what *actually* matters. 

Hopefully, this means less **pain and suffering**, but more appreciation for the real beauty of custom layout. Enjoy.



# Contents

![image-right](/images/vlsi/pretty/overall/overall_1.png){: .align-right width="30%"}

1. **Intro to 4321 Layout** (this article)
2. [Inverter](/articles/vlsi/inverter) 
    - [Virtuoso FAQ](/articles/vlsi/inverter#faq)
3. [Project Floorplan](/articles/vlsi/floorplan)
4. [Adder and Shifter](/articles/vlsi/adder)
5. [SRAM](/articles/vlsi/sram) 
    - [What if things don't fit](/articles/vlsi/sram#what-if-things-dont-fit)
6. [Overall Data and Control Paths](/articles/vlsi/overall)
    - [DRC and LVS Tips](/articles/vlsi/overall#drc-and-lvs-tips)

Appendix. [Pictures!](/articles/vlsi/gallery)

# Disclaimer

Our project is **FAR from perfect**. In fact, when I was writing this, I constantly realize how much I still don't know about Cadence Virtuoso, and how our layout can be more efficient in countless ways.

That's okay.

The goal of this project is to get something *done*, and done *well*, but not *perfectly*. This is an older technology node, intended for learning and practice, so don’t pull your hair out.


- There may be a lot of naming inconsistencies; some names are chosen using common sense and local context.
- Apologies for the image quality and resolution inconsistencies. All images should be clear, but may not all display properly in your browser. Download them if necessary.
- There are be suboptimal designs from the early (and late) stages of our project. I point out the obvious ones, but if you find something important, or if you have a better suggestion, I am MORE THAN HAPPY to include it! 
    - Feel free to email me at mg4264@columbia.edu
- This article set mainly cover the **layout** aspects of this project, but **testing** is **equally important**
- This guide is never intended to help you cheat (and realistically, you can't). I included more details in the early design stages, but you should come with your own at later stages.
- TSMC don't sue me!


# General Advice
> Find a good teammate

Half of the class were having teammate issues; the other half *are* the teammate issues

> Pull a few all-nighters

Yes. You need stamina

> Ask people around you

They may happen to know a lot more you've never seen before. Read relevant sections of the textbook. Search online for how other people do it

> Focus on exams

They worth more, and generally easier to prepare

Don’t stress about making this section perfect on the first pass. You will **almost certainly** revisit and modify the peripheral-peripheral logic as the rest of the design evolves. That's normal and expected.

> Should I take this class for fun?


> Automation


> More to be added...