import joblib
from fastai.tabular.all import *
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def organize_data(collisions_file, new_collisions_file):
    """
    Takes the file name for the collisions file and the new collisions file,
    combines and makes final edits of the data, and loads the data into a 
    tabular panda for use in the machine learning model
    """
    collisions = pd.read_csv(collisions_file, low_memory=False)
    collisions["SEVERITYCODE"] = 1
    no_collision = pd.read_csv(new_collisions_file, low_memory=False)

    combined = pd.concat([collisions, no_collision], ignore_index=True)
    combined = combined.sample(frac = 1)

    dep_var = 'SEVERITYCODE'
    continuous, categorical = cont_cat_split(combined, 1, dep_var=dep_var)
    procs = (Categorify, FillMissing)

    time_condition = combined.INCDATEYear<2019
    train_idx = np.where(time_condition)[0]
    valid_idx = np.where(~time_condition)[0]
    splits = (list(train_idx),list(valid_idx))

    organized_data = TabularPandas(combined, procs, categorical, continuous, y_names=dep_var, splits=splits)

    return organized_data

def random_forest(data, file_name):
    """Saves the random forest generated from the data to the file name"""
    indep_vars, dep_vars = data.train.xs, data.train.y

    random_forest = RandomForestRegressor(n_jobs=-1, n_estimators=50,
        max_samples=200000, max_features=0.5,
        min_samples_leaf=20, oob_score=True)
    random_forest.fit(indep_vars, dep_vars)

    joblib.dump(random_forest, file_name)

def predictor()

if __name__ == "__main__":
    data = organize_data(
        "/home/alec/Desktop/code/personal_projects/safe-path-finder/data/collisions.csv",
        "/home/alec/Desktop/code/personal_projects/safe-path-finder/data/new_collisions.csv"
    )
    random_forest(data, "/home/alec/Desktop/code/personal_projects/safe-path-finder/src/random_forest.joblib")