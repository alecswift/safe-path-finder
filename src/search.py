import heapq
import pickle

from pyrosm import get_data, OSM
from shapely import Point
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
    entry = 1
    minheap = [(0, 0, start, 0)] # add first item
    distances = {start: (0, None)} # also the visited set
    end_lat, end_lon = end['lat'], end['lon']

    # need to create node object with parents to find path
    while minheap[0][0] != end:
        _, _, curr_node, curr_dist = heapq.heappop(minheap)

        for out_edge_idx in seattle_graph.incident(curr_node, mode="out"):
            out_edge = seattle_graph.es[out_edge_idx]
            new_dist = curr_dist + out_edge["length"]
            neighbor = out_edge["v"]
            dist_to_end = haversine((neighbor['lat'], neighbor['lon']), (end_lat, end_lon)) * 1000 # kilometers to meters


            # need to add parent traversal
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = (new_dist, curr_node)
            else: # visited
                continue
            
            weight = 2 * (new_dist + dist_to_end)
            heapq.heappush(minheap, (weight, entry, neighbor, new_dist))
            entry += 1


    path = []
    curr = distances[end]
    while curr is not None:
        path.append(curr)
        curr = distances[curr][1]

    return path[::-1]




# neighbors: https://igraph.org/r/html/1.2.7/neighbors.html

#print(seattle_graph.vs.attribute_names())
#print(seattle_graph.es.attribute_names())
#print(seattle_graph.vs["geometry"][0:10])
# print(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471))) # need to round to 7 digits after the decimal point and find nearest point
# print(seattle_graph.incident(seattle_graph.vs.find(geometry=Point(-122.3186189, 47.6426471)), mode="out")) # returns vertex edges
print(seattle_graph.es[0]["length"])
# length is measured in meters