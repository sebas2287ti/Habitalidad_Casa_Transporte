import osmnx as ox

def build_graph_map(G):
    
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    
    return G 