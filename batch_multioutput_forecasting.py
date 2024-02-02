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

from river import preprocessing
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

# local functions
from utils import *


# Create more features
def feature_engineering(data, lags, window_sizes):
    """
    Perform feature engineering on a Pandas DataFrame by calculating rolling statistics
    and creating lag features.

    ## ARGS:
    - data (pd.DataFrame): Input DataFrame containing the original data.
    - lags (int): Number of lag features to create for each column in the DataFrame.
    - window_sizes (list of int): List of window sizes for calculating rolling statistics.

    ## RETURNS:
    - If returns is True, returns a new DataFrame with added features.
    - If returns is False, modifies the input DataFrame in place.

    Example:
    >>> new_data = feature_engineering(df, 12, [24, 48])

    Notes:
    - This function creates various rolling statistics (mean, std, min, max, median,
      min-max difference) for each column in the input DataFrame based on the specified
      window sizes.
    - It also generates lag features for each column up to the specified number of lags.
    - The resulting DataFrame may contain NaN values for rows where features could not
      be calculated due to insufficient historical data or lag values.
    - If returns is set to True, the function returns a new DataFrame with added features.
      If returns is set to False, the function modifies the input DataFrame in place.
    """

    # create denoised features with rolling statistical moments
    data2 = data.copy()
    for col in data.columns:
        for window in window_sizes:
            data2["rolling_mean_" + col + '-' + str(window)] = data[col].rolling(window=window).mean()
            data2["rolling_std_" + col + '-' + str(window)] = data[col].rolling(window=window).std()
            data2["rolling_min_" + col + '-' + str(window)] = data[col].rolling(window=window).min()
            data2["rolling_max_" + col + '-' + str(window)] = data[col].rolling(window=window).max()
            data2["rolling_median_" + col + '-' + str(window)] = data[col].rolling(window=window).median()
            data2["rolling_min_max_diff_" + col + '-' + str(window)] = data2["rolling_max_" + col + '-' + str(window)] - \
                                                                       data2["rolling_min_" + col + '-' + str(window)]
    # create lag features
    cols = data.columns.to_list()

    for col in cols:
        for i in range(1, lags):
            data2[f'{col}_lag_{i}'] = data[col].shift(i)
    return data2.dropna()

# MAIN

future = 12; num_feats = 12
path = '/home/evan/venv/Beijing_Air_Quality_Forecasting/raw_data/'; files = sorted(os.listdir(path))
targets = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# load and concatenate all the files into a single dataframe
dfs = pd.concat([pd.read_csv(path + file, index_col=0) for file in files])

# reconstruct the datetime index
dfs.index = pd.to_datetime(dfs[['year', 'month', 'day', 'hour']])
dfs = dfs.drop(['year', 'month', 'day', 'hour'], axis=1)

# transform wind directions into floats and transform the column
dfs['wd'] = dfs['wd'].apply(wind_dir).apply(transform)
stations = list(dfs['station'].unique())

for target in targets:
    print(target)
    target_by_station = pd.DataFrame()
    for station in stations:
        temp = dfs[dfs['station']==station]
        target_by_station[f"{target}_{station}"] = temp[target]
        
    target_by_station = target_by_station.fillna(method='ffill').dropna().reset_index(drop=True)
    
    x = []; y = []
    for i in range(len(target_by_station)-num_feats-future):
        x.append(np.ravel(np.array(target_by_station.iloc[i:i+num_feats, :])))
        y.append(np.ravel(np.array(target_by_station.iloc[i+num_feats:i+num_feats+future, :])))
    
    x = np.stack(x); y = np.stack(y)
    
    scaler = StandardScaler()
    split = int(0.5*x.shape[0])
    x_train = x[:split,:]
    #y_train_raw = raw_y[:split,:]
    y_train = y[:split,:]
    x_test = x[split:,:]    
    y_test = y[split:,:]
    
    model1 = LassoLars(alpha=0.001)#Lasso(alpha=0.0001)
    model2 = MLPRegressor()
    model3 = RandomForestRegressor(n_estimators=100, n_jobs=-1)
    model4 = XGBRegressor(n_estimators = 50, objective='reg:squarederror', n_jobs=-1)
    model5 = LGBMRegressor(n_estimators = 5, n_jobs=-1, verbose=-1)
    

    preds = []# "LR":model1, "MLP":model2, "RF":model3, "XGB":model4
    models = {"RF":model3}
    for model in tqdm(models.keys()):
        
        #x_train = scaler.fit_transform(x_train)
        #x_test = scaler.transform(x_test)
        
        if model == 'LGB': models[model] = MultiOutputRegressor(models[model])
        models[model].fit(x_train, y_train)
        #with open(models_path + f"{model}_{y_train}.sav", "wb") as f:
        #    pickle.dump(models[model], f)

        p = models[model].predict(x_test).reshape(y_test.shape[0],future,len(stations))
        preds.append(p)

    y_pred = np.stack(preds).mean(axis=0)
    y_test = np.array(y_test).reshape(y_test.shape[0],future,len(stations))

    # plot preds by hour (optional) * display performance metrics
    for j in range(len(stations)):
        for i in range(future):
            p = y_pred[:,i,j]
            t = y_test[:,i,j]
            display_metrics(t, p)
        p_gif = pd.DataFrame(y_pred[:,:,j])
        t_gif = pd.DataFrame(y_test[:,:,j])
        print(p_gif.shape, t_gif.shape)
        if j == 0: make_forecast_video(target, stations[j], t_gif, p_gif, path, 'batch multioutput')
    

