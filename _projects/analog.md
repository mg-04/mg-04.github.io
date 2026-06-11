---
title: "Two-Stage OTA"
excerpt: "Two-stage operational transconductance amplifier with extensive DC/AC/step testing and PVT variation analysis."
collection: projects
date: 2025-11-20
authors: "Elijah Johnson, Ming Gong"
teaser: '/images/projects/analog.png'
venue: "Analog Electronic Circuits, Fall 2025"
---

{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}

A two-stage OTA. See slides [here](https://docs.google.com/presentation/d/1X57wWXOmFS8GEKzkkm-Z88IRd0pvfkJFl6O1uyyqaIM/edit?usp=sharing) (Columbia accounts only)

# Design
- $$I_{DDmax}$$ = 446 $$\mu A$$
- Gain = 9.988
- Integrated noise power = 10.3 $$\mu V_{RMS}$$

![](/images/projects/analog.png)

# Testing
- DC Operating point
- DC transfer curve
- AC open loop, loop, closed loop gain
- Transient step response
- PVT variations