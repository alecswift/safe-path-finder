from pyrosm import OSM, get_data

data_seattle = get_data("Seattle", directory="/home/alec/Desktop/code/personal_projects/safe-path-finder/data")
osm_seattle = OSM(data_seattle)
nodes, edges = osm_seattle.get_network(nodes=True, network_type="driving")
nodes.head()