---
title: "Out-of-Order Rename Core"
permalink: /projects/rename/
excerpt: "4-wide register renaming back end for an OoO core in SystemVerilog: reorder buffer, issue queue, unified physical register file, and a rename unit with single-cycle branch recovery.<br>Parallel prefix-count logic and slot banking placed #1 in area and #3 in frequency on the class leaderboard."
teaser: /images/projects/rename/top.png
course: "Modern Computer Architecture and Design, Fall 2026"
collection: projects
tags:
  - architecture
  - digital
date: 2026-10-16
authors: "Ming Gong, Paul Wright, Christian Cherry"
---

The rename and scheduling back end of a 4-wide out-of-order processor, written in SystemVerilog and synthesized in Cadence Genus

---
# Overview
- **4-wide** dispatch, issue, and retire
- 32 architectural / 256 physical registers
- 128-entry reorder buffer, 64-entry issue queue
- Branch recovery with 8 specRAT checkpoints, **single-cycle restore**
- **61.9 MHz**, 0.505 mm² at the default sizing

Four modules work together: the RRU renames and allocates, the IQ schedules, the ROB keeps program order, and the PRF tracks every physical register's state

![](/images/projects/rename/top.png)

---
# Modules

## Register Renaming Unit (RRU)
Maps architectural registers to physical registers and removes false dependencies
- **Allocate**: picks 4 free physical registers at once with a parallel prefix count over the PRF states
- **Rename**: slots 0–3 rename in order through a working copy of the specRAT, so younger instructions in a batch see older ones' new mappings
- **Checkpoints**: snapshots the specRAT at every branch, and restores it in one cycle on a mispredict

![](/images/projects/rename/rru.png)

## Issue Queue (IQ)
Holds renamed instructions until their operands are ready
- **Wakeup**: every entry snoops the execution broadcasts, including the cycle it is inserted
- **Select**: lowest ready slot first, ranked by a prefix count with no age comparators
	- 24% faster and 35% smaller than oldest-first, for under 0.1% more cycles across the traces

![](/images/projects/rename/iq.png)

## Reorder Buffer (ROB)
A 128-entry circular buffer that retires instructions in program order
- Retires up to 4 completed entries per cycle from the head
- On a mispredict, younger entries are marked squashed and drain through the normal retire path, freeing their registers without committing

![](/images/projects/rename/rob.png)

## Physical Register File (PRF)
A unified register file: speculative and architectural values live together, told apart by the specRAT and archRAT
- Each register is a small FSM: *Available → Renamed → Valid → Architectural*
- No separate free list: the RRU allocates directly from the state array
- Commit only updates mappings, never moves data

![](/images/projects/rename/prf.png)

---
# Leaderboard Version
A separate, tuned variant for the class [leaderboard](https://cmu-ece18740.github.io/labs.html), where we placed **#1 in area** and **#3 in frequency** (group *phwright*)

## Frequency Optimizations
- **Allocation one cycle ahead**: the RRU computes the next free registers in advance and stores them in flops, taking the allocator off the rename path. The candidates are kept as one-hot vectors, so no decoder is needed
- **Early ready bits**: source ready bits no longer wait for the allocator; the RRU applies that cycle's completion broadcasts itself
- **One-hot ROB head pointer**
- **Displaced register in the ROB**: each entry carries the register it overwrites, so the PRF no longer looks up the archRAT at commit
- **Parallel PRF next state** across all ports
- **Cheaper flush check**: the IQ's "younger than the flushing branch" test uses three compares instead of a subtraction per entry
- **Circular checkpoint buffer** instead of shifting every checkpoint on each retire

## Area Optimizations
- **Banking by slot mod 4** for IQ, RRU, and ROB. Each bank has one read and one write port instead of a 4-way mux on every slot
	- Biggest area win: IQ area 218k → 95k, RRU 220k → 119k
- **Two-level prefix count** in the RRU instead of one flat 256-wide tree
- **Narrower machine**: issue width 2 instead of 4, and 4 checkpoints instead of 8

