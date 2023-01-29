# Quantum State Preparation

The idea behind quantum state preparation is to leverage the limited resources inside a quantum machine, e.g., finite-time, to prepare a quantum state with the highest possible fidelity. There is a lot of literature on this subject, both on the mathematical side and in practical applications. Below we discuss two relevant methods for our challenge.

## The Basics

We can understand the dynamics of a quantum system beyond the adiabatic theorem through something called adiabatic perturbation theory. The idea for a well-behaved quantum system, the quantum wavefunction, can be expanded as a function of the speed of the Hamiltonian, $v$. We won't go too much into the theory here, but from dimensional analysis, we know that the wavefunction amplitudes and probability are dimensionless. The adiabatic theorem states that if we start in the ground state, the probability of being in an excited state is 0. That implies, to leading order in $v$, the probability amplitudes of the wavefunction for the excited states must be 0. Since the quantum problem is well-behaved, the wavefunction amplitudes must be analytic functions of $v$. As such, we know that the probability of being in an excited state must be:

$ p_{excitation} = C v + \cdots$

But what is $C$? 

Well, this is a more complicated question to answer. However, we can use dimensional analysis again to guess what it might be. 

Before we continue, we must obtain the units of $v$. Typically $v$ is related to the derivative of one (or more) parameters in the Hamiltonian. Parameters can be static or a function of time. For simplicity, let us assume we have absorbed $\hbar$ into the definition of the Hamiltonian, so all parameters are scaled by $\hbar$. With $\hbar$ taken care of, we now know that the units of the parameters are: 

${\rm [energy]} = \frac{1}{\rm [time]}$. 

Therefore, since $v$ is a derivative of the Hamiltonian, it must have units of $1/{\rm [time]}^2$, which is simply ${\rm [energy]^2}$. Therefore $C$ must have units:

${\rm [time]^2} = \frac{1}{\rm [energy]^2}$ 

The relevant energy is the gap between the ground and excited states. Hence the probability amplitude of the $n^{\rm th}$ excited state goes as: 

$a_n = \frac{v}{(E_{n}-E_0)^2}$,

where $E_n$ is the energy of the $n^{\rm th}$ excited state and $E_0$ is the energy of the ground state. The probability is the square of the probability amplitude, so:

$p_n \propto \frac{v^2}{(E_n-E_0)^4}$

For multiple velocities, the result is a bit more complicated, but all we really care about is a general principle.

This can be used to design pulses, as when the gap is large, the speed can be faster than when the gap is small. 

For a generic graph with many atoms, it is hopeless to find the ground state energy classically, let alone the gap. So finding the location of the minimum gap is useless. 

The exception are graphs that have repeating patterns. For these graphs, each size is related to the others. While the minimum gap won't be in the same spot, it will only drift slightly. This means that in smaller graphs, where the spectrum can be obtained classically, one can ballpark the minimum gap's location for the full-size problem.

## Machine-learning and Hybrid methods

Many quantum state preparation problems are cast in terms of a classical optimization problem. Suppose you treat the analog hamiltonian evolution as a black box. In that case, you can create a cost function related to how well the quantum state is prepared and where the functions' input values are the pulse shapes. There are many references available discussing these methods. 


## Counter-diabatic Driving

This involves driving multiple terms in your analog Hamiltonian to prevent excitations from occurring. During the evolution, the system may go far away from the ground state only to return at the very end. There are lots of different methods of obtaining the counter-diabatic protocol. Some references are below:

* [this](https://www.pnas.org/doi/full/10.1073/pnas.1619826114) reference as it discusses a method directly applicable to Aquila's platform. We suggest you look at the section titled *1D Spin Chain*, pg. E3914. 

* Another related reference is [here](https://arxiv.org/abs/1904.03209) which also can be implemented on Aquila. 

While the problems in these papers do not look like our rydberg atoms at first, you can map the rydberg Hamiltonian to Pauli-operators with some work. 

