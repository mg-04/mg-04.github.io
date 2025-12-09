



# Floorplan
There are a lot of ways to 


# Extraction
You might get the following warnings:

```
WARNING: [FDI3034] Schematic instance XI24/XI63/XI3/XI0<0>/M0 not found, use found instance XI24/XI63/XI3/XI0<0> instead.
WARNING: [FDI3046] Failed to create mapping for device "nchpg_sr". Netlist for "XI24/XI63/XI3/XI0<0>/M0" instance has more pins than schematic view.
WARNING: [FDI3014] Could not find cell mapping for device nchpg_sr. Ignoring instance XI24/XI63/XI3/XI0<0>/M0.
```

Those are fine, since the internal schematic for the 6T SRAM cell is not shown. The instance is used for the extraction.