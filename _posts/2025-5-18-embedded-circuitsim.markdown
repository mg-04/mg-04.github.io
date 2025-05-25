---
layout: post
title:  "Embedded Project: CircuitSim"
date:   2025-5-18 05:58:30 -0500
categories: aca
---

Here's a walkthrough of our Embedded final project: Circuit Simulator on FPGA
## Topic
This was such an amazing topic for this course! I was quite surprised that no one has done SPICE before, or any application related to matrix inversion--none of these are particularly challenging. 

I was pretty sure that if we make it working, Edwards would LOVE it!

## [CircuitCim](/cc)
I completed the framework [CircuitCim](/cc), the circuit simulation engine of the project pretty soon after the project start. Originally, we only planned to do linear elements: RLC, but after finding out that diodes are not too hard to do, I added diode functions soon. 

We can call it a done from here, since there are just too many interesting things you can do with diodes, such as analog multiplier and different kinds of rectifiers. I still wanted to go a step beyond to get FETs working, so we can simulate logic.

The MOS small-signals are all original, but they follow naturally as the diode models, and the elementary results are exactly the small signal models. After fixing some glitches, we got simple logic gates working. This officially marks our "digital age", simulating digital circuits with our *analog* core

Then it's all about test circuits. I spent a bit of time building the DFF and 555, each with 30-ish transistors and 20-ish nodes. Each took me about a night, since I need to first build the elements on a working simulator like Falstad, split it to netlist, and migrate on CircuitCim

All works payed off. CircuitCim worked perfectly

## Gaussian Elimination
During our design review, Edwards suggested our next month will be focusing on the Gaussian Elimination. 

I thought this was a pretty well-defined program, as the algorithm was only 10 lines of C, 
```c
void gaussian_elim(int n) {   // n: number of unknowns
    for (int k = 0; k < n; k++) {
        for (int i = k+1; i < n; i++) {
            float m = G[i][k] / G[k][k];
            for (int j = k; j <= n; j++)
                G[i][j] -= m * G[k][j];
        }
    }
    for (int i = n-1; i >= 0; i--) {
        float sum = I[i];
        for (int j = i+1; j < n; j++)
            sum -= G[i][j] * v[j];
        v[i] = sum / G[i][i];
    }
}
```

We do need to pivot to prevent large numbers and detect singularity. That will make it 20 lines of code. 

I don't know exactly how many cycles it would take for the C code to execute one iteration. It shouldn't look too complicated in Assembly

But in hardware, without those predefined instructions, we'll need temporary registers to register and restore the intermediate results. The hardware needs to interact:

1. Floating point modules: Although this can be done combinatorially, the delay will be way more than what our 50 MHz can tolerate. Therefore, those smart people split the module into sequential cycles. For 50 MHz the division module would take 11 cycles. We need to set up the inputs properly and fetch the fp results precisely at that cycle.

2. Memory read. Memory read is buffered, meaning that results come 2 cycles later, not 1. There are multiple practical challenges:
    1. Address resolution: converting `[i][j]` to actual memory address. This is not too hard, given that you do it carefully enough
        - Bit shift is much cheaper than multiplication. That's why we fixed the matrix dimension in memory.
    2. Branch resolution: It becomes a pain if you have to resolve the address two cycles later that may branch as well. We used the early branch resolution concept from Fundies: precompute the branch condition, decide the branch, and input the appropriate address
        - It was a pain going and debugging through this--would have been much easier in SW, but none of us realized this issue until the very last week

3. Software control: software sends a start signal to the hardware, and polls the results from it. 

## Interface
The interface is not particular challenging, if you know what you are doing and trust it works (unfortunately I was not)

## Reflection
We were out of time to write any complete evaluation or reflection. Here's a better one:

## Result
4th order filter and rectifier worked perfectly

555 didn't work. The hardware kept returning the same result (seems to be the first time step) for every time step. It seems to solve each operating point correctly. What we suspect:
- Version control issue: 
    - MOSFET model
    - Capacitor model and `update()` function
    - Broken outer/inner `update()` call
    - Wrong SPICE netlist
    - Wrong internal component type
- Hardware IO
    - Improper reset signal sent
    - Improper hardware `open()` and `close()`
- Resource
    - Misdefined node number

I'm sure it's more than fixable, given that rectifier works. It's just a matter of time

瑕不掩瑜, Edwards really liked it. We got A+ and the infamous Edwards star ![Edwards](/images/cc/staricon.png)

## Future Work
We also ran out of time to write a future work section

### GUI
We desparately need a GUI!!   
This will take some memory, so we may need to shrink the max nodes to 64.
- We can also figure out smarter ways to store sparse matrices, such as using a list-like structure  

The GUI would have a matrix grid to connect circuit components. Some software is needed to translate component grid to SPICE netlist. That should be it.
