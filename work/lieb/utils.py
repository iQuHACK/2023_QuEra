import numpy as np
import matplotlib.pyplot as plt

import networkx as nx

def postprocess_MIS(G,results):
    '''
    Removes vertices that violate the independent set condition
    G - networkx graph
    results - an AWS AnalogHamiltonianSimulationQuantumTaskResult
    
    returns
    data_out - a list of bitstrings which are valid independent sets of G
    '''
    data_out = []
    for measurement in results["measurements"]: # For each measurement...
        pre_sequence = np.array(measurement["pre_sequence"])
        post_sequence = np.array(measurement["post_sequence"])
        if np.any(pre_sequence==0): continue # skip anyshots with defects
            
        bitstring = post_sequence
        inds = np.nonzero(bitstring==0)[0]    # Find indices of IS vertices
        subgraph = nx.subgraph(G,inds)        # Generate a subgraph from those vertices. If the bitstring is an independent set, this subgraph has no edges.
        inds2 = nx.maximal_independent_set(subgraph,seed=0) # Find the mIS of this subgraph. If there are no edges, it is the original bitstring. Else, it randomly chooses within each graph.
        payload = np.ones(len(bitstring))     # Forge into the correct data structure (a list of 1s and 0s)
        payload[inds2] = 0
        data_out.append(payload)
        
    if len(data_out) == 0: 
        raise ValueError("no independent sets found! increase number of shots.")
        
    return np.asarray(data_out)

def analysis_MIS(graph,result_json):
    '''
    Helper function to analyze a MIS result and plot data
    '''

    post_bitstrings = np.array([q["post_sequence"] for q in result_json["measurements"]])
    pp_bitstrings = postprocess_MIS(graph, result_json)


    IS_sizes = np.sum(1-pp_bitstrings,axis=1)
    unique_IS_sizes,counts = np.unique(IS_sizes,return_counts=True)
    
    pre_IS_sizes = np.sum(1 - post_bitstrings, axis = 1)
    pre_unique_IS_sizes, pre_counts = np.unique(pre_IS_sizes, return_counts = True)


    avg_no_pp = 'Average pre-processed size:  {:0.4f}'.format( (1-post_bitstrings).sum(axis=1).mean() )
    avg_pp = 'Average post-processed IS size: {:0.4f}'.format(IS_sizes.mean())
    print(avg_no_pp)
    print(avg_pp)
    
    plt.bar(pre_unique_IS_sizes, pre_counts/pre_counts.sum())
    plt.title("Raw Results")
    plt.xticks(pre_unique_IS_sizes)
    plt.xlabel("IS Sizes",fontsize=14)
    plt.ylabel("Probability",fontsize=14)
    plt.show()
    
    plt.bar(unique_IS_sizes, counts/counts.sum())
    plt.title("Processed Results")
    plt.xticks(unique_IS_sizes)
    plt.xlabel("IS Sizes",fontsize=14)
    plt.ylabel("Probability",fontsize=14)
    plt.show()
    
    return IS_sizes,pp_bitstrings
    