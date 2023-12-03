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
            instruction = f"{idx + 1}. Depart from {location}"
        elif type_of_maneuver == 'arrive':
            instruction = f"{idx + 1}. Arrive at {location}"
        else:
            instruction = f"{idx + 1}. {type_of_maneuver} {direction} at {location}"
        directions.append([location, instruction])
        
    return directions

def safe_path(directions):
    # add user input for the rest of the predictor variables
    maximum = (0, 0) # prediction value, directions index
    for idx, direction in enumerate(directions):
        location, _ = direction
        prediction = random_forests.predictor(location)
        if prediction > maximum:
            maximum = (prediction, idx)
        
    _, idx = maximum
    directions[idx][1] += "accident is most likely at this location"
    return directions

    


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
    
    
