---
title: "VLSI Mini Processor"
permalink: /articles/vlsi
---

{% include toc %}


In this set of articles, I will walk through the **essentials of the 4321 design project**, so you can achieve an A tier layout even you are **completely new** to layout (like I was). It will be a *huge* learning curve, and that's exactly the point. 

Think of this project as a process of **successive approximation** (Shepard’s favorite exam technique): make an initial attempt, realize how bad it is, learn something new, refine it, and repeat. 

This guide is meant to help you **converge faster**, avoiding many of the traps and misjudgments we fell early on, and focusing on what *actually* matters. 

Hopefully, this means less **pain and suffering**, but more **appreciation** for the real beauty of custom layout. Enjoy.

---

# Contents

![image-right](/images/vlsi/pretty/overall/overall_1.png){: .align-right width="55%"}

1. **Intro to 4321 Layout** (this article)
2. [Inverter](/articles/vlsi/inverter) 
    - [Layout](/articles/vlsi/inverter#layout)
    - [DRC](/articles/vlsi/inverter#drc)
    - [LVS](/articles/vlsi/inverter#lvs)
    - [Virtuoso FAQ](/articles/vlsi/inverter#faq)
3. [Project Plan](/articles/vlsi/floorplan)
    - [Architecture](/articles/vlsi/floorplan#architecture)
    - [ISA](/articles/vlsi/floorplan#isa)
    - [Floorplan](/articles/vlsi/floorplan#floorplan)
4. [Adder and Shifter](/articles/vlsi/adder)
    - [Design](/articles/vlsi/adder#design)
    - [Schematic](/articles/vlsi/adder#schematic)
    - [Carry Circuit Walkthrough](/articles/vlsi/adder#carry-circuit-walkthrough)
    - [1-Bit Adder](/articles/vlsi/adder#1-bit-adder)
    - [8-Bit Adder](/articles/vlsi/adder#8-bit-adder)
    - [Shifter](/articles/vlsi/adder#shifter)
5. [SRAM](/articles/vlsi/sram) 
    - [SRAM Array](/articles/vlsi/sram#sram-array)
    - [Decoder](/articles/vlsi/sram#decoder)
    - [Read Write](/articles/vlsi/sram#read-write)
    - [What if things don't fit](/articles/vlsi/sram#what-if-things-dont-fit)
6. [Overall Data and Control Paths](/articles/vlsi/overall)
    - [Power Grid](/articles/vlsi/overall#power-grid)
    - [Data Path](/articles/vlsi/overall#data-path)
    - [PLA](/articles/vlsi/overall#pla)
    - [Control Path](/articles/vlsi/overall#control-path)
    - [DRC and LVS tips](/articles/vlsi/overall#drc-and-lvs-tips)
    - [Wrap Up!](/articles/vlsi/overall#wrap-up)

Appendix. [Pictures!](/articles/vlsi/gallery)

---

# About
Our final design features:
- ~1100 µm² core area
- 4 Metal layers
- 4x16 physical SRAM
- 2.1 µm data path bit pitch (2 SRAM columns)
- High data path density and regularity

## Disclaimer
> mg-04-io is a personal blog. It is not affiliated with Columbia EE or BioEE.
{: .notice--info}

Our project is **FAR from perfect**. In fact, when I was writing this, I constantly realize how much I still don't know about Cadence Virtuoso, and how our layout can be more efficient in countless ways.

That's okay.

The goal of this project is to get something *done*, and done *well*, but not *perfectly*. This is an older technology node, intended for learning and practice, so don’t pull your hair out.

## Caveats
- This guide is based on *our* design project. Our design evolution produces a lot of naming inconsistencies; all names should make common sense and fit local context.
- Apologies for the image quality and resolution inconsistencies. All images should be readable, but the thumbnails may not all display properly in your browser. Download them if necessary.
- There are be suboptimal designs from the early (and late) stages of our project. I point out the obvious ones, but if you
    - See any mistakes or inefficiencies
    - Have suggestions on improving this guide
    - Want to share your layout/experience
    Feel free to **email** me at [mg4264@columbia.edu](mailto:mg4264@columbia.edu). I am **MORE THAN HAPPY** to include it! 
- These articles focus primarily on **layout**, but **testing** is **equally important**
- We did not explore much in Virtuoso's **design automation** features. This is an area worth studying on
- This guide is **never** intended to **help you cheat** (and realistically, you can't).
- TSMC, please don't sue me

---

# General Advice and FAQ
> This is a generic FAQ. Specific debugging tips are in later articles
{: .notice--info}

## Logistics

> What are the prereq?

**Officially**: ECircuits and Fundies  
**Unofficially**: a resilient spine, functioning caffeine metabolism, and enough tears

> Find a good teammate

Half of the class were having teammate issues; the other half **are** the teammate issues

> Should I take this class for **fun**?

Yes, if you enjoy circuits, symmetry, compulsive optimization, or the unique **pleasure** of being **tortured** by Shepard.

## Workload

> Do the PSets get harder and harder?

Yes. Not linearly, but **exponentially**  
Consider PS4 the *bare minimum*.   
**START EARLY!!!** Start them **the day they are released**.

> Do they give extensions?

Not officially, but TAs are typically nice

The real question is: **will an extension actually help you?**
- If you are stuck on some last-minute bugs: absolutely
- If you are fundamentally behind: **almost certainly not**. 

At that point, you are not buying time. You are taking out a **high-interest loan** that compounds **daily**... until you declare **layout-rupcy**

> Do I need All-nighters?

A extremely accurate review from [CULPA](https://culpa.info/professor/4500): 
> On a scale of one to crazy, you're looking at Deadpool level insanity. I kid you not, "dat shit cray". "Kill me now" would be your default state of existence  



## Resources

> Ask Prof and TAs

**Bring questions** to class, to recitations, to office hours.

> Ask people around you

Your classmates know things you don’t.  
They also know things you *don’t know* you don’t know.  
Talk to them. Compare your layouts. Steal their ideas


> Online resources?

There are a lot. The textbook is good, too.  
But by week 5, your brain will *reject new PDFs*.  
These articles try to *distill* what's actually important.


## Design
> Run DRC and LVS **early and often**

Small mistakes are cheap early and extremely expensive later. Frequent checks save time and sanity.

> Don't be messy

Symmetry and consistency will save you from debugging hell. "Messy but working" layouts *will* stab you some point in the futures.

> Don't be perfect

Don’t stress about getting *anything* perfect on the first pass. You will **almost certainly** revisit, modify, and sometimes **completely nuke** them as your design evolves. That's part of the learning process

> What if my layout sucks?

- Before PS7: **RESTART, NOW!**
- After PS8: Accept your fate, BS the project, and lock in for the exams

> More to be added...

# Special Thanks
Many thanks to the following folks for their help and guidance throughout this project:
- My teammate Charlotte Chen;
- TAs Kaden Du, James Jagielski; 
- Professor Ken Shepard;
- Former student Yuxi Zhang;
- Current students David Kim, Stephen Ogunmwonyi, Simon Mao.

Additional thanks to William Wang on sharing his [PLA layout](/articles/vlsi/overall#layout-by-william-wang)