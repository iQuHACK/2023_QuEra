# Modularized Sharp Networks for State Preparation into MIS
QuEra Challenge, iQuHACK 2023

Yale University Team
Members: Alex Deters, Ben McDonough, Pranav Parakh, Sofia Fausone, Wyatt Kremer

## Contents

[TOC]

## Theoretical Motivation

QuEra Aquila is a 256-qubit quantum processor realized as a programmable array of optically-trapped ultracold $Rb$ atoms. Aquila belongs to the class of neutral atom hardware platforms. A two-level system is established by identifying the ground state $\ket{0}$ and excited "Rydberg" state $\ket{1}$ of a neutral $Rb$ atom with the electron configurations $[Kr]\space5s^1$ and $[Kr]\space70s^1$, respectively. The Gaussian laser beams that trap the arrays of $Rb$ atoms may be used to drive time-dependent Rabi oscillations $\Omega(t)$ with induced relative phase $e^{2i\phi(t)}$ and introduce a *global* time-dependent Rydberg detuning $\Delta(t)$. The global nature of $\Delta(t)$ imposed by the hardware inherently prevents the *direct* preparation of the $i$th atom in the Rydberg state $\ket{1_i}$. Therefore, it is necessary to place the atoms on the 75 $\mu m$ by 76 $\mu m$ processor in such a way that the geometry and interatomic interactions, which govern the time evolution of the system, would bring an initial uniform state to any given state. It is this sense that a state can be *indirectly* prepared to have the $i$th atom in the Rydberg state $\ket{1_i}$. 

The Hamiltonian for the array of $N\space Rb$ atoms is given as:

$\frac{H}{\hbar}=\sum_i{\Omega (t)(e^{i\phi(t)}\ket{0_i}\bra{1_i}+e^{-i\phi(t)}\ket{1_i}\bra{0_i})}-\Delta(t)\sum_i{\hat{n_i}}+\sum_{i<j}{V_{ij}\hat{n_i}\hat{n_j}}$,

where $\ket{0_i}$ and $\ket{1_i}$ are the ground and Rydberg states for atoms $i=1,2,...,N$, $\hat{n_i}=\ket{1_i}\bra{1_i}$ is the projection operator onto the Rydberg state $\ket{1_i}$, and the interatomic interaction potential is of the form $V_{ij}=\frac{C_6}{|\vec{r_i}-\vec{r_j}|^6}$ with characteristic interaction energy (working in natural units with $\hbar=1$ such that energy may be expressed in terms of frequency) $C_6 =5.42\cdot10^{-24}$.

$\hat{n_i}=\ket{1_i}\bra{1_i}$ is the projection operator onto the Rydberg state $\ket{1_i}$

Interaction Tail



## Graph Pictures

|                            Graph                             |                                                              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![con_graph_original](Documentation.assets/con_graph_original-1674976175318-23-1674976180988-25.png) | ![graph_original](Documentation.assets/graph_original-1674976222266-31.png) |
| ![con_graph_original](Documentation.assets/con_graph_with_four_turned_on_3tails-1674976129323-15-1674976130635-17.png) | ![graph_with_four_turned_on_3tails](Documentation.assets/graph_with_four_turned_on_3tails-1674976229812-34.png) |
| ![con_graph_with_one_node_turned_off](Documentation.assets/con_graph_with_one_node_turned_off-1674976189641-28.png) | ![graph_with_one_node_turned_off](Documentation.assets/graph_with_one_node_turned_off-1674976240084-37-1674976241998-39.png) |
|                                                              |                                                              |





















## Companion for Unit Disk Graph Construction 

Exact alignment of y is going to be necessary



## Pulse Optimization 

Denote the sine cardinal function as $${sinc}(t) = \cases{\frac{\sin(t)}{t}&$,t\neq0$\cr1&$,t=0$}$$.

Then consider the wave profile $p(t)=af(\frac{\omega t}{2}-\pi), t\ge0$,

 where $${f}(t) = \cases{{sinc^2}(t)&$,t\le0$\cr1&$,t>0$}$$  and the maximum amplitude $a$ and radial frequency $\omega$ are parameters to be determined.

In order

Logistic: $p_{logistic}(t)=\frac{A}{1+Be^{-Cx}}$

## Post Processing



## Experience



## Sources

https://www.quera.com/aquila

https://github.com/iQuHACK/2023_QuEra
