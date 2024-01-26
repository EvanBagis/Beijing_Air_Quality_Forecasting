# basic
import os
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
    return predictions, observations

# read the file names and set the targets
path = '/home/evan/venv/Beijing_Air_Quality_Forecasting/raw_data/'; files = sorted(os.listdir(path))
targets = ['O3', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO']

# load and concatenate all the files into a single dataframe
dfs = pd.concat([pd.read_csv(path + file, index_col=0) for file in files])

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
    
    # results and plotting
    for col in target_by_station.columns[:5]:
        print(col)
        predictions, observations = recursive_forecast_multistep(target_by_station[col].fillna(method='ffill').reset_index(drop=True), 12, 24)
        #print(predictions.keys(), observations.keys())
        for key in predictions.keys():
            display_metrics(np.array(observations[key]), np.array(predictions[key]))
            #plt.figure(figsize=(10, 6))
            #plt.plot(observations[key], label='Original')
            #plt.plot(predictions[key], linestyle='--', color='orange')
            #plt.xlabel('Index')
            #plt.ylabel('Target Variable')
            #plt.legend()
            #plt.title('Recursive Forecasting with Linear Regression (pd.Series)')
            #plt.show()
            #plt.close('all')
            #break
        #break