---
title: "4321 Inverter"
permalink: /articles/vlsi/inverter
---
> This article is under construction.

Take a read of Shepard's [Online CAD Tutorial](https://www.bioee.ee.columbia.edu/courses/cad/html/)

The first real task is to layout an [Inverter](https://www.bioee.ee.columbia.edu/courses/cad/html/layout.html)

It's a pretty comprehensive guide, but if you follow that into your project, for sure you will get in trouble! So let's still systematically go over it, and I'll highlight every possible caveat you might encounter, so it save you a huge learning curve.

FAQ
> When I open Cadence, all my instances look like red boxes

Click `Shift+F` to display instances, and `Ctrl+F` to hide

> My pins do not have labels on them (or LVS doesn't recognize them)

In "I/O Pins", you have to set "Pin Label/Create Label As/Label", and set the font height to (0.1 recommended), and 
- "Layer Name": "Same As Pin"
- "Layer Purpose": "Same As Pin"