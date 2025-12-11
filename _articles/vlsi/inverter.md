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

The new body vias are nothing special. They are simply a stack of 5 layers:
- `NW` (P) / substrate (N)
- `NP` (P) / `PP` (N)
- `OD`
- `CO`
- `M1`

You can double click on a layer to make it exclusively visible, and you can see each other

## 3. Connections



![](/images/vlsi/inv/vias.png)

# DRC
Now, skip to DRC immediately, it will help you locate any possible potential errors!

# Via

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