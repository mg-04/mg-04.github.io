---
title: "4321 Inverter"
permalink: /articles/vlsi/inverter
---
> This article is under construction.

Take a read of Shepard's [Online CAD Tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/)

The first real task is to layout an [Inverter](https://www.bioee.ee.columbia.edu/courses/cad/html/layout.html)

It's a pretty comprehensive guide, but if you follow that into your project, for sure you will get in trouble! So let's still systematically go over it, and I'll highlight every possible caveat you might encounter, so it save you a huge learning curve.

# Generated From Source


# Schematic
In your schematic, I'd recommend naming every pin CAPITAL (PEX will convert pins to capital).
![](/images/vlsi/inv/schem.png)

# Layout
## 1. Generate from Source
After "Generate from Source", you will get this. Rotate the devices by 90 degrees. 
![](/images/vlsi/inv/start.png)

## Layers
Before you start , I think it's useful to understand what each layer means here, so you actually know what you are doing, and how to avoid trouble

### Body
- `NW` (N-well): where PMOS sit
- `SUB` (P-well, substrate): where NMOS sit
    - Marked by `PDK`

### Diffusion
- `OD` (Oxide Diffusion): source and drain
- `PP` (P implant mask)
    - When `PP` overlaps `OD` the region becomes p+ doped
- `NP` (N implant mask)
    - When `NP` overlaps `OD`, the region become n+ doped

### Gate
- `PO` (polysillicon): used for gate

### Metal
Electrical wires from silicon
- `CO` (contact): between `M1` and `PO`/`OD`
- `M1` (metal 1): metal wires
- `VIA1`: connect between `M1` and `M2`
- and so on...

### Pin
They are used to label outside connection to higher hierarchies

## 2. Body Via
Now, we need to add the body VIAs. Click "o" to add `M1-SUB` and `M1-NW` VIAs.
- Make sure the `NP` boundary perfectly overlaps with the `PP` boundary. There can't be any **gaps** or **overlaps**

![](/images/vlsi/inv/vias.png)


The new body vias are nothing special. They are simply a stack of 5 layers:
- `NW` (P) / substrate (N)
- `NP` (P) / `PP` (N)
- `OD`
- `CO`
- `M1`

You can double click on a layer to make it exclusively visible, and you can see each layer individually



## 3. Connections
Now let's connect the `PO` gate and `M1` source/drain to complete the circuit:
![](/images/vlsi/inv/conn.png)

# DRC
> It's always good practice to check DRC **as frequently as possible**, especially if you are a beginner!!
Skip to the DRC [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html)

These are the main types of DRC errors for TSMC N65:
- **Spacing**
- **Area**
    - Width, or shape
- **Enclosure** (for example, M1 must enclose `CO` by more than 0.25 um)
- **Body connection**

Let's run a DRC **right now**
![](/images/vlsi/inv/drc_body.png)

RIP, got 4 errors. You should be grateful that we *only* got 4...

2 each for the N and P body vias
- `OD` layer area too small
- `PP`/`NP` layer area too small.

There are two ways to solve it
1. Change the via to have more rows and columns
    - This is simple. Changing it to 4 will work
2. Manually draw a larger `OD`/`PP`/`NP` around the current layer
    - This is more risky, as changing one layer may violate other spacing/enclosure rules
    - but useful for aggressive optimizations, if you know what you are doing

![](/images/vlsi/inv/drc_body_fixed.png)
After fixing it and making sure the area rules are satisfied, we are now DRC clean!


## 4. VIA
We are done, are we? There's one more step to connect a wire from our silicon poly. Add a `M1-PO` via.

The `M1-PO` via they provide also has 3 layers: `PO`, `CO`, `M1` (start, via, destination sandwich). You need to make sure **every** layer does not violate DRC!


Now run a DRC:

![](/images/vlsi/inv/drc_co.png)

RIP, another two violations. Make only the `M1` layer visible for more clarity
- `M1` of the via is too close with our VOUT `M1`.
    - Fix: Move either one away to at least 0.09 um apart
- `M1` of the via's area is too small. It's like an island
    - Fix: Add more `M1` to the via so its area is more than 0.042 um2

![](/images/vlsi/inv/drc_co_clean.png)


# LVS
Move the M1 pins over to the metals. 

Now let's check LVS. Read the [tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/calibre.html) again...

![](/images/vlsi/inv/lvs.png)

RIP, we got 4 "Incorrect Ports" errors. LVS somehow does not recognize our pins and decide, despite they are created with labels! This is very rare

In this case, first check if Virtuoso recognizes the pin. Try moving the pins around and see if the label ("VOUT") and the cross shows up. If not, delete the pins and "Update from Source" again. Make sure you check "Create Label"!

![](/images/vlsi/inv/lvs_check.png)



Here, we have everything, let's *manually* add the labels to the pins again to let LVS know.
- Click "l" and create label "VOUT". 
- Click the center of your pin
- Choose "Purpose": "pin" as the object

![](/images/vlsi/inv/lvs_pin.png)

Now, as a proof of concept, run LVS again to see if the error count drops to 3

![](/images/vlsi/inv/lvs_fix.png)

Yep, so add labels to the other 3, and you will be LVS clean!




# FAQ
> When I open Cadence, all my instances look like red boxes

Click `Shift+F` to display instances, and `Ctrl+F` to hide

> My pins do not have labels on them (or LVS doesn't recognize them)

In "I/O Pins", you have to set "Pin Label/Create Label As/Label", and set the font height to (0.1 recommended), and 
- "Layer Name": "Same As Pin"
- "Layer Purpose": "Same As Pin"

> I
Stacked functions. Close some tabs, and press `ESC`

> My layout nets are not showing up
Open with Layout XL