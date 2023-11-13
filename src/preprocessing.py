
from random import randint

import numpy as np
import pandas as pd
from fastai.tabular.all import *

# First import pandas to help us work with the collision data excel file.


pd.set_option('display.max_columns', None)
raw_collisions = pd.read_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/raw_collisions.csv", low_memory=False)
raw_collisions["accident"] = [1] * 242131
add_datepart(raw_collisions, 'INCDATE')


# Here we read our collisions data file into the program as a DataFrame. We set the pandas options to display the max columns so pandas doesn't hide any of the columns when we display the DataFrame. The low memory, False key value pair also ensures the displayed DataFrame doesn't hide any data. Additionally, we add a column for our dependant variable, accident, whether or not there was an accident. Some important columns to look at for the machine learning model are location: ('X', 'Y'), time: 'INCDATE', weather: 'WEATHER', and light conditions: 'LIGHTCOND'. Finally, we'll use the fastai function add_datepart to split up our date column to change the data from categorical to numerical. 


collisions = raw_collisions[[
    'X', 'Y', 'SEVERITYCODE', 'WEATHER', 'LIGHTCOND',
    'INCDATEYear', 'INCDATEMonth', 'INCDATEWeek',
    'INCDATEDay', 'INCDATEDayofweek', 'INCDATEDayofyear'
]].copy()


# As this is the first iteration of the machine learning model I will drop columns are not significant factors. Note that it's difficult to decide whether or not a factor is significant. However, for simplicity the columns I will keep are: the location in coordinates, the date columns, the weather, and the light conditions.



dep_var = 'SEVERITYCODE'
# If i want to use root mean squared log error (RMSLE) as the metric for
# the dependant variable than I'll need to take the log of the column
continuous, categorical = cont_cat_split(collisions)
procs = (Categorify, FillMissing)
tp_collisions = TabularPandas(collisions, procs, categorical, continuous, y_names=dep_var)
tp_collisions['SEVERITYCODE'] += 1
# tp_collisions.items.to_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/collisions.csv")
collisions = tp_collisions.items


# I'll possibly need to define splits later (training set and validation set) Probably random splits

# Categorify and FillMissing are TabularProcs. These transform data in place by replacing categorical data with numerical data and replacing missing values with the median of the column respectively. Fill missing also adds a boolean column to indicate replaced rows. I add one to all of the data points in the severity code column as 0 will indicate no accident once I generate the fake data. Finally I save this data to a file in the last line of code that is commented out.

new_collisions = pd.DataFrame(columns=collisions.columns)
num = 1
while num <= 242131 * 3:
    if num % 10000 == 0:
        print(num/(242131 * 3)*100, '%')
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
    new_collisions = pd.concat([new_collisions, row.to_frame().T], ignore_index=True)
    num += 1

new_collisions.to_csv("/home/alec/Desktop/code/personal_projects/safe-path-finder/data/new_collisions.csv")
