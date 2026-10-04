import matplotlib.pyplot as plt
import osmnx as ox



def view_route_map(G):
    ox.plot_graph(
    G,  
    node_size=1.5,
    node_color="#FF3E2C",         
    edge_color="#555555",  
    edge_linewidth=1,
    bgcolor="white"       
    )
    plt.show()

