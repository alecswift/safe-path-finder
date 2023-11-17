from pyrosm import OSM, get_data

data_seattle = get_data("Seattle", directory="/home/ubuntu/safe-path-finder/data")
osm_seattle = OSM(data_seattle)
nodes, edges = osm_seattle.get_network(nodes=True, network_type="driving")
graph = osm_seattle.to_graph(nodes, edges)
#load this data to a pickle file for later
