
---
title: "4321 SRAM"
permalink: /articles/vlsi/sram
---

{% include toc %}


# Floorplan
There are a lot of ways to floorplan this. You don't have to, but it would be *really* nice if all the peripherals match the width of the SRAM. The SRAM cell is dense, so we use **column multiplexing**, sharing one set of R/W circuitry for each **two** adjacent columns
- *Logically*, the array is 8x8 SRAM. (8 wordlines, 3-bit addresses)
- *Physically*, we lay it out **4x16**, where each pair of the 16 columns maps to one of the logical 8 columns
- Essentially, we shift a dimension from the row direction to the column dimension. A wordline address bit now becomes the column MUX select bit.

# SRAM Array

# Decoder

# Read Write
## Column MUX

## Write Select

## Read Driver


# Extraction
You might get the following warnings:

```
WARNING: [FDI3034] Schematic instance XI24/XI63/XI3/XI0<0>/M0 not found, use found instance XI24/XI63/XI3/XI0<0> instead.
WARNING: [FDI3046] Failed to create mapping for device "nchpg_sr". Netlist for "XI24/XI63/XI3/XI0<0>/M0" instance has more pins than schematic view.
WARNING: [FDI3014] Could not find cell mapping for device nchpg_sr. Ignoring instance XI24/XI63/XI3/XI0<0>/M0.
```

Those are fine, since the internal schematic for the 6T SRAM cell is not shown. The instance is used for the extraction.