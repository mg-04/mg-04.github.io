---
title: "4321 Adder and Shifter"
permalink: /articles/vlsi/adder
---

{% include toc %}

Now comes the first real task of 4321: adder

> This is very, very important. You will learn the fundamentals of tight layout and diffusion sharing!

# Overview
- Fix your design with a bit pitch of 2.1 um
- Use ripple carry
- Make a (rough) stick diagram before you start
- Edge DRC
- Do not use their default VIAs
- Diffusion share, and if you can't, put fets as closely as possible
- Leave room for upper-level connections

## What we could have done better on
I would like to point out a few inaccuracies we've made, so it doesn't lead you to the wrong direction

**Adder**
- More organized M2 data grid
- Smaller sizing on the non-critical path PFETs
- Better diffusion sharing with S/D swapping
- Using inverted `COUT` to save a gate in the propagation path
- MUX-based `SUB` select
- Use an odd number of fingers for better diffusion sharing
- You don't have to put body vias everywhere
- An organized M3 power grid and M4 segments

and a lot of more...

**Shifter**
- Since we are buffering all I/O, we can do the MUX with NMOS only
- Shift wires on M3, not M1 (that will save a lot of space between the stages)

# Design

A ripple carry adder has two parts, carry and sum. The CMOS implementation is pretty standard, and you can find plenty of resources

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
Below is our carry schematic.  you want to use the textbook sizing, change the non-critical path NMOS to 150.

![](/images/vlsi/Adder/schem.png)

A few notes:
- Use multiple fingers so every transistor has the same width
- Set up one P/NMOS with the *right parameters*, the **duplicate** them over
- Connect all PMOS bodies to VDD, NMOS bodies to GND. No exception
- Label the nets and explicitly add the IO pins
- I recommend using capital letters for net names, and global VDD/GND

## Stick Diagram
You should make a stick diagram of your adder layout. [This](https://www.eecs.umich.edu/courses/eecs427/w07/lecture8.pdf) article from UMich discusses one way of layout and diffusion sharing with *one finger*. Adapt it for your design.

Alternatively, you can also not plan and do "vibe layout", not a bad choice either!

![](/images/vlsi/Adder/adder_stick.png)

This stick diagram is rotated 90 degrees. I used magenta for PMOS OD, and dark grey for NMOS OD. 

Note that I only drew with one finger. In the actual layout things will be a bit different.



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

We run out of diffusion shares for M28/M26, a suboptimal situation. The key is to know what can still be overlapped, and what can't. We can still lay the FETs as closely as possible, edging the DRC
- `NW` and `PP`/`NP` can still be overlapped. The bodies have the saem potential.
- `OD`s are now different nets. They need to be **0.13 um** apart
- (when the `PP`/`NP` box perfectly overlaps with the neighboring `OD`)

![](/images/vlsi/Adder/nsd.png)

Check DRC again.


## 5. M1 and PO connections
Now let's make DRC pleased by connecting the simple poly and metal wires
1. Draw an `M1` rectangular extension from the `VDD!`/`GND!` vias
    - Place `M1-M2` vias (make sure they are 0.1 um squares)
2. Draw rectangles, or paths, to connect every S/D labeled `VDD!`/`GND!` to the supplies
3. Draw poly paths to connect every poly with its neighbor

Check DRC again. 
- All `PO` area issues should go away, as well as some `M1` area issues.
- You will get a `PP` enclosure error. Draw a `PP` rectangle to perfectly cover the `PP`-`NP` gap in the center, and this will go away.

## 6. M2 Connections and Vias
We still have a few sources and drains left. Let's route them vertically using **M2** layer. Draw a single M2 wire with minimum width (0.1 um).

I do **not8* recommend using the vias generated with `o`. They are too fat and ugly, and they are the root cause of DRC miseries if used improperly. Instead, let's manually construct the M1-VIA1-M2 sandwich:

1. Select the **VIA1** `drw` layer. Draw a **0.1 um x 0.1 um** square at the intersection
2. A VIA1 requires enclosure by **both** M1 and M2, of either:
    - **0.04 um** on 2 opposite edges (we almost always choose this one)
    - 0.03 um on all 4 edges
3. Use the ruler tool to measure 0.04. Use `s` to extend the both layers.
    - You may be tempted to extend M1 to the left, but that will violate the M1 spacing DRC rules with the `GND!` wire.
4. Done! Check DRC

![](/images/vlsi/Adder/via1.png)

![](/images/vlsi/Adder/via1_bare.png)


Do the same thing for other nets. You can also use the same technique for power and ground connections.

![](/images/vlsi/Adder/via1_drc.png)


## 7. PO Connections and Contacts
From our floorplan, our input signals `A`, `BS`, `CIN` will arrive from the vertical M2 layers. We can "Update from Source/IO Pins" to create `M2` pins and label them.

We need to via from `M1` all the way to `PO`. There needs to be five layers: `M2-VIA1-M1-CO-PO`. Each layer must satisfy the design rules:

Be aware of the following common design rule violations (all units in um)
- `PO` spacing > 0.12
- `M1` spacing > 0.09; 0.11 in corners
- `M2` spacing > 0.10; 0.12 in corners
- `M1` area > 0.042
- `M2` area > 0.052
- `CO` side length = 0.09
- `VIA1` side length = 0.10
- `CO` must be enclosed by `PO` by > 0.01;
- `CO` must be enclosed by `PO` by > 0.04 on opposite sides; or > 0.025 on all sides
- `CO`/`VIA1` must be enclosed by `M1` by > 0.04 on opposite sides; or > 0.03 on all sides
- `VIA1` must be enclosed by `M2` by > 0.04 on opposite sides; or > 0.03 on all sides

The layout should be straightforward, although there may be a lot of trouble when starting to do these custom contacts and vias. The single `BS` gate in the middle is espcially hard to contact. 
- Any vertical `PO` extension 0.04 um from the `CO` will violate the `PO` spacing rules. Therefore, we extend the `PO` horizontally.
- The `M1` island is too small. Extend it so that it covers the `CO` and `M1` by the DR, and not violate spacing rules with its neighbors

Check DRC. Below I show each layer for more clarity:
![](/images/vlsi/Adder/drc_mp.png)

Measure the distance to its neighbor. Clean!

![](/images/vlsi/Adder/drc_12.png)

I also added the `M2-M1` via to connect the power.

![](/images/vlsi/Adder/drc_full.png)


Once you connect the pins, you should pass LVS too!


CONGRATS on completing 1/3 of this assignment!
# Our Adder

Below is our adder from a few months ago. It is less optimal, but fine.
## Sum
The sum bits use minimum P/N sizing. They can be really well diffusion-shared!

![](/images/vlsi/Adder/sum.png)

We can closely align the PO, M1, and M2 layers

![](/images/vlsi/Adder/sum_det.png)



## Subtraction
You can implement subtraction in two ways
- Static XOR gate
- MUX
We chose the XOR implementation.

# 8-bit Adder
This is *very important*. We need to use our single-bit adder 8 times. You definitely don't want to draw the same thing 8 times. Fortunately, we can **Instantiate** the single-bit layout as a **symbol**, just as how you use the `pch` and `nch` symbols.

## Transformed Adder
Before you do that, though, because we use the alternating VDD-GND-VDD-GND-VDD power grid plan, for odd bits, we have GND on the left, VDD on the right, but for even bits, we have the opposite. You can simply "Flip Vertically". Can you? 

Mostly yes, but with the caveat of pins. Our current M2 pins have "ABC" order, but if flipped, it will have "CBA". It's not a nightmare if you are consistent on that for all flipped bits. A bigger issue are the carry chain wires

![](/images/vlsi/Adder/adder_frame.png)


We created a new schematic and layout `hw6t` for the flipped version by copying (`c`) the `hw6` layout, flipping it, and adjusting the pin orders appropriately. 

![](/images/vlsi/Adder/addert.png)


There are definitely other ways to do this:
- Enforce symmetry in your layout
- Create schematic and layout for 2 bits at a time

## Layout Hierarchy
Now the final push! We want a coherent pattern and minimally wasted space. If you lay out your single bit like this, it's gonna suck. You want it as **tight** as possible

![](/images/vlsi/Adder/old_8b.png)

1. Make sure your `hw6` and `hw6t` layouts are DRC and LVS clean
2. Create a symbol for `hw6` and `hw6t`. It doesn't have to be fancy
3. Create a new 8-bit schematic. Connect the bits with alternating `hw6t` and `hw6`
    ![](/images/vlsi/Adder/8b_schem.png)
4. Check and test the 8-bit schematic on the sample inputs
5. Create a layout. "Generate All From Source"

You will see the 1-bit instances. We need to connect them. 

Layouts communicate across hierarchies through **pins**. If you zoom into the pins, you will see it's labelled. For example, "/SN/SN7"
- "/SN" is the internal net name (sum out)
- "/SN7" is the current net name (7th sum out)

![](/images/vlsi/Adder/8b_label.png)

Wires connected through the pin will be labelled by Virtuoso. Wires connected, but *not* through the pin will **still** be the same net, and checked equally under DRC/LVS. It will just be harder to see. 

In this case, the bottom `VDD` is connected through a pin and labelled. The top one is also connected, but not labelled.
- If you want labels on the top too (say you misaligned the pins), you can lay another M2 *overlapping* with the M2 in the instance (no worries, they will be the same layer) from the pin.

## Alignment

Now for the hairy part: align each bit **perfectly**. Fortunately, our design accommodates **exactly** that. Make sure neighboring M2/M1/vias/pins overlap **exactly**, both vertically and horizontally. In the end, the M2 center points between both ends should be 2.1x8 = 16.8 um. If not, you've done somethign wrong. Your 8-bit layout will have a P-N-P-N-P-N-P-N-P structure

![](/images/vlsi/Adder/adder_ddet.png)


I went up to `M3` for the carry propagation wires, but you may as well do it in `M1`. The `M1` power/ground *vertical* wires don't have to be contiguous. We can via local `M1` wires from the `M2` lanes.

It is good practice to use `M3` for global control signals, such as `SUB`

Here's how it should look like:

![](/images/vlsi/Adder/adder_det.png)



## Overflow
You can 


# Shifter
There's nothing too much to write about the shifter. It's not very interesting.


We choose a **complementary pass transistor MUX** for our shifter. You can also choose an NMOS-only version.
## Sizing

Textbook pp 351-352 discusses pass transistor sizing and layout

![](/images/vlsi/Adder/book1.png)


## Stick Diagram

![](/images/vlsi/Adder/book2.png)

We chose to buffer at the **output** stage to reduce the poly length.

![](/images/vlsi/Adder/shifter_stick.png)


## Layout

You can see the iconic "alternating gates"

![](/images/vlsi/Adder/s1.png)

![](/images/vlsi/Adder/shifter.png)



# Misc
We didn't follow the design rules before, and it sucked that we have to re-layout