
from csv import writer
from random import randint
import time

import numpy as np
import pandas as pd
from fastai.tabular.all import *


# First import pandas to help us work with the collision data excel file.


pd.set_option('display.max_columns', None)
raw_collisions = pd.read_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/raw_collisions.csv", low_memory=False)
raw_collisions["accident"] = [1] * 242131
add_datepart(raw_collisions, 'INCDATE')


# Here we read our collisions data file into the program as a DataFrame. We set the pandas options to display the max columns so pandas doesn't hide any of the columns when we display the DataFrame. The low memory, False key value pair also ensures the displayed DataFrame doesn't hide any data. Additionally, we add a column for our dependant variable, accident, whether or not there was an accident. Some important columns to look at for the machine learning model are location: ('X', 'Y'), time: 'INCDATE', weather: 'WEATHER', and light conditions: 'LIGHTCOND'. Finally, we'll use the fastai function add_datepart to split up our date column to change the data from categorical to numerical. 

column_names = [
    'X', 'Y', 'SEVERITYCODE', 'WEATHER', 'LIGHTCOND',
    'INCDATEYear', 'INCDATEMonth', 'INCDATEWeek',
    'INCDATEDay', 'INCDATEDayofweek', 'INCDATEDayofyear'
]
collisions = raw_collisions[column_names].copy()
collisions.to_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/collisions.csv", index=False)

with open('/home/alec/Desktop/code/personal_projects/safe-path-finder/data/new_collisions.csv', 'w') as csv_file:
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
    row.to_frame().T.to_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/new_collisions.csv", header=False, index=False, mode='a')
    num += 1
