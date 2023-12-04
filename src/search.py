import osmnx
import requests

from datetime import date, datetime
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
    url = (
        f"http://router.project-osrm.org/route/v1/driving/{source_x},"
        f"{source_y};{target_x},{target_y}?alternatives=true&steps=true"
        f"&continue_straight=true"
    )
    r = requests.get(url)
    res = r.json()
    return res

def get_directions(routes):
    """Returns a list of directions from the given routes"""
    directions = []
    # loop this for every leg of journey?
    for idx, step in enumerate(routes['routes'][0]['legs'][0]['steps']):
        location, instruction = build_instruction(step, idx)
        directions.append([location, instruction])
        
    return directions

def build_instruction(step, idx):
    """
    Returns the location and instruction for the given
    direction step and index
    """
    type_of_maneuver = step['maneuver']['type']
    location = step['name']
    direction = step['maneuver']['modifier']
    if type_of_maneuver == 'depart':
        instruction = f"{idx + 1}. Depart from {location}"
    elif type_of_maneuver == 'arrive':
        instruction = f"{idx + 1}. Arrive at {location}"
    else:
        instruction = f"{idx + 1}. {type_of_maneuver} {direction} at {location}"
    return location, instruction

def get_safe_path(directions, weather, light_cond):
    """Returns a safe path string from the given directions, weather, and light condition"""
    maximum = (0, 0) # prediction value, directions index
    for idx, direction in enumerate(directions):
        location, _ = direction
        prediction = random_forests.predictor((location, weather, light_cond, *get_date()))
        if prediction > maximum[0]:
            maximum = (prediction, idx)
        
    _, idx = maximum
    directions[idx][1] += " - accident is most likely at this location"
    return "\n".join(instruction for _, instruction in directions)

def get_date():
    """Returns information about the current date"""
    today = date.today()
    week_day = today.timetuple()[6]
    year_day = today.timetuple()[7]
    week = today.isocalendar()[1]
    return today.day, week, today.month, today.year, week_day, year_day

def valid_address(address):
    """Returns a bool for whether or not the given address string is valid"""
    return True

if __name__ == "__main__":
    routes = shortest_path(
        "819, Nob Hill Avenue North, Uptown, Queen Anne, Seattle, King County, Washington, 98109, United States",
        "501, Roy Street, South Lake Union, Belltown, Seattle, King County, Washington, 98109, United States"
    )
    directions = get_directions(routes)
    print(get_safe_path(directions, "Clear", "Dawn"))

