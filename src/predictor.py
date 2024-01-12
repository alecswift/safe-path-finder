import osmnx

from datetime import date
import random_forests

def get_accident_prediction(address, weather, light_cond):
    """
    Takes a graph, source address, and target address and returns the shortest
    path from the source address to the target address
    """
    #location = osmnx.geocode(address)
    prediction = random_forests.predictor((address, weather, light_cond, *get_date()))
    return prediction

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
    prediction = get_accident_prediction(
        "3902, Densmore Avenue North, Wallingford, Seattle, King County, Washington, 98103, United States",
        "Clear",
        "Dawn"
        )
    print(prediction)

