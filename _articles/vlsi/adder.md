---
title: "4321 Adder and Shifter"
permalink: /articles/vlsi/adder
date: 2025-12-24
---

{% include toc %}

Now comes the first real task of 4321: adder

> This is very, very important. You will learn the fundamentals of tight layout and diffusion sharing!
{: .notice--info}

1. [Intro](/articles/vlsi)
2. [Inverter](/articles/vlsi/inverter) 
3. [Project Plan](/articles/vlsi/floorplan)
4. **Adder and Shifter**
5. [SRAM](/articles/vlsi/sram) 
6. [PLA, Control, Data, Overall](/articles/vlsi/overall)

---


# Overview
- Fix a bit pitch of 2.1 um
- Use ripple carry
- Make a (rough) stick diagram before you start
- Edge DRC
- Do not use the default Vias
- Diffusion share, and if you can't, put FETs as closely as DRC allows
- Leave room for upper-level Metal routing

> Below are some inefficiencies in our implementation. Don't copy them blindly.
{: .notice--warning}


> **Adder**
- More organized M2 data grid
- Smaller sizing on the non-critical path PFETs
- Better diffusion sharing with S/D swapping
- Using inverted `COUT` to save a gate in the propagation path
- MUX-based `SUB` select
- Use an odd number of fingers for better diffusion sharing
- You don't have to put body vias everywhere
- An organized M3 power grid and M4 segments  
{: .notice--warning}


> **Shifter**
- Since we are buffering all I/O, we can do the MUX with NMOS only
- Shift wires on M3, not M1 (that will save a lot of space between the stages)  
and a lot of more...  
{: .notice--warning}

---

# Design

A ripple carry adder/subtracter has 3 parts: 
- Subtraction inversion
- Carry generation
- Sum generation   

The CMOS implementation is pretty standard, and you can find plenty of resources

## Sizing
Textbook page 432 discusses the sizing

![](/images/vlsi/Adder/sizing.png){: .align-center}


The minimum width of our technology is 150 nm
- Below that, the MOSFETs will turn into a **dogbone** shape, which actually takes more space!
We used the following sizing
- Critical path: 300 nm * 4 / 150 nm * 4
- Non-critical path: 300 nm / 150 nm
    - It's a better idea to size the PMOS to 150 as well :( We went lazy, but it's fine

---

# Schematic
Below is our carry schematic. If you want to use the textbook sizing, change the non-critical path NMOS to 150 nm.

![](/images/vlsi/Adder/schem.png){: .align-center}

A few notes:
- Use multiple fingers so every transistor **equal width**
- SIet up one P/NMOS with the *parameters*, then **duplicate** them over
- Connect all PMOS bodies to VDD!, NMOS bodies to GND!. No exception
- Label the nets and explicitly add the IO pins
- I recommend using capital letters for net names, and global VDD!/GND!

> I will refer to the device numbers Mx in the layout section. They will differ in your schematic
{: .notice--info}

## Stick Diagram
Make a stick diagram of your adder layout. This [UMich note](https://www.eecs.umich.edu/courses/eecs427/w07/lecture8.pdf) shows diffusion sharing with *single fingers*. Adapt it to your design.

Alternatively, you can also not plan and do **"vibe layout"**, sometimes not bad

![](/images/vlsi/Adder/adder_stick.png)

This stick diagram is rotated 90 degrees. I used magenta for PMOS OD, and dark grey for NMOS OD. 

Note that I only drew with one finger. In the actual layout things will be a bit different.

---

# Carry Circuit Walkthrough
## 1. Bit Pitch!
Right after "Generate All From Source", draw your M2 [bit pitch](/articles/vlsi/floorplan#metal-routing). 
- Center-to-center **2.1 um**
- Width: 0.1 um

![](/images/vlsi/Adder/pitch.png)

You can use the `p` shortcut to draw a path. It shows its DRC rules, too

![](/images/vlsi/Adder/p.png)

## 2. `A` and Body Via
Same thing as the inverter
1. Add the M1-NW and M1-SUB vias. 
    - **Align their centers with the M2!**
2. Place the 8/4 transistors gated by `A`. 
    - Make sure PP and NP touch, but not overlap


## 3. Diffusion Sharing
Find the single-fingered transistors gated by `A`. 
- The top terminal (S) should be connected to `GND!`, so does the bottom terminal (S) of the four-fingered device. 
- We can make them share the same diffusion

Move the transistors together:
![](/images/vlsi/Adder/diff0.png)

Move the bottom transistor further up, and release your mouse. Virtuoso snaps them together.
![](/images/vlsi/Adder/diff1.png)

Repeat for the PMOS

Now, check DRC. I would recommend deleting the transistors you haven't yet placed and Connectivity/*Update* (not *Generate*) them back, so their DRC disconnections doesn't obstruct any actual errors. 

![](/images/vlsi/Adder/t1.png)

You will get quite a few errors. It's complaining that the M1 and PO areas are too small. That's *fine*, since we haven't connected them yet

Now, restore the deleted transistors by "Connectivity/**Update** All From Source"

### S/D Swap

For M30/M5, with its drain to `COUTN`. However, the generated instance has its source `net1` on the outside. We need to swap the source and the drain.

1. Select the FET, click "q"
2. Go to "Parameter", check "S D swap"

![](/images/vlsi/Adder/sd.png)

Now you can happily diffusion share!

## 4. Non-sharing Neighbors
> Most people fuck up on this one. They start crying once they could't diffusion share
{: .notice--warning}


We run out of diffusion shares for M28/M26, a suboptimal situation. 

The key is to know what can still be overlapped, and what can't. 
- NW and PP/NP rectangles **can overlap**. The bodies have the same potential.
- OD regions are different nets. They need to be **0.13 um** apart
    - This happens exactly when the PP/NP boxes overlap with the neighboring OD

![](/images/vlsi/Adder/nsd.png)

Check DRC again.


## 5. Simple connections
Now let's make DRC pleased by connecting the simple poly and metal wires
1. Draw an M1 rectangular extension from the `VDD!`/`GND!` vias
    - Place M1-M2 vias (make sure they are 0.1 um squares)
2. Draw rectangles, or paths, to connect every S/D labeled `VDD!`/`GND!` to the supplies
3. Draw poly paths to connect every poly with its neighbor

Check DRC again. 
- All PO area issues should go away, as well as some M1 area issues.
- You will get a PP enclosure error. Draw a PP rectangle to perfectly cover the PP-NP gap in the center, and this will go away.

## 6. M2 Connections and Vias
We still have a few sources and drains left. Let's route them vertically using **M2** layer. Draw a single M2 wire with minimum width (0.1 um).

> I do **not** recommend using the vias generated with `o`. They are too fat and ugly, and they are the root cause of DRC miseries if used improperly. Instead, let's manually construct the M1-VIA1-M2 sandwich
{: .notice--warning}

1. Select the **VIA1** `drw` layer. Draw a **0.1 um x 0.1 um** square at the intersection
2. A VIA1 requires enclosure by **both** M1 and M2, of either:
    - **0.04 um** on 2 opposite edges (we almost always choousese this one)
    - 0.03 um on all 4 edges
3. Use the ruler tool to measure 0.04. Use `s` to extend the both layers.
    - You may be tempted to extend M1 to the left, but that will violate the M1 spacing DRC rules with the `GND!` wire.
4. Done! Check DRC

![](/images/vlsi/Adder/via1.png)

![](/images/vlsi/Adder/via1_bare.png)


Do the same thing for other nets. You can also use the same technique for power and ground connections.

![](/images/vlsi/Adder/via1_drc.png)


## 7. PO Connections and Contacts
From our floorplan, our input signals `A`, `BS`, `CIN` will arrive from the vertical M2 layers. We can "Update/All From Source/IO Pins" to create M2 pins and label them.

We need to via from M1 all the way to PO. There needs to be five layers: M2-VIA1-M1-CO-PO. Each layer must satisfy the design rules:

> Be aware of the following [common design rule](/articles/vlsi/inverter) violations (all units in powers of um)
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
{: .notice--warning}



The layout should be straightforward, although there may be a lot of trouble when starting to do these custom contacts and vias. The single `BS` gate in the middle is especially hard to contact. 
- Any vertical PO extension 0.04 um from the CO will violate the PO spacing rules. Therefore, we extend the PO horizontally.
- The M1 island is too small. Extend it so that it covers the CO and M1 without violating spacing rules with its neighbors

Check DRC. Below I show each layer for more clarity:
![](/images/vlsi/Adder/drc_mp.png)

Measure the distance to its neighbor. Clean!

![](/images/vlsi/Adder/drc_12.png)

I also added the M2-M1 via to connect the power.

![](/images/vlsi/Adder/drc_full.png)


Once you connect the pins, you should pass LVS too!


**CONGRATS** on completing 1/3 of this assignment!
{: .notice--success}

---

# 1-Bit Adder

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

---

# 8-Bit Adder
This is *very important*. You do **not** want to draw this eight times. Fortunately, we can **Instantiate** the single-bit layout as a **symbol**, just as the `pch` and `nch` symbols.

## Flipped Adder
Because we use the alternating VDD-GND-VDD-GND-VDD [power grid plan](/articles/vlsi/floorplan#metal-routing)
- Odd bits: GND left, VDD right
- Even bits: VDD left, GND right  
You can simply "Flip Vertically". Can you? 

Mostly yes, but with the caveat on **pin order**. 
- Our current M2 pins have "ABC", which will turn to "CBA" if flipped. 
- `cin` currently comes from the left, and `cout` from the right. They need to be flipped.

![](/images/vlsi/Adder/adder_frame.png)


We created a new schematic and layout `hw6t` for the flipped version by copying (`c`) the `hw6` layout, flipping it, and adjusting the pin orders appropriately. 

![](/images/vlsi/Adder/addert.png)


> There are definitely other ways to do this:
- Enforce symmetry for simple layouts
- Build schematic and layout for [2 bits at a time](/articles/vlsi/overall#mux)
{: .notice--info}

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

Layouts communicate across hierarchies through **Pins**. If you zoom into the Pins, you will see it's labelled. For example, "/SN/SN7"
- "/SN" is the internal net name (sum out)
- "/SN7" is the current net name (7th sum out)

![](/images/vlsi/Adder/8b_label.png)

- Wires connected **through a pin** are automatically labelled by Virtuoso. 
- Wires connected, but *not* through a pin will **still** be the same net, and checked equally under **DRC/LVS**. Just harder to see.

In the case above, the bottom M2 `VDD` is connected through a pin and labelled. The top M2 is also connected, but not labelled.
- If you want the top M2 to be labelled as well (say you [misaligned the pins](/articles/vlsi/overall#connecting-data-blocks)), simply draw another M2 segnment *overlapping* the instance M2 **from the pin** (no worries, they are the same layer).

## Alignment

Now the hairy part: align each bit **perfectly**. Fortunately, our design accommodates **exactly** that. 

Make sure neighboring M2/M1/vias/pins overlap **exactly**, both vertically and horizontally. 
- The M2 center points between both ends should be 2.1x8 = 16.8 um. If not, you've done something wrong.
- Your 8-bit layout will have a [P-N-P-N-P-N-P-N-P](/articles/vlsi/floorplan#metal-routing) structure

![](/images/vlsi/Adder/adder_ddet.png)


> I went up to `M3` for the carry propagation wires, but you may as well do it in `M1`. The `M1` power/ground *vertical* wires do **not** have to be contiguous. We can via local `M1` wires from the `M2` power lanes.
{: .notice--info}

It is good practice to use `M3` for **global control signals**, such as `SUB`

Here's how it should look like:

![](/images/vlsi/Adder/adder_det.png)



## Overflow
Get `c7` and `c8` from M3. In our top-level layout, I placed the control logic near the LSB, so the `overflow` signal needs a long detour. It's cleaner to place it as the **MSB**

> Do a **C+CC** extraction only. RCC might crash Cadence
{: .notice--danger}


---

# Shifter
> There's nothing too much to write about the shifter. It's not very interesting.
{: .notice--info}



We choose a **complementary pass transistor MUX** for our shifter. You can also choose an NMOS-only version.
## Sizing

Textbook page 351-352 discusses pass transistor sizing and layout

![](/images/vlsi/Adder/book1.png){: .align-center}


## Stick Diagram

![](/images/vlsi/Adder/book2.png){: .align-center}

We chose to buffer at the **output** stage to reduce the poly length.

![](/images/vlsi/Adder/shifter_stick.png)


## Layout

You can see the iconic "alternating gates"

![](/images/vlsi/Adder/s1.png)

![](/images/vlsi/Adder/shifter.png)



