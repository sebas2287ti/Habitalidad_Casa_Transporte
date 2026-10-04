import osmnx as ox
import matplotlib.pyplot as plt

ox.settings.use_cache = True
ox.settings.cache_folder = "./cache"

def download_map(location):

    G = ox.graph_from_place(location, network_type="drive")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    return G
