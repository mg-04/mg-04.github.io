---
title: "4321 Inverter"
permalink: /articles/vlsi/inverter
date: 2025-12-24
---


{% include toc %}

1. [Intro](/articles/vlsi)
2. **Inverter**
3. [Project Plan](/articles/vlsi/floorplan)
4. [Adder and Shifter](/articles/vlsi/adder)
5. [SRAM](/articles/vlsi/sram) 
6. [PLA, Control, Data, Overall](/articles/vlsi/overall)


> Take a read of Shepard's [Online CAD Tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/). It's very comprehensive guide. 
- Below, we’ll walk through the process systematically and highlight common pitfalls so you can avoid a **massive learning curve**.
- If anothing messes up, see if it's in the [Virtuoso FAQ](/articles/vlsi/inverter#virtuoso-faq)
{: .notice--info}


---

# Layout
> Assuming you have already designed and [tested](https://charlottechen.blog/posts/VLSI_testing) the inverter schematic
- You may find `vbit` from `analogLib` useful
{: .notice--success}

## 1. Instance Generator
1. In Virtuoso, create a new "Layout" with the same name as your schematic
2. Use "Connectivity/Generate/All From Source". It will generate the two **transistors**, and a few cyan (M1) **Pins**
    - The instances between *schematic* and *layout* should match. Selecting one highlights the other.
3. **Rotate** the transistors by 90 degrees. 
4. Align the transistors
    - Make sure `NP` and `PP` boundaries **perfectly** align. No **gaps** or **overlaps**

![](/images/vlsi/inv/start.png)

## Layers
Before drawing, it's important to understand each layer in `tsmc-n65`:

> On the sidebar, you can double click on a layer to make it exclusively visible, and inspect each layer individually
{: .notice--info}

### MOSFET
A MOSFET is a piece of silicon with 4 terminals: Gate, Source, Drain, and Body. S and D are typically *symmetrical*.

**Body**  
- `NW` (N-Well): PMOS body
- `SUB` (P-Well, SUBstrate): NMOS body
    - Marked by `PDK`

**Source/Drain** (diffusion)  
- `OD` (Oxide Diffusion): source and drain
- `PP` (P imPlant mask, ~~pimp~~)
    - `PP` ∩ `OD`: p+ diffusion
- `NP` (N imPlant mask)
    - `NP` ∩ `OD`: n+ diffusion

**Gate**  
- `PO` (POlysillicon)

### Metal
Silicon/metal interface
- `CO` (COntact, Ohmic): connects `PO`/`OD` (silicon) with `M1` (metal)
- `M1`: First Metal layer
- `VIA1`: connects `M1` and `M2`
- `M2`: Second Metal layer
- `VIA2`: connects `M2` and `M3`
- and so on...



### Pin
Used to **label** connections across hierarchies. Nothing electrical.



> If you are interested in the physical implementation of these layers, [this](https://www.vlsi-expert.com/2014/) article explains in glorious detail
- In fact, you can manually draw the layers, instead of using the instance generator. Fitting the parameters and passing [DRC](/articles/vlsi/inverter#drc) would be a pain, though.
{: .notice--info}


## 2. Body Taps
Next, we need to tap (via) the Bodies to the power supplies. Click `o` to add `M1-SUB` and `M1-NW` Vias.
- Again, make sure `NP` and `PP` boundaries between the transistors and vias perfectly overlap.

![](/images/vlsi/inv/vias.png)


The Vias have a similar stack of 5 layers connecting Body to Metal:
- `NW` (P) / substrate (N)
- `NP` (P) / `PP` (N)
- `OD`
- `CO`
- `M1`

> Different body taps are functionally equivalent, provided they tap the bodies to respective power rails. One body tap can cover a large region of P/N substrate
- The "Detached Body" option places Body contacts explicitly on individual transistors. We don't need that, since we've already added decidated Body Vias.  
- In typical standard cell design, we typically dedicate **tap** cells placed in parallel with the logic
- Here for our custom layout, we have ample space on the left/right power rails. Placing body taps there saves space.
{: .notice--info}


## 3. Connections
Now, use the rectangle (`r`) or path (`p`) tool to connect the `PO` gate and `M1` source/drain to complete the circuit.
- Use **minimum width** (60 nm for `PO`, 90 nm for `M1`). It should be the same as what's already on the transistors.

![](/images/vlsi/inv/conn.png)

> You are allowed to overlap the rectangles. Only their union counts.
{: .notice--info}

---

# DRC
> Run DRC **as frequently as possible**, especially if you are a beginner!!
{: .notice--warning}

Skip to Shepard's Calibre DRC [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html) and set up the environment


Below are the main types of DRC errors for TSMC N65:
- **Shape rules**
    - Shapes must satisfy a **minimum area**
    - Shapes must have a **minimum width**
    - Shapes must also meet **constraints**, such as a minimum side length
- **Inter-shape rules**
    - **Enclosure**: for example, a Via must be properly enclosed by its associated Metal layers
        - Sometimes, minimum **overlap** or enclosure area also apply.
    - **Spacing**: minimum spacing must be maintained
        - between shapes of the **same layer**, and
        - between shapes on **different layers**, such as spacing to body connections

Here's a (simplified) list from textbook pages 118-119

![](/images/vlsi/inv/dr1.png)

![](/images/vlsi/inv/dr2.png)



Let's run a DRC right now:
![](/images/vlsi/inv/drc_body.png)

RIP, got 4 errors. They are because the `OD` and `PP`/`NP` areas of our Body Vias are too small. Since we have ample space, we can simply make them larger. You can:
1. Increase the number of rows/columns of the Vias
    - This is simple. 4 rows/cols will work
	- Feels like a waste of space for now, but we will expand our logic
2. Manually draw a larger `OD`/`PP`/`NP` around the current layer
    - This is more risky, as changing one layer may violate other spacing/enclosure rules,
    - but useful for aggressive optimizations, as you will see [later](/articles/vlsi/adder#6-m2-connections-and-vias)

![](/images/vlsi/inv/drc_body_fixed.png)


> We are now **DRC clean!**
{: .notice--success}



## 4. Gate Via
There's one more step to connect the gate input. Add a `M1-PO` via.

Similar to the Body Vias, this `M1-PO` also has layers `PO`, `CO`, and `M1`. **All layers** must satisfy DRC rules.


Now run a DRC:

![](/images/vlsi/inv/drc_co.png)

RIP, another two violations. Make only `M1` layer visible for more clarity
- `M1` of the via is too close with our VOUT `M1`.
    - **Fix:** Move either `M1` rectangle away, so that they are at least 0.09 um apart
- `M1` of the via's area is too small. It's like an island
    - **Fix:** Add a larger `M1` rectangle to the via to make the `M1` area more than 0.042 um²

![](/images/vlsi/inv/drc_co_clean.png)

---

# LVS
Use `m` to move the Generated M1 Pins over to the metals. 

Check LVS. Read the [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html) for the setup

![](/images/vlsi/inv/lvs.png)

> If your layout is LVS clean, skip this part
{: .notice--success}

RIP, we got 4 "Incorrect Ports" errors. Calibre LVS somehow does not recognize our pins, despite that they are created with labels! This is very rare...

In this case, first check if Virtuoso recognizes the pin. Try moving the pins around and see if the label ("VOUT") and the cross shows up. If not, delete the pins and do "Connectivity/Update/All from Source" again. Make sure you select the **"Create Label"** option

![](/images/vlsi/inv/lvs_check.png)



Here, Virtuoso *does* have the label, so let's *manually* add the labels to the pins again to let Calibre LVS know.
1. Click `l` and create label "VOUT". 
2. Click the center of your pin
3. Choose "Purpose": "pin" as the object

![](/images/vlsi/inv/lvs_pin.png)

Now, as a **proof of concept**, run LVS again to see if the error count drops to 3:

![](/images/vlsi/inv/lvs_fix.png)

Yep, so add labels to the other three, and you will be **LVS clean!**

---

# Virtuoso FAQ
> When I open Virtuoso, all my instances show up as [red boxes](/images/vlsi/sram/s_demo_master.png)

Click `Shift+F` to display instance details, and `Ctrl+F` to abstract them

---
> "Connectivity/" doesn't have a "Generate"/"Update" option

Open the layout with **Layout XL**.

---
> My pins do not have labels on them (or LVS doesn't recognize them)

In the "I/O Pins" tab of "Connectivity/Generate/All From Source", you have to set "Pin Label/Create Label As/Label". Set:
- "Font Height": 0.1 (recommended) 
- "Layer Name": "Same As Pin"
- "Layer Purpose": "Same As Pin"

---
> Cadence keyboard shortcuts stopped responding

Stacked functions. If you accidentally start commands before previous ones (possibly in other tabs) have cleanly finished, it may mess up Virtuoso's stack, blocking the UI. In this case, **close unused tabs**, and press `ESC` to pop the stack

---
> I'm having trouble selecting the shape I want

Keep clicking the shape, until it is highlighted by a **white box**. The yellow dashed box shows the next shape to be selected.

---
> How to make multibit wires/instances?

Take 8 bits for example: Append `<7:0>` to the label and instance names. You can also splice individual bits off a multibit wire.

---
> My simulation waveform spits nonsense :(

You might forgot to power VDD. This is dumb, but a recurring theme of the project.

---
> My extraction is taking forever

It should be fine for the inverter, but for more complex designs like the adder, extract only **C+CC**. RCC will blow up the number of nets.  
If the extracted delay has jumped by a massive amount (e.g. more than 2x), there's a problem in your layout.