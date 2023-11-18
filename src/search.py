import heapq
import pickle

from pyrosm import get_data, OSM
from shapely import Point

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

with open("src/graph.pkl", "rb") as in_file:
    seattle_graph = pickle.load(in_file)

# convert user input to a start/end in the graph by finding the closest point in the graph either using the vs.find function or another method as this won't work for every coordinate

def a_star_search(start, end):
    """
    parameters
    start: starting vertex in the graph
    end: ending/target vertex in the graph
    return: path through the graph
    """

    minheap = []
    distances = {start: 0} # also the visited set

    # need to create node object with parents to find path
    while minheap[0][0] != end:
        curr_node, curr_dist = heapq.heappop(minheap)

        for out_edge_idx in seattle_graph.incident(curr_node, mode="out"):
            out_edge = seattle_graph.es[out_edge_idx]
            out_dist = out_edge["length"]
            end_dist = 
            neighbor = out_edge["v"]

            if neighbor in distances:
                pass

            # watch the a* search computerphile video, how does the visited/distance set work?




# neighbors: https://igraph.org/r/html/1.2.7/neighbors.html

#print(seattle_graph.vs.attribute_names())
#print(seattle_graph.es.attribute_names())
#print(seattle_graph.vs["geometry"][0:10])
# print(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471))) # need to round to 7 digits after the decimal point and find nearest point
# print(seattle_graph.incident(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471)), mode="out")) # returns vertex edges
print(seattle_graph.es[0]["length"])