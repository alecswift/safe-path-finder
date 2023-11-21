import pickle

import networkx
from pyrosm import get_data, OSM
import osmnx

def build_graph(directory):
    """
    Saves a graph of open street map data
    Directory String: The directory to save the map data file
    return: None
    """
    data_seattle = get_data("Seattle", directory=directory)
    osm_seattle = OSM(data_seattle)
    nodes, edges = osm_seattle.get_network(nodes=True, network_type="driving", graph_type="networkx")
    graph = osm_seattle.to_graph(nodes, edges)
    with open("src/graph.pkl", "wb") as out_file:
        pickle.dump(graph, out_file)

def shortest_path(graph, source_address, target_address):
    """
    Takes a graph, source address, and target address and returns the shortest
    path from the source address to the target address
    """
    source = osmnx.geocode(source_address)
    target = osmnx.geocode(target_address)

    source_node = osmnx.get_nearest_node(graph, source)
    target_node = osmnx.get_nearest_node(graph, target)

    route = networkx.shortest_path(graph, source_node, target_node, weight="length")
    
    return route


if __name__ == "__main__":
    # build_graph("/home/ubuntu/safe-path-finder/src")
    with open("src/graph.pkl", "rb") as in_file:
        seattle_graph = pickle.load(in_file)
    
    
