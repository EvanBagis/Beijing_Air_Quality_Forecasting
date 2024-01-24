# basic
import os
import warnings
from sklearn.exceptions import ConvergenceWarning
import pickle
import pandas as pd
import requests
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy

from river import preprocessing, linear_model, optim, neighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.multioutput import MultiOutputRegressor
# metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr, spearmanr

# models
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, RANSACRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

from tsmoothie.smoother import LowessSmoother, KalmanSmoother, ConvolutionSmoother, SpectralSmoother

import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=ConvergenceWarning)
warnings.filterwarnings("ignore")

plt.rcParams.update({'font.size': 22})

# Functions

def display_metrics(true, pred, returns=False):
    """Displays or returns the regression metrics.
    ##ARGS:
    
        true:<<list or np.array or pd.series>> the measurements
        
        pred:<<list or np.array or pd.series>> the predictions
        
    ##RETURNS
        
        returns: <<boolean>> specifies if the metrics are to be returned or displayed
    """
    def index_agreement(s, o):
        """
        This function calculates the index of agreement between two arrays.
        It is a measure of the accuracy of a model prediction compared to observed data.
        The function expects two arrays of equal length.
        The function returns a float representing the index of agreement.
        """
        ia = 1 - (np.sum((o - s) ** 2)) / (
            np.sum((np.abs(s - np.mean(o)) + np.abs(o - np.mean(o))) ** 2))
        return ia
    
    rmse = np.sqrt(mean_squared_error(true, pred))
    mae = mean_absolute_error(true, pred)
    r = pearsonr(true, pred)[0]
    rs = spearmanr(true, pred)[0]
    r2 = r2_score(true, pred)
    MBE = np.mean(true-pred)
    ia = index_agreement(pred, true)

    if returns:
        return rmse, mae, r2, r, rs, MBE, ia
    else:
        print(f"RMSE = {rmse:.2f}, MAE = {mae:.2f}, r2 = {r2:.2f}, Pearson = {r:.2f}, Spearman = {rs:.2f}, MBE = {MBE:.2f}, IA = {ia:.2f}")
        return 0

# Transform wind to degrees
def wind_dir(di):
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

# Transform degrees to sinusoidal feature
def transform(angle):
    return np.sin(angle * np.pi / 180)


def recursive_forecast_multistep(data, num_steps, num_lags):
    
    predictions = {i:[] for i in range(num_steps)}; observations = {i:[] for i in range(num_steps)}
    scaler = preprocessing.RobustScaler()
    #model = linear_model.LinearRegression(optimizer=optim.RMSProp(lr=0.01))
    model = neighbors.KNNRegressor(n_neighbors=19,  p=1, window_size=400)
    for i in tqdm(range(0, len(data) - (num_lags + num_steps), num_steps )):
        # Extract training data for the current window
        x = data.iloc[i:i+num_lags]
        x = x.reset_index(drop=True)
        x = x.to_dict()
        y = data.iloc[i+num_lags]
        #print(data.head(23),x,y); break

        # prediction loop
        x_new = deepcopy(x); x_train = []
        for j in range(num_steps):
            
            
            #scaler.learn_one(x_new)
            #x_new = scaler.transform_one(x_new)
            #print(data.iloc[i:i+num_lags+j], x_new, data.iloc[i+num_lags+j])
            x_train.append(x_new)
            y_pred = model.predict_one(x_new)
            
            # collect predictions in a dictionary
            predictions[j].append(round(y_pred))
            
            # create the next instance
            x_new = {k:x_new[k+1] for k in range(len(x_new)-1)}
            x_new[len(x_new)] = round(y_pred)
            
            #print(x_new)
            
        # training loop
        for l, xx in enumerate(x_train):
            #print(data.iloc[i:i+num_steps+l], xx, data.iloc[i+num_steps+l])
            #if l ==0: print('------------------------------------------', y-data.iloc[i+num_lags+l])
            model = model.learn_one(xx, data.iloc[i+num_lags+l])
            #model = model.learn_one(data.iloc[i+l:i+num_lags+l].reset_index(drop=True).to_dict(), data.iloc[i+num_lags+l])
            observations[l].append(data.iloc[i+num_lags+l])
    #print([len(predictions[key]) for key in predictions.keys()])
    #print([len(observations[key]) for key in observations.keys()])
    return predictions, observations


path = '/home/evan/venv/Beijing_Air_Quality_Forecasting/raw_data/'; files = sorted(os.listdir(path))
targets = ['PM2.5', 'O3', 'PM10', 'SO2', 'NO2', 'CO']

# load and concatenate all the files into a single dataframe
dfs = pd.concat([pd.read_csv(path + file, index_col=0) for file in files])

# reconstruct the datetime index
dfs.index = pd.to_datetime(dfs[['year', 'month', 'day', 'hour']])
dfs = dfs.drop(['year', 'month', 'day', 'hour'], axis=1)

# transform wind directions into floats and transform the column
dfs['wd'] = dfs['wd'].apply(wind_dir).apply(transform)
stations = list(dfs['station'].unique())

for target in targets:
    target_by_station = pd.DataFrame()
    for station in stations:
        temp = dfs[dfs['station']==station]
        target_by_station[f"{target}_{station}"] = temp[target]
        
    target_by_station = target_by_station.dropna().reset_index(drop=True)
    
    #print(target_by_station)
    for col in target_by_station.columns:
        predictions, observations = recursive_forecast_multistep(target_by_station[col], 12, 24)
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