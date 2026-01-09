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


> Take a read of Shepard's [Online CAD Tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/). It's a pretty comprehensive guide, but if you follow it *blindly* into your project, for sure you will get in trouble! Below, we’ll go through the process systematically and highlight common pitfalls so you can avoid a **massive learning curve**.
{: .notice--info}


---

# Layout
## 1. Generate All From Source
1. Create a new "Layout" the same name as your schematic
2. Go to "Connectivity/Generate/All From Source". You will get two **transistors**, and a few cyan (M1) **Pins**
    - You should see matching instances between schematic and layout. Selecting one highlights the other.
    - Ignore the Pins for now
3. **Rotate** the devices by 90 degrees. 
4. Align the transistors
    - Make sure `NP` and `PP` boundaries **perfectly** align. No **gaps** or **overlaps**
![](/images/vlsi/inv/start.png)

## Layers
Before drawing, it's important to understand the layers we have:

> You can double click on a layer to make it exclusively visible, and inspect each layer individually
{: .notice--info}

### Body
- `NW` (N-well): where PMOS sit
- `SUB` (P-well, substrate): where NMOS sit
    - Marked by `PDK`

### Diffusion
- `OD` (Oxide Diffusion): source and drain
- `PP` (P implant mask)
    - `PP` ∩ `OD`: p+ diffusion
- `NP` (N implant mask)
    - `NP` ∩ `OD`: n+ diffusion

### Gate
- `PO` (Plysillicon): used for gate

### Metal
Electrical wires from silicon
- `CO` (Contact, Ohmic): connects `PO`/`OD` with `M1`  
- `M1`: First Metal layer
- `VIA1`: connects `M1` and `M2`
- and so on...



### Pin
Used to **label** connections across hierarchies. Nothing electrical.



> If you are interested in the physical implementation of these layers, [this](https://www.vlsi-expert.com/2014/) article explains in glorious detail
{: .notice--info}


## 2. Body Vias
Next, add Body Vias. Click `o` to add `M1-SUB` and `M1-NW` Vias.
- Again, make sure `NP` and `PP` boundaries perfectly overlap.

![](/images/vlsi/inv/vias.png)


The Body contacts are nothing special: simply a stack of 5 layers connecting Body to Metal:
- `NW` (P) / substrate (N)
- `NP` (P) / `PP` (N)
- `OD`
- `CO`
- `M1`

> "Detached Body" creates Body contacts explicitly. Not needed if you've used Body Vias  
A Body Via can power a large region of P/N substrate (~30 um)
{: .notice--info}




## 3. Connections
Now let's connect the `PO` gate and `M1` source/drain to complete the circuit:
![](/images/vlsi/inv/conn.png)

---

# DRC
> Run DRC **as frequently as possible**, especially if you are a beginner!!
{: .notice--warning}

Skip to Shepard's Calibre DRC [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html) and set up the environment


These are the main types of DRC errors for TSMC N65:
- **Spacing**
- **Area**
    - Width, or shape
- **Enclosure**
    - E. M1 must enclose `CO` by more than 0.25 um
- **Body connection**

Here's a (simplified) list from textbook pages 118-119

![](/images/vlsi/inv/dr1.png)

![](/images/vlsi/inv/dr2.png)



Let's run a DRC **right now**
![](/images/vlsi/inv/drc_body.png)

RIP, got 4 errors. You should be grateful that we *only* got 4...

2 each for the N and P body vias
- `OD` layer area too small
- `PP`/`NP` layer area too small.

There are two ways to solve it:
1. Increase via rows/columns
    - This is simple. Changing it to 4 will work
2. Manually draw a larger `OD`/`PP`/`NP` around the current layer
    - This is more risky, as changing one layer may violate other spacing/enclosure rules
    - but useful for aggressive optimizations, as you will see [later](/articles/vlsi/adder#6-m2-connections-and-vias)

![](/images/vlsi/inv/drc_body_fixed.png)


> After fixing them and making sure the area rules are satisfied, we are now **DRC clean!**
{: .notice--success}



## 4. Gate Via
There's one more step to connect a wire from our silicon Poly. Add a `M1-PO` via.

Similar to the Body Vias, this `M1-PO` also has layers: 
- `PO`
- `CO`
- `M1`

**All layers** must satisfy DRC rules.


Now run a DRC:

![](/images/vlsi/inv/drc_co.png)

RIP, another two violations. Make only `M1` visible for more clarity
- `M1` of the via is too close with our VOUT `M1`.
    - Fix: Move either one away to at least 0.09 um apart
- `M1` of the via's area is too small. It's like an island
    - Fix: Add more `M1` to the via so its area is more than 0.042 um²

![](/images/vlsi/inv/drc_co_clean.png)

---

# LVS
Move the Generated M1 Pins over to the metals. 

Check LVS. Read the [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html) for the setup

![](/images/vlsi/inv/lvs.png)

RIP, we got 4 "Incorrect Ports" errors. LVS somehow does not recognize our pins and decide, despite they are created with labels! This is very rare...

In this case, first check if Virtuoso recognizes the pin. Try moving the pins around and see if the label ("VOUT") and the cross shows up. If not, delete the pins and "Connectivity/Update/All from Source" again. Make sure you select the **"Create Label"** option

![](/images/vlsi/inv/lvs_check.png)



Here, we *do* have everything, let's *manually* add the labels to the pins again to let LVS know.
1. Click `l` and create label "VOUT". 
2. Click the center of your pin
3. Choose "Purpose": "pin" as the object

![](/images/vlsi/inv/lvs_pin.png)

Now, as a **proof of concept**, run LVS again to see if the error count drops to 3

![](/images/vlsi/inv/lvs_fix.png)

Yep, so add labels to the other three, and you will be **LVS clean!**

---

# Virtuoso FAQ
> When I open Virtuoso, all my instances show up as [**red boxes**](/articles/vlsi/sram#8x8-layout)

Click `Shift+F` to display instances, and `Ctrl+F` to hide them

> My pins do not have labels on them (or LVS doesn't recognize them)

In "I/O Pins", you have to set "Pin Label/Create Label As/Label". Set:
- "Font Height": 0.1 (recommended) 
- "Layer Name": "Same As Pin"
- "Layer Purpose": "Same As Pin"

> Cadence keyboard shortcuts stopped responding

Stacked functions. Close unused tabs, and press `ESC` to quit current functions

> My layout nets are not showing up

Open with **Layout XL**
