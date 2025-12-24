---
title: "Intro to the Design Project"
layout: single
permalink: /articles/vlsi/floorplan
---

{% include toc %}

Before even starting the project, read through the requriements so you know what you *should* be doing.

# Architecture

## Bus

Our microprocessor consists of:
- **Bus**: one writer, multiple readers
- **Computation**: adder, shifter
- **Accumulator** (Acc): A flip-flop holding temporary values (think of it as a register)
- **SRAM**

![](/images/vlsi/floorplan/dataflow.png){: .align-center}

## Building Blocks
Here is the suggested floorplan from PS9

![](/images/vlsi/floorplan/block.png){: .align-center}


- The accumulator is split into two D-latches
- One additional latch is used to latch the memory output from the bus
- Three bus drivers are needed
    - Acc → Internal bus
    - External bus → Internal bus
    - Internal bus → External bus

---

# ISA
Try to derive what to do, combining with the data path above:

When **holding**, the value in Acc must not change. The MUX should select the shifter path, but **bypass** it, effectively feeding Acc back to itself


| Opcode | Assembly | Description                 | Internal bus driven by | MUX | Action | 
|--------|----------|-----------------------------| ------ | ---- | --- | 
| 000    | NOP      | Hold Acc    | -- | Hold | No change
| 001    | LOAD     | Mem[i] ← External bus       |external bus| hold |  Memory write
| 010    | STORE    | External bus ← Mem[i]      | SRAM | hold | Memory read; Drive external bus
| 011    | GET      | Acc ← Mem[i]               | SRAM | Memory | Memory read
| 100    | PUT      | Mem[i] ← Acc               | Acc | Hold | Memory write
| 101    | ADD      | Acc ← Acc + Mem[i]         | SRAM | Adder | Memory read; Bypass shifter
| 110    | SUB      | Acc ← Acc - Mem[i]         | SRAM | Adder | Memory read; Bypass shifter
| 111    | SHIFT    | Left logical shift of Acc  | -- | Shifter | Don't bypass

> Yes, this ISA is terrible for logic simplification.  
And yes, there are obvious optimizations.

---

# Floorplan

> Floorplan! Floorplan! Floorplan! Many layouts don't suck at the end, they suck at the **beginning**! A bad initial decision will make you either **REDO** from scratch, or make **WORSE** and **WORSE** compromises to accommodate that
{: .notice--danger}


We've laid out an inverter. The processor is basically many inverter-like gates neatly coordinated.

There are always 3 things to plan:
- Data
- Control
- Power




## Metal Routing
> This is Shepard's suggested floorplan, **rotated 90 degrees**
{: .notice--info}

Adapt a consistent Metal routing rules.

![](/images/vlsi/floorplan/stick.jpg)

Since the Polys and their Diffusion contact M1s are horizontal, make
- **Odd** Metal layers horizontal
- **Even** Metal layers vertical.
- There can be local violations, especially at lower levels



This is an 8-bit processor built from identical 1-bit slices placed side by side. Since we use near-minimum device widths, each slice can have the identical **widths**, enabling a clean, regular layout.
- Larger transistors will be made of multiple **fingers**


This creates an organized **vertical grid**, reference for all other wires. Keep the M2 widths and spacings **uniform** to maintain this regularity
- Reserve these long, continuous rails for VDD and GND
- Alternate N-type and P-type diffusions
- Place power straps (body Vias) at the center

> You may also want to keep all blocks with the **same height**, so the horizontal grid is also organized.

Each block will have input/output data, primarily in M2; this is the **data path**. 

Blocks also need control signals, such as subtraction and MUX select. Such signals are typically identical across all bits and can be shared through a horizontal M3 layers; this is the **control path**



