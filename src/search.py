import osmnx
import requests

def shortest_path(source, target):
    """
    Takes a graph, source address, and target address and returns the shortest
    path from the source address to the target address
    """
    source = osmnx.geocode(source)
    target = osmnx.geocode(target)
    source_y, source_x = source
    target_y, target_x = target
    url = f"http://router.project-osrm.org/route/v1/driving/{source_x},{source_y};{target_x},{target_y}?alternatives=true&steps=true"
    r = requests.get(url)
    res = r.json()
    return res


if __name__ == "__main__":
    print(shortest_path(
        "819, Nob Hill Avenue North, Uptown, Queen Anne, Seattle, King County, Washington, 98109, United States",
        "501, Roy Street, South Lake Union, Belltown, Seattle, King County, Washington, 98109, United States"
    ))
    
    
