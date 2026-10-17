---
title: "CircuitSim: A Simple FPGA-Based Circuit Simulation Accelerator"
collection: publications
category: thesis
permalink: /publication/thesis
excerpt: 'Senior thesis. A SPICE-like transient circuit simulator that offloads its matrix solve to a Gaussian elimination accelerator on an FPGA SoC.'
date: 2026-5-1
authors: Ming Gong
venue: B.A. Thesis, Bard College at Simon's Rock
codeurl: 'https://github.com/mg-04/circuit-sim'
paperurl: '/files/research/thesis/main.pdf'
teaser: '/images/circuitsim/555.png'
---

Senior thesis for the Bachelor of Arts at Bard College at Simon's Rock, advised by Prof. Michael Bergman, with Prof. Stephen Edwards as second reader.

The thesis builds on the [CircuitSim project](/projects/circuitsim/): a SPICE-like simulator that parses netlists, linearizes nonlinear and time-varying components, and solves each step's matrix on a small floating-point Gaussian elimination core on the FPGA. It is validated on circuits from filters and rectifiers up to a transistor-level 555 timer.
