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

def make_forecast_video(n_station, y_test, y_pred):
    '''
    note:total number of frames = duration*fps
    y_test: numpy array
    y_pred: numpy array
    '''
    duration = 12
    tqdm._instances.clear()
    
    yy_pred = pd.DataFrame(y_pred[:,:,n_station]).iteritems()
    yy_test = pd.DataFrame(y_test[:,:,n_station]).iteritems()
    
    fig, ax = plt.subplots(figsize=(20, 5))
    
    #right_side = ax.spines["right"]; right_side.set_visible(False)
    #upper_side = ax.spines["top"]; upper_side.set_visible(False)
    def make_frame(t):
        #print(t)
        #print(next(yy_test))
        ax.clear()
        # element 1 because next return tuple (i, row(i))
        tt = (t, y_test[:,int(t),n_station]); p = (t, y_pred[:,int(t),n_station])
        #print(tt, p)
        ax.plot(tt[1], linewidth=2)
        ax.plot(p[1], linewidth=2, color="r")
        plt.legend(["Observations", "Predictions"], loc="upper left")
        plt.title(f"Forecast of hour {tt[0]+1} ({display_metrics(tt[1], p[1], returns=True)})")
        #plt.text(tt[1].shape[0]-200, tt[1].mean(), display_metrics(tt[1], p[1], returns=True))
        plt.tight_layout()
        plt.box("off")
        return mplfig_to_npimage(fig)

    animation = VideoClip(make_frame, duration=duration)
    animation.write_gif(results_path + f"{target}/station={n_station}.gif", fps=1)
    #animation.ipython_display(fps=30, loop=False, autoplay=True, maxduration=12000)


    
def denoise(series, sm):
    if sm == "conv":
        smoother = ConvolutionSmoother(window_len=20, window_type='ones')
        a = smoother.smooth(series); b = np.squeeze(a.smooth_data)
    elif sm == "kalman":
        smoother = KalmanSmoother(component='level', component_noise={'level':0.01})
        a = smoother.smooth(series); b = np.squeeze(a.smooth_data)
    elif sm == "spectral":
        smoother = SpectralSmoother(smooth_fraction=0.1, pad_len=1)
        a = smoother.smooth(series)
        #b = np.array(list(np.squeeze(a.smooth_data)) + [0])
        b = np.squeeze(a.smooth_data)

    return b

def scale(df):
    return (df-np.min(df))/(np.max(df)-np.min(df))

def diurnal(df, days):
    
    result = []
    for i in range(len(df) - 24*days):
        temp = df.iloc[i:i+24*days,:]
        h = temp.index[-1].hour
        result.append(temp.groupby(temp.index.hour).mean().loc[h,:])

    b = pd.DataFrame(result); b.columns = b.columns + '_diurnal'
    return b

def create_x_y_raw(path, enf_target, n_stations, future, num_feats, sm):
    
    enf_data = pd.read_csv(path+enf_target, index_col=0)
    enf_data.index = pd.DatetimeIndex([pd.to_datetime(item) for item in enf_data.index])
    enf_data2 = enf_data[enf_data<200].iloc[:,:n_stations].dropna()
    enf_data = [pd.Series(denoise(enf_data2[col], sm), name=col) for col in enf_data2.columns]
    enf_data = pd.concat(enf_data, axis=1)
    #enf_data.index = enf_data2.index
    
    #days = 30
    #enf_diurnal = diurnal(enf_data2, days)
    #enf_data3 = pd.concat([enf_data.iloc[days*24:,:].reset_index(drop=True), enf_diurnal.reset_index(drop=True)], axis=1)

    #enf_data2 = enf_data2.iloc[days*24:,:].reset_index(drop=True)
    target = enf_data.reset_index(drop=True)
    x = []; y = []; raw_y = []
    for i in range(len(target)-num_feats-future):
        x.append(np.ravel(np.array(target.iloc[i:i+num_feats, :])))
        y.append(np.ravel(np.array(target.iloc[i+num_feats:i+num_feats+future, :n_stations])))
        raw_y.append(np.ravel(np.array(enf_data2.iloc[i+num_feats:i+num_feats+future, :])))
    
    x = np.stack(x); y = np.stack(y); raw_y = np.stack(raw_y)
    return x, y, raw_y

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
    target_by_station = pd.DataFrame()
    for station in stations:
        temp = dfs[dfs['station']==station]
        target_by_station[f"{target}_{station}"] = temp[target]
        
    target_by_station = target_by_station.dropna().reset_index(drop=True)
    
    x = []; y = []; raw_y = []
    for i in range(len(target_by_station)-num_feats-future):
        x.append(np.ravel(np.array(target_by_station.iloc[i:i+num_feats, :])))
        y.append(np.ravel(np.array(target_by_station.iloc[i+num_feats:i+num_feats+future, :])))
        #raw_y.append(np.ravel(np.array(target_by_station.iloc[i+num_feats:i+num_feats+future, :])))
    
    x = np.stack(x); y = np.stack(y)#; raw_y = np.stack(raw_y)
    #print(x, y)
    
    scaler = StandardScaler()
    split = int(0.5*x.shape[0])
    x_train = x[:split,:]
    #y_train_raw = raw_y[:split,:]
    y_train = y[:split,:]
    x_test = x[split:,:]    
    y_test = y[split:,:]
    
    model1 = LassoLars(alpha=0.001)#Lasso(alpha=0.0001)
    model2 = MLPRegressor()
    model3 = RandomForestRegressor(n_estimators=20, n_jobs=-1)
    model4 = XGBRegressor(n_estimators = 50, objective='reg:squarederror', n_jobs=-1)
    model5 = LGBMRegressor(n_estimators = 5, n_jobs=-1, verbose=-1)
    

    preds = []# , "MLP":model2, "RF":model3, "XGB":model4
    models = {"LR":model1, 'LGB':model5}
    for model in tqdm(models.keys()):
        
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
            #plt.plot(t); plt.plot(p); 
            #plt.legend(["Observations", "Predictions"], loc="upper center"); plt.title(f"Forecast of hour {i+1}")
            #plt.text(t.shape[0]-200, t.max()-10, display_metrics(t, p, returns=True))
            #plt.savefig(results_path + f"{target}/station={j+1}_hour={i+1}.png")
            #plt.clf()
            #plt.show()
        #make_forecast_video(j, y_test, y_pred)

    # plot preds by station (optional)
    #for i in range(100):
    #    p2 = y_pred[i,:,:]
    #    t2 = y_test[i,:,:]
    #    pd.DataFrame(np.hstack([p2, t2])).plot()
    #    plt.show()
    
    

