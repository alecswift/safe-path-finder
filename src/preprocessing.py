
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

def organize_data(collisions_file, new_collisions_file):
    """
    Takes the file name for the collisions file and the new collisions file,
    combines and makes final edits of the data, and loads the data into a 
    tabular panda for use in the machine learning model
    """
    combined = combine_collisions(collisions_file, new_collisions_file)
    dep_var = 'SEVERITYCODE'
    continuous, categorical = cont_cat_split(combined, 1, dep_var=dep_var)
    procs = (Categorify, FillMissing)
    time_condition = combined.INCDATEYear<2019
    train_idx, valid_idx = np.where(time_condition)[0], np.where(~time_condition)[0] 
    splits = (list(train_idx),list(valid_idx))
    organized_data = TabularPandas(
        combined, procs, categorical, continuous, y_names=dep_var, splits=splits
    )
    return organized_data

def combine_collisions(collisions_file, new_collisions_file):
    """Combine the collisions file and new collisions file and return the combined dataframe"""
    collisions = pd.read_csv(collisions_file, low_memory=False)
    collisions["SEVERITYCODE"] = 1
    no_collision = pd.read_csv(new_collisions_file, low_memory=False)

    combined = pd.concat([collisions, no_collision], ignore_index=True)
    combined = combined.sample(frac = 1)
    return combined

def random_forest_builder(data, file_name):
    """Saves the random forest generated from the data to the file name"""
    indep_vars, dep_vars = data.train.xs, data.train.y

    random_forest = RandomForestRegressor(n_jobs=-1, n_estimators=50,
        max_samples=200000, max_features=0.5,
        min_samples_leaf=20, oob_score=True)
    random_forest.fit(indep_vars, dep_vars)

    joblib.dump(random_forest, file_name)

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