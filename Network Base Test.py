import networkx as nx

b = nx.Graph()
b.add_nodes_from([i for i in range(8)])
block_edges = [(0,1),(0,3),(0,4),(1,2),(1,5),(2,3),(2,6),(3,7),(4,5),(4,7),(5,6),(6,7)]
b.add_edges_from(block_edges)
nx.draw(b)