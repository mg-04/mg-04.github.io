---
title: "CircuitCim Framework"
permalink: /articles/cc/framework
---
# Framework
To code SPICE, the main challenges are: how do you keep the component information, and how do you tell which value goes where

Here we define the data structure to store the general resistor info
```c
typedef struct { 
    int n1, n2;
    float R; 
} Res;
```

Sources are a bit complicated. Let's just support DC for now

```c
typedef struct { 
    int n1, n2;
    float I;
} ISrc;
```

### Generic Structure

We maintain a generic `Comps[]` array to keep track of all circuit components. Each entry is a generic `struct Component`, with each device's type and parameters, and functions pointers to **stamp** (add it to matrix)
```c
typedef struct Component {
    CompType type;  // let it be STA_T for now
    void (*stamp)(struct Component*, float[][MAT_SIZE], float[]);
    /* void (*update)   (struct Component*, float[][MAT_SIZE], float[]); */
    union {
        ISrc   isrc;
        Res    res;
    } u;
} Component;

// component registry
Component comps[MAX_COMPS];
int       ncomps;           // number of components in the circuit
```

### Registering Components

Now we need to define the component register functions `add_res()` and `add_isrc()`
```c
void add_isrc(int n1,int n2, TransientSource *src) {
    Component *c = &comps[ncomps++];
    c->type      = STA_T;
    c->stamp     = isrc_stamp;
    c->u.isrc    = (ISrc){n1,n2, src};
}

void add_res(int n1, int n2, float R) {
    Component *c = &comps[ncomps++];
    c->type      = STA_T;
    c->stamp     = res_stamp;
    c->u.res     = (Res){n1,n2,R};
}
```

### Stamping
Now time for node voltage analysis! Let's count all currents *leaving* the node as positive.

The **ground** node is registered as -1.
```c
void res_stamp(Component *c, float Gm[][MAT_SIZE], float I[]) {
    (void)I;                        // not used
    Res *r = &c->u.res;
    float G = 1.0f / r->R;
    int   n1 = r->n1, n2 = r->n2;

    if (n1 != -1) Gm[n1][n1] += G;  // current leaving
    if (n2 != -1) Gm[n2][n2] += G;
    if (n1 != -1 && n2 != -1) {     // current entering
        Gm[n1][n2] -= G;
        Gm[n2][n1] -= G;
    }
}
```

```c
void isrc_stamp(Component *c, float Gm[][MAT_SIZE], float I[]) {
    (void)Gm; (void)I;
    ISrc *s = &c->u.isrc;
    float Ieq = s.I
    int   n1 = s->n1, n2 = s->n2;

    if (n1 != -1) I[n1] += Ieq;
    if (n2 != -1) I[n2] -= Ieq;
}
```

# Test Driver
We first write a simple driver program that reads a circuit, runs our simulation block, and returns the result in a CSV

```c
#include <stdio.h>

// each test must define this:
void setup(void);               // defined in test programs
void stamp_static(void);        // adds resistors to the matrix

void print_header(FILE *f);     // write CSV header line
void print_row(FILE *f);        // write one line of data each time step

// global nodal matrix, state, and time
float G[MAT_SIZE][MAT_SIZE];
float Ivec[MAT_SIZE];
float v[MAT_SIZE], v_prev[MAT_SIZE];

/*
extern float G_sta[MAT_SIZE][MAT_SIZE];
extern float I_sta[MAT_SIZE];
extern float G_lin[MAT_SIZE][MAT_SIZE];
extern float I_lin[MAT_SIZE];
*/

float t;
extern float time_step; // time step for simulation
extern int nsteps;      // number of steps for simulation

int main(void) {
    // zero‑out everything
    memset(G,      0, sizeof G);
    memset(Ivec,   0, sizeof Ivec);
    memset(v,      0, sizeof v);
    memset(v_prev, 0, sizeof v_prev);
    t = 0.0f;

    // open CSV
    FILE *fp = fopen("results.csv", "w");
    if (!fp) { perror("fopen"); return 1; }
    print_header(fp);

    // build the circuit (calls your add_*()s)
    setup();

    // simulate
    clear_system();
    stamp_static();
    clear_system_sta();

    /*
    for (int n = 0; n < nsteps; n++) {
        t = n * time_step;
        update_all(t);
        print_row(fp); // write a row of data
    }
    */

    fclose(fp);
    return 0;
}
```

Our job is to write `stamp_static()` to add the resistor contribution to G and I.

### Your First Circuit
Time to build a first circuit! It will be a simple current source with a resistor. There will only be *one* node 0 and the ground node -1
```c
// Source-resistor circuit

#include "circuit.h"
#include "driver.h"
#include "input_funcs.h"
#include <string.h>   // for memset

float time_step = 5e-6f;    // these are arbitrary
int nsteps = 500;

void setup(void) {
    add_isrc(0, -1, 5);
    add_res(0, -1, 10);
    nnodes = 1;
}

// csv header
void print_header(FILE *f) {
    fprintf(f, "time,v0\n");
}

// csv row
void print_row(FILE *f) {
    fprintf(f, "%g,%g\n", t, v[0]);
}
```
and you can play around and add more linear components.