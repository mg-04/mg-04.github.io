---
title: "Nonlinear Components"
permalink: /articles/cc/nl
---

## Contents
1. [Intro to SPICE Algorithm](/articles/cc)
2. [Framework](/articles/cc/framework) and your first circuit!
3. [More Static Linear Components](/articles/cc/sta)
4. Nonlinear and Diode (this article)
5. [MOSFET](/articles/cc/mos)
6. [Time Variance](/articles/cc/tv)
7. [Applications](/articles/cc/app)

Time for the inner loop of the SPICE algorithm: nonlinear components!

We use the infamous Newton-Raphson method to take successive linear approximations until a solution is reached

This part of the report is pretty well-written, so I'll just quote it.

## Newton's Method

Diodes has a nonlinear current-voltage relation:

$$
i_d = I_s (e^{v_d/V_t} - 1)
$$

where $$I_s$$, $$V_t$$ are constants.

\input{circuits/diode-demo}

At step $$0$$, let $$G_{eq}$$ be derivative $$\frac{di_d}{dv_d}$$, where $$i_d = i_{d0}$$, $$v_d = v_{d0}$$:
$$G_{eq} \equiv \frac{di_d}{dv_d} = \frac{I_s}{V_t}\, e^{v_{d0}/V_t}$$

We apply the Newton–Raphson algorithm to build a linear estimate model around an initial guess.

$$
\begin{align*}
    i_{d} &\approx i_{d0} + G_{eq} (v_d - v_{d0})\\
    &= (i_{d0} -G_{eq}v_{d0}) + G_{eq}v_d
\end{align*}
$$

Fortunately, any  linear relation can be modelled by circuit elements. The constant term can be represented by a current source $$I_{eq} = (i_{d0} -G_{eq}v_{d0})$$, and the linear term can be represented by a resistor $$G_{eq} = \frac{1}{R_{eq}}$$. We add them to the matrix. This process is called **stamping**.

$$
\usepackage[american]{circuitikz}
\usepackage{tikz}
\begin{circuitikz}[american]
  % Coordinates for nodes and ground
  \coordinate (v1) at (0,2);
  \coordinate (v2) at (5,2);
  \coordinate (vn1) at (2, 2);
  \coordinate (vn2) at (2, 0);
  \coordinate (vn) at (5, 0);
  \coordinate (gnd) at (0,0);

  \draw (vn1) to[R, l_=$R$, *-*] (vn2);

  \draw (vn1) -- (v2);

  % Resistor R3 between v2 and ground
  \draw (v2) to[D, l_=$D$, *-*] (vn);

  % Current source I1 between v1 and ground
  \draw (gnd) to[I, l_=$I_1$] (v1);

  \draw (v1) -- (vn1);
  \draw (vn2) -- (vn);
  \draw (vn2) -- (gnd);

  % Label for v1 and v2 nodes
  \node at (vn1) [above] {$v_1$};
  %\node at (v2) [above] {$v_2$};
  \node at (vn2) [below] {GND};

\end{circuitikz}
$$

We can **solve** this linear circuit and get the node voltages.


From the node voltages, we **update** our initial guess.

The above procedure of stamp-solve-update is repeated until the solution converges, which is detected when the deviation of the solution $$\mathbf{v}$$ is below a threshold.

## Registration
Same format, but the following are new:
- `struct Diode`
    - `Is`, `Vt` are constants from the diode equation
    - `v_prev` is the memory element from the last approximation
- `type`: `NL_T`: for CircuitCim to recognize nonlinear components and optimize
- `update()`: pointer to the updater function. Will be mentioned below
- Initial voltage guess: This is tricky
    - You obviously don't want a value too large (like 5 V). `Vt` is small number. This will blow up the floating point
    - You also don't want it to be small (smaller than voltage drop, like 0.5 V). This approximation will have a very shallow slope, leading to a very high V for the next step, and falling back to the previous case
    - A moderate value, like 1 V is good. You will get some large initial currents, but they will converge.

```c
typedef struct { 
    int n1, n2; 
    float Is, Vt;
    float v_prev; 
} Diode;

void add_diode(int n1, int n2, float Is, float Vt) {
    Component *c = &comps[ncomps++];
    c->type      = NL_T;
    c->stamp     = dio_stamp_nl;
    c->update    = dio_update;
    c->u.dio     = (Diode){n1,n2,Is,Vt,1.0f};   // initial guess: 1V
}
```


## Stamping
`stamp()` uses the initial guess/prev values to make a linear approximation of the diode model: a conductor(resistor) and a current source in parallel. 
```c
void dio_stamp_nl(Component *c, float Gm[][MAT_SIZE], float I[]) {
    Diode *d = &c->u.dio;
    // 1. read last stage's voltage
    float Vd = d->v_prev;

    // 2. compute new iteration parameters
    float ExpV = expf(Vd / d->Vt);  
    float Geq = (d->Is / d->Vt) * ExpV;             // Geq = Is/Vt * exp(Vd/Vt)
    float Ieq = d->Is * (ExpV - 1.0f) - Geq * Vd;   // Ieq = Id - Geq*Vd

    // 3. stamp G and I
    int n1 = d->n1, n2 = d->n2;
    if (n1 != -1) Gm[n1][n1] += (Geq);
    if (n2 != -1) Gm[n2][n2] += (Geq);
    if (n1 != -1 && n2 != -1) {
        Gm[n1][n2] -= (Geq);
        Gm[n2][n1] -= (Geq);
    }
    if (n1 != -1) I[n1] -= (Ieq);
    if (n2 != -1) I[n2] += (Ieq);
}
```
## Updating

This is done after solving the matrix
```c
void dio_update(Component *c) {
    Diode *d = &c->u.dio;
    d->v_prev = (d->n1!=-1? v[d->n1]:0) - (d->n2!=-1? v[d->n2]:0);
}
```

## Solving an operating point
Now we will use this to solve an operating point (one point in time)
```c
/* clear everything EXCEPT static components */
void clear_system_sta(void) {
    memcpy(G_lin, G_sta, sizeof G_sta);
    memcpy(G, G_sta, sizeof G_sta);
    memcpy(I_lin, I_sta, sizeof I_sta);
    memcpy(Ivec, I_sta, sizeof I_sta);
}

/* stamp all static components */
void stamp_static(void) {
    for (int i = 0; i < ncomps; i++) {
        if (comps[i].type == STA_T && comps[i].stamp_lin) {
            comps[i].stamp_lin(&comps[i], G_sta, I_sta);
        }
    }
}

void operating_point() {
    (void)t;
    int ret = 0;

    // Newton-Raphson loop for all nonlinear components
    for (int iter = 0; iter < MAX_NR_ITER; iter++) {

        // 1 restore the static linear stamps
        clear_system_sta();

        // 2 stamp all nonlinear components
        for (int i = 0; i < ncomps; i++) {
            if (comps[i].type == NL_T && comps[i].stamp)
                comps[i].stamp_nl(&comps[i], G, Ivec);
        }

        // 3 solve the system
        solve_system(nnodes);

        // 4 compute dv, check for convergence
        float maxdv = 0.0f;
        for (int n = 0; n < nnodes; n++) {
            float dv = fabsf(v[n] - prev_v[n]);
            if (dv > maxdv) maxdv = dv;
        }

        if (maxdv < NR_TOL) {   // converged!
            break;
        }

        // 5 Update every device's internal operating point
        for (int i = 0; i < ncomps; i++) {
            if (comps[i].type == NL_T && comps[i].update) {
                comps[i].update(&comps[i]); // update diode only
            }
        }

        // 6 prepare for next iteration
        memcpy(prev_v, v, sizeof prev_v);
    }
}
```
