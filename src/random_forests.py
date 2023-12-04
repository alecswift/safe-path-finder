import joblib
import osmnx
import pandas as pd

WEATHER_NAMES = ['na', 'Blowing Sand/Dirt', 'Blowing Snow', 'Clear', 'Fog/Smog/Smoke', 'Other', 'Overcast', 'Partly Cloudy', 'Raining', 'Severe Crosswind', 'Sleet/Hail/Freezing Rain', 'Snowing', 'Unknown']
LIGHT_COND_NAMES = ['na', 'Dark - No Street Lights', 'Dark - Street Lights Off', 'Dark - Street Lights On', 'Dark - Unknown Lighting', 'Dawn', 'Daylight', 'Dusk', 'Other', 'Unknown']
INDEP_VAR_NAMES = ['WEATHER', 'LIGHTCOND', 'X_na', 'Y_na', 'X', 'Y', 'INCDATEYear',
        'INCDATEMonth', 'INCDATEWeek', 'INCDATEDay', 'INCDATEDayofweek', 'INCDATEDayofyear']



def predictor(data):
    """Predict the accident likelihood from the given independent variables"""
    location, weather, light_cond, day, week, month, year, week_day, year_day = data
    random_forest = joblib.load(
        "/home/alec/Desktop/code/personal_projects/safe-path-finder/src/random_forest.joblib"
    )
    light_cond_dict = {light_cond: idx for idx, light_cond in enumerate(LIGHT_COND_NAMES)}
    weather_dict = {name: idx for idx, name in enumerate(WEATHER_NAMES)}
    x, y = osmnx.geocode(location)
    indep_vars = pd.DataFrame(columns=INDEP_VAR_NAMES)
    indep_vars.loc[len(indep_vars)] = (
        weather_dict[weather], light_cond_dict[light_cond], 1, 1, x, y,
        year, month, week, day, week_day, year_day
    )
    return random_forest.predict(indep_vars)

if __name__ == "__main__":
    print(predictor((
        "8814, 28th Avenue Northwest, North Beach, Seattle, King County, Washington, 98117, United States",
        "Snowing", "Dusk", 1, 1, 1, 2024, 1, 1
    )))