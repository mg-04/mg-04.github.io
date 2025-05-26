---
title: "More (Static) Linear Components"
permalink: /articles/cc/sta
---
## More Linear Components
Here is a set of more linear elements. Voltage sources need an additional row from MNA (instead of supernodes in the Tsividis textbook, because we do want to keep track of every subnode in the supernode)
```c
typedef struct { 
    int n1, n2, ni;             // VSrc has an internal node
    float *V;
} VSrc;   
// dependent sources
typedef struct { 
    int n1, n2;
    int np, nn, ni;   
    float A;         // gain    
} Vcvs;
typedef struct { 
    int n1, n2;
    int np, nn;
    float A; 
} Vccs;
```
Register functions
```c
void add_vsrc(int n1,int n2, int ni, float V) {
    // ni for an internal node for an extra row in the equation.
    Component *c = &comps[ncomps++];
    c->type      = STA_T;
    c->stamp     = vsrc_stamp;
    c->u.vsrc    = (VSrc){n1,n2, ni, V};
}
void add_vcvs(int n1, int n2, int np, int nn, int ni, float A) {
    Component *c = &comps[ncomps++];
    c->type      = STA_T;
    c->stamp     = vcvs_stamp;
    c->u.vcvs    = (Vcvs){n1,n2, np,nn, ni, A};
}
void add_vccs(int n1, int n2, int np, int nn, float A) {
    Component *c = &comps[ncomps++];
    c->type      = STA_T;
    c->stamp     = vccs_stamp;
    c->update    = NULL;
    c->u.vccs    = (Vccs){n1,n2, np,nn, A};
}
```
Update functions
```c
/* add an ideal voltage source; stamps a "virtual" node (ni) to the circuit.*/
void vsrc_stamp(Component *c, float Gm[][MAT_SIZE], float I[]) {
    VSrc *s = &c->u.vsrc;
    float E = vsrc.V;

    int n1 = s->n1, n2 = s->n2, ni = s->ni;

    // internal node
    if (n1 != -1) {         
        Gm[n1][ni] += 1.0f;
        Gm[ni][n1] += 1.0f;  // symmetry for the voltage equation
    }
    if (n2 != -1) {
        Gm[n2][ni] -= 1.0f;
        Gm[ni][n2] -= 1.0f;
    }

    // Voltage equation: v(n1) - v(n2) = E
    // stamped as  +1·v(n1) -1*v(n2) +0*I_vs  = E
    I[ni] += E;
}

/*
 * Voltage‐Controlled Voltage Source (VCVS):
 *    v(n1)-v(n2) = mu * (v(np)-v(nn))
 * adds one extra current‐unknown at index ni.
 */
void vcvs_stamp(Component *c, float Gm[][MAT_SIZE], float I[]) {
    (void)I;
    Vcvs *s = &c->u.vcvs;
    int n1   = s->n1,
        n2   = s->n2,
        np   = s->np,
        nn   = s->nn,
        ni   = s->ni;
    float mu = s->A;

    if (n1) Gm[n1][ni] +=  1.0f;
    if (n2) Gm[n2][ni] += -1.0f;

    if (n1) Gm[ni][n1] +=  1.0f;
    if (n2) Gm[ni][n2] += -1.0f;
    if (np) Gm[ni][np] += -mu;
    if (nn) Gm[ni][nn] +=  mu;

    //no direct RHS contribution for a pure dependent source
}

/*
 * Voltage‐Controlled Current Source (VCCS):
 *    i = gm * (v(np)-v(nn))
 * injects from n2 to n1.
 */
void vccs_stamp(Component *c, float Gm[][MAT_SIZE], float I[]) {
    (void)I;
    Vccs *s = &c->u.vccs;
    int   n1 = s->n1,
          n2 = s->n2,
          np = s->np,
          nn = s->nn;
    float gm = s->A;

    if (n1 && np) Gm[n1][np] += -gm;
    if (n1 && nn) Gm[n1][nn] += gm;
    if (n2 && np) Gm[n2][np] += gm;
    if (n2 && nn) Gm[n2][nn] += -gm;
}
```