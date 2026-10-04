import matplotlib.pyplot as plt
import osmnx as ox

def view_route_map(G, route):
    ox.plot_graph_route(
    G, 
    route, 
    route_color="#ff0000", 
    route_linewidth=3, 
    node_size=0,          
    edge_color="#555555",  
    edge_linewidth=0.5,
    bgcolor="white"       
    )
    plt.show()

