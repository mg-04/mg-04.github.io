---
title: "Gallery"
permalink: /articles/vlsi/gallery
author: "Ming Gong, Charlotte Chen"
date: 2025-12-29
authors:
    - Ming Gong
    - Charlotte Chen
---

{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}

Here's a picture page, just for fun

1. [Intro](/articles/vlsi)
2. [Inverter](/articles/vlsi/inverter) 
3. [Project Plan](/articles/vlsi/floorplan)
4. [Adder and Shifter](/articles/vlsi/adder)
5. [SRAM](/articles/vlsi/sram) 
6. [PLA, Control, Data, Overall](/articles/vlsi/overall)
    - **Gallery**

{% include toc %}

---

# Overall Layout

## 1x  
![](/images/vlsi/pretty/overall/overall_1.png)

## 2x  
![](/images/vlsi/pretty/overall/overall_2.png)

## 4x  
![](/images/vlsi/pretty/overall/overall_4.png)

## 8x  
![](/images/vlsi/pretty/overall/overall_8.png)

## 16x  
![](/images/vlsi/pretty/overall/overall_16.png)

---

# Various Layers

## OD-CO-PO  
![](/images/vlsi/pretty/layers/overall_1.png)

## PO-CO-M1  
![](/images/vlsi/pretty/layers/overall_2.png)

## M1-VIA1-M2  
![](/images/vlsi/pretty/layers/overall_3.png)

## M2-VIA2-M3  
![](/images/vlsi/pretty/layers/overall_4.png)

## M3-VIA3-M4  
![](/images/vlsi/pretty/layers/overall_5.png)
