---
title: "4321 Overall and PLA"
permalink: /articles/vlsi/overall
---

{% include toc %}

> I hate putting all these into one article, but all these parts: overall layout, data blocks, and PLA have to be designed and optimized together. 

It's not hard to lay out a PLA, but it's hard to do it *well*
> We didn't do your PLA too well either. I've seen designs that completely shocked me

> Again, most of this can be done in parallel. There is something called successive approximation to an optimal layout. However, **plan you PLA carefully** before you start your layout!!! It will make your team converge fast!

# Power Grid
I probably don't need to reiterate that, but you need the entire chip to have an ample supply of power.

# Data Path

Here's a detailed floorplan derived from Shepard's PDF, following all his implementations

> You don't have to understand everything perfectly for now. Go back and read the floorplan article.

![](/images/vlsi/pla/overall_stick.jpg)

## Connecting Data Blocks


Since we don't have some of the blocks yet. Let's start the overall layout by connecting the **shifter** and the **adder**
1. Create a schematic.
2. Instantiate the shifter and the adder. Align their power pins
3. Shift them closer together vertically, until there is a **critical** DRC spacing violation
    - This does not include NW, PP, NP spacing, as you can fill that with a rectangle
    - The limiting factor is typically M1 or PO
    - If you have a M3 grid defined for both, align that grid.
4. Fix any DRC errors. If the M2/pins stand out too far, fix them.
5. Connect power at M2 level, if they are not already connected
6. **Connect the signal wires** The `out<i>` of the shifter should go in `A<i>` of the adder
7. Check DRC and LVS again. Make sure nothing's shorted

> include a picture

These elements are quite trivial. Just make sure you handle the inversions correctly

## M4 Data Wires
Our design did not reserve space for long-distance data wires at M2 (I don't think it's possible). Those need to go to M4. For example, the `B<i>` input of the adder comes from `Acc`, which is supplied from the very top.

At M4 we can have a very organized grid. Since it's spacious, I added an additional pair of thick power wires.

![](/images/vlsi/pla/wire_data.png)

Above are the M4 wires above the adder block, where data wires are the densest.


> I really don't like the color of M4. It makes parallel wires look like the Twin Towers...

> You can already see if the M2s are misaligned, or too dense, it would be a pain to layout. In future data blocks, lay them out so they are **compatible** with connecting other data blocks.


Okay, so let's knock out the rest of the data blocks. You are a layout master rn. Pretty simple.

## Latch
Same schematic as hw5.

![](/images/vlsi/pla/latch.png)

## MUX
We chose a one-hot encoding for the inputs, making decoding much simpler in the MUX end

We used an NMOS-only layout, since the inputs are buffered; The outputs go immediately to the latch, which is also buffered.

![](/images/vlsi/pla/mux.png)

## Bus Driver
Same as the SRAM bus driver, except to not use a *skewed* inverter
![](/images/vlsi/pla/bus_driver.png)

There are a total of 4 bus drivers:
    - Accumulator -> Internal bus
    - External bus -> Internal bus
    - Internal bus -> External bus
    - SRAM -> Internal bus (done)

> There are ways to optimize it, for example, make the 4th input of the MUX take from the external bus, so external inputs are driven to the internal bus through the `Acc` -> `Int` driver



# PLA

## Planning
> **Before** you start your PLA, have a clear floorplan of the entire processor

- What control signals are needed from the PLA? (link to the first floorplan article) What are their formats (binary encoded? One-hot?) Do they need to be inverted? Can I optimize the encoding in any obvious ways?
- Based on your dataflow blocks, where shall I place it? On what **order**?

In this project, we used a one-hot encoding for the MUX outputs. (one extra output, but simplicity in MUX design and internal logic)

## Schematic from Espresso
Make a table of the logical outputs.


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

Now convert the table above to **actual** logic signals. Be **precise**.


### General principles
- When something is not active (this include `NOP`), do not modify the values in `Acc`
- If something is a don't-care, you have two choices
    - Use `X`: room to simplify PLA logic
    - Turn it off: saves power

As you will see from the Espresso output, because the instructions are fully encoded (3 opcodes -> 8 bytes), there's not much room for optimization on the AND-OR plane.

Make sure you handle inversion correctly. 

Make a schematic from your Espresso logic. Start with minimum sizing for both NMOS and the pullup PMOS

> This consumes a lot of power, though, as the pullup PMOS is not "weak" enough, leading to a lot of crowbar. You may wan tto use non-minimum length for that.

**Test your PLA under all possible input vectors, and see if the output is expected**


## Layout
The textbook explains it on page 539.
![](/images/vlsi/pla/textbook_stick.png)

However, this diagram has an important drawback: the Polys are too long. You will get huge delay at the top!

![](/images/vlsi/pla/pla.png)

The OR plane is laid pretty densely. Further optimizations are possible, but it's good enough. 
- I broke the long Poly into **shorter pieces** and laid a higher-level Metal above it. Whenever there is a gate needs a product term, it is **Viaed** to the Poly (complex routing, but very worth it)

The AND plane is not. I didn't fully understand the textbook's stick diagram when I first did it. As a result, I rotated transistor by 90 degrees
- In our design, we didn't have enough space Via to Poly at every gate. Therefore, we put Metal-Poly Via stacks where there is an empty space, and used thicker Polys (not sure of the side effects), to reduce the Poly resistance as much as possible

**Before** you actually do layout, please determine the preferred orientation of the PLA. 
- We did not do that, but then decided to rotate our entire PLA by 90 degrees, which messed up with our Metal grid orientation. Very suboptimal!

Start at somewhere with a dense transistors, and lay it out edging DRC to build a "standard cell". The rest of the layout basically follows the schematic

- I recommend extracting the PLA and test its functionality and delay. Make sure you don't fuck up

## What we could have done better
I was so proud of our PLA design, yet there are still so much to improve: 
- Weaker PMOS pullup
- Better AND plane design
- Better Metal orientation planning

# Control Path

Below are the important signals. Make sure to reserve a M4 slot for it
- `phi_1` and `phi_2`
- `instr<0:5>`

## Latched Control Signals

## 

# Wrap Up!
## Decap


## Pins

## 遮羞布




