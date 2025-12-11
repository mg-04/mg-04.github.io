---
title: "4321 Adder"
permalink: /articles/vlsi/adder
---

Now comes the first real task of 4321: adder

> This is very, very important, as you will learn the basics of tight layout and diffusion sharing!

A few points:
- Use a bit pitch width of 2.1 um!!! You will know why.
- For the purpose of this final project, use ripple carry, since it's only 8-bits. You can show off with a more complex carry structure, but they won't help you much in pre-sim, and *definitely* won' help you in post-sim. 
{: .notice--info}

As we covered in class, and adder has two parts:

# Design

## Sizing
Textbook pp. 432 discusses the sizing
![](/images/vlsi/Adder/sizing.png)


The minimum width of our technology is 150 um
- Below that, the MOSFETs will turn into a **dogbone** shape, which actually takes more space!
We used the following sizing
- Critical path: 300 um * 4 / 150 um * 4
- Non-critical path: 300 um / 150 um
    - It's a better idea to size the PMOS to 150 as well :( We went lazy, but it doesn't matter

# Schematic
If you want to use the textbook sizing, change the non-critical path NMOS to 150.

## Stick Diagram
You should make a stick diagram of your adder layout. [This](https://www.eecs.umich.edu/courses/eecs427/w07/lecture8.pdf) article from UMich discusses one way of layout and diffusion sharing with one finger. Adapt it for your design.

Alternatively, you can also not plan and do "vibe layout", not a bad choice either!



# Sample Carry Circuit Walkthrough
## 1. Bit Pitch!
Right after "Generate from Source", draw your M2 bit pitch. Make their centers 2.1 um apart, and each 0.1 um wide!
![](/images/vlsi/Adder/pitch.png)

You can use the "p" shortcut to draw a path. It labels its DRC rules, too
![](/images/vlsi/Adder/p.png)

I would recommend **deleting** all transistors you are not planning to use, to avoid obstructing the real DRC errors

## 2. `A` and Body Via
Same thing as the inverter
1. Add the `M1-NW` and `M1-SUB` vias. **Align their centers with the `M2`!**
2. Place the 8/4 transistors gated by `A`. Make sure the `PP`s and `NP`s touch, but not overlap, each other


## 3. Diffusion Sharing
Find the single-fingered transistors gated by A. You can see its top terminal (S) should be connected to `GND!`, so does the bottom terminal (S) of the four-fingered device. We can make them share the same diffusion

Move the transistors close together
![](/images/vlsi/Adder/diff0.png)

Move the bottom transistor further up, and release your mouse. You should see they "snap" together. Virtuoso recognizes this as a diffusion share!
![](/images/vlsi/Adder/diff1.png)

Do the same thing for the PMOS



Now, check DRC. I would recommend deleting the transistors you haven't yet placed and *Update* (not Generate) them back, so their DRC violations doesn't block any actual errors. 

![](/images/vlsi/Adder/t1.png)

You will get quite a few errors. It's complaining that the `M1` and `PO` areas are too small. That's *fine*, since we haven't connected them yet

Now, you can regenerate the deleted transistors by "Connectivity/Update from Source"

### S/D Swap

Up next is M30/M5, with its drain to `COUTN`. However, the generated instance has its source `net1` on the outside. We need to swap the source and the drain.

1. Select the FET, click "q"
2. Go to "Parameter", check "S D swap"

![](/images/vlsi/Adder/sd.png)

Now you can happily diffusion share!

## 4. Non-sharing Neighbors
Most people fuck up on this one. They start crying once they could't diffusion share

We run out of diffusion shares for M28/M26, a suboptimal situation, but we can still lay the FETs as closely as possible, borderline DRC
- The `OD` layers need to be 0.13 um apart
- (when the `PP`/`NP` box perfectly overlaps with the neighboring `OD`)

![](/images/vlsi/Adder/nsd.png)

Check DRC again.


## 5. `M1` and `PO` connections
Now let's make DRC pleased by connecting the simple poly and metal wires
1. Draw an `M1` rectangular extension from the `VDD!`/`GND!` vias
    - Place `M1-M2` vias (make sure they are 0.1 um squares)
2. Draw rectangles, or paths, to connect every S/D labeled `VDD!`/`GND!` to the supplies
3. Draw poly paths to connect every poly with its neighbor

Check DRC again. All `PO` area issues should go away, as well as some `M1` area issues.

## 6. `M2` Connections and Vias
I don't recommend using the vias generated from "o". They are too fat and ugly, and they are the root cause of DRC miseries if used improperly.

## 7. `PO` Connections and Contacts

CONGRATS on completing 1/3 of this assignment!
# Our Adder

Below is our adder from a few months ago. It is less optimal, but fine.
## Sum

## Subtraction

## Multibit



## Overflow


# Misc
We didn't follow the design rules before, and it sucked that we have to re-layout