
from csv import writer
from random import randint

import pandas as pd
from fastai.tabular.all import *

def process_raw_data(raw_data_file, data_file):
    """
    Saves processed raw data from the given raw csv file to a
    new given csv file and returns a dataframe
    """
    pd.set_option('display.max_columns', None)
    raw_collisions = pd.read_csv(raw_data_file, low_memory=False)
    raw_collisions["accident"] = [1] * 242131
    add_datepart(raw_collisions, 'INCDATE')
    collisions = raw_collisions[COLUMN_NAMES].copy()
    collisions.to_csv(data_file, index=False)
    return collisions

def generate_data(collisions, new_data_file):
    """
    Takes the file names of the raw data file, the data file for the processed data, and the
    data file for the generated data. Then creates the data for the processed data and
    generated data
    """
    write_column_names(new_data_file)
    num = 1

    while num <= 242131 * 3:
        row = build_row(collisions)
        if data_exists(row, collisions):
            continue
        row.to_frame().T.to_csv(new_data_file, header=False, index=False, mode='a')
        num += 1

def write_column_names(new_data_file):
    """Write the datas column names to the given new csv file"""
    with open(new_data_file, 'w') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(COLUMN_NAMES)

def build_row(collisions):
    """Build and return a new randomly generated row from the given collisions file"""
    rand_index_1 = randint(0, len(collisions) - 1)
    row = collisions.iloc[rand_index_1].copy(deep=True)
    rand_index_2 = randint(0, len(collisions) - 1)
    rand_x, rand_y = collisions.iloc[rand_index_2]['X'], collisions.iloc[rand_index_2]['Y']
    row['X'], row['Y'] = rand_x, rand_y
    row['SEVERITYCODE'] = 0
    return row

def data_exists(row, collisions):
    """Check if the given row exists in the given collisions file and return the bool"""
    exists = (
            (collisions['X'] == row['X']) & (collisions['Y'] == row['Y']) &
            (collisions['INCDATEYear'] == row['INCDATEYear']) &
            (collisions['INCDATEMonth'] == row['INCDATEMonth']) &
            (collisions['INCDATEWeek'] == row['INCDATEWeek']) &
            (collisions['INCDATEDay'] == row['INCDATEDay']) &
            (collisions['INCDATEDayofweek'] == row['INCDATEDayofweek']) &
            (collisions['INCDATEDayofyear'] == row['INCDATEDayofyear'])
    ).any()
    return exists

if __name__ == "__main__":
    COLUMN_NAMES = [
        'X', 'Y', 'SEVERITYCODE', 'WEATHER', 'LIGHTCOND',
        'INCDATEYear', 'INCDATEMonth', 'INCDATEWeek',
        'INCDATEDay', 'INCDATEDayofweek', 'INCDATEDayofyear'
    ]
    collisions = process_raw_data("data/raw_collisions.csv", "data/collisions.csv")
    generate_data(collisions, "data/new_collisions.csv")