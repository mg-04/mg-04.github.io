---
title: "FFT Accelerator"
excerpt: "RTL-GDS flow of a high-performance 1024-point Radix-2 DIF FFT core in TSMC 65nm CMOS with 400 MHz clock and 39.8 MS/s throughput."
teaser: /images/projects/ad.png
course: "Advanced Digital Design, Spring 2026"
collection: projects
date: 2026-5-25
authors: "Ming Gong"
---


Design and VLSI Implementation of a high-performance, 1024-point Radix-2 DIF FFT core

---
# Architecture
- 16-bit fixed-point precision
- Data SRAM, twiddle factor ROM
- TSMC 65 nm CMOS process


---
# Optimization Features
- **Four-stage interleaved pipeline**: Dedicated FSM controller that coordinates alternating read, execute, and writeback, balancing cycle time and keeping memory utilization near 100%
- **RTNE ALU**: 3 dB SQNR improvement
- **Programmable scaling mask**: Let the user trade between accuracy and overflow protection depending on input profiles

![](/images/projects/ad/fft.png)

---
# Physical Implementation
Full RTL-to-GDSII layout flow via Synopsys Design Compiler, QuestaSim, Cadence Innovus, and Virtuoso
- **Clock frequency**: 400 MHz (limited by twiddle ROM). Logic capable for 500 MHz
- **Throughput**: 39.8 MS/s
- **Area**: 0.148 mm², mostly data SRAM
- **Precision**: 60 dB SQNR, 0.0067% NRMSE against FP models

![](/images/projects/ad/virtuoso.png)

---
# Simulation
- Post-APR Qsim on Python FP golden model and bit-accurate C Int16 model 
- Gate-level simulation and power analysis on a subset of inputs

![](/images/projects/ad/qsim-apr.png)