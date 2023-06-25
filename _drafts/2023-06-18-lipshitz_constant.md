---
layout: post
title: Lipschitz constant of linear transformation
---

DISCLAIMER: If you spot an error, please feel free to email me. 


The "Understanding Deep Learning" book has recently come out (you can look at it [here](https://udlbook.github.io/udlbook/)), and in the appendices, it contains several statements presented without explanation or proof which can be non-obvious to those of us who have been out of touch with our linear algebra in our day jobs. 

Here is one such statement: 

"The Lipschitz constant of a linear transformation $f[z] = Az + b$ is equal to the maximum eigenvalue of the matrix A."

A function $f[z]$ is Lipschitz continuous if for all $z1,z2$:

$$
||f[z1] − f[z2]|| ≤ β||z1 − z2||,
$$
This is not an obvious result at all. Let us try and break this down step by step.

## Definitions

### Vector norm
Definition lifted from this very useful resource [here](https://www.math.drexel.edu/~foucart/TeachingFiles/F12/M504Lect6.pdf) (Definition 3)


TODO: FINISH

Let $\mathcal{V}$ be a vector space over a field $\mathbb{R}$. A function $||· || : \mathcal{V} → \mathbb{R}$ is called a (vector) norm if

-  $||x|| ≥ 0$ for all $x ∈ \mathcal{V}$ , with equality iff x = 0, [positivity]
- kλxk = |λ|kxk for all λ ∈ K and x ∈ V , [homogeneity]
- kx + yk ≤ kxk + kyk for all x, y ∈ V . [triangle inequality]


where $A \in \mathbb{R}^{m\times n}$

### Matrix norm
Also from the above resourece (Definition 7)

Important sub-results


Look at [here](https://math.stackexchange.com/questions/1513399/ax%E2%89%A4-a-x-space-forall-x-in-mathbbrn-rudins-principles)
$$
|Ax| \leq ||A||x|, \, \forall x \in \mathbb{R}^n
$$


Will also need results from Lecture 5 of the Drexel university resource
https://www.math.drexel.edu/~foucart/TeachingFiles/F12/M504Lect5.pdf