import heapq
import pickle

from pyrosm import get_data, OSM
from haversine import haversine

def build_graph(directory):
    """
    Saves a graph of open street map data
    Directory String: The directory to save the map data file
    return: None
    """
    data_seattle = get_data("Seattle", directory=directory)
    osm_seattle = OSM(data_seattle)
    nodes, edges = osm_seattle.get_network(nodes=True, network_type="driving")
    graph = osm_seattle.to_graph(nodes, edges)
    with open("src/graph.pkl", "wb") as out_file:
        pickle.dump(graph, out_file)

# convert user input to a start/end in the graph by finding the closest point in the graph either using the vs.find function or another method as this won't work for every coordinate

if __name__ == "__main__":
    # build_graph("/home/ubuntu/safe-path-finder/src")
    with open("src/graph.pkl", "rb") as in_file:
        seattle_graph = pickle.load(in_file)
    print(path)
    
    

# neighbors: https://igraph.org/r/html/1.2.7/neighbors.html

#print(seattle_graph.vs.attribute_names())
#print(seattle_graph.es.attribute_names())
#print(seattle_graph.vs["geometry"][0:10])
# print(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471))) # need to round to 7 digits after the decimal point and find nearest point
# print(seattle_graph.incident(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471)), mode="out")) # returns vertex edges
# print(seattle_graph.es[0]["length"])
# length is measured in meters