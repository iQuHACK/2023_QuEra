import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

def kings_graph(numx,numy,filling=0.7,seed=None):
    '''
    Generate a next nearest neighbor graph with a lattice constant 1, with some number of nodes removed
    numx    - number of grid points in the X direction
    numy    - number of grid points in the Y direction
    filling - Fraction of vertices to be kept. Total number of vertices is int(numx*numy*filling)
    
    Returns
    pos     - [N x 2] array of points on a square grid
    graph   - networkx connectivity graph
    '''
    xx,yy = np.meshgrid(range(numx),range(numy))
    num_points = int(numx*numy*filling)
    rand = np.random.default_rng(seed=seed)
    # Generate points
    points = np.array([xx.flatten(),yy.flatten()]).T
    points = points[rand.permutation(numx*numy)[0:num_points],:]
    
    distances = np.sqrt((points[:,0] - points[:,0,None])**2 + (points[:,1] - points[:,1,None])**2)
    graph     = nx.Graph(distances<=np.sqrt(2))#+1E-10)
    
    graph.remove_edges_from(nx.selfloop_edges(graph))
    print("GRAPH: ", graph.edges)
    return points, graph

def manual_snake_example():
    points=[]

    # 100 qubit sssssnakee---------------------------
    points.append([1,0])
    points.append([2,0])
    points.append([3,0])
    points.append([4,0])
    points.append([5,0])
    points.append([6,0])
    points.append([7,0])
    points.append([8,0])
    points.append([9,0])
    points.append([10,0])
    points.append([11,0])
    points.append([12,0])
    points.append([13,1])
    points.append([12,2])
    points.append([11,2])
    points.append([10,2])
    points.append([9,2])
    points.append([8,2])
    points.append([7,2])
    points.append([6,2])
    points.append([5,2])
    points.append([4,2])
    points.append([3,2])
    points.append([2,2])
    points.append([1,2])
    points.append([0,3])
    points.append([1,4])
    ##
    points.append([2,4])
    points.append([3,4])
    points.append([4,4])
    points.append([5,4])
    points.append([6,4])
    points.append([7,4])
    points.append([8,4])
    points.append([9,4])
    points.append([10,4])
    points.append([11,4])
    points.append([12,4])
    points.append([13,5])
    points.append([12,6])
    points.append([11,6])
    points.append([10,6])
    points.append([9,6])
    points.append([8,6])
    points.append([7,6])
    points.append([6,6])
    points.append([5,6])
    points.append([4,6])
    points.append([3,6])
    points.append([2,6])
    points.append([1,6])
    points.append([0,7])
    points.append([1,8])
    ##
    points.append([2,8])
    points.append([3,8])
    points.append([4,8])
    points.append([5,8])
    points.append([6,8])
    points.append([7,8])
    points.append([8,8])
    points.append([9,8])
    points.append([10,8])
    points.append([11,8])
    points.append([12,8])
    points.append([13,9])
    points.append([12,10])
    points.append([11,10])
    points.append([10,10])
    points.append([9,10])
    points.append([8,10])
    points.append([7,10])
    points.append([6,10])
    points.append([5,10])
    points.append([4,10])
    points.append([3,10])
    points.append([2,10])
    points.append([1,10])
    points.append([0,11])
    points.append([1,12])
    ##
    points.append([2,12])
    points.append([3,12])
    points.append([4,12])
    points.append([5,12])
    points.append([6,12])
    points.append([7,12])
    points.append([8,12])
    points.append([9,12])
    points.append([10,12])
    points.append([11,12])
    points.append([12,12])
    points.append([13,13])
    points.append([12,14])
    points.append([11,14])
    points.append([10,14])
    points.append([9,14])
    points.append([8,14])
    points.append([7,14])
    points.append([6,14])
    points.append([5,14])
    points.append([4,14])
    #points.append([3,14])
    #points.append([2,14])
    #points.append([1,14])
    #points.append([0,15])
    #points.append([1,16])
    #
 
    #points2 = points.tolist()
    #print("POINTS 2:", points2)
    points=np.array(points)
    #print("test: " , points[:0])
    # Generate a unit disk graph by thresholding distances between points.
    distances = np.sqrt((points[:,0] - points[:,0,None])**2 + (points[:,1] - points[:,1,None])**2)
    graph     = nx.Graph(distances<=np.sqrt(2))#+1E-10)
    
    graph.remove_edges_from(nx.selfloop_edges(graph))
    print("GRAPH: ", graph.edges)
    return points, graph

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
        if len(inds) == 0: continue
        subgraph = nx.subgraph(G,inds)        # Generate a subgraph from those vertices. If the bitstring is an independent set, this subgraph has no edges.
        inds2 = nx.maximal_independent_set(subgraph,seed=0) # Find the mIS of this subgraph. If there are no edges, it is the original bitstring. Else, it randomly chooses within each graph.
        payload = np.ones(len(bitstring))     # Forge into the correct data structure (a list of 1s and 0s)
        payload[inds2] = 0
        data_out.append(payload)
        
    if len(data_out) == 0: 
        raise ValueError("no independent sets found! increase number of shots.")
        
    return np.asarray(data_out)

def analysis_MIS(graph,result_json, print_extra = True):
    '''
    Helper function to analyze a MIS result and plot data
    '''

    post_bitstrings = np.array([q["post_sequence"] for q in result_json["measurements"]])
    pp_bitstrings = postprocess_MIS(graph, result_json)


    IS_sizes = np.sum(1-pp_bitstrings,axis=1)
    unique_IS_sizes,counts = np.unique(IS_sizes,return_counts=True)


    if print_extra:
        avg_no_pp = 'Average pre-processed size:  {:0.4f}'.format( (1-post_bitstrings).sum(axis=1).mean() )
        print(avg_no_pp)
    avg_pp = 'Average post-processed IS size: {:0.4f}'.format(IS_sizes.mean())
    print(avg_pp)
    
    if print_extra:
        plt.bar(unique_IS_sizes,counts/counts.sum())
        plt.xticks(unique_IS_sizes)
        plt.xlabel("IS sizes",fontsize=14)
        plt.ylabel("probability",fontsize=14)
        plt.show()
    
    return IS_sizes,pp_bitstrings
    
