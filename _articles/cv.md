---
layout: archive
title: "Ming Gong"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume--verbose
---

{% include base_path %}

<div class="cv" markdown="1">

Pittsburgh, PA \| [Short version →](/resume)
{: .cv-meta}

**Research interests:** digital VLSI, computer architecture, hardware acceleration, and systems programming.

## Education

<span class="cv-date">2026 – present</span> **Carnegie Mellon University**  
*PhD in Electrical and Computer Engineering*

<span class="cv-date">2024 – 2026</span> **Columbia University**  
*Bachelor of Science in Computer Engineering*, Summa Cum Laude · GPA 4.26/4.33

<span class="cv-date">2021 – 2024</span> **Bard College at Simon's Rock**  
*Bachelor of Arts in Physics*, Summa Cum Laude · GPA 3.99/4.0

## Publications

- Leung, H. M. C., Tong, K., **Gong, M.**, Bui, N., & Zhou, X. (2026). [Continuous Electrocardiogram Monitoring with a Loose T-Shirt](https://doi.org/10.1145/3842657.3842785). *Hot Topics in Mobile and Wireless Systems for Health (MobiDx '26)*. ACM.
- **Gong, M.** & Bergman, M. I. (2025). [An Experimental Ultrasonic Method to Determine a Scattering Quality Factor, with Application to Earth’s Inner Core](https://doi.org/10.1016/j.pepi.2025.107456). *Physics of the Earth and Planetary Interiors*, 368, 107456.
- Cao, X., **Gong, M.**, Tula, A., Chen, X., Gani, R., & Venkatasubramanian, V. (2024). [An Improved Machine Learning Model for Pure Component Property Estimation](https://doi.org/10.1016/j.eng.2023.08.024). *Engineering*, 39, 61–73.

## Posters & Presentations

- **Gong, M.**, Bergman, M. I., & Bhadwal, N. (2024). [An Experimental Ultrasonic Method to Determine a Scattering Quality Factor, with Application to Earth’s Inner Core](/publication/2025-04-25-Interpreting-Inner-Core-Attenuation-Scattering-through-Ultrasonic-Experiments). Poster, *Study of the Earth's Deep Interior (SEDI)*.
- Grae, L., **Gong, M.**, Patrick, M., & Barmak, K. (2025). [Deep Learning Loss Function and Data Optimization for A.I. Detection of Thin Film Grain Boundaries](/publication/2025-04-14-Barmak). Poster, *Yale Undergraduate Research Conference*.

## Research Experience

<span class="cv-date">Jul. 2026 – present</span> **Graduate Research Assistant**  
*VLSI Design Group, CMU*
- Built a PyTorch fault-injection framework for YOLOv8n to size the trusted partition for a secure-FPGA + Jetson deployment. Identified a 448-weight critical set (1% of FLOPs) at the network’s input and output boundaries.
- Exploring heterogeneous eFPGA architectures and routing fabric configs to improve interconnect efficiency.
- Building a PyVISA-based automated post-silicon testing framework to extract ASIC operating margins.

<span class="cv-date">Jan. 2025 – May 2026</span> **Research Assistant with Dr. Xia Zhou**  
*Mobile X Lab, Columbia University*
- Designed hybrid FPCB electrodes with a capacitive motion-reference channel and driven bias for a loose-shirt ECG; 92.7% full-waveform detection at rest (r = 0.89) and 4.58 bpm HR error while walking.
- Developed multichannel impedance monitoring PCBs, from schematic through board bring-up, to infer patient health conditions.
- Designed, fabricated, and tested fabric sensors integrated into SoftSleep orthopedic pillows.

<span class="cv-date">Sept. 2024 – May 2025</span> **Research Assistant with Dr. Katayun Barmak**  
*Barmak Lab, Columbia University*
- Used PyTorch to train U-Net convolutional neural networks for polycrystalline grain boundary detection.
- Built a data-augmentation pipeline that crops micrographs and their ground-truth tracings into aligned sub-images to enlarge the training set, and binarized model predictions for comparison against human hand tracings.
- Showed that binary cross-entropy loss double-penalizes slightly misaligned traces, and proposed two alternative evaluation metrics: a fixed-pixel "top-hat" criterion and a continuous Gaussian-dilation loss.

<span class="cv-date">Jun. 2022 – Jun. 2025</span> **Physics Intern with Dr. Michael Bergman**  
*Bard College at Simon's Rock*
- Cast directionally solidified (1K/min) and fine-grained Zn-alloy samples (0.2 to >30 mm grains) and ran ultrasonic pulse-echo experiments at 1–10 MHz across 90 measurement spots on 4 samples.
- Developed a Python echo-detection algorithm that splits each pulse-echo trace into scattered (R₁) and transmitted (T₁) energy per cycle, defining a new scattering quality factor Q_Z = (R₁ + T₁)/R₁.
- Scaled lab Q_Z to Earth's inner core for 5–20% single-crystal Fe anisotropy, ruling out randomly oriented ~10 km grains and linking lateral variations in seismic attenuation (Q_P) to grain size; first-author [paper](https://doi.org/10.1016/j.pepi.2025.107456) (PEPI 2025).
<!-- - Experimented with a new foil technique in high-temperature ultrasonic shear wave coupling. -->
- Presented a poster at the 2024 SEDI Conference.

<span class="cv-date">Mar. 2022 – Jul. 2024</span> **Research Assistant with Dr. Xi Chen**  
*Zhejiang University*
- Benchmarked DNN, CNN, and decision tree architectures to model nonlinear pure component properties.
- Co-authored a peer-reviewed [paper](https://doi.org/10.1016/j.eng.2023.08.024) on ML-based pure component property estimation (Engineering, 2024).

## Teaching

<span class="cv-date">Fall 2026</span> **Teaching Assistant**  
*Carnegie Mellon University*
- TA for 18-622 Digital IC Design

<span class="cv-date">Jan. 2025 – May 2026</span> **Teaching Assistant**  
*Columbia University*
- TA for Embedded Systems (CSEE 4840)
- Head TA for Fundamentals of Computer Systems (CSEE 3827)
- Developed and optimized exam problems. Created supplemental materials to enhance and extend lecture content.
- Disability Services [notetaker](/ods) for a variety of CSEE courses

<span class="cv-date">Feb. 2022 – May 2024</span> **Tutor**  
*Bard College at Simon's Rock*
- Peer tutor in math, physics, chemistry, and computer science.
- Class tutor for Quantum Physics, Classical Mechanics, and Ordinary Differential Equations.
- Guided students on math and CS projects, offering outline planning and step-by-step hints.

## Industry Experience

<span class="cv-date">Jun. – Aug. 2025</span> **Algorithms Intern**  
*Alibaba Group*
- Built deep-search LLM agents for large-scale business web scraping, raising business-development contact email search success from 20% to 60%.
- Fine-tuned Qwen multilingual LLMs with supervised fine-tuning (SFT) to improve translation quality across 92 languages.

## Awards and Honors

- <span class="cv-date">2026</span> [Jonathan L. Gross Award for Academic Excellence](https://www.cs.columbia.edu/2026/celebrating-the-class-of-2026/)
- <span class="cv-date">2026</span> [Computer Engineering Award of Excellence](https://www.ee.columbia.edu/news/celebrate-excellence-eece-senior-awards-2026)
- <span class="cv-date">2024 – 2026</span> Columbia Dean's List (all semesters)
- <span class="cv-date">2024</span> Fisher Poster Session Contest, 2nd place
- <span class="cv-date">2021 – 2024</span> Simon's Rock Dean's List (all semesters)
- <span class="cv-date">2023</span> SCUDEM VIII Outstanding Award
- <span class="cv-date">2022</span> Simon's Rock Faculty Scholarship
- <span class="cv-date">2021</span> Center for Talented Youth Scholarship
- <span class="cv-date">2021</span> AP Scholar with Distinction

## Skills

- **EDA:** Cadence Genus, Innovus, Virtuoso; Synopsys Design Compiler; AMD Vitis; Intel Quartus; VTR; SPICE
- **Languages & Tools:** SystemVerilog, Chisel/Scala, Tcl, Python, C/C++, MATLAB, Java, Git, Linux
- **Digital Design:** RTL, Logic Synthesis, Place & Route, Static Timing Analysis, Timing Closure, FPGA Prototyping, eFPGA Architecture, Hardware Accelerators, Fault Injection
- **Hardware & Mixed-Signal:** Analog Design, PCB Design, Post-Silicon Validation, PyVISA, Signal Processing
- **Machine Learning:** PyTorch, TensorFlow, CNN/U-Net, CNN Fault Injection, LLM Fine-Tuning (SFT)

## Selected [Projects](/projects)

- [16-bit DIF FFT Accelerator](/projects/fft/)
- [8-bit 65nm Mini Processor Custom Layout](/articles/vlsi)
- [Capacitive ECG Loose T-shirt](/publication/cecg)
- [FPGA Gaussian Elimination Accelerator](/projects/circuitsim/)

## [Courses](/courses)

**Computer Engineering:**  
Computer Networks, Embedded Systems, Computer Architecture, Advanced Logic Design, Digital VLSI Circuits, Advanced Digital Electronic Systems, Reconfigurable Logic, Modern Computer Architecture

**Computer Science:**  
Advanced Programming, Advanced Systems Programming, Computer Science Theory, Artificial Intelligence, Networked Autonomous Systems, Operating Systems, C++ Deep Dive for C Programmers, Machine Learning

**Electrical Engineering:**  
Solid-State Devices and Materials, Analog Electronic Circuits, Random Signals and Noise

**Mathematics:**  
Probability and Statistics, Real Analysis, Abstract Algebra

**Physics:**  
Quantum Physics, Relativity & Cosmology, Classical Mechanics, Electrodynamics, Statistical Thermodynamics

**Chemistry:**  
Organic Chemistry

## Activities

<span class="cv-date">Oct. 2024 – May 2026</span> **Electrical and Programming Lead**  
*Columbia Robotics Club*
- Founding member of the Combat Robot Subteam.
- Coordinated with the team lead and programming team to design robot electronics and control software.
- Event supervisor for Robot Tour at the Columbia University Science Olympiad Invitational.

<span class="cv-date">Aug. 2025 – May 2026</span> **Executive Board**  
*Columbia IEEE*
- Maintained the Columbia IEEE [website](https://ieee.ee.columbia.edu/).
- Hosted Open Project Space and beginner-friendly Arduino workshops.

<span class="cv-date">Sept. 2024 – May 2026</span> **Organizational Committee Member**  
*Columbia Global China Connection*
- Organized social, cultural, and pre-professional events for Chinese students at Columbia.
- Collaborated with a team of 10 to manage GCC's website and social media platforms.

<span class="cv-date">Sept. 2024 – May 2026</span> **Executive Board Member**  
*Columbia Data Science Society*
- Organized data-science events and workshops for the Columbia community and the NYC area.

**Member**  
*Tau Beta Pi*

<span class="cv-date">Sept. 2021 – May 2024</span> **President**  
*Simon's Rock Robotics Club*
- Established a team of 10 from scratch; planned and allocated team budgets.
- Lectured Arduino lessons for beginners.

<span class="cv-date">Sept. 2021 – May 2024</span> **Member**  
*Simon's Rock STEM Competition Club*
- Conducted weekly math modeling sessions, dedicating 3 hours per week to lead a team of 5.
- Competed in SCUDEM VIII and won the Outstanding Award.

## Interests

Electronics, Lego, combat robots; road trip, swimming, hiking, badminton, tennis

## References

{: .cv-refs}
- **Ken Mai**  
  Principal Systems Scientist, Electrical and Computer Engineering, Carnegie Mellon University
- **Michael Bergman**  
  Emily H. Fisher Professor of Physics, Bard College at Simon's Rock
- **Xia Zhou**  
  Associate Professor of Computer Science, Columbia University
- **Martha Kim**  
  Associate Professor of Computer Science, Columbia University
- **Stephen Edwards**  
  Associate Professor of Computer Science, Columbia University
- **David Vallancourt**  
  Senior Lecturer in Electrical Engineering, Columbia University
- **Xiaodong Wang**  
  Professor of Electrical Engineering, Columbia University
- **David Myers**  
  Professor of Chemistry, Bard College at Simon's Rock
- **Miha Habič**  
  Assistant Professor of Mathematics, Bard College at Simon's Rock

</div>

<!---
Teaching
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
-->
