import osmnx
import requests

import random_forests

def shortest_path(source, target):
    """
    Takes a graph, source address, and target address and returns the shortest
    path from the source address to the target address
    """
    source = osmnx.geocode(source)
    target = osmnx.geocode(target)
    source_y, source_x = source
    target_y, target_x = target
    url = f"http://router.project-osrm.org/route/v1/driving/{source_x},{source_y};{target_x},{target_y}?alternatives=true&steps=true&continue_straight=true"
    r = requests.get(url)
    res = r.json()
    return res

def get_directions(routes):
    directions = []
    # loop this for every leg of journey?
    for idx, step in enumerate(routes['routes'][0]['legs'][0]['steps']):
        type_of_maneuver = step['maneuver']['type']
        location = step['name']
        direction = step['maneuver']['modifier']
        if type_of_maneuver == 'depart':
            directions.append(f"{idx + 1}. Depart from {location}")
        elif type_of_maneuver == 'arrive':
            directions.append(f"{idx + 1}. Arrive at {location}")
        else:
            directions.append(f"{idx + 1}. {type_of_maneuver} {direction} at {location}")
    return directions

def safe_path(directions):
    # change directions to return actual location
    # add user input for the rest of the predictor variables
    # find the maximum accident risk node
    # add a string caution warning for the maximum accident risk node
    maximum = (0, 0) # prediction value, directions index
    for node in directions:
        pass


def valid_address(address):
    return True

if __name__ == "__main__":
    routes = shortest_path(
        "819, Nob Hill Avenue North, Uptown, Queen Anne, Seattle, King County, Washington, 98109, United States",
        "501, Roy Street, South Lake Union, Belltown, Seattle, King County, Washington, 98109, United States"
    )
    print(get_directions(routes))
    
        

    # format of directions
    # start at source
    # turn right/left onto x
    # so on
    # end at desination
    
    
