import os
import warnings
from tqdm import tqdm
import pickle
import pandas as pd
import requests
import numpy as np

# metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import pearsonr, spearmanr

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


def make_forecast_video(target, n_station, y_test, y_pred, path, mode):
    """
    Generate a GIF animation visualizing the forecasted values compared to the observed values.

    Parameters:
    - target (str): Name or description of the target variable.
    - n_station (int): Station number or identifier.
    - y_test (numpy.ndarray): Array containing the observed values.
    - y_pred (numpy.ndarray): Array containing the predicted values.
    - path (str): Path to the directory where the GIF will be saved.

    Returns:
    None

    Notes:
    - Total number of frames in the GIF is calculated as duration multiplied by fps.
    - The function creates a video clip visualizing the forecasted values compared to the observed values.
    - The video clip is saved as a GIF file.

    Example:
    make_forecast_video("Temperature", 1, y_test, y_pred, "/path/to/directory")
    """
    duration = 12
    tqdm._instances.clear()
    
    yy_pred = y_pred.iteritems()
    yy_test = y_test.iteritems()
    
    fig, ax = plt.subplots(figsize=(20, 5))
    def make_frame(t):
        """
        Generate a frame for the video clip.

        Parameters:
        - t (int): Time index for the frame.

        Returns:
        numpy.ndarray: Image of the frame.

        Notes:
        - This function is called for each frame in the video clip.
        """
        
        ax.clear()
        # element 1 because next return tuple (i, row(i))
        tt = (t, y_test.iloc[:,int(t)]); p = (t, y_pred.iloc[:,int(t)])
        ax.plot(tt[1], linewidth=2)
        ax.plot(p[1], linewidth=2, color="r")
        plt.legend(["Observations", "Predictions"], loc="upper left")
        rmse, mae, r2, r, rs, MBE, ia = display_metrics(tt[1], p[1], returns=True)
        plt.title(f"Forecast of hour {tt[0]+1}\n (RMSE = {rmse:.2f}, MAE = {mae:.2f}, r2 = {r2:.2f}\n Pearson = {r:.2f}, Spearman = {rs:.2f}\n MBE = {MBE:.2f} , IA = {ia:.2f})")
        plt.tight_layout()
        plt.box("off")
        return mplfig_to_npimage(fig)

    animation = VideoClip(make_frame, duration=duration)
    animation.write_gif(path + f"/gifs/{target}/{mode}{n_station}.gif", fps=1)