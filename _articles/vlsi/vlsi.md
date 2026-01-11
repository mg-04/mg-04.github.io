---
title: "VLSI Mini Processor"
permalink: /articles/vlsi
date: 2026-1-6
authors:
  - Ming Gong
  - Charlotte Chen
---

{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}

{% include toc %}


In this set of articles, I will walk through the **essentials of the 4321 design project**, so you can achieve an A tier layout even you are **completely new** to layout (like I was). It will be a *huge* learning curve, and that's exactly the point. 

Think of this as a process of **successive approximation** (Shepard’s favorite exam technique): make an initial attempt, realize how bad it is, learn something new, refine it, and repeat. 

This guide is meant to help you **converge faster**, avoiding many of the traps and misjudgments we fell early on, and focusing on what *actually* matters. 

Hopefully, this means less **pain and suffering**, but more **appreciation** for the real beauty of custom layout. Enjoy!

---

# Contents

![image-right](/images/vlsi/pretty/overall/overall_1.png){: .align-right width="55%"}

1. **Intro to 4321 Layout** (this article)
2. [**Inverter**](/articles/vlsi/inverter) (PS4)
    - [Layout](/articles/vlsi/inverter#layout)
    - [DRC](/articles/vlsi/inverter#drc)
    - [LVS](/articles/vlsi/inverter#lvs)
    - [**Virtuoso FAQ**](/articles/vlsi/inverter#faq)
3. [**Project Plan**](/articles/vlsi/floorplan)
    - [Architecture](/articles/vlsi/floorplan#architecture)
    - [ISA](/articles/vlsi/floorplan#isa)
    - [Floorplan](/articles/vlsi/floorplan#floorplan)
4. [**Adder and Shifter**](/articles/vlsi/adder) (PS6-7)
    - [Design](/articles/vlsi/adder#design)
    - [Schematic](/articles/vlsi/adder#schematic)
    - [Carry Circuit Walkthrough](/articles/vlsi/adder#carry-circuit-walkthrough)
    - [1-Bit Adder](/articles/vlsi/adder#1-bit-adder)
    - [8-Bit Adder](/articles/vlsi/adder#8-bit-adder)
    - [Shifter](/articles/vlsi/adder#shifter)
5. [**SRAM**](/articles/vlsi/sram) (PS8)
    - [SRAM Array](/articles/vlsi/sram#sram-array)
    - [Decoder](/articles/vlsi/sram#decoder)
    - [Read Write](/articles/vlsi/sram#read-write)
    - [**Testing**](/http://localhost:4001/articles/vlsi/sram#testing)
    - [**What If Things Don't Fit**](/articles/vlsi/sram#what-if-things-dont-fit)
6. [**Overall**](/articles/vlsi/overall) (PS9)
    - [Power Grid](/articles/vlsi/overall#power-grid)
    - [Data Path](/articles/vlsi/overall#data-path)
    - [PLA](/articles/vlsi/overall#pla)
    - [Control Path](/articles/vlsi/overall#control-path)
    - [**DRC and LVS Tips**](/articles/vlsi/overall#drc-and-lvs-tips)
    - [Wrap Up!](/articles/vlsi/overall#wrap-up)

Appendix. [Pictures!](/articles/vlsi/gallery)  
Appendix. [Class Notes](/courses/vlsi)

---

# About
Our final design features:  
- ~1100 µm² core area
- 4 Metal layers  
- 2.1 µm data path bit pitch (2 SRAM columns)
- High data path density and regularity  
- Static CMOS ripple-carry adder
- Transmission gate logarithmic shifter (buffered)
- 4x16 physical SRAM
- Pseudo-NMOS ratio PLA
- Master-slave accumulator
- C²MOS bus drivers

## Disclaimer
> mg-04-io is a personal blog. It is not affiliated with Columbia EE or BioEE.  
This article is not an official TA guide. It's independent from the [official layout tutorials](https://www.bioee.ee.columbia.edu/courses/cad/html/)
{: .notice--info}

Our project is **FAR from perfect**. In fact, when I was writing this, I constantly realize how much I still don't know about Cadence Virtuoso, and how our layout can be more efficient in countless ways.

That's okay.

The goal of this project is to get something *done*, and done *well*, not *perfectly*. This is an older technology node, intended for learning and practice, so don’t pull your hair out.

## Caveats
- This guide is based on *our* design project. Our design evolution produces a lot of naming inconsistencies. Nevertheless, all names should make common sense and fit local context.
- Apologies for the image quality and resolution inconsistencies. Everything should be readable, but some thumbnails may not render properly in your browser. Download them if necessary.
- There **are** suboptimal designs from the early (and late) stages of our project. I point out the obvious ones, but if you  
    - Spot any mistakes or inefficiencies
    - Have suggestions on improving this guide
    - Want to share your layout/experience  

    Feel free to **email** me at [ming.g@columbia.edu](mailto:ming.g@columbia.edu). I am **MORE THAN HAPPY** to include it! 
- These articles focus primarily on **layout**, but **testing** is **equally important**
- We did not explore much in Virtuoso's **design automation** features. This is an area worth studying on
- This guide is **never** intended to **help you cheat** (and realistically, you can't).
- TSMC, please don't sue me!

---

# General Advice and FAQ
> This is a generic FAQ. You can find specific debugging tips in [later articles](/articles/vlsi/#contents)
{: .notice--info}

## Logistics

> **What are the prereq?**

**Officially**: ECircuits and Fundies  
**Realistically**: a resilient spine, functioning caffeine metabolism, and enough tears

---

> **Find a good teammate.**

Half of the class were having teammate issues; the other half **are** the teammate issues

---

> **Should I take this class for *fun*?**

Yes, if you enjoy circuits, symmetry, compulsive optimization, or the unique **pleasure** of being **tortured** by Shepard.

## Workload

> **Do the PSets get harder and harder?**

> Check out a few extremely accurate reviews from [CULPA](https://culpa.info/professor/4500)
{: .notice--warning}

Yes. Not linearly, but **exponentially**  
Consider PS4 the *bare minimum*. You will likely need a few **all-nighters** after that
**START EARLY!!!** Start them **the day they are released**.

---

> **Do they give extensions?**

Not officially, but TAs are typically nice  
The real question is: **will an extension actually help you?**
- If you are stuck on some last-minute bugs or sicknesses: absolutely
- If you are fundamentally behind: **almost certainly not**. 

At that point, you are not buying time. You are taking out a **high-interest loan** that compounds **daily**... until you declare **layout-rupcy**

---

> **How would my partner and I coordinate?**

Introducing **"Out of Order Layout"**... Most of the design projects can be parallelized: design, schematic, layout, testing, and writing the report. Just make sure you can handle the "dependencies" well


## Resources

> **Ask Prof and TAs.**

**Bring questions** to class, to recitations, to office hours.

---

> **Ask people around you.**

Your classmates know things you don’t.  
They also know things you *don’t know* you don’t know.  
Talk to them. Compare your layouts. Steal their ideas

---

> **Ask Chat.**

LLMs are **surprisingly helpful**, especially at fetching and reading instructions and manuals. Of course, you can't upload any TSMC NDA material to Chat to make it lay it out for you, but it is super useful at explaining concepts and interpreting unknown errors, as well as debugging Cadence.

---

> **What are some other resources?**

There are a lot. The **textbook** is really good.  
But by week 5, your brain will *reject new PDFs*.  
These articles try to *distill* those resources, listing the ones that I find helpful.

## Design
> **Run DRC and LVS early and often.**

Small mistakes are cheap early and extremely expensive later. 

---

> **Don't be messy.**

Symmetry and consistency will save you from debugging hell. "Messy but working" layouts *will* stab you some point in the futures.

---

> **Don't be perfect.**

Don’t stress about getting *anything* perfect on the first pass. You will **almost certainly** revisit, modify, and sometimes **completely nuke** them as your design evolves. That's part of the learning process

---

> **Don't blindly follow Shepard.**

He's really good at being **off-by-one**, whether it's index, an inverter, or a 90-degree rotation. So don’t take anything on faith. Make sure you understand what’s happening yourself.

---

> **What if my layout sucks?**

- Before PS7: **RESTART, NOW!**
- After PS8: Accept your fate, BS the project, and lock in for the exams

---

> **What are some examples that suck?**

Just find (and buy) the ones on **StudyDocu** or similar sites. Most of these **suck**. I've also shared some of our own inefficient early designs, as concrete counterexamples of what to avoid.


## Grading
> This class is **curved**, so if you are an A tier student, with "proper" work, you should expect an A tier grade.
{: .notice--info}

> **How will the project be graded?**

Shepard will grade all projects himself, which leaves no room for BS. 

> This is actually good, compared to leaving grading to EE ~~TAs~~ (more often, CAs or graders) who treat it like a paycheck task, rather than any academic responsibility.
{: .notice--success}

---

> **What is the distribution?**

The letter grade distribution was not published in Fall 2025, but here's the project distribution:

![](/images/vlsi/grades.png)

It's quite a left-heavy tail, with a similar mean to exams, but a much **wider IQR**

---

> **How are the exams?**

They are relatively easy to prepare. There are two types of exam problems:
1. **Freebies**  
    These are straightforward. Some may involve a lot of computation, but as long as you understand the concepts and have done the practice problems, you’ll be fine.
2. **Problems that "tell the boys apart from the men"** (according to Shepard)  
    Those are multi-part problems that require complex calculations or new concepts/equations, things that you haven't seen. Sometimes even the TA got them wrong. Sometimes Shepard himself finds the problem unsolvable. Who knows.

> Over the years, the proportion of the second type has increased, as Shepard was "running out of easy problems"
{: .notice--warning}

The point is: **if you fail, the class fails with you**. If you can't solve the trick questions, neither can most of the class. Don't stress too much about the exam. Just do all 4 practices, understand the fundamentals, and you’ll be in good shape.

> I considered writing a "4321 Exam Guide." Shepard exam tricks definitely exist, but I don't think obsessing over them is productive in the long run.
{: .notice--info}

---

> **More to be added...**

---

# Special Thanks
Many thanks to the following folks for their help and guidance throughout this project:
- My teammate Charlotte Chen;
- Professor Ken Shepard;
- TAs Kaden Du, James Jagielski; 
- Former students Yuxi Zhang, Yingrui Wei;
- Current students David Kim, Stephen Ogunmwonyi, Simon Mao.

Additional thanks to William Wang on sharing his [PLA layout](/articles/vlsi/overall#layout-by-william-wang)