---
title: "CircuitSim"
excerpt: "An analog/digital circuit simulator on FPGA written in C and Verilog, featuring Modified Nodal Analysis and hardware-accelerated matrix inversion."
collection: projects
date: 2025-05-20
authors: Ming Gong, Case Schemmer, Andrew Yang, Jary Tolentino, Faustina Cheng
venue: Embedded Systems, Spring 2025
teaser: /images/cc/555.png
---

{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}

A+ final project for CSEE 4840 Embedded Systems, Edward's favorites <br/><img src='/images/cc/staricon.png'>

An analog/digital circuit simulator, written in C

[Here](/posts/2025/05/cs)'s a bit more detail!

Features:
- Modified Nodal Analysis
- Companion linear models for non-linear devices
- Newton-Raphson approximation
- Hardware-accelerated matrix inverter
- On-chip RAM

Things are not perfect, but good enough. I'm planning to make this my SR Thesis.
- [Report](https://www.cs.columbia.edu/~sedwards/classes/2025/4840-spring/reports/CircuitSim-report.pdf)
- [Slides](https://www.cs.columbia.edu/~sedwards/classes/2025/4840-spring/reports/CircuitSim-presentation.pdf)
- [Files](https://www.cs.columbia.edu/~sedwards/classes/2025/4840-spring/reports/CircuitSim.tar.gz)

