---
title: "Project Floorplan"
layout: single
permalink: /articles/vlsi/floorplan
---
Before even starting the project, I would recommend going over the requirements, so you know what you *should* be doing

# Architecture

## Bus

Our microprocessor will have the following parts:
- Bus: there will be one writer and multiple readers
- **Computation**: adder, shifter
- **Accumulator**: A flip-flop that holds temporary values (think of it as your register)
- **SRAM**

## Building Blocks
Here is a detailed floorplan from PS9

- The accumulator is split into two D-latches
- One additional latch is used to latch the memory output from the bus
- Three bus drivers are needed
    - Accumulator -> Internal bus
    - External bus -> Internal bus
    - Internal bus -> External bus

# Opcodes
Try to derive what to do, combining with the data path above:

Whenever you are vacant, the value in `Acc` should not change. The MUX should select the shifter path, but bypass the shifter, so the `Acc` is essentially feeding back the old value (I know it's stupid)


| Opcode | Assembly | Description                 | Internal bus driven by | MUX | What to do | 
|--------|----------|-----------------------------| ------ | ---- | --- | 
| 000    | NOP      | Hold `Acc` value    | | Hold
| 001    | LOAD     | Mem[i] ← External bus       |external bus| hold |  write internal bus value to memory
| 010    | STORE    | External bus ← Mem[i]      | SRAM | hold | drive external bus by internal bus
| 011    | GET      | Acc ← Mem[i]               | SRAM | Memory
| 100    | PUT      | Mem[i] ← Acc               | Acc | Hold | Make SRAM write from bus
| 101    | ADD      | Acc ← Acc + Mem[i]         | SRAM | Adder | Bypass shifter
| 110    | SUB      | Acc ← Acc - Mem[i]         | SRAM | Adder | Bypass shifter
| 111    | SHIFT    | Left logical shift of Acc  |  | Shifter | Don't bypass

> Of course, this instruction set is SHIT for logic simplification!

> Of course, you can probably see optimizations here and there


# Floorplan
> Floorplan! Floorplan! Floorplan! Many layouts don't suck at the end, they suck at the **beginning**! A bad initial decision will make you either **REDO** from scratch, or make **WORSE** and **WORSE** compromises to accomodate that

There are always 3 things to plan: data, control, and power

## Data Path
Please plan a **tight** datapath layout!

We have laid out an inverter. Think of adders as a series of gates like the inverter. 

While in schematic level, you could try to achieve an *optimal* sizing, it's *rarely* achieved in layout. Layout is always a compromise between delay, area, and perfection. 
- Plus it's very hard to find any global optima. It's all about approximates.

## Power Distribution


## Control Path
The control signals are a bit random

## Pitfalls
Below I'll show you some common pitfalls


