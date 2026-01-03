---
title: "4321 SRAM"
permalink: /articles/vlsi/sram
author: "Ming Gong, Charlotte Chen"
date: 2025-12-31
---

{% include toc %}


Now you are at the next *stage* of 4321: the mighty **SRAM**

> Many parts of this PS can be done in parallel. Get your teammate to work!
{: .notice--info}

1. [Intro](/articles/vlsi)
2. [Inverter](/articles/vlsi/inverter) 
3. [Project Plan](/articles/vlsi/floorplan)
4. [Adder and Shifter](/articles/vlsi/adder)
5. **SRAM**
6. [PLA, Control, Data, Overall](/articles/vlsi/overall)

---


# Floorplan
There are a lot of ways to floorplan the SRAM. You don't have to, but it would be *really* nice if all the peripherals match the width of the SRAM array. 

Because the SRAM cell is extremely dense, we use **column multiplexing**, sharing one set of R/W circuitry for each **two** adjacent columns
- *Logically*, the array is 8x8. (8 wordlines, 3-bit addresses; 8 bits for `iobus`)
- *Physically*, we lay it out as **4x16** (16 bitline *pairs*), where each pair of the **adjacent** physical column map to one logical column
- Essentially, we shift a dimension from rows into columns to the column: one wordline address bit becomes the **column MUX select**.

![](/images/vlsi/sram/mux_concept.jpg){: .align-center}

---

# SRAM Array

> Throughout this article, an array written as $$x\times y$$ always mean **row** $$\times$$ **column**
{: .notice--info}

## 8x8 Layout
The following demo array was given in **Fall 2025**.

Take a moment to appreciate this fabulous SRAM. The `065_d499_M4_` prefixes are abbreviated for clarity
![](/images/vlsi/sram/s_demo_master.png)

`v1d1_demo_array_4x4` (8x4) contains:
- `v1d1_x4 (2x2)` (4x4)
    - `v1d1_x1`
- `v1d1_wells_strap_x2 (1x2)` (1x4)
    - `v1d1_wells_strap_x1` (power strap)
- `v1d1_row_edge_x2 (2x1)` (4x1) (I think they are decap)
    - `v1d1_row_edge_x1` (x4)
- `v1d1_corner_edge_x1`
- M2 and M4 pins
- **There is an extra M3 layer at the left that will cause DRC errors. Delete it.**

![](/images/vlsi/sram/s_demo_hie.png)



### Inner Cells
Here is an SRAM section zoomed in. Try to hide the NW and M4 layers, and analyze layer by layer, and appreciate such a *fantastic* design

![](/images/vlsi/sram/sram_det.png)

Below is its *intensely* annotated stick diagram. I highlighted the cell at `wordline<2>`, `bit<0>`, clearly showing the coupled inverters and access transistors.

![](/images/vlsi/sram/sram_stick.jpg)


Meanwhile, appreciate its elegance, and try to make your own layout just as cute


> Don't forget to check **DRC and LVS** of the SRAM cell. If there are nontrivial errors, **tell Shepard to fix immediately!**
{: .notice--danger}



## 4x16 Layout
Enough appreciation--time to build. 

The provided 8×4 array is constructed from 4×4 blocks. Your task is to reorganize this into 4×16. As long as you understand what’s happening, this is very manageable.

You can group 4x4 cells together, and then piece 4 of them for 4x16.

1. Make a 4x4 schematic and symbol with four `v1d1_x1` symbols
    - 4 wordlines, bitline `<3:0>`
2. Generate a 4x4 layout. 
    - Move entire rows/columns to save effort
    - Make sure they are **perfectly** aligned. I'd like to look at the vias, as their sizes are fixed
        - Sanity check, does your 4x4 dimension match with the sample 4x4 layout?
    - Add instances of the top and bottom `wells_strap_x2` to the **layout**. They don't appear in the schematic, but that's OK.

    ![](/images/vlsi/sram/sram_4x4.png)
3. Create a 4x16 schematic and symbol with four of your 4x4
    ![](/images/vlsi/sram/sram_4x16.png)
4. Generate a 4x16 layout
    - Add `row_edge` and `corner_edge` instances to the layout
    - Again, make sure everything's **perfectly** aligned
5. **Check DRC and LVS**
6. Add the pins.
    - The width of the M2 wires vary, but there is a pretty clear "center line"
    - Measure the distance between the center lines of `bit<0>` and `bit<2>`. You should get **2.1 um**. This is the bit pitch I've been talking about
    - Measure the M2 wires to the left of `bit<0>` and to the right of `bit_bar<15>` (GND). You should get **16.8 um**. If not, something is misaligned.
    - Add M2 pins for power and bitlines. They don't have to be perfectly square.
    - Add M3 pins for wordlines and power
    - Add M4 pins for power
    - You don't have to be perfect for now. We will refine later

![](/images/vlsi/sram/sram.png)

---

# Decoder

Shepard has probably showed off multiple decoder designs in lecture and practice exams. However, most people converted to a **static CMOS decoder** for this project
- With column MUXing, only **two** rows need decoding. 
- Wordlines must be **qualified** with `phi_1`. 
    - Address change happens when `phi_2` is high
    - Evaluation happens when `phi_1` is high. 
    - Multiple (**even transiently**) active wordlines will lead to **catastrophic** data corruption, as cells will be shorted.

We chose a 4-in-1 **NAND-NOT** layout that fits neatly within four SRAM rows and scales naturally with predecoding.

> The drawback? Kind of huge in width. It will be better for *this* project if we can put them to a more squared shape.
{: .notice--warning}


The idea is simple: 
1. Spam M3 horizontal wires for all signals and power (Yes they fit)
2. Use M2 to fetch the signals vertically from M3
3. Use our M2-VIA2-M1-CO-PO stack to control the gates
4. Route the outputs with M1-VIA1-M2-VIA2-M3

![](/images/vlsi/sram/dec.jpg){: .align-center}

Implementing it is tricky, but once you have one block, the rest is simple.

![](/images/vlsi/sram/dec.png)

---

# Read Write
Below is the 2-bit (4 bitline *pairs*) R/W schematic, closely following lecture
1. **Column MUX** selects between adjacent columns.
2. **Write Select** pulls down the bitliens. 
    - We merged the `write` and `data` NMOSes to save a stack height
3. **Read Driver** taps from `bit_bar`, amplifies with a *skewed* inverter and a bus driver

![](/images/vlsi/sram/wr_sch.png)




## Testing
At schematic level, the common failures are:
- **Forgot to power** `vdd!`/`VDD!`/`VDD`. 
    - If node voltage hover near 0V, or 0.5V, it's very likely a power issue
    - The SRAM cell implicitly uses `vdd!`, and after extraction, it may appear as `VDD!`.
    - At schematic level, there is a simple fix
        - Use 1V `vdc` to drive `vdd!` relative to `gnd!`. 
        - Use 1V `vdc` to tie all other powers and `gnd!`
        - Use **0V** `vdc` to tie all other grounds and `gnd!`
- **Wordline glitch**
    - Addresses much change only when `phi_2` is high. 
    - Probe all wordlines to ensure they are **one-hot**
- **Off-by-one inversion**: 
    - The lecture circuit is **inverted**
    - Simple test: invert your input vector
- **Clock phase overlap**
    - The circuit should work fine if `phi_1` and `phi_2` are both 50% duty cycle. 
    - If problems appear, try reducing the duty cycle for both, and slow down the period.
- **Readability and writability**
    - This is mostly handled in the SRAM cell. 
    - Make sure bitline transistors add minimal **parasitics**.  Close-to-minimum sizings are fine.
    - **Probe** `bit` and `bit_bar` to see if it's a skew issue
- **Tristate issues**
    - Only **one driver** should be connected to `iobus`
    - When writing, `iobus` is driven by the testbench sources. The read driver should be in [tristate](/articles/vlsi/sram#read-driver).
    - When reading, `iobus` is driven by the read driver. Use **transmission gates** in the **testbench** to **disconnect** the testbench sources!

> Make sure your circuit functions **very well** at schematic level, or else post-sim will be a **nightmare**! 
{: .notice--warning}


## Stick Diagram
> This is legacy layout. Horizontal gates may save a lot more space
{: .notice--warning}

We used a vertical Poly layout for this part. You will see the pros and cons in a moment. We laid out two units at a time.

![](/images/vlsi/sram/rw.jpg)


## Column MUX
Four NMOS devices steer either column into the R/W circuitry.

We initially attempted a single-row diffusion-shared layout and missed by a fraction of um :( The final solution uses gate sharing instead.

A lot of wires, but also a lot of space

![](/images/vlsi/sram/mux.png)

The pulldown path is short. Good for delay.


## Write Pulldown

Now to the interesting (and hard) part. In lecture, we know that we can control the write pulldown NMOS of `bit` by `write AND iobus` (`iobus_bar` for `bit_bar`). For stability, we also want to qualify this with `phi_1`. The logic is 

```
write AND iobus<i> AND phi_1
```

`iobus<i>` will differ from bits, but `write AND phi_1` is the same. We **factor out** the shared term and supply it from **outside**, drastically reducing the complexity inside!

And bubble push:
```
(write NAND phi_1) NOR iobus<i>
```

Omg this is too beautiful

We need `iobus_bar<i>` for `bit_bar<i>`. Fortunately, there's ample space to squeeze in an inverter

![](/images/vlsi/sram/rw.png){: .align-center}

Vertical Poly allows aggressive diffusion sharing if S/D Contact and Metal is aligned **directly** under the M2 bit grid. Otherwise, space is wasted quickly.


## Read Driver

The read driver's pretty straightforward. 
1. A skewed inverter to handle bitlines
2. A large tristate driver for `iobus`

We chose a 4:1 *width* ratio. You should test it to make sure it works at **schematic** level.

We then used a (600/300)x3 C²MOS tristate bus driver. Note that it has a stack height of 2. It is discussed in textbook pp 393

![](/images/vlsi/sram/tristate.png){: .align-center}

> Do not add inverters **after** a tristate driver. That defeats the point.
{: .notice--warning}



With careful tuning and diffusion sharing, you can make everything perfectly fit


![](/images/vlsi/sram/rw_real.png){: .align-center}

## What if things don't fit?
Cry, but not too much
1. **Check the basics.** Start with diffusion sharing, efficient routing and viaing, avoid oversizing etc.
2. **Resize device.** People constantly miss that. Ask you self: Is the device on the **critical path**? How slow would it be if I size it smaller? Can I finger it differently? Can I orient it differently?
3. **Use straight lines.** Bends increase contention not only itself, but its neighbors as well! Try to make lines as straight as possible, or **shift** them away from tight regions.
4. **Detour.** If you've really tried, take a detour. Find **gaps** on each layer, and consider moving your routing to these gaps to free space for the tight area.
5. **(Temporarily) move to a higher Metal layer.** Only do this for short, local routing, as it may horribly interfere with your global routing plans. Also vias are not cheap.
6. **Accept tradeoffs.** If there are truly no ways, increase spacing. Note that this is not an *excuse* to sloppy layouts. In our case spacing should always be increased vertically (the horizontal dimension fixed at 2.1 um).  
A slightly area-inefficient design is not a failure -- It's a deliberate **tradeoff**. In fact, you can often reclaim the space by fitting in power straps, inverters, or decaps. 

![](/images/vlsi/sram/contention.png)
An example of diffusion sharing and detour

---
> **CONGRATS ON FINISHING HALF THE DESIGN PROJECT!!!**
{: .notice--success}


# Peripheral-Peripheral
The rest of the circuit is what I call the "peripheral" of peripheral circuits, which include
- PMOS for cell precharge
- Logic for `(write NAND phi_1)`
- A couple of inverted control signals
- Power grids and pins

This is where **overall** layout organization starts to hurt. The main challenges are:
- Decide transistor size to drive the shared control signals
    - Calculate the total fanout
    - I typically make it under FO4, which is fine in practice 
    - I chose area over delay, not accurately optimizing large-fanout drivers.
- Find a place to place such transistors
- Find a place to *prettily* place such transistors
- Floorplan the grids that integrate well with the rest of the design

> Here's how I did it  
1. Draw the core transistors within the grid. Pass DRC. (proof of concept)
2. Roughly connect the remaining structures (even if not DRC clean) to pass LVS (proof of concept)
3. Go back and refine the details. Resolve the remaining DRC issues.
4. STOP for now. Don't try to make it perfect, as you will probably revisit it
{: .notice--info}


![](/images/vlsi/sram/pp_stick.png)
> **Disclaimer**: these sizings are for an older version. Calculate your own!
{: .notice--warning}

With these decisions in-place, you can lay out the whole thing:
![](/images/vlsi/sram/overall.png)



---

# Calibre
It's a pain dealing with third-party libraries

## LVS
You may get a few LVS warnings on **M2 pin short**. This is from the `v1d1_x1` cells' pin **naming**. The M4 pins are fine.
- We externally connected power through **M4** and M2 at the **boundary**
- As long as you leave the shorted pins in the center untouched, it should work fine

![](/images/vlsi/sram/lvs_clean.png)

## PEX
You might get the following warnings:

```
WARNING: [FDI3034] Schematic instance XI24/XI63/XI3/XI0<0>/M0 not found, use found instance XI24/XI63/XI3/XI0<0> instead.
WARNING: [FDI3046] Failed to create mapping for device "nchpg_sr". Netlist for "XI24/XI63/XI3/XI0<0>/M0" instance has more pins than schematic view.
WARNING: [FDI3014] Could not find cell mapping for device nchpg_sr. Ignoring instance XI24/XI63/XI3/XI0<0>/M0.
```

Those are fine, since the internal schematic for the 6T SRAM cell is not shown. The entire instance is used for the extraction.

They post-extraction delays are around 50 ns.