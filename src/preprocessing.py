
from csv import writer
from random import randint
import time

import pandas as pd
from fastai.tabular.all import *

def generate_data(raw_data_file, data_file, new_data_file):
    """
    Takes the file names of the raw data file, the data file for the processed data, and the
    data file for the generated data. Then creates the data for the processed data and
    generated data
    """
    pd.set_option('display.max_columns', None)
    raw_collisions = pd.read_csv(raw_data_file, low_memory=False)
    raw_collisions["accident"] = [1] * 242131
    add_datepart(raw_collisions, 'INCDATE')

    column_names = [
        'X', 'Y', 'SEVERITYCODE', 'WEATHER', 'LIGHTCOND',
        'INCDATEYear', 'INCDATEMonth', 'INCDATEWeek',
        'INCDATEDay', 'INCDATEDayofweek', 'INCDATEDayofyear'
    ]
    collisions = raw_collisions[column_names].copy()
    collisions.to_csv(data_file, index=False)

    with open(new_data_file, 'w') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(column_names)

    num = 1
    start = time.perf_counter()

    while num <= 242131 * 3:
        if num % 10000 == 0:
            end = time.perf_counter()
            print(num/(242131 * 3)*100, '%', end - start)
            start = end
        rand_index_1 = randint(0, len(collisions) - 1)
        row = collisions.iloc[rand_index_1].copy(deep=True)
        rand_index_2 = randint(0, len(collisions) - 1)
        rand_x, rand_y = collisions.iloc[rand_index_2]['X'], collisions.iloc[rand_index_2]['Y']
        row['X'], row['Y'] = rand_x, rand_y
        row['SEVERITYCODE'] = 0
        exists = (
            (collisions['X'] == row['X']) &
            (collisions['Y'] == row['Y']) &
            (collisions['INCDATEYear'] == row['INCDATEYear']) &
            (collisions['INCDATEMonth'] == row['INCDATEMonth']) &
            (collisions['INCDATEWeek'] == row['INCDATEWeek']) &
            (collisions['INCDATEDay'] == row['INCDATEDay']) &
            (collisions['INCDATEDayofweek'] == row['INCDATEDayofweek']) &
            (collisions['INCDATEDayofyear'] == row['INCDATEDayofyear'])
        ).any()
        if exists:
            continue
        row.to_frame().T.to_csv(new_data_file, header=False, index=False, mode='a')
        num += 1
