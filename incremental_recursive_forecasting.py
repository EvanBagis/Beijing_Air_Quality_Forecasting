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
from river import preprocessing, linear_model, optim, neighbors

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

# Functions
def check_and_create_directories(parent_directory, directory_list):
    """
    Checks if directories from a list exist within a parent directory,
    and creates them if they don't exist.

    Parameters:
    - parent_directory (str): The name of the parent directory where the directories will be created.
    - directory_list (list): A list containing the names of directories to be created within the parent_directory.

    Returns:
    - None
    """
    for directory_name in directory_list:
        new_directory = os.path.join(parent_directory, directory_name)

        # Check if the directory exists
        if os.path.exists(new_directory) and os.path.isdir(new_directory):
            pass # print(f"The directory '{directory_name}' already exists in '{parent_directory}'.")
        else:
             os.makedirs(new_directory)

def display_metrics(true, pred, returns=False):
    """
    Calculate and display or return regression metrics.

    Parameters:
    - true (array-like): True values.
    - pred (array-like): Predicted values.
    - returns (bool): Whether to return the metrics or display them (default: False).

    Returns:
    - tuple or int: Tuple of regression metrics if returns is True, 0 otherwise.
    """
    
    def index_of_agreement(observed, predicted):
        """
        Calculate the Index of Agreement (IA) between two continuous variables.

        Parameters:
        - observed (array-like): Observed values.
        - predicted (array-like): Predicted values.

        Returns:
        - float: Index of Agreement value.
        """
        observed = np.array(observed)
        predicted = np.array(predicted)

        mean_observed = np.mean(observed)

        numerator = np.sum((observed - predicted) ** 2)
        denominator = np.sum((np.abs(predicted - mean_observed) + np.abs(observed - mean_observed)) ** 2)

        ia = 1 - (numerator / denominator)
        return ia
    
    rmse = np.sqrt(mean_squared_error(true, pred))
    mae = mean_absolute_error(true, pred)
    r = pearsonr(true, pred)[0]
    rs = spearmanr(true, pred)[0]
    r2 = r2_score(true, pred)
    MBE = np.mean(true-pred)
    ia = index_of_agreement(true, pred)

    if returns:
        return rmse, mae, r2, r, rs, MBE, ia
    else:
        print(f"RMSE = {rmse:.2f}, MAE = {mae:.2f}, r2 = {r2:.2f}, Pearson = {r:.2f}, Spearman = {rs:.2f}, MBE = {MBE:.2f} , IA = {ia:.2f}")

def wind_dir(di):
    """
    Convert wind direction from cardinal direction to degrees.

    This function takes a wind direction specified in cardinal direction
    (e.g., 'N', 'NNE', 'NE', etc.) and converts it to degrees.

    Parameters:
    - di (str): Wind direction in cardinal direction format.

    Returns:
    - float: Wind direction in degrees.
    
    Example:
    >>> wind_dir('N')
    0.0
    """
    if di == 'N':
        di = 0
    elif di == 'NNE':
        di = 22.5
    elif di == 'NE':
        di = 45
    elif di == 'ENE':
        di = 67.5
    elif di == 'E':
        di = 90
    elif di == 'ESE':
        di = 112.5
    elif di == 'SE':
        di = 135
    elif di == 'SSE':
        di = 157.5
    elif di == 'S':
        di = 180
    elif di == 'SSW':
        di = 202.5
    elif di == 'SW':
        di = 225
    elif di == 'WSW':
        di = 247.5
    elif di == 'W':
        di = 270
    elif di == 'WNW':
        di = 292.5
    elif di == 'NW':
        di = 315
    elif di == 'NNW':
        di = 337.5
    return di

def transform(angle):
    """
    Transform an angle from degrees to sine value.

    This function takes an angle in degrees and returns the sine value of the angle.

    Parameters:
    - angle (float): Angle in degrees.

    Returns:
    - float: Sine value of the angle.

    Example:
    >>> transform(90)
    1.0
    """
    return np.sin(angle * np.pi / 180)

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
    model = neighbors.KNNRegressor(n_neighbors=19, p=1, window_size=400)

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
            #print(train_start, train_end, observation_date)
            model = model.learn_one(xx, data.loc[observation_date])
            
            # Collect observations
            observations[l].append(data.loc[observation_date])
            observations_all.append(data.loc[observation_date])

    return predictions, observations, predictions_all, observations_all

'''def recursive_forecast_multistep(data, num_steps, num_lags):
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
        The first dictionary contains predictions for each step, and
        the second dictionary contains corresponding observed values.

    Example:
    >>> predictions, observations = recursive_forecast_multistep(data, 12, 24)
    """
    # initialize empty dictionaries to collect the predictions and the observations
    predictions = {i:[] for i in range(num_steps)}; observations = {i:[] for i in range(num_steps)}
    
    # define scaler
    #scaler = preprocessing.StandardScaler()
    
    # define the model
    #model = linear_model.LinearRegression(optimizer=optim.RMSProp(lr=0.001))
    model = neighbors.KNNRegressor(n_neighbors=19,  p=1, window_size=400)
    
    # loop that runs every "num_steps", equivalent to forward cross validation with gap=num_steps
    for i in tqdm(range(0, len(data) - (num_lags + num_steps), num_steps )):
        
        # Extract training data for the current window
        x = data.iloc[i:i+num_lags].reset_index(drop=True).to_dict()
        # y = data.iloc[i+num_lags]      # ----debuging---
        #print(data.head(23),x,y); break # ----debuging---

        # prediction loop
        x_new = deepcopy(x); x_train = []
        for j in range(num_steps):
            
            # scaling, ---removed because it hurts the metrics---
            #scaler.learn_one(x_new)
            #x_new = scaler.transform_one(x_new)
            
            #print(data.iloc[i:i+num_lags+j], x_new, data.iloc[i+num_lags+j]) # ----debuging---
            x_train.append(x_new)
            y_pred = model.predict_one(x_new)
            
            # collect predictions in a dictionary
            predictions[j].append(round(y_pred)) # round to match the observations
            
            # create the next instance
            x_new = {k:x_new[k+1] for k in range(len(x_new)-1)}
            x_new[len(x_new)] = round(y_pred) # round to match the observations
            
        # training loop
        for l, xx in enumerate(x_train):
            #print(data.iloc[i:i+num_steps+l], xx, data.iloc[i+num_steps+l])   # ----debuging---
            
            # learn from the model predictions (refering to inputs)
            model = model.learn_one(xx, data.iloc[i+num_lags+l])
            
            # learn from observations (refering to inputs)
            #model = model.learn_one(data.iloc[i+l:i+num_lags+l].reset_index(drop=True).to_dict(), data.iloc[i+num_lags+l])
            
            # collect observations in a dictionary
            observations[l].append(data.iloc[i+num_lags+l])
    #print([len(predictions[key]) for key in predictions.keys()])     # ----debuging---
    #print([len(observations[key]) for key in observations.keys()])   # ----debuging---
    return predictions, observations'''

def make_forecast_video(target, n_station, y_test, y_pred, path):
    '''
    note:total number of frames = duration*fps
    y_test: numpy array
    y_pred: numpy array
    '''
    duration = 12
    tqdm._instances.clear()
    
    yy_pred = y_pred.iteritems()
    yy_test = y_test.iteritems()
    
    fig, ax = plt.subplots(figsize=(20, 5))
    
    #right_side = ax.spines["right"]; right_side.set_visible(False)
    #upper_side = ax.spines["top"]; upper_side.set_visible(False)
    def make_frame(t):
        #print(t)
        #print(next(yy_test))
        ax.clear()
        # element 1 because next return tuple (i, row(i))
        #print(y_test.iloc[:,int(t)])
        tt = (t, y_test.iloc[:,int(t)]); p = (t, y_pred.iloc[:,int(t)])
        #print(tt, p)
        ax.plot(tt[1], linewidth=2)
        ax.plot(p[1], linewidth=2, color="r")
        plt.legend(["Observations", "Predictions"], loc="upper left")
        rmse, mae, r2, r, rs, MBE, ia = display_metrics(tt[1], p[1], returns=True)
        plt.title(f"Forecast of hour {tt[0]+1}\n (RMSE = {rmse:.2f}, MAE = {mae:.2f}, r2 = {r2:.2f}\n Pearson = {r:.2f}, Spearman = {rs:.2f}\n MBE = {MBE:.2f} , IA = {ia:.2f})")
        #plt.text(tt[1].shape[0]-200, tt[1].mean(), display_metrics(tt[1], p[1], returns=True))
        plt.tight_layout()
        plt.box("off")
        return mplfig_to_npimage(fig)

    animation = VideoClip(make_frame, duration=duration)
    animation.write_gif(path + f"/gifs/{target}/station={n_station}.gif", fps=1)
    #animation.ipython_display(fps=30, loop=False, autoplay=True, maxduration=12000)




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
        if i == 0: make_forecast_video(target, col, observations, predictions, path)
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
        # Write the updated content back to the Markdown file
        with open(markdown_file_path, 'w') as f:
            f.writelines(lines)