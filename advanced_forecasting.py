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
# metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr

# models
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, RANSACRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from tsmoothie.smoother import LowessSmoother, KalmanSmoother, ConvolutionSmoother, SpectralSmoother

import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
from tqdm import tqdm

plt.rcParams.update({'font.size': 22})

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

warnings.simplefilter(action='ignore', category=ConvergenceWarning)

def display_metrics(true, pred, returns=False):

    if returns:
        return f"RMSE = {np.sqrt(mean_squared_error(true, pred)):.2f}, MAE = {mean_absolute_error(true, pred):.2f}, r2 = {r2_score(true, pred):.2f}, R = {pearsonr(true, pred)[0]:.2f}"
    else:
        print(f"RMSE = {np.sqrt(mean_squared_error(true, pred)):.2f}, MAE = {mean_absolute_error(true, pred):.2f}, r2 = {r2_score(true, pred):.2f}, R = {pearsonr(true, pred)[0]:.2f}")
        return 0
    
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

results_path = f"/var/snap/docker/common/var-lib-docker/volumes/fmi-vol/_data/forecast_results/"
path = "/var/snap/docker/common/var-lib-docker/volumes/fmi-vol/_data/FMI_ref/" # docker
#path = '/media/evan/5a4571f6-ff19-4d1f-a2f9-f74087bdf128/FMI/FMI_ref/' # local
targets = ["coarsePM", "PM25", "PM10", "O3", "NO2"]
num_stations = [11, 11, 12, 4, 11]
future = 12; num_feats = 12
for target, n_stations in zip(targets, num_stations):

    enf_target = f'{target}_ref.csv'
    models_path = f"/var/snap/docker/common/var-lib-docker/volumes/fmi-vol/_data/forecaster/{target}/"
    #x, y1, raw_y = create_x_y_raw(path, enf_target, n_stations, future, num_feats, sm="conv")
    #x, y2, raw_y = create_x_y_raw(path, enf_target, n_stations, future, num_feats, sm="kalman")
    x, y3, raw_y = create_x_y_raw(path, enf_target, n_stations, future, num_feats, sm="spectral")
    scaler = StandardScaler()
    split = int(0.8*x.shape[0])
    x_train = x[:split,:]
    y_train_raw = raw_y[:split,:]
    y_train3 = y3[:split,:]
    x_test = x[split:,:]    
    y_test = raw_y[split:,:]
    
    model1 = LassoLars(alpha=0.001)#Lasso(alpha=0.0001)
    model2 = MLPRegressor()
    model3 = RandomForestRegressor(n_estimators=20, n_jobs=-1)
    model4 = XGBRegressor(n_estimators = 200, objective='reg:squarederror', n_jobs=-1)
    

    preds = []# , "MLP":model2, "RF":model3, "XGB":model4
    models = {"LR":model1, "XGB":model4}; ys = {"raw":y_train_raw}#y_train1, y_train2, y_train3, 
    for model in models.keys():
        for y_train in ys.keys():
            
            
            models[model].fit(x_train, ys[y_train])
            with open(models_path + f"{model}_{y_train}.sav", "wb") as f:
                pickle.dump(models[model], f)
                
            p = models[model].predict(x_test).reshape(y_test.shape[0],future,n_stations)
            preds.append(p)

    y_pred = np.stack(preds).mean(axis=0)
    y_test = np.array(y_test).reshape(y_test.shape[0],future,n_stations)

    # plot preds by hour (optional) * display performance metrics
    for j in range(n_stations):
        for i in range(future):
            p = y_pred[:,i,j]
            t = y_test[:,i,j]
            display_metrics(t, p)
        #    plt.plot(t); plt.plot(p); 
        #    plt.legend(["Observations", "Predictions"], loc="upper center"); plt.title(f"Forecast of hour {i+1}")
        #    plt.text(t.shape[0]-200, t.max()-10, display_metrics(t, p, returns=True))
        #    plt.savefig(results_path + f"{target}/station={j+1}_hour={i+1}.png")
        #    plt.clf()
        #    #plt.show()
        make_forecast_video(j, y_test, y_pred)

    # plot preds by station (optional)
    #for i in range(100):
    #    p2 = y_pred[i,:,:]
    #    t2 = y_test[i,:,:]
    #    pd.DataFrame(np.hstack([p2, t2])).plot()
    #    plt.show()
    
    

