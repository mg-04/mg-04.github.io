---
layout: archive
title: "Ming Gong"
permalink: /resume/
author_profile: true
redirect_from:
---

{% include base_path %}

<div class="cv" markdown="1">

Pittsburgh, PA \| [Full CV →](/cv)
{: .cv-meta}

ECE PhD student at CMU specializing in digital VLSI and computer architecture, with hands-on RTL-to-GDSII and post-silicon validation experience and three peer-reviewed publications in hardware, signal processing, and ML.

## Education

<span class="cv-date">2026 – present</span> **Carnegie Mellon University**  
*PhD in Electrical and Computer Engineering*

<span class="cv-date">2024 – 2026</span> **Columbia University**  
*BS in Computer Engineering*, Summa Cum Laude · GPA 4.26/4.33

<span class="cv-date">2021 – 2024</span> **Bard College at Simon's Rock**  
*BA in Physics*, Summa Cum Laude · GPA 3.99/4.0

## Experience

<span class="cv-date">Jul. 2026 – present</span> **Graduate Research Assistant**  
*VLSI Design Group, CMU*
- Built a PyTorch fault-injection framework for YOLOv8n to size the trusted partition for a secure-FPGA + Jetson deployment. Identified a 448-weight critical set (1% of FLOPs) at the network’s input and output boundaries.
- Exploring heterogeneous eFPGA architectures and routing fabric configs to improve interconnect efficiency.
- Building a PyVISA-based automated post-silicon testing framework to extract ASIC operating margins.

<span class="cv-date">Jan. 2025 – May 2026</span> **Teaching Assistant**  
*Columbia University*
- TA for Embedded Systems
- Head TA for Fundamentals of Computer Systems
- CSEE ODS [notetaker](/ods)

<span class="cv-date">Jan. 2025 – May 2026</span> **Research Assistant with Dr. Xia Zhou**  
*Mobile X Lab, Columbia University*
- Designed hybrid FPCB electrodes with a capacitive motion-reference channel and driven bias for a loose-shirt ECG; 92.7% full-waveform detection at rest (r = 0.89) and 4.58 bpm HR error while walking.
- Built multichannel impedance-monitoring PCBs (schematic to bring-up) for impedance plethysmography (IPG) of fingertip blood flow.
- Designed, fabricated, and tested fabric sensors integrated into SoftSleep orthopedic pillows.

<span class="cv-date">Jun. – Aug. 2025</span> **Algorithms Intern**  
*Alibaba Group*
- Built deep-search LLM agents for large-scale business web scraping, raising business-development contact email search success from 20% to 60%.
- Fine-tuned Qwen multilingual LLMs with supervised fine-tuning (SFT) to improve translation quality across 92 languages.

<span class="cv-date">Jun. 2022 – Jun. 2025</span> **Physics Intern with Dr. Michael Bergman**  
*Bard College at Simon's Rock*
- Cast directionally solidified and fine-grained Zn-alloy samples (0.2 to >30 mm grains) and ran ultrasonic pulse-echo experiments at 1–10 MHz across 90 measurement spots on 4 samples.
- Developed an echo-detection algorithm defining a new scattering quality factor; first-author [paper](https://doi.org/10.1016/j.pepi.2025.107456) (PEPI 2025).
- Presented a poster at the 2024 SEDI Conference.

<span class="cv-date">Mar. 2022 – Jul. 2024</span> **Research Assistant with Dr. Xi Chen**  
*Zhejiang University*
- Benchmarked DNN, CNN, and decision tree architectures to model nonlinear pure component properties.
- Co-authored a peer-reviewed [paper](https://doi.org/10.1016/j.eng.2023.08.024) on ML-based pure component property estimation (Engineering, 2024).

## Publications

- Leung, H. M. C., Tong, K., **Gong, M.**, Bui, N., & Zhou, X. (2026). [Continuous Electrocardiogram Monitoring with a Loose T-Shirt](https://doi.org/10.1145/3842657.3842785). *Hot Topics in Mobile and Wireless Systems for Health (MobiDx '26)*. ACM.
- **Gong, M.** & Bergman, M. I. (2025). [An Experimental Ultrasonic Method to Determine a Scattering Quality Factor, with Application to Earth’s Inner Core](https://doi.org/10.1016/j.pepi.2025.107456). *Physics of the Earth and Planetary Interiors*, 368, 107456.
- Cao, X., **Gong, M.**, Tula, A., Chen, X., Gani, R., & Venkatasubramanian, V. (2024). [An Improved Machine Learning Model for Pure Component Property Estimation](https://doi.org/10.1016/j.eng.2023.08.024). *Engineering*, 39, 61–73.

## Awards and Honors

- <span class="cv-date">2026</span> [Jonathan L. Gross Award for Academic Excellence](https://www.cs.columbia.edu/2026/celebrating-the-class-of-2026/)
- <span class="cv-date">2026</span> [Computer Engineering Award of Excellence](https://www.ee.columbia.edu/news/celebrate-excellence-eece-senior-awards-2026)
- <span class="cv-date">2024 – 2026</span> Columbia Dean's List (all semesters)
- <span class="cv-date">2021 – 2024</span> Simon's Rock Dean's List (all semesters)
- <span class="cv-date">2023</span> SCUDEM VIII Outstanding Award
- <span class="cv-date">2021</span> AP Scholar with Distinction

## Skills

- **EDA:** Cadence Genus, Innovus, Virtuoso; Synopsys Design Compiler; AMD Vitis; Intel Quartus; VTR; SPICE
- **Languages & Tools:** SystemVerilog, Chisel/Scala, Tcl, Python, C/C++, MATLAB, Java, Git, Linux
- **Digital Design:** RTL, Logic Synthesis, Place & Route, Static Timing Analysis, Timing Closure, FPGA Prototyping, eFPGA Architecture, Hardware Accelerators, Fault Injection
- **Hardware & Mixed-Signal:** Analog Design, PCB Design, Post-Silicon Validation, PyVISA, Signal Processing
- **ML for Hardware:** PyTorch, TensorFlow, CNN Fault Injection, LLM Fine-Tuning

## Selected [Projects](/projects)

- [16-bit DIF FFT Accelerator](/projects/fft/)
- [8-bit 65nm Mini Processor Custom Layout](/articles/vlsi)
- [Capacitive ECG Loose T-shirt](/publication/cecg)
- [FPGA Gaussian Elimination Accelerator](/projects/circuitsim/)

</div>

<!---
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
-->
