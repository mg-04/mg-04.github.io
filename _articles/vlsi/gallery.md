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

{% include vlsi-series.html current=7 %}

{% include toc %}

---

# Overall Layout

## 1x  
![](/images/vlsi/pretty/overall/overall_1.png)

## 2x  
![](/images/vlsi/pretty/overall/overall_2.png)

## 4x  
![](/images/vlsi/pretty/overall/overall_4.png){: .blurred}

## 8x  
![](/images/vlsi/pretty/overall/overall_8.png){: .blurred}

## 16x  
![](/images/vlsi/pretty/overall/overall_16.png){: .blurred}

---

# Various Layers

## OD-CO-PO  
![](/images/vlsi/pretty/layers/overall_1.png){: .blurred}

## PO-CO-M1  
![](/images/vlsi/pretty/layers/overall_2.png){: .blurred}

## M1-VIA1-M2  
![](/images/vlsi/pretty/layers/overall_3.png){: .blurred}

## M2-VIA2-M3  
![](/images/vlsi/pretty/layers/overall_4.png)

## M3-VIA3-M4  
![](/images/vlsi/pretty/layers/overall_5.png)

---

# Manhattan Sunrise
Nothing can be more rewarding than watching the Manhattan **sunrise**! Walking out DRC clean, LVS clean; sleep? not quite.

<div class="photo-grid">
  <a class="image-popup" href="/images/vlsi/manhattan/skyline-dawn.jpg"><img src="/images/vlsi/manhattan/skyline-dawn.jpg" alt="Skyline at dawn" loading="lazy"></a>
  <a class="image-popup" href="/images/vlsi/manhattan/broadway-dawn.jpg"><img src="/images/vlsi/manhattan/broadway-dawn.jpg" alt="Dawn over the Upper West Side" loading="lazy"></a>
  <a class="image-popup" href="/images/vlsi/manhattan/golden-clouds.jpg"><img src="/images/vlsi/manhattan/golden-clouds.jpg" alt="Golden clouds" loading="lazy"></a>
  <a class="image-popup" href="/images/vlsi/manhattan/tower-sunrise.jpg"><img src="/images/vlsi/manhattan/tower-sunrise.jpg" alt="Tower and flag at sunrise" loading="lazy"></a>
  <a class="image-popup" href="/images/vlsi/manhattan/window-grid.jpg"><img src="/images/vlsi/manhattan/window-grid.jpg" alt="Morning through the window grid" loading="lazy"></a>
  <a class="image-popup" href="/images/vlsi/manhattan/lab-reflection.jpg"><img src="/images/vlsi/manhattan/lab-reflection.jpg" alt="The lab, reflected" loading="lazy"></a>
</div>

{% include vlsi-series.html current=7 position="bottom" %}
