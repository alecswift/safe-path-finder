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
    nodes, edges = osm_seattle.get_network(nodes=True, network_type="driving")
    graph = osm_seattle.to_graph(nodes, edges, graph_type="networkx")
    with open("src/graph.pkl", "wb") as out_file:
        pickle.dump(graph, out_file)

def shortest_path(graph, source_address, target_address):
    """
    Takes a graph, source address, and target address and returns the shortest
    path from the source address to the target address
    """
    source = osmnx.geocode(source_address)
    target = osmnx.geocode(target_address)
    print(source, target)
    source_node = osmnx.nearest_nodes(graph, source[1], source[0])
    target_node = osmnx.nearest_nodes(graph, target[1], target[0])
    
    routes = networkx.all_shortest_paths(graph, source_node, target_node, weight="length")
    
    return routes


if __name__ == "__main__":
    # build_graph("/home/ubuntu/safe-path-finder/src")
    with open("src/graph.pkl", "rb") as in_file:
        seattle_graph = pickle.load(in_file)

    print([path for path in shortest_path(seattle_graph, "Corner Market, 1530, Post Alley, West Edge, Belltown, Seattle, King County, Washington, 98101, United States", "3710, Wallingford Avenue North, Wallingford, Seattle, King County, Washington, 98103, United States")])
    
    
