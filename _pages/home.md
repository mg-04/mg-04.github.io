---
permalink: /
title: "Ming Gong"
author_profile: true
redirect_from: 
  - /home/
  - /home.html
---

<div class="home" markdown="1">

<p class="home-intro">
First-year ECE PhD student at <strong>Carnegie Mellon University</strong>, advised by Prof. Ken Mai, working on digital VLSI and computer architecture. B.S. in Computer Engineering from <strong>Columbia University</strong>.
</p>

<nav class="home-hot" aria-label="Popular pages">
  <a href="/articles/vlsi"><i class="fas fa-fw fa-microchip" aria-hidden="true"></i><span><strong>VLSI Layout Guide</strong><small>Columbia 4321 project, inverter to full processor</small></span></a>
  <a href="/projects/circuitsim/"><i class="fas fa-fw fa-wave-square" aria-hidden="true"></i><span><strong>CircuitSim</strong><small>FPGA-accelerated SPICE-like simulator</small></span></a>
  <a href="/teaching/2025-fundies"><i class="fas fa-fw fa-chalkboard-teacher" aria-hidden="true"></i><span><strong>Fundies Study Guides</strong><small>Head TA notes for CSEE 3827</small></span></a>
</nav>

## Research

I'm interested in the intersection of **circuit design** and **low-level systems**: how hardware is built, how it fails, and how it interacts with software.

<h3 class="home-sub">Current <span>· VLSI Design Group, CMU</span></h3>

<div class="research-feature">
  <a class="rf-card" href="/publication/yolov8">
    <svg class="rf-fig" viewBox="-19.5 7.5 259 113" role="img" aria-label="FP32 bit field with the exponent MSB flipped">
      <text class="rs-flip-text" x="21.75" y="30">bit 30: 0 → 1</text>
      <path class="rs-arrow" d="M15.75 26V56"/>
      <text class="rs-label rs-small" x="9.25" y="50">31</text>
      <text class="rs-label rs-small" x="61.25" y="50">23</text>
      <text class="rs-label rs-small" x="210.75" y="50">0</text>
      <rect class="rs-sign" x="6" y="58" width="6.5" height="26"/>
      <rect class="rs-flip" x="12.5" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="19" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="25.5" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="32" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="38.5" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="45" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="51.5" y="58" width="6.5" height="26"/>
      <rect class="rs-exp" x="58" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="64.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="71" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="77.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="84" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="90.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="97" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="103.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="110" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="116.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="123" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="129.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="136" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="142.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="149" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="155.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="162" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="168.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="175" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="181.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="188" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="194.5" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="201" y="58" width="6.5" height="26"/>
      <rect class="rs-man" x="207.5" y="58" width="6.5" height="26"/>
      <g class="rs-brace"><path d="M6 90v4h6.5v-4M12.5 90v4h52v-4M64.5 90v4h149.5v-4"/></g>
      <text class="rs-label rs-small" x="9.25" y="104">s</text>
      <text class="rs-label rs-small" x="38.5" y="104">exponent</text>
      <text class="rs-label rs-small" x="139.25" y="104">mantissa</text>
    </svg>
    <div class="rf-text">
      <h4>Hardware Fault Injection in YOLOv8</h4>
      <p>Which bit flips silently break object detection, and which layers to protect.</p>
    </div>
  </a>
  <a class="rf-card" href="/publication/efpga">
    <svg class="rf-fig" viewBox="0 0 220 96" role="img" aria-label="Row of three eFPGA blocks with a routed net through two switch boxes">
      <g class="rs-track">
        <path d="M76 2V94M80 2V94M84 2V94M136 2V94M140 2V94M144 2V94"/>
        <path d="M2 12H218M2 16H218M2 20H218M2 76H218M2 80H218M2 84H218"/>
      </g>
      <g class="rs-sb">
        <rect x="70" y="6" width="20" height="20"/><rect x="130" y="6" width="20" height="20"/>
        <rect x="70" y="70" width="20" height="20"/><rect x="130" y="70" width="20" height="20"/>
      </g>
      <g class="rs-lb">
        <rect x="26" y="28" width="44" height="40"/><rect x="90" y="28" width="40" height="40"/><rect x="150" y="28" width="44" height="40"/>
      </g>
      <path class="rs-net" d="M70 40H80V16H140V58H150"/>
      <circle class="rs-pin" cx="70" cy="40" r="3"/><circle class="rs-pin" cx="150" cy="58" r="3"/>
    </svg>
    <div class="rf-text">
      <h4>Embedded FPGA Routing</h4>
      <p>Heterogeneous eFPGA architectures and more efficient routing fabrics.</p>
    </div>
  </a>
</div>

<h3 class="home-sub">Interests</h3>

<div class="home-cards">
  <div class="home-card">
    <i class="fas fa-microchip" aria-hidden="true"></i>
    <h3>IC Design</h3>
    <p><a href="/articles/vlsi">Digital</a> and <a href="/projects/analog/">analog</a> IC, from transistors to <a href="/projects/fft/">RTL-to-GDS</a></p>
  </div>
  <div class="home-card">
    <i class="fas fa-bolt" aria-hidden="true"></i>
    <h3>Hardware Acceleration</h3>
    <p><a href="/projects/circuitsim">Custom accelerators</a> on FPGAs, and the <a href="/projects/rename/"> cores</a> they sit next to</p>
  </div>
  <div class="home-card">
    <i class="fas fa-terminal" aria-hidden="true"></i>
    <h3>Systems Programming</h3>
    <p>Drivers, <a href="/projects/os/">kernels</a>, and the software layer that talks to <a href="/posts/2026/10/pyvisa">real hardware</a></p>
  </div>
</div>

<h3 class="home-sub">Before</h3>

<ul class="home-past">
  <li>
    <span class="home-year">2026</span>
    <div><a href="/publication/thesis">CircuitSim: an FPGA circuit simulation accelerator</a><br>
    <small>B.A. thesis · Simon's Rock · Prof. Michael Bergman, Prof. Stephen Edwards</small></div>
  </li>
  <li>
    <span class="home-year">2026</span>
    <div><a href="/publication/cecg">Continuous vital signs monitoring with a loose T-shirt</a><br>
    <small>MobiDx '26 · Prof. Xia Zhou, Columbia</small></div>
  </li>
  <li>
    <span class="home-year">2025</span>
    <div><a href="/publication/ic">Earth's inner core structure via ultrasonic scattering</a><br>
    <small>Physics of the Earth and Planetary Interiors · Prof. Michael Bergman, Simon's Rock</small></div>
  </li>
  <li>
    <span class="home-year">2025</span>
    <div><a href="/publication/2025-04-14-Barmak">Deep learning for thin-film grain boundary detection</a><br>
    <small>Yale Undergraduate Research Conference · Prof. Katayun Barmak, Columbia</small></div>
  </li>
  <li>
    <span class="home-year">2024</span>
    <div><a href="/publication/gaussian">Machine learning for pure component property estimation</a><br>
    <small>Engineering · Prof. Xi Chen, Zhejiang University</small></div>
  </li>
</ul>

More details, posters, and reports are in the [research](/research/) section.

## Teaching

I like to master hard and interesting classes, and pass on my knowledge to others.

<ul class="home-teach">
  <li><span>2026</span><div>TA, <a href="/teaching/2026-vlsi">18-422/622 Digital Integrated Circuit Design</a>, CMU <small>· <a href="/posts/2026/10/elmore">recitation notes</a></small></div></li>
  <li><span>2026</span><div>TA, <a href="https://www.cs.columbia.edu/~sedwards/classes/2026/4840-spring/index.html">CSEE 4840 Embedded Systems</a>, Columbia</div></li>
  <li><span>2025</span><div>Head TA, <a href="/teaching/2025-fundies">CSEE 3827 Fundamentals of Computer Systems</a>, Columbia <small>· study guides</small></div></li>
  <li><span>2022–24</span><div>Think Tank drop-in tutor, Simon's Rock <small>· <a href="/sr-archive">archived materials</a></small></div></li>
</ul>

## Personal

<ul class="home-personal">
  <li><i class="fas fa-fw fa-bus" aria-hidden="true"></i><span>I am a <a href="https://en.wikipedia.org/wiki/User:MGD04">roadgeek</a>. I'm a fan of roads, buses, trains (and their connections). I love long road trips and bus rides as a way to unwind.</span></li>
  <li><i class="fas fa-fw fa-seedling" aria-hidden="true"></i><span>I was a <a href="https://www.youtube.com/@minggong">PvZ YouTuber</a>, still playing casually from time to time.</span></li>
  <li><i class="fas fa-fw fa-archive" aria-hidden="true"></i><span>I love archiving. I keep records of my old files, and it is always fun to look back at them. This website serves my purpose well too!</span></li>
</ul>


</div>
