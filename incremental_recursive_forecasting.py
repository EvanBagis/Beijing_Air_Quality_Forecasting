# basic
import os
import re
import warnings
from tqdm import tqdm
import pickle
import pandas as pd
import requests
import numpy as np
from copy import deepcopy

# metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr, spearmanr

# models
from river import preprocessing, linear_model, optim, neighbors, ensemble

# plotting
import seaborn as sns
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

# settings
from sklearn.exceptions import ConvergenceWarning
warnings.simplefilter(action='ignore', category=ConvergenceWarning)
warnings.filterwarnings("ignore")
plt.rcParams.update({'font.size': 22})

# local functions
from utils import *

def recursive_forecast_multistep(data, num_steps, num_lags):
    """
    Perform multistep recursive forecasting using a machine learning model.

    This function takes a time series data (single column) and performs multistep recursive forecasting
    using a machine learning model, such as K-Nearest Neighbors Regressor.

    Parameters:
    - data (pd.DataFrame): Time series data with the target variable.
    - num_steps (int): Number of steps to forecast into the future.
    - num_lags (int): Number of lagged values to consider as features.

    Returns:
    - tuple: Tuple containing dictionaries of predictions and observations.
    """
    # Ensure the index is a DateTimeIndex
    data.index = pd.to_datetime(data.index)

    predictions = {i: [] for i in range(num_steps)}
    observations = {i: [] for i in range(num_steps)}
    predictions_all = []; observations_all = []
    
    # Define the model
    #knn_model = neighbors.KNNRegressor(n_neighbors=9, p=1, window_size=400)
    #model = ensemble.AdaptiveRandomForestRegressor(leaf_model=knn_model, n_models=5, split_confidence=0.001)
    
    model = neighbors.KNNRegressor(n_neighbors=9, p=1, window_size=400)

    # Get start and end dates for the loop
    start_date = data.index[num_lags]
    end_date = data.index[-num_steps]

    for current_date in tqdm(pd.date_range(start=start_date, end=end_date, freq=pd.DateOffset(hours=num_steps))):
        train_start = current_date - pd.DateOffset(hours=num_lags)
        train_end = current_date

        # Extract training data for the current window
        x = data.loc[train_start:train_end].reset_index(drop=True).to_dict()

        # Prediction loop
        x_new = deepcopy(x)
        x_train = []
        for j in range(num_steps):
            x_train.append(x_new)
            #print(x_new)
            y_pred = model.predict_one(x_new)
            
            # Collect predictions
            predictions[j].append(round(y_pred))
            predictions_all.append(round(y_pred))

            # Create the next instance
            x_new = {k: x_new[k + 1] for k in range(len(x_new) - 1)}
            x_new[len(x_new)] = round(y_pred)

        # Training loop
        for l, xx in enumerate(x_train):
            observation_date = current_date + pd.DateOffset(hours=l)
            model = model.learn_one(xx, data.loc[observation_date])
            
            # Collect observations
            observations[l].append(data.loc[observation_date])
            observations_all.append(data.loc[observation_date])

    return predictions, observations, predictions_all, observations_all

# MAIN

# define static parameters for the problem
path = '/home/evan/venv/Beijing_Air_Quality_Forecasting/'
path_data = path + 'raw_data/'; files = sorted(os.listdir(path_data))
targets = ['NO2', 'O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO']
check_and_create_directories(path + "gifs/", targets)

# load and concatenate all the files into a single dataframe
dfs = pd.concat([pd.read_csv(path_data + file, index_col=0) for file in files])

# get the station names
stations = list(dfs['station'].unique())

# reconstruct the datetime index
dfs.index = pd.to_datetime(dfs[['year', 'month', 'day', 'hour']])
dfs = dfs.drop(['year', 'month', 'day', 'hour'], axis=1)

# transform wind directions into floats and transform the column
dfs['wd'] = dfs['wd'].apply(wind_dir).apply(transform)

# run forecasting for all the pollutant species
for target in targets:
    #print(target)
    
    # collect the target time series for each station
    target_by_station = pd.DataFrame()
    for station in stations:
        temp = dfs[dfs['station']==station]
        target_by_station[f"{target}_{station}"] = temp[target]
    
    # initialize the results df for every horizon
    results_df = pd.DataFrame(columns=["RMSE", "MAE", "r2", "Pearson", "Spearman", "MBE", "IA"])
    # results and plotting
    for i, col in enumerate(target_by_station.columns):
        print(col)
        predictions, observations, predictions_all, observations_all = recursive_forecast_multistep(target_by_station[col].fillna(method='ffill').dropna(), 12, 24) # .reset_index(drop=True)
        rmse, mae, r2, r, rs, MBE, ia = display_metrics(np.array(observations_all), np.array(predictions_all), returns=True)
        
        predictions = pd.DataFrame(predictions); observations = pd.DataFrame(observations)
        if i == 0: make_forecast_video(target, col, observations, predictions, path, 'incremental recursive')
        results_df.loc[col,:] = rmse, mae, r2, r, rs, MBE, ia

    print(results_df)
    # Define the title to search for
    title_to_find = f'{target} Forecasting (incremental recursive)'

    # Open the existing Markdown file and read its content
    markdown_file_path = path + 'README.md'
    with open(markdown_file_path, 'r') as f:
        lines = f.readlines()

    # Find the line number containing the title
    title_line_index = next((i for i, line in enumerate(lines) if title_to_find in line), None)

    if title_line_index is not None:
        # Insert the DataFrame in Markdown format after the title line
        lines.insert(title_line_index + 1, '\n' + '<div align="center"> \n\n' + results_df.to_markdown() + '\n\n' + '</div> \n\n')
        lines.insert(title_line_index + 2, f'![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/{target}/station={target}_Aotizhongxin.gif)')
        # Write the updated content back to the Markdown file
        with open(markdown_file_path, 'w') as f:
            f.writelines(lines)