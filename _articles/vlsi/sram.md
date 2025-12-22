---
title: "4321 SRAM"
permalink: /articles/vlsi/sram
author: "Ming Gong, Charlotte Chen"
---

{% include toc %}

> This article is under construction.
{: .notice--info}


Now you are at the next *stage* of 4321: the mighty SRAM

> Things can be done parallel here. Throw some tasks to your teammate


# Floorplan
There are a lot of ways to floorplan this. You don't have to, but it would be *really* nice if all the peripherals match the width of the SRAM. The SRAM cell is dense, so we use **column multiplexing**, sharing one set of R/W circuitry for each **two** adjacent columns
- *Logically*, the array is 8x8 SRAM. (8 wordlines, 3-bit addresses)
- *Physically*, we lay it out **4x16**, where each pair of the 16 columns maps to one of the logical 8 columns
- Essentially, we shift a dimension from the row direction to the column dimension. A wordline address bit now becomes the column MUX select bit.

![](/images/vlsi/sram/mux_concept.jpg)

# SRAM Array

> In this article, any $$x\times y$$ represents **row** $$\times$$ **column**

## Demo Array

Take a moment to appreciate this fabulous SRAM. The `065_d499_M4_` prefixes are abbreviated
![](/images/vlsi/sram/s_demo_master.png)
`v1d1_demo_array_4x4` (8x4) has the following components:
- `v1d1_x4 (2x2)` (4x4)
    - `v1d1_x1`
- `v1d1_wells_strap_x2 (1x2)` (1x4)
    - `v1d1_wells_strap_x1` (x4 top, center, bottom)
- `v1d1_row_edge_x2 (2x1)` (4x1) (I think they are decap)
    - `v1d1_row_edge_x1` (x4)
- `v1d1_corner_edge_x1`
- M2 and M4 pins
- **There is an extra M3 layer at the left that will cause DRC errors. Delete it.**

![](/images/vlsi/sram/s_demo_hie.png)



### Inner Cells
Here's a stick diagram in detail. Try to hide the NW and M4 layers, and analyze layer by layer, and appreciate such a beautiful design

![](/images/vlsi/sram/sram_det.png)

Below is an *intensely* annotated stick diagram for the region above. I highlighted the cell at `wordline<2>`, `bit<0>`. You can see the coupled inverters and the access transistors in detail

It takes a while to "calibrate" your view from the schematic to the stick diagram. 

Meanwhile, appreciate its beauty, and try to make your own layout as cute as that.


Don't forget to check DRC and LVS of the SRAM cell. If this fails, then the rest of the article is pointless.

![](/images/vlsi/sram/sram_stick.jpg)

## Layout
Enough appreciation. Now it's time to build our own layout. 

From the previous section, the 8x4 cell uses 4x4 

The task is basically to reassemble the given 8x4 array to 4x16. Shouldn't be too hard as long as you know what you are doing

You can group 4x4 cells together, and then piece 4 of them for 4x16.

1. Make a 4x4 schematic and symbol with four `v1d1_x1` symbols (4 wordlines, bitline `<3:0>`). 
2. Make a 4x4 layout. "Generate All From Source". Piece all 1x1s together
    - You can move an entire row/column, saving lots of work
    - Make sure they are **perfectly** aligned. I'd like to look at the vias, as their sizes are fixed
        - Sanity check, does your 4x4 dimension match with the sample 4x4 layout?
    - Add instances of the top and bottom `wells_strap_x2` to the **layout**

    ![](/images/vlsi/sram/sram_4x4.png)
3. Make a 4x16 schematic and symbol with four of your 4x4
    ![](/images/vlsi/sram/sram_4x16.png)
4. Make a 4x16 layout
    - Add `row_edge` and `corner_edge` instances to the layout
    - Again, make sure everything's **perfectly** aligned
5. **Check DRC and LVS**
6. Now it's time to add the pins. You don't have to, but it will make your bit pitch super clear!
    - The width of the M2 wires vary, but there is a pretty clear "center line"
    - Measure the distance between the center lines of `bit<0>` and `bit<2>`. You should get **2.1 um**. This is the bit pitch I've been talking about
    - Measure the M2 wires to the left of `bit<0>` and to the right of `bit_bar<15>`. You should get **16 um**. If not, something is misaligned.
    - Add M2 pins for power and bitlines, and add M4 pins for power. They don't have to be perfectly square.
    - Add M2 pins for wordlines and power
    - You don't have to be perfect for now. We may get back to it later

![](/images/vlsi/sram/sram.png)


# Decoder

Shepard has probably showed off multiple decoder designs in class and in his practice exams. However, most people converted to a static CMOS decoder for this mini-design projects
- With column MUXing, there are only two rows to decode. 
- We need to **qualify** the wordlines with `phi_1`. We will change the address when `phi_2` is high, and evaluate when `phi_1` is high. If multiple wordlines are high simultaneously, this will be **catastrophic**, as cells will be shorted with each other, and will overwrite each other

We decided to use a 4-in-1 NAND-NOT layout, so that everything fits well inside 4 SRAM rows, and this circuit can be easily expanded to 8/16 rows with predecoding. The drawback? Kind of huge in width. It will be better for *this* project if we can put them to a more squared shape.

The idea is simple: 
1. spam M3 horizontal wires for all signals and power (Yes they fit)
2. Use M2 to fetch the signals vertically from M3
3. Use our M2-VIA2-M1-CO-PO trick to control the gates
4. Route the outputs with M1-VIA1-M2-VIA2-M3

Implementing it is tricky, but once you have one block, the rest is simple.
![](/images/vlsi/sram/dec.png)

# Read Write
Below is the 2-bit (4 pairs of bitlines) R/W schematic, similar to Shepard's lecture notes
1. **Column MUX:** select between adjacent columns to do R/W
2. **Write Select:** we combined the `write` and `data` NMOSes to save a stack height
3. **Read Driver:** branched from `bit_bar`, amplifies with a *skewed* inverter and a bus driver

![](/images/vlsi/sram/wr_sch.png)

> This is legacy design. You can probably benefit more from a horizontal Poly
{: .notice--warning}

We used a vertical Poly layout for this part. You will see the pros and cons in a moment.

We also laid out two units at a time, to account for flipping.

![](/images/vlsi/sram/rw.jpg)


## Testing
My teammate mainly handled this part.

At schematic level, the common failures are:
- Forgot to power `vdd!`/`VDD!`/`VDD`. Sometimes different parts use a different net name for power. If you see your values close to 0, or 0.5, it's very likely a power issue
- Multiple wordlines glitch. Make sure to adjust address when `phi_2` is high. If more than one wordline is high, the memory will overwrite each other
- Off by one inversion: The circuit Shepard presented in class is **inverted**. A simple test will be to invert your input vector
- Clock phase overlap. The circuit should work fine if `phi_1` and `phi_2` are both 50% duty cycle. If you believe this presents an issue, try reducing the duty cycle for both, and slow down the period.
- Qualify your `iobus` input if you are not writing. Otherwise, the SRAM read output will be polluted.
- Improper skew: if `bit` and `bit_bar` variations are not 
- Readability and writability

Make sure your circuit works **very well** at schematic level, or else post-sim will be a **nightmare**!

It is always useful to probe `bit` and `bit_bar`


## Column MUX
4 NMOSes that direct either bit to the R/W circuitry. I originally tried to put all of them in one row, but failed miserably by just a fraction of micrometer. We therefore chose to use "Poly sharing" instead of diffusion sharing. The M1 for the diffusion cross (kind of nasty) to the other edge, instead of Poly crossing as you've seen in your shifter MUX

A lot of wires, but also a lot of space

![](/images/vlsi/sram/mux.png)

The four MUXes (two Polys) on the edge are the column MUX. The central two are the final footer transistor controlled by the write signal

As you can see, the pulldown path is short. Good for delay.


## Write Select

Now to the interesting (and hard) part. In lecture, we know that we can control the write pulldown NMOS of `bit` by `write AND data` (`data_bar` for `bit_bar`). For stability, we also want to qualify this with `phi_1`. Here, our `data` is `iobus`. The logic is 

```
write AND iobus<i> AND phi_1
```

`iobus` will differ from bits, but `write AND phi_1` is the same. We can pull that term out and supply it from **outside**, drastically reducing the complexity and stack height at the inside!

And bubble push:
```
(write NAND phi_1) NOR iobus<i>
```

Omg this is too beautiful

We need `iobus_bar<i>` for `bit_bar<i>`. Fortunately, we have enough space for an inverter in the center
![](/images/vlsi/sram/rw.png)

With this vertical Poly layout, you can do aggressive **diffusion sharing** with neighbors. Align the M1 of your transistors **directly** under the M2 bit pitch. However, if you are not diffusion sharing, there's plenty of wasted space.

## Read Driver

The read driver's pretty straightforward. 
1. First a skewed inverter to handle bitlines
2. A large tristate driver for `iobus`

We chose a 4:1 *width* ratio. You should test it to make sure it works at **schematic** level.

We then used a (600/300)x3 tristate bus driver. Note that it has a stack height of 2. It is discussed in textbook pp 393

![](/images/vlsi/sram/tristate.png)

Also do **NOT** put inverters after the tristate driver. It defeats the purpose of a tristate.


With some turing and diffusion sharing, you can make everything perfectly fit


Should have put more Contacts on the Poly

![](/images/vlsi/sram/rw_real.png)

## What if things don't fit?
Cry, but not too much
1. **Get better.** If your layout skills are horrible, force yourself to get better. Start with diffusion sharing, efficient routing and viaing, avoid oversizing etc.
2. **Resize device** People constantly miss that. Ask you self: Is the device on the **critical path**? How slow would it be if I size it smaller? Can I finger it differently? Can I orient it differently?
3. **Use straight lines** Bends increase contention not only itself, but its neighbors as well! Try to make lines as straight as possible, or **shift** them away from tight regions.
4. **Detour** If you've really tried, take a detour. Find **gaps** on each layer, and consider moving your routing to these gaps to free space for the tight area.
5. **(Temporarily) move to a higher Metal layer** Only do this for short, local routing, as it may horribly interfere with your global routing plans. Also vias are not cheap.
6. **Accept area tradeoffs** If there are truly no ways, increase spacing. Note that this is not an *excuse* to sloppy shit layouts. In our case spacing should always be increased vertically (the horizontal dimension fixed at 2.1 um).
A slightly less area-efficient design is not a failure -- It's a deliberate **tradeoff**. In fact, you can often reclaim the space by fitting in power straps, inverters, or decaps. A sloppy design is a failure, though.

![](/images/vlsi/sram/contention.png)

---
**CONGRATS ON FINISHING HALF THE DESIGN PROJECT!!!**

---

# Peripheral-Peripheral
Here you will start to feel the pain of overall layout organization. There are the following main difficulties
- Decide transistor size to drive the shared signals
    - I typically make it under FO4, then it's fine. I didn't bother too much on the large fanout sizing
- Find a place to place such transistors
- Find a place to *prettily* place such transistors
- Floorplan the power grids for these parts

![](/images/vlsi/sram/pp_stick.png)
> Disclaimer: these sizings are just examples, not real transistor sizings. Calculate your own!

With that, you can lay out the whole thing
![](/images/vlsi/sram/overall.png)

Don't worry too much for getting the "peripheral-peripheral" part perfectly. You will (very likely) need to get back and modify it in your later design



# Testing
## Testbench


## Extraction
You might get the following warnings:

```
WARNING: [FDI3034] Schematic instance XI24/XI63/XI3/XI0<0>/M0 not found, use found instance XI24/XI63/XI3/XI0<0> instead.
WARNING: [FDI3046] Failed to create mapping for device "nchpg_sr". Netlist for "XI24/XI63/XI3/XI0<0>/M0" instance has more pins than schematic view.
WARNING: [FDI3014] Could not find cell mapping for device nchpg_sr. Ignoring instance XI24/XI63/XI3/XI0<0>/M0.
```

Those are fine, since the internal schematic for the 6T SRAM cell is not shown. The instance is used for the extraction.