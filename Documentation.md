# Modularized Sharp Networks for State Preparation into MIS
QuEra Challenge, iQuHACK 2023

QuEra Yale University Team
Members: Alex Deters, Ben McDonough, Pranav Parakh, Sofia Fausone, Wyatt Kremer

## Contents

[TOC]

## Theoretical Motivation

QuEra Aquila is a 256-qubit quantum processor realized as a programmable array of optically-trapped ultracold $Rb$ atoms. Aquila belongs to the class of neutral atom hardware platforms. A two-level system is established by identifying the ground state $\ket{0}$ and excited "Rydberg" state $\ket{1}$ of a neutral $Rb$ atom with the electron configurations $[Kr]\space5s^1$ and $[Kr]\space70s^1$, respectively. The Gaussian laser beams that trap the arrays of $Rb$ atoms may be used to drive time-dependent Rabi oscillations $\Omega(t)$ with induced relative phase $e^{2i\phi(t)}$ and introduce a *global* time-dependent Rydberg detuning $\Delta(t)$. The global nature of $\Delta(t)$ imposed by the hardware inherently prevents the *direct* preparation of the $i$th atom in the Rydberg state $\ket{1_i}$. Therefore, it is necessary to place the atoms on the 75 $\mu m$ by 76 $\mu m$ processor in such a way that the geometry and interatomic interactions, which govern the time evolution of the system, would bring an initial uniform state to any given state. It is this sense that a state can be *indirectly* prepared to have the $i$th atom in the Rydberg state $\ket{1_i}$. 

The Hamiltonian for the array of $N\space Rb$ atoms is given as:

$\frac{H}{\hbar}=\sum_i{\Omega (t)(e^{i\phi(t)}\ket{0_i}\bra{1_i}+e^{-i\phi(t)}\ket{1_i}\bra{0_i})}-\Delta(t)\sum_i{\hat{n_i}}+\sum_{i<j}{V_{ij}\hat{n_i}\hat{n_j}}$,

where $\ket{0_i}$ and $\ket{1_i}$ are the ground and Rydberg states for atoms $i=1,2,...,N$, $\hat{n_i}=\ket{1_i}\bra{1_i}$ is the projection operator onto the Rydberg state $\ket{1_i}$, and the interatomic interaction potential is of the form $V_{ij}=\frac{C_6}{|\vec{r_i}-\vec{r_j}|^6}$ with characteristic interaction energy  $C_6 =5.42\cdot10^{-24}$ (working in natural units with $\hbar=1$ such that energy may be expressed in terms of frequency). The natural characteristic distance $R=(\frac{C_6}{\Delta_{max}})^{1/6}$ is called the **blockade radius**. We note that $\Delta_{max}\sim10^7$ so . Suppose atoms $i,j$ are in their respective Rydberg states $\ket{1_i},\ket{1_j}$ and have separation distance $|\vec{r_i}-\vec{r_j}|<R$.  Then the interaction potential $V_{ij}=\frac{C_6}{|\vec{r_i}-\vec{r_j}|^6}\gg\Delta_{max}$ , demonstrating that a large repulsive interaction cannot be overcome by atom-field coupling in such close proximity. The notion of  the **Rydberg blockade** is simply the tendency for atoms to not simultaneous occupy Rydberg states at distance scales $L\lesssim R$ . It is notable that the potential $V_{ij}=\frac{C_6}{|\vec{r_i}-\vec{r_j}|^6}$ has an interaction tail; even for separation distances $|\vec{r_i}-\vec{r_j}|>R$, $V_{ij}$ does not vanish despite being very small as shown in the figure below. This has important consequences for the time evolution of the system.

![inverse_sixth_power_spike](Documentation.assets/inverse_sixth_power_spike.png)

**Figure 1:**  The neighborhood around an inverse sextic potential $V\propto\frac{1}{|\vec{r}|^6}$

## Exploiting the Interaction Tail

|                            Graph                             |                                                              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![con_graph_original](Documentation.assets/con_graph_original-1674976175318-23-1674976180988-25.png) | ![graph_original](Documentation.assets/graph_original-1674976222266-31.png) |
| ![con_graph_original](Documentation.assets/con_graph_with_four_turned_on_3tails-1674976129323-15-1674976130635-17.png) | ![graph_with_four_turned_on_3tails](Documentation.assets/graph_with_four_turned_on_3tails-1674976229812-34.png) |
| ![con_graph_with_one_node_turned_off](Documentation.assets/con_graph_with_one_node_turned_off-1674976189641-28.png) | ![graph_with_one_node_turned_off](Documentation.assets/graph_with_one_node_turned_off-1674976240084-37-1674976241998-39.png) |
|                                                              |                                                              |

**Figure 2: Rydberg-Tail Selective State Initialization**

We decided to simulate and run a modular graph that can be "stitched" together with other graphs in order to create larger maximum independent sets. This required us to be able to control the edge node behaviour of our modular pieces in order to put them together while minimally affecting the maximum independent sets. Our inital idea was to do this through selective detuning of certain atoms that occured on the edge of our graph. Working within the hardware constraints, we realized that was not possible, and so set out to create a different way to be able to selectively influence edge-atom state behaviour. 

There interaction potential in the Hamiltonian is determined by a constant interaction energy, $C_6$, and decreases as the inverse of the separation distance to the sixth power. To an approximation, this means that only atoms within the unit disk radius influence each other. Atoms on the exterior of the graph (those with a small degree), are more likely to be in a Rydberg state. The atoms on the exterior of the graph experience a lower potential penalty when in a Rydberg state, influencing them to be in a Rydberg state with a high probability. Even without the advantage of selective detuning, we realized that by connecting external atoms to atoms we wanted to influence, we could influence their initial state.

In the above figure, we present a graph that whose vertices we change from their default state by using the external node (tail) strategy described above. in the top row, we present a graph with a well defined maximum indepndent set, which was run through the classical simulator and produced the expected value. In the second row, we attempted to change the "4" node from the first graph from the ground state to the Rydberg state. We did this by connecting three two-node tails to this node. The external most node of these tails was generally in the Rydberg state, forcing the second node to be more often in the ground state. This in turn successfully increased the probability that the "4" state was in the Rydberg state, from 0 to about 50%. In the bottom-most row, we tried to use tails to change the "1" node from the Rydberg state into the ground state. By attaching two single-node tails to the "1" node, we effectively changed it from being in the Rydberg state 100% of the time to being in the ground state 100% of the time, controlling the atom.

We used this property in our method of stitching modular graphs together, now that we had a reliable way to set the boundary conditions of each small piece of a graph.

## Analysis of the $(N,\lambda)$ Regular Polyhedron Junction

Suppose that $N\geq 2$ unit disks are to be brought as close as possible under the constraint that the centers of the disks must always  define the vertices of a regular polygon of $N$ sides. This can be accomplished by considering the set of points

$\set{\lambda cos(\frac{2\pi k}{N}),\lambda sin(\frac{2\pi k}{N})\space|\space k\in\set{0,1,...,N-1}}$ where $\lambda$ is a scalar multiple equal to the new radii of the disks under a dilation by the factor $\lambda$. We wish to find the largest integer $N$ such that there is some $\lambda<1$ such that all disks enclose exactly one center.

By the Law of Cosines, the distance separating the centers of a pair of adjacent disks after a dilation by factor $\lambda$ is given as

$d(N)=\sqrt{\lambda^2+\lambda^2-2(\lambda)(\lambda)\cos(\frac{2\pi}{N})}=\sqrt{2\lambda^2(1-\cos(\frac{2\pi}{N})}=\lambda\sqrt{2(1-\cos(\frac{2\pi}{N})}$

and requiring that $d(N)\geq1$ yields

$\lambda(N)\geq\frac{1}{\sqrt{2(1-cos(\frac{2\pi}{N})}}$. It immediately follows that if $\lambda=\lambda_{min}(N)=\frac{1}{\sqrt{2(1-cos(\frac{2\pi}{N})}}$, the distance between the centers of adjacent disks is exactly $1$. For some fixed $N$, $\lambda<\lambda_{min}$ would imply that $d(N)<1$ and therefore that there is a disc that encloses at least two

| ![N4](Documentation.assets/N4.png) | ![N5Unscaled](Documentation.assets/N5Unscaled.png) |
| ---------------------------------- | -------------------------------------------------- |
| ![N5](Documentation.assets/N5.png) | ![N6](Documentation.assets/N6.png)                 |

**Figure 3:** Regular polyhedron junctions for $(N,\lambda)=(4,1),(5,1),(5,\lambda_{min}(5)),(6,1)$









## Companion for Designing Unit Disk Graphs



Exact alignment of y is going to be necessary



## Pulse Optimization 

Denote the sine cardinal function as $${sinc}(t) = \cases{\frac{\sin(t)}{t}&$,t\neq0$\cr1&$,t=0$}$$.

Then consider the wave profile $p_{sinc}(t)=af(\frac{\omega t}{2}-\pi), t\ge0$,

 where $${f}(t) = \cases{{sinc^2}(t)&$,t\le0$\cr1&$,t>0$}$$  and the maximum amplitude $a$ and radial frequency $\omega$ are parameters to be determined.

Gaussian pulse: $p_{gaussian}(t)=e^{-x^2}$



Logistic?: $p_{logistic}(t)=\frac{A}{1+Be^{-Cx}}$

## Post Processing

22 unextractable for big_ben

## Experience



## Sources

https://www.quera.com/aquila

https://github.com/iQuHACK/2023_QuEra
