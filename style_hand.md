---
title: "Handwritten Style"
permalink: /style2
date: 2026-06-19
author: "Ming Gong"     # optional, for collaborative posts
---

# Handwritten Note-Taking Style Guide

This document captures the structural, visual, and textual style of engineering and physics handwritten notes taken in Notability. Use it as a framework for replicating this dense, visual, and efficient style.

---

## Document Layout & Density

Notes are optimized for high spatial density. Text flows dynamically around diagrams and equations, with minimal whitespace. Pages sometimes use a **dual-column layout**: the left side carries the primary mathematical or signal derivation path; the right side is reserved for architectural diagrams, vector charts, or waveform sketches.

---

## Headings

Headings function as immediate conceptual tags, not full phrases. They are strictly telegraphic.

**Major sections** are written as punchy, isolated topic titles or physical models:
- `## Scaling (Dennard)`, `## Linear Estimation (Weiner-Hopf)`, `## MOS/FET`
- Every major topic begins with a **bold, standalone banner title** at the top of the section

**Subsections** immediately specify the constraint or design domain being analyzed:
- `### Short channel`, `### Body effect if $U_{SB}\ne 0$`, `### PMOS load SS`
- Sub-banners are placed directly above algorithmic implementations, derivations, or circuit topologies: `Matched Filter (North)`, `RHP zero compensation`

**Telegraphic labels** appear inside diagrams to mark functional blocks: `Bias point`, `Filter`, `Miller effect`, `High freq`

**Formatting in handwriting**: Headings are underlined or boxed to separate them from surrounding dense text blocks.

---

## Prose Style

Sentence structures are abandoned in favor of lecture-note fragments with extreme word economy. Articles, helping verbs, and transition words are completely omitted.

**Direct fact statements** — immediate technical rules as the first word:
- `Material Si us 35 vs wide-bondgap`
- `As size ↓, # dopants countable`
- `Want filter Pn(f) w/ Hw() whitened Pn`
- `Change amp/phase/freq of carrier`

**Conditional and system assertions** use explicit shorthand:
- `if A >> n_R(t)`, `as v -> c`, `if m=1`

**Inline directives** guide step-by-step verification:
- `Watch overflow!`, `Check: 1 unit`, `Need to tune μ`, `safer to bias I_D, not V_GS`

### Standard Shorthand Abbreviations

| Shorthand | Meaning |
|-----------|---------|
| `w/` / `w/o` | with / without |
| `vs` | versus |
| `clk` | clock |
| `inv.` | inverter / inversion |
| `dev.` | device |
| `sys.` | system |
| `sat` / `lin` / `dep` | saturation / linear / depletion |
| `freq` | frequency |
| `fucn.` / `vars.` | function / variables |
| `mat.` | matrix |
| `fwd` | forward |
| `den.` / `num.` | denominator / numerator |
| `cas` | cascade |
| `instr` | MIPS instruction designations |

---

## Implication & Evaluation Symbols

Causality, performance metrics, and system behavior are tracked using a strict symbolic language:

| Symbol | Meaning |
|--------|---------|
| `→` | Leads to, implies, evaluates to, transitions to |
| `↑` | Increase, high state, rise, growth; curved for nonlinear growth |
| `↓` | Decrease, low state, fall, minimization |
| `~` | Proportional to, or related to |
| `✓` | Advantage, benefit, "pro" of a design choice |
| `✗` | Disadvantage, drawback, pitfall, "con" |
| `→ :)` | Favorable or highly optimal design result |
| `→ :(` | Unfavorable result, hazard, or performance penalty |

---

## Emphasis

| Visual Element | Use |
|----------------|-----|
| **Full framing boxes** | Drawn around definitive analytical outcomes, optimum filter designs, or final coordinate transformations |
| **Color highlights** (red/green) | State-change interventions, signal alterations (flip bits, add +1), structural hazard paths in pipelines |
| **Underlines** | Key foundational tracking terms or dimensional invariants (e.g., `WSS`, `invariant interval`, `ideal diode`) |

---

## Color Coding Layer

Color establishes a clear hierarchy over dense black text:

- **Base layer (black/dark ink)**: Core derivations, main formulas, structural block text, initial diagrams
- **Annotation layer (blue ink)**: Auxiliary notes written on top of graphs, trace paths, signal names, layout additions, and inline evaluation marks (`✓`, `✗`)
- **Highlighting layer (yellow/neon green)**: Localized translucent circles or blocks pinpointing critical physical thresholds — bandgaps ($E_g$), equilibrium dimensions ($a_0$), vital intersections on transfer curves

---

## Sequential & Multi-Step Structure

Multi-step processing pipelines, structural loops, and proof sequences are tracked using **circled digits** to establish programmatic flow down the page:

① → ② → ③ → ④ → ⑤

---

## Lists & Implication Chains

Standard bullet lists are rarely used. Notes rely on causal chains, transformation notations, and structural mapping instead.

**Implication and processing paths** — directional arrows track variable flow, algorithmic conversions, or state consequences:
```
Pn(f)|Hw(f)|^2 = N_0/2  →  H_MF(f) = ...
Switch off  →  V = L dt/di
```

**Domain shift notation** — explicit operator tags mark frame transformations:
$$h_{mf}(t) \stackrel{\mathcal{F}^{-1}}{\longleftrightarrow} S^*(-f)\, e^{-j2\pi fT}$$

---

## Logic & Execution Blocks

Algorithmic validation rules or architecture checks are written as clean plaintext logic strings:

```
Forwarding Condition:
if (RegWriteM) and (rsE != 0) and (rsE == WriteRegM)  →  FwdAE = 10

Stall Trigger:
lwstall = MemToRegE and ((rsD == rtE) or (rtD == rtE))
```

---

## Diagrams & Visual Annotations

Visual sketches are primary note components and fall into three categories:

### 1. Device Physics & Waveform Plots
- **Axes and traces**: Clean lines with slopes (`slope=μ`), saturation thresholds ($V_{ov},\, \text{sat} \approx 0.2\,\text{V}$), and asymptotic limits annotated directly on the curve
- **Critical markers**: Operational zones labeled inline (`cond.` for conduction band, `val.` for valence band, inversion boundaries)
- **Reference points**: Hand-drawn stars ($\star$) mark critical design reference points

### 2. Circuit & Layout Sketches
- **Transistor stacks**: Simplified logic configurations with sizing written next to gates (`4W`, `2W/W`)
- **Physical layout templates**: Stick-diagram representations with power rails clearly labeled `vdd!` and `gnd!`

### 3. System & Signal Block Diagrams
- **Signal flow graphs**: Summation nodes ($\Sigma$), integrators ($1/s$), and multipliers linked by directional arrows
- **Pipeline matrix mapping**: Structural dependencies and hardware hazard bypass paths traced using colored interconnect pathways beneath code sequence columns
- **Hardware architecture blocks**: Datapath layouts link PC, instr. mem., reg. file, ALU, and data mem. using directional buses with explicit bit-widths (`31:26`, `15:0`, `32`)
- **FSM state bubbles**: Circles contain current states; edges are labeled `X/Y` for input/output transitions

---

## Mathematical Notation

Math is highly integrated into text flow using direct algebraic transitions rather than verbal descriptions.

**Inline parameters** embedded directly in prose:
- `$E_g = 1.1\,\text{eV}$`, `$np = n_i^2$`, `$I_{sat} \sim V_{ov}$`

**Calculus and matrix system models** — compact and clean:
$$\frac{dE}{dx} = \frac{\rho}{K_s \epsilon_0}$$
$$\underline{\dot{x}} = \underline{A}\,\underline{x} + \underline{b}f$$

**Rational function steps** — long-division polynomial remainders and partial fraction expansions mapped out step by step.

**Statistical operators** — expectation explicitly encased:
- `$E[\epsilon^2(t)]$`, `$E[|x|]$`

**Calculus fields** — vector derivatives and definite loop integrals:
$$\oint_S \vec{E} \cdot d\vec{a} = \frac{Q_\text{enc}}{\epsilon_0}$$
$$\int_{-\infty}^{\infty} f(x)\,\delta(x-a)\,dx = f(a)$$

**System matrices** — multi-node parameter equations grouped into arrays before solving:
$$\begin{bmatrix} \frac{1}{R} + sC & -\frac{1}{R} \\ \frac{1}{R} & sC \end{bmatrix} \begin{bmatrix} V_1 \\ V_2 \end{bmatrix} = \begin{bmatrix} -\frac{1}{R_1} \\ 0 \end{bmatrix} V_\text{in}(s)$$

---

## Hand-Drawn Graphs & Waveforms

Note segments are consistently paired with illustrative spatial plots, signal sweeps, or device parameters:

- **Coordinate contexts**: Angle overlays ($\theta, \phi, r\sin\theta$) map mathematical transformations onto physical systems
- **Signal & noise envelopes**: Frequency parabolas, power spectrum drops, and noise distribution boundaries annotated with critical cutoffs ($\pm W$, $B_{FM}/2$)
- **Characteristic sweeps**: Graphical intersections represent non-linear operating points (load lines crossing Shockley curves) or device response limits ($V_{out}$ vs $V_{in}$ switches)

---

## Separator Rules

Horizontal divider lines are drawn across pages to:
- Segment sub-topics completely
- Block off multi-stage proofs (e.g., separating a Bose-Einstein derivation from ideal Bose gas modeling)

---

## Notice Boxes & Callouts

**Marginal pitfalls** — highlighted via bracketed indicators for hardware layout issues, scaling limitations, or parameter breakdowns:
- `DIBL: Drain Induced Barrier Lowering`, `RHP zero hurts PM`

**Status indicators** — text markers for final evaluations:
- `→ best outcome`
- `Worst E[ε²] = s(t)²`

**Unresolved sections** — open questions tagged inline:
- `???` over unresolved mathematical links (e.g., `dt' = ???`)

---

## Homework & Project References

Problem set solutions and diagnostic checks are integrated into the relevant architectural notes with sharp contextual markers:
- `HW1`, `HW2 All comp. give same pole...`, `Pn(f) = HW`

---

## Overall Tone

- **Authoritative and quantitative**: Completely analytical and deterministic. Facts exist as direct system behaviors, mathematical definitions, or performance bottlenecks — no conversational assumptions.
- **Visual-logical balance**: Mathematical proofs are paired directly with visual layout configurations — a relativity derivation alongside a Minkowski spacetime diagram, an op-amp poles transformation paired with an open-loop Bode plot sweep.
- **Efficiency-focused**: Physical limitations and optimization trade-offs are front and center — power constraints, scaling penalties ($1/K$), timing hazards ($t_{setup}$, $t_{hold}$), and system stability margins.
