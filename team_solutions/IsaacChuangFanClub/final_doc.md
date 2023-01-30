# Hi! We are the IsaacChuangFansClub team!

---

# Problem

Find Maximum Independent State of graphs that constructed by repetition of small 3*N graphs (like the one we used) while trying to be in the lowest energy state.

# Approach 

The idea we used in the challenge was to encode the MIS solution into the ground state of Hamiltonian. Next, we used the quantum adiabatic algorithm (QAA) to evolve simple Hamiltonian to desired complicated Hamiltonian. 

## Graph design
On the picture below one can find the graph structure we have used in the challenge in order to maximize the number of independent sets. The way the pattern is created is by multiplying the building block element depicted in the next figure. 
![Graph structure](./assests/graph.png)

![Building block element](./assests/element.png)

### Other graphs we've looked into

## Blockade radius optimization

## Pulse Optimization

### References

[1] **Minimizing irreversible losses in quantum systems by local counterdiabatic driving**

# Results
The result of running the demonstration algorithm with the enhanced parameters is presented below.

|Variable|Quantity|
|:----|----:|
|Nshots|80|
|Size of Maximum independent set|51|
|Total number of nodes|93|


![Graph result](./assests/result.png){width=60%}

![Graph shots analysis](./assests/analysis.png){width=60%}