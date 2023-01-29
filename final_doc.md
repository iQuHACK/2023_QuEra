# MIS problem evolved

Team IsaacChuangFansClub

---

## Problem

An analog Hamiltonian simulation computer solves this problem by trying to be in the lowest energy state.

## Results

### Graph design

### Blockade radius optimization

### Pulse Optimization

We tried to use Sels and Polkovnikov's counterdiabatic protocol. The driving Hamiltonian
$$H =H_0+A= - \Delta(t)\sum_i n_i + \sum_{<{i,j}>}V_{ij}n_i n_j + \sum_i \frac{\Omega(t)}{2}(e^{i\phi(t)}\ket{g_i}\ket{e_i}+e^{-i\phi(t)}\ket{e_i}\ket{g_i})$$
where $<i,j>$ represents nearest neighbor in our graph. It can be viewed as the sum of a base
$$H_0 = - \Delta(t)\sum_i n_i + \sum_{<{i,j}>}V_{ij}n_i n_j + \sum_i \frac{\Omega(t)}{2}\cos(\phi(t))\left(\ket{g_i}\bra{e_i}+\ket{e_i}\bra{g_i}\right)$$
and a counterdiabatic component
$$A = \sum_i \frac{\Omega(t)}{2}i\sin(\phi(t))\left(\ket{g_i}\bra{e_i}-\ket{e_i}\bra{g_i}\right)$$
in which way $H_1$ is a purely imaginary part of $H_0$, respecting the constraint according to [1]. 

It is worth noting that the two terms can be rewritten using Pauli operators defined on the $\ket{e_i},\ket{g_i}$ bases as
$$\begin{align}
H_0 &=-\Delta(t) \sum_i \frac{\sigma_i^z+1}{2} + \sum_{<i,j>}\frac{V_{ij}}4 (\sigma_i^z+1)(\sigma_j^z+1) + \sum_i \frac{\Omega(t)}2\cos(\phi) \sigma_i^x \\
	&= -\Delta(t) \sum_i \frac{\sigma_i^z+1}{2} + \sum_{<i,j>}\frac{V_{ij}}4 (\sigma_i^z+1)(\sigma_j^z+1) + \sum_i \frac{\Omega(t)}2\cos(\phi) \sigma_i^x 
\end{align}$$

$$A=\sum_i\frac{\Omega(t)}2 \sin(\phi) \sigma_i^y$$







### References

[1] **Minimizing irreversible losses in quantum systems by local counterdiabatic driving**

