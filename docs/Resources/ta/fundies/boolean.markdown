---
layout: page
title: "Boolean Algebra Revisited with K-maps"
permalink: /f1
git_path: "/ee-labs.markdown"
---
# Boolean Algebra Revisited with K-maps

**Author:** Fundies TA Team\
**Date:** Updated February 7, 2025

Boolean algebra is not easy, and some steps get counterintuitive. Karnaugh maps provide a systematic way to guide you through these manipulations.

Here's a problem from the Fall 2024 Midterm 1:

---

**Problem:** Use **algebraic manipulation** to reduce the following expression to two literals:

A natural start is to distribute:

$$f = A + \overline{A}\, \overline{B} + \overline{B} C$$

and get stuck with the letters. Let's try another way: first find the answer using a K-map, and translate the steps back to Boolean algebra.

As you'll see, this may not lead to the simplest derivation, but it provides a very intuitive sequence of logic that you can easily follow.

## K-map Solution

First, use a K-map to obtain the simplest Sum of Products (SoP) expression.

|                                                                             | \(\Longrightarrow\) |                                         |
| --------------------------------------------------------------------------- | ------------------- | --------------------------------------- |
| \(f = \red{A} + \blue{\overline{A} \overline{B}} + \green{\overline{B} C}\) |                     | \(f = \red{A} + \orange{\overline{B}}\) |

## From K-map to Algebra

We took two steps in the K-map above. Let's translate each into Boolean algebra.

1. Eliminate \(\green{\overline{B} C}\).
2. Expand \(\blue{\overline{A}\, \overline{B}}\) to \(\orange{\overline{B}}\).

\(\overline{B} C\) is redundant, suggesting that all of its constituent minterms can be absorbed by other terms:

\(\overline{B} C = A \overline{B} C + \overline{A}\, \overline{B} C\)

|                     |
| ------------------- |
| Absorption of terms |

#### Derivation:

$$
\usepackage[usenames,dvipsnames]{xcolor}

\newcommand{\red}[1]{\textcolor{red}{#1}}
\begin{aligned}
f &= \red{A} + \blue{\overline{A} \overline{B}} + \green{\overline{B} C}\\
&= A + \overline{A} \overline{B} + (1) \overline{B} C\\
&= A + \overline{A} \overline{B} + (A+\overline{A}) \overline{B} C\\
&= \red{A} + \blue{\overline{A} \overline{B}} + \green{A \overline{B} C + \overline{A}\, \overline{B} C}\\
&= (\red{A} + \green{A \overline{B} C}) + (\blue{\overline{A} \overline{B}} + \green{\overline{A}\, \overline{B} C})\\
&= A (1 + \overline{B} C) + \overline{A}\,\overline{B}(1+C)\\
&= A(1) + \overline{A}\, \overline{B}(1)\\
&= \red{A} + \blue{\overline{A} \overline{B}}
\end{aligned}
$$

|                       |
| --------------------- |
| Expanding K-map boxes |

$$
\begin{aligned}
f &= \red{A} + \blue{\overline{A} \overline{B}} \\
&= (\red{A} + \orange{A \overline{B}}) + \blue{\overline{A} \overline{B}} \\
&= \red{A} + (\orange{A \overline{B}} + \blue{\overline{A} \overline{B}}) \\
&= \red{A} + \orange{\overline{B}}
\end{aligned}
$$

K-map boxes represent SoP expressions. However, a simpler derivation can be done using PoS (Product of Sums):

$$
f = A + \overline{A} \overline{B} = (A + \overline{A}) (A + \overline{B}) = A + \overline{B}
$$

## Brute Force Translation

If the K-map transformations are not obvious, you can always break expressions down into a sum of minterms as a last resort:

$$
\begin{aligned}
f &= \red{A} + \blue{\overline{A} \overline{B}} + \green{\overline{B} C}\\
&= \red{ABC} + \red{A\overline{B} C} + \red{AB\overline{C}} + \red{A\overline{B} \overline{C}} \\
& \quad + \blue{\overline{A} \overline{B} C} + \blue{\overline{A} \overline{B} \overline{C}} \\
& \quad + \green{A \overline{B} C + \overline{A}\, \overline{B} C}\\
&= \red{A} + \orange{\overline{B}}
\end{aligned}
$$

This will generate a lot of intermediate terms, but the fundamental logic remains intact.

## Summary

Direct algebraic simplification can be challenging, but reverse engineering with K-maps provides a systematic graphical approach:

1. First, simplify with the distributive property and DeMorgan's law.
2. Use a K-map to find the final minimal form.
3. Break down the K-map simplification into distinct steps.
4. For each step,
   - Establish a skeleton: identify which variables should be split or absorbed in the K-map.
   - Write out the skeleton of algebraic expressions.
   - Flesh out the steps using basic axioms.
5. If you can't easily relate the K-map transformations, you can always reduce the expressions to minterms and work with those instead.

We start big with the final simplified expression, analyze how the K-map achieves it step by step, and then refine each transformation into its algebraic form.

---

*Written by Ming Gong in Spring 2025.*

