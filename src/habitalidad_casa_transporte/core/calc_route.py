import networkx as nx
import osmnx as ox


def route_ideal(G, start_cords_node, end_cords_node):
    
    start_node_y, start_node_x = start_cords_node
    end_node_y, end_node_x = end_cords_node
    
    node_start = ox.nearest_nodes(G, start_node_y, start_node_x)
    node_end = ox.nearest_nodes(G, end_node_y, end_node_x)
    
    route = nx.shortest_path(G, source=node_start, target=node_end, weight="travel_time")
    
    return route