import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.axes import Axes
import numpy as np
from braket.ahs.analog_hamiltonian_simulation import AnalogHamiltonianSimulation
from braket.ahs.atom_arrangement import AtomArrangement,SiteType
import warnings
import networkx as nx
import json

C6 = 5.42E-24

def is_IS(graph,node_types):
    inds = np.argwhere(np.array(node_types)==0).ravel()
    subgraph = nx.subgraph(graph,inds)
    print(subgraph)
    return subgraph.number_of_edges() == 0
    
    
def find_UDG_radius(position, graph):
    '''
    Computes the optimal unit disk radius for a particular set of positions and graph.
    position   - [N x 2] array of points
    graph       - network connectivity graph. This should be a unit disk graph.
    
    returns
    radius      - Optimal unit disk radius of the graph
    rmin        - Minimum distance
    rmax        - Maximum distance
    '''
    
    dists = np.sqrt((position[:,0,None] - position[:,0])**2
               + (position[:,1,None] - position[:,1])**2)
    rmin = 0
    rmax = np.inf
    for i in range(position.shape[0]):
        for j in range(i+1,position.shape[0]):
            if (i,j) in graph.edges:
                if rmin<dists[i,j]:
                    rmin = dists[i,j]
            elif (i,j) not in graph.edges:
                if rmax>dists[i,j]:
                    rmax = dists[i,j]
    
    if rmin>rmax:
        print(rmin,rmax)
        raise BaseException("Graph is not a unit disk graph!")
    
    return np.sqrt(rmin*rmax),rmin,rmax
    
    return np.sqrt(rmin*rmax),rmin,rmax


def visualize_graph(ax,graph,pos_dict,node_colors = "#6437FF"):
    """Visualize graph using networkx

    Args:
        ax (matplotlib.axes.Axes): Axes object to plot graph on.
        graph (networkx.Graph): Graph to be plotted
        pos_dict (dict): dictionary containing the x,y coordiantes where the nodes are the keys.
        node_colors (str or list, optional):  Defaults to "#6437FF". The color(s) to color the nodes of the graph. 
    
    """
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    # pos_dict = {a:positions[a] for a in range(positions.shape[0])}
    nx.draw_networkx_edges(graph,pos_dict,width=10/np.sqrt(len(graph.nodes)),ax=ax)
    nx.draw_networkx_nodes(graph,pos_dict,node_size=1225/np.sqrt(len(graph.nodes)),node_color=node_colors,ax=ax)
    

def get_graph_from_blockade_radius(register : AtomArrangement, blockade_radius:float):
    """Get graph based on blockade radius. 

    Args:
        register (braket.ahs.atom_arrangement.AtomArrangement): register for analog quantum simulation. 
        blockade_radius (float): the blockade radius calculated using (C_6/final_detuning)^(1/6).

    Returns:
        networkx.Graph: The graph of the effective unit disk graph set by the blockade radius. 
    """
    filled_sites = [site.coordinate for site in register if site.site_type == SiteType.FILLED]
    graph = nx.Graph()
    
    positions = {n:c for n,c in enumerate(filled_sites)}

    graph.add_nodes_from(positions.keys())
    
    for n,r_1 in positions.items():
        for m,r_2 in positions.items():
            if n <= m: continue
            dist = np.linalg.norm(np.array(r_1)-np.array(r_2))
            if dist < blockade_radius:
                graph.add_edge(n,m)
                
    return graph,positions


def get_blockade_radius(detuning: float, rabi: float) -> float:
    """calculate Blockade Radius given the detuning and rabi amplitude. 

    Args:
        detuning (float): detuning value.
        ravi (float): rabi value
    Returns:
        float: blockade radius
    """
    
    demon = np.sqrt(detuning**2+rabi**2)
    if demon > 0:
        return (C6/demon)**(1/6)
    else:
        return np.inf
    
    

def plot_task_results(
    ahs_program : AnalogHamiltonianSimulation,
    n_shots : int,
    pre_processed_shot : list[int],
    post_processed_shot : list[int],
):
    """function to generate figure summarizing iQuHack task results.

    Args:
        ahs_program (AnalogHamiltonianSimulation): Braket AHS program used to generate shots
        n_shots (int): number of shots for Task
        pre_processed_shot (list[int]): The list showing the independent set before post processing, 
        post_processed_shot (list[int]): The list showing the independent set after post processing
    """
    
    fig = plt.figure(tight_layout=True,figsize=(9,6))
    gs = gridspec.GridSpec(6, 3)
    
    graph_axs = [
        fig.add_subplot(gs[0:3, 2]),
        fig.add_subplot(gs[3:6, 2])
    ]
    
    drive_axs = [
        fig.add_subplot(gs[0:2, 0:2]),
        fig.add_subplot(gs[2:4, 0:2]),
        fig.add_subplot(gs[4:6, 0:2])
    ]
    
    drive_axs[0].sharex(drive_axs[1])
    drive_axs[1].sharex(drive_axs[2])


    register = ahs_program.register
    drive = ahs_program.hamiltonian
    
    data = {
        'amplitude [rad/s]': drive.amplitude.time_series,
        'detuning [rad/s]': drive.detuning.time_series,
        'phase [rad]': drive.phase.time_series,
    }
    
    detuning_data = list(data['detuning [rad/s]'].values())
    blockade_radius = get_blockade_radius(detuning_data[-1],0)

    
    
    graph,positions = get_graph_from_blockade_radius(register,blockade_radius)

    
    for ax, data_name in zip(drive_axs, data.keys()):
        ax.tick_params('both',direction='in')
        ax.tick_params('x',top=True)
        ax.tick_params('y',left=True)

        if data_name == 'phase [rad]':
            ax.step(data[data_name].times(), data[data_name].values(), '.-', where='post')
        else:
            ax.plot(data[data_name].times(), data[data_name].values(), '.-')
            ax.xaxis.set_ticklabels([])        

        ax.set_ylabel(data_name)
        ax.grid(ls=':')
    ax.set_xlabel("time (s)")

    color = {
        0:'red',
        1:'black'
    }
    
    pre_processed_shot = [s for s,site in zip(pre_processed_shot,register) if site.site_type == SiteType.FILLED]
    post_processed_shot = [s for s,site in zip(post_processed_shot,register) if site.site_type == SiteType.FILLED]

    shots = [
        pre_processed_shot,
        post_processed_shot
    ]
    
    titles = [
        "pre-processed",
        "post-processed"
    ]
    
    if not is_IS(graph,post_processed_shot):
        warnings.warn("'post_processed_shot' is not a valid independent set of the effective graph.")
    
    
    for (ax,shot,title) in zip(graph_axs,shots,titles):    
        colors = [color[s] for s in shot]
        visualize_graph(ax,graph,positions,colors)
        ax.title.set_text(title)
    
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.25)
    fig.suptitle(f'number of shots: {n_shots}')
    return fig,drive_axs,graph_axs
    

def generate_test_program(Nx,Ny,lattice_spacing=6.5e-6):
    from quera_ahs_utils.drive import get_drive


    register = AtomArrangement()
    for ix in range(Nx):
        for iy in range(Ny):
            x = ix * lattice_spacing
            y = iy * lattice_spacing
            register.add((x,y))
    

    time_points = [0, 2.5e-7, 2.75e-6, 3e-6]
    amplitude_min = 0
    amplitude_max = 1.57e7  # rad / s

    detuning_min = -5.5e7  # rad / s
    detuning_max = 5.5e7  # rad / s

    amplitude_values = [amplitude_min, amplitude_max, amplitude_max, amplitude_min]  # piece-wise linear
    detuning_values = [detuning_min, detuning_min, detuning_max, detuning_max]  # piece-wise linear
    phase_values = [0, 0, 0, 0]  # piece-wise constant


    drive =  get_drive(time_points, amplitude_values, detuning_values, phase_values)

    return AnalogHamiltonianSimulation(
        register=register, 
        hamiltonian=drive
    )

def save_result_json(json_file,result):
    '''
    Helper function to save results locally
    '''
    result_dict = {"measurements":[]}
    for measurement in result.measurements:
        shot_result = {
            "pre_sequence":[int(qubit) for qubit in measurement.pre_sequence],
            "post_sequence":[int(qubit) for qubit in measurement.post_sequence]
                      } 
        result_dict["measurements"].append(shot_result)
        
    with open(json_file,"w") as io:
        json.dump(result_dict,io,indent=2)
        
def open_json(json_file):
    '''
    Helper function to load and open json data
    '''
    with open(json_file,"r") as io:
        return json.load(io) 

if __name__ == '__main__':
    L = 10
    ahs_program = generate_test_program(L,L,lattice_spacing=4e-6)
    pre_processed_shot = list(np.random.randint(2,size=L*L))
    post_processed_shot = list(np.random.randint(2,size=L*L))
    
    fig,drive_axs,graph_axs = plot_task_results(
        ahs_program,100,pre_processed_shot,post_processed_shot
    )
    
    plt.show()
