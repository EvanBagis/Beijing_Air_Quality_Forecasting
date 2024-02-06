# Beijing_Air_Quality_Forecasting

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/imgs/inversion.jpg)

## Introduction

This repository implements two (2) different forecasting frameworks. The frameworks are tested on the [Beijing Air Quality Dataset](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data).

- **Approach 1: Incremental recursive forecasting** uses the [river](https://riverml.xyz/0.21.0/) python library to implement an incremental forecasting model that aims to forecast 12 hours in the future. The model accepts 24 lag features from the time series that will be forecasted. The approach is a recursive one where the model initially accepts the last 24 observations to predict the future value one step ahead. The prediction becomes the last value of the input instance to predict the future value 2 steps ahead and so on.

- **Approach 2: Batch multioutput forecasting** uses [sklearn](https://scikit-learn.org/stable/) type models to perform multioutput forecasting. In this approach, the model accepts lagged features from multiple time series (each one corresponding to a specific station for this problem) and forecasts the following hours for all the time series simultaneously. The advantage of this approach is that the model not only learns from it's lags but also learns from the correlations between the other time series as well.

- **Evaluation**:evaluated with multiple metrics, namely, the root mean squared error (RMSE), the mean absolute error (MAE), the coefficient of determination (r2), the Pearson and Spearman correlation coefficients, the mean bias error (MBE) and the index of aggreement (IA).

- **Plots & tables**: The plots are generated for every step of the forecasting horizon. For example forecast of hour = 3, corresponds to the predictions to 3 hours after the final observation in the input vectors. The metrics in the tables correspond to the concatenated predictions over the full time series interval.

### Conceptual framework

- **Approach 1: Incremental recursive forecasting**. The current framework works as follows: Initially, the first N lags from the time series formulate the first input vector ( e.g. y(t-24) ... y(t) ). The model forcasts the target for the next hour y(t+1). In the next step, the model accepts the N-1 lags and the prediction from the previous step ( e.g. y(t-23) ... y(t+1) ) and forecasts the target for the next hour y(t+2). The process repeats for the selected horizon (e.g. 12 hours ahead). After all the values from the horizon are forecasted, the model enters the learning mode and uses the same input vectors as before to train. Therefore, in this example, the model will 1) forecast 12 hours in the future and 2) it will train on the same x and y. Incrementally, the process continues untill it scans the whole series. 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/imgs/incremental_recursive_forecasting.png)


- **Approach 2: Batch multioutput forecasting**. The inner workings of this framework are as follows: Intially, the input vector (x) comprises N lag values of each of the multile time series (e.g. 24(lags)x12(hours ahead)x12(time series) ). The forecasts are the next M hours values for all the time series as well (e.g. 24(lags)x12(hours ahead)x12(time series) ). Both x and y vectors are flattened and the dataset is split into train and test sets. Therefore, the input and the output vectors shapes are 288 in this example. 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/imgs/batch_multioutput_forecasting.png)

### Results

# Incremental recursive forecasting

<p align="center">O3 Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|--------:|---------:|
| O3_Aotizhongxin  | 36.3981 | 24.8349 | 0.600683 |  0.783168 |   0.743906 | 2.81195 | 0.878885 |
| O3_Changping     | 34.4897 | 23.6276 | 0.59872  |  0.778909 |   0.749024 | 2.61294 | 0.87335  |
| O3_Dingling      | 40.6802 | 25.3361 | 0.623839 |  0.795731 |   0.749554 | 1.59144 | 0.88525  |
| O3_Dongsi        | 40.7794 | 24.0469 | 0.517222 |  0.726581 |   0.756037 | 3.00862 | 0.836744 |
| O3_Guanyuan      | 36.033  | 24.3328 | 0.604449 |  0.785482 |   0.753575 | 3.21793 | 0.879683 |
| O3_Gucheng       | 35.4742 | 24.4063 | 0.629237 |  0.799946 |   0.74047  | 3.66235 | 0.888124 |
| O3_Huairou       | 35.0231 | 24.0757 | 0.626897 |  0.796879 |   0.738742 | 1.82733 | 0.886701 |
| O3_Nongzhanguan  | 35.7393 | 24.7948 | 0.62534  |  0.797197 |   0.739211 | 3.15897 | 0.886471 |
| O3_Shunyi        | 35.7242 | 24.4631 | 0.576517 |  0.766533 |   0.71687  | 2.90485 | 0.866769 |
| O3_Tiantan       | 41.9266 | 26.4646 | 0.52545  |  0.738625 |   0.732399 | 3.30512 | 0.85035  |
| O3_Wanliu        | 33.4241 | 22.0137 | 0.623459 |  0.795792 |   0.736095 | 3.03934 | 0.885591 |
| O3_Wanshouxigong | 35.9737 | 24.8986 | 0.604248 |  0.784971 |   0.731144 | 2.44295 | 0.879985 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/incremental_recursive_O3_Aotizhongxin.gif)










<p align="center">PM10 Forecasting (incremental recursive)</p>

<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM10_Aotizhongxin  | 78.9788 | 52.0642 | 0.314215 |  0.588557 |   0.617098 |  1.92281   | 0.749229 |
| PM10_Changping     | 68.5994 | 43.8455 | 0.333154 |  0.600651 |   0.630011 |  0.835665  | 0.756046 |
| PM10_Dingling      | 65.8603 | 41.5185 | 0.326671 |  0.602174 |   0.620352 |  1.76802   | 0.761297 |
| PM10_Dongsi        | 81.3528 | 53.8643 | 0.313386 |  0.58541  |   0.595024 |  1.81847   | 0.745402 |
| PM10_Guanyuan      | 77.2155 | 51.1614 | 0.303015 |  0.579958 |   0.602988 |  0.647429  | 0.742596 |
| PM10_Gucheng       | 83.1655 | 57.3027 | 0.274598 |  0.555781 |   0.559631 |  0.0636216 | 0.725818 |
| PM10_Huairou       | 68.2979 | 43.9931 | 0.356324 |  0.61749  |   0.633405 |  1.57355   | 0.768871 |
| PM10_Nongzhanguan  | 77.9432 | 52.5297 | 0.343496 |  0.606192 |   0.60277  |  1.595     | 0.759805 |
| PM10_Shunyi        | 76.008  | 49.7614 | 0.314744 |  0.586687 |   0.604011 |  1.85108   | 0.745315 |
| PM10_Tiantan       | 75.5815 | 50.499  | 0.301447 |  0.572814 |   0.583763 |  0.652917  | 0.733793 |
| PM10_Wanliu        | 77.8741 | 52.5156 | 0.307938 |  0.593716 |   0.59206  | -1.46078   | 0.758329 |
| PM10_Wanshouxigong | 82.2387 | 54.9131 | 0.305699 |  0.5781   |   0.572261 |  2.00006   | 0.740456 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/incremental_recursive_PM10_Aotizhongxin.gif)









<p align="center">PM2.5 Forecasting (incremental recursive)</p>

<div align="center"> 

|                     |    RMSE |     MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:--------------------|--------:|--------:|---------:|----------:|-----------:|--------:|---------:|
| PM2.5_Aotizhongxin  | 64.1346 | 39.6812 | 0.39263  |  0.645456 |   0.666458 | 2.99059 | 0.789258 |
| PM2.5_Changping     | 55.4365 | 34.083  | 0.414151 |  0.664898 |   0.685161 | 1.02886 | 0.805887 |
| PM2.5_Dingling      | 56.1898 | 33.3599 | 0.436102 |  0.686326 |   0.6917   | 1.00253 | 0.822165 |
| PM2.5_Dongsi        | 69.4022 | 43.6152 | 0.353871 |  0.621342 |   0.642327 | 2.01519 | 0.774619 |
| PM2.5_Guanyuan      | 65.4695 | 40.1371 | 0.351674 |  0.623613 |   0.663035 | 1.92602 | 0.777306 |
| PM2.5_Gucheng       | 66.2093 | 40.56   | 0.367222 |  0.632081 |   0.647868 | 3.1562  | 0.782548 |
| PM2.5_Huairou       | 54.5479 | 32.9519 | 0.413068 |  0.662808 |   0.694557 | 1.59912 | 0.80311  |
| PM2.5_Nongzhanguan  | 67.3813 | 42.7504 | 0.399995 |  0.648705 |   0.659064 | 2.4099  | 0.790113 |
| PM2.5_Shunyi        | 64.7657 | 40.7151 | 0.377697 |  0.642141 |   0.652142 | 1.68783 | 0.789908 |
| PM2.5_Tiantan       | 63.9635 | 40.8351 | 0.378478 |  0.637223 |   0.644795 | 1.70618 | 0.78518  |
| PM2.5_Wanliu        | 63.1622 | 39.3159 | 0.409288 |  0.660527 |   0.670556 | 1.02297 | 0.802254 |
| PM2.5_Wanshouxigong | 69.3806 | 43.5625 | 0.358619 |  0.62112  |   0.624755 | 2.94342 | 0.77242  |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/incremental_recursive_PM2.5_Aotizhongxin.gif)










<p align="center">NO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| NO2_Aotizhongxin  | 30.5087 | 22.3539 | 0.320303 |  0.588338 |   0.581884 |  0.0425381 | 0.74988  |
| NO2_Changping     | 24.3198 | 17.7773 | 0.32725  |  0.599941 |   0.561217 |  0.668524  | 0.761278 |
| NO2_Dingling      | 20.8253 | 13.594  | 0.373926 |  0.639563 |   0.605944 |  0.94843   | 0.790303 |
| NO2_Dongsi        | 28.5767 | 20.6501 | 0.313077 |  0.595168 |   0.593389 | -0.236595  | 0.761281 |
| NO2_Guanyuan      | 28.8897 | 21.1423 | 0.326813 |  0.603434 |   0.585885 | -0.895171  | 0.766108 |
| NO2_Gucheng       | 32.1062 | 23.6149 | 0.227835 |  0.540428 |   0.511923 | -0.365911  | 0.730764 |
| NO2_Huairou       | 21.4241 | 14.6116 | 0.336497 |  0.615786 |   0.619914 |  0.550125  | 0.774832 |
| NO2_Nongzhanguan  | 30.6856 | 22.5952 | 0.292294 |  0.580028 |   0.563672 | -0.410344  | 0.752014 |
| NO2_Shunyi        | 26.3422 | 18.9776 | 0.305899 |  0.584364 |   0.556465 |  1.45085   | 0.751394 |
| NO2_Tiantan       | 27.3191 | 20.1312 | 0.271058 |  0.559315 |   0.543351 |  0.493136  | 0.734163 |
| NO2_Wanliu        | 29.7919 | 21.8833 | 0.393122 |  0.649521 |   0.622486 | -1.63363   | 0.796176 |
| NO2_Wanshouxigong | 29.2628 | 21.3989 | 0.342567 |  0.616375 |   0.594836 | -0.674323  | 0.776073 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/incremental_recursive_NO2_Aotizhongxin.gif)










<p align="center">SO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                   |    RMSE |      MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:------------------|--------:|---------:|---------:|----------:|-----------:|--------:|---------:|
| SO2_Aotizhongxin  | 17.2037 |  9.37219 | 0.431945 |  0.678046 |   0.738745 | 1.71305 | 0.806145 |
| SO2_Changping     | 15.2491 |  8.1526  | 0.477951 |  0.703525 |   0.712174 | 1.43531 | 0.821648 |
| SO2_Dingling      | 12.3692 |  6.70401 | 0.369828 |  0.643233 |   0.65537  | 1.02226 | 0.787578 |
| SO2_Dongsi        | 17.6086 | 10.1288  | 0.41284  |  0.664387 |   0.704698 | 1.52122 | 0.79846  |
| SO2_Guanyuan      | 18.0291 |  9.67216 | 0.418877 |  0.671274 |   0.724119 | 1.20499 | 0.804861 |
| SO2_Gucheng       | 21.1552 |  8.26701 | 0.38787  |  0.642485 |   0.78482  | 1.2076  | 0.774757 |
| SO2_Huairou       | 14.3207 |  6.9688  | 0.427517 |  0.672708 |   0.69044  | 1.42883 | 0.800646 |
| SO2_Nongzhanguan  | 18.5645 | 10.4324  | 0.421677 |  0.675288 |   0.708009 | 1.404   | 0.808489 |
| SO2_Shunyi        | 15.5605 |  8.17542 | 0.367335 |  0.631521 |   0.652    | 1.8675  | 0.770781 |
| SO2_Tiantan       | 17.3183 |  8.97848 | 0.287314 |  0.590441 |   0.644893 | 1.53563 | 0.747095 |
| SO2_Wanliu        | 15.7662 |  8.69729 | 0.519721 |  0.732865 |   0.793243 | 0.72319 | 0.844938 |
| SO2_Wanshouxigong | 18.5066 |  9.86097 | 0.418895 |  0.674178 |   0.737087 | 1.59425 | 0.806909 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/incremental_recursive_SO2_Aotizhongxin.gif)












<p align="center">CO Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|--------:|---------:|
| CO_Aotizhongxin  | 959.733 | 561.698 | 0.403206 |  0.650984 |   0.626162 | 76.0277 | 0.78738  |
| CO_Changping     | 899.778 | 505.527 | 0.362969 |  0.622966 |   0.641725 | 69.1997 | 0.766298 |
| CO_Dingling      | 688.772 | 389.001 | 0.411646 |  0.659    |   0.668349 | 52.7513 | 0.795851 |
| CO_Dongsi        | 951.467 | 558.987 | 0.372741 |  0.636466 |   0.611965 | 57.4963 | 0.783795 |
| CO_Guanyuan      | 918.298 | 552.606 | 0.367345 |  0.625933 |   0.608511 | 51.9137 | 0.771963 |
| CO_Gucheng       | 921.152 | 544.229 | 0.44511  |  0.683625 |   0.654268 | 29.1748 | 0.815335 |
| CO_Huairou       | 722.869 | 422.189 | 0.347726 |  0.610964 |   0.624639 | 51.5644 | 0.759913 |
| CO_Nongzhanguan  | 998.67  | 600.624 | 0.371856 |  0.628518 |   0.604891 | 73.7989 | 0.772002 |
| CO_Shunyi        | 951.464 | 557.213 | 0.340472 |  0.605372 |   0.619358 | 84.5209 | 0.753656 |
| CO_Tiantan       | 944.741 | 570.59  | 0.363991 |  0.622974 |   0.604306 | 54.4142 | 0.770065 |
| CO_Wanliu        | 980.4   | 571.462 | 0.402306 |  0.656441 |   0.62857  | 40.8427 | 0.797427 |
| CO_Wanshouxigong | 990.665 | 609.437 | 0.360642 |  0.631189 |   0.59392  | 51.4735 | 0.78128  |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/incremental_recursive_CO_Aotizhongxin.gif)






# Batch multioutput forecasting

<p align="center">O3 Forecasting (batch multioutput)</p>

<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| O3Aotizhongxin  | 35.5014 | 24.2946 | 0.655581 |  0.819428 |   0.785857 |  7.47273  | 0.886368 |
| O3Changping     | 30.4539 | 21.1907 | 0.664949 |  0.821146 |   0.804937 | -3.75076  | 0.89921  |
| O3Dingling      | 42.4419 | 24.8341 | 0.693415 |  0.843469 |   0.816234 |  3.27316  | 0.888967 |
| O3Dongsi        | 33.6876 | 22.8178 | 0.614235 |  0.787493 |   0.773266 |  0.482338 | 0.880039 |
| O3Guanyuan      | 33.7352 | 23.0035 | 0.664144 |  0.816415 |   0.795459 |  2.76031  | 0.892366 |
| O3Gucheng       | 34.1669 | 23.3176 | 0.665702 |  0.820195 |   0.792555 |  4.85095  | 0.89004  |
| O3Huairou       | 32.815  | 22.3637 | 0.6403   |  0.803523 |   0.782021 | -1.43473  | 0.889315 |
| O3Nongzhanguan  | 33.3218 | 22.9131 | 0.67416  |  0.822433 |   0.785215 |  2.27738  | 0.897963 |
| O3Shunyi        | 34.1537 | 23.8708 | 0.606346 |  0.782872 |   0.70101  | -2.76597  | 0.876124 |
| O3Tiantan       | 36.0515 | 25.0111 | 0.634835 |  0.798215 |   0.770416 |  1.22823  | 0.883822 |
| O3Wanliu        | 34.954  | 23.6253 | 0.639164 |  0.809118 |   0.767238 |  6.87387  | 0.877244 |
| O3Wanshouxigong | 32.7139 | 22.5942 | 0.676349 |  0.824531 |   0.793665 |  3.38864  | 0.896775 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/batch_multioutput_O3_Aotizhongxin.gif)




<p align="center">PM10 Forecasting (batch multioutput)</p>

<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM10Aotizhongxin  | 63.7753 | 41.0673 | 0.554634 |  0.747455 |   0.736989 |  -4.66696  | 0.832337 |
| PM10Changping     | 55.6963 | 34.5189 | 0.554965 |  0.745995 |   0.72146  |  -2.73427  | 0.836018 |
| PM10Dingling      | 52.5052 | 31.6559 | 0.563896 |  0.750964 |   0.743464 |   0.44166  | 0.845171 |
| PM10Dongsi        | 68.6353 | 42.5965 | 0.557075 |  0.750976 |   0.743076 |   1.66845  | 0.825513 |
| PM10Guanyuan      | 63.9276 | 40.5833 | 0.559962 |  0.751996 |   0.743659 |   0.873154 | 0.828929 |
| PM10Gucheng       | 68.6538 | 45.9694 | 0.526948 |  0.728458 |   0.698924 |  -1.29217  | 0.813567 |
| PM10Huairou       | 54.4693 | 35.7424 | 0.574238 |  0.761821 |   0.720411 |  -6.48134  | 0.85304  |
| PM10Nongzhanguan  | 63.9239 | 41.0187 | 0.553401 |  0.747356 |   0.741352 |  -2.41585  | 0.826269 |
| PM10Shunyi        | 61.6306 | 39.201  | 0.550389 |  0.743369 |   0.732902 |  -3.47588  | 0.831886 |
| PM10Tiantan       | 62.8767 | 39.264  | 0.547784 |  0.744493 |   0.733275 |  -1.297    | 0.820376 |
| PM10Wanliu        | 59.4705 | 39.4612 | 0.562667 |  0.759208 |   0.727974 | -10.3234   | 0.843041 |
| PM10Wanshouxigong | 64.4692 | 41.6874 | 0.55572  |  0.751415 |   0.727748 |  -2.40198  | 0.823676 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/batch_multioutput_PM10_Aotizhongxin.gif)




<p align="center">PM2.5 Forecasting (batch multioutput)</p>

<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| PM2.5Aotizhongxin  | 50.3491 | 30.2505 | 0.646582 |  0.805049 |   0.789915 |  0.372928 | 0.878404 |
| PM2.5Changping     | 40.981  | 24.6027 | 0.63877  |  0.801725 |   0.771319 | -3.17151  | 0.886483 |
| PM2.5Dingling      | 42.9077 | 24.6987 | 0.652866 |  0.809029 |   0.783344 | -1.02232  | 0.8912   |
| PM2.5Dongsi        | 54.6657 | 32.2582 | 0.626718 |  0.793959 |   0.778501 |  3.54611  | 0.868521 |
| PM2.5Guanyuan      | 48.9332 | 29.2541 | 0.661048 |  0.814983 |   0.793851 |  2.21263  | 0.883825 |
| PM2.5Gucheng       | 49.874  | 30.2138 | 0.669895 |  0.821228 |   0.781889 |  1.79315  | 0.886191 |
| PM2.5Huairou       | 38.9876 | 23.8868 | 0.698465 |  0.835874 |   0.795472 | -0.938171 | 0.904522 |
| PM2.5Nongzhanguan  | 53.2696 | 31.8353 | 0.628045 |  0.793062 |   0.785618 |  1.29805  | 0.871436 |
| PM2.5Shunyi        | 51.7688 | 31.2031 | 0.630994 |  0.796455 |   0.777127 |  2.31294  | 0.869522 |
| PM2.5Tiantan       | 50.6653 | 29.9177 | 0.629446 |  0.794117 |   0.78343  |  0.995696 | 0.871223 |
| PM2.5Wanliu        | 46.7953 | 27.9499 | 0.666304 |  0.816777 |   0.788832 | -2.30435  | 0.891785 |
| PM2.5Wanshouxigong | 54.3755 | 31.9516 | 0.631858 |  0.798002 |   0.771399 |  2.54569  | 0.868274 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/batch_multioutput_PM2.5_Aotizhongxin.gif)




<p align="center">NO2 Forecasting (batch multioutput)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| NO2Aotizhongxin  | 25.3635 | 18.6671 | 0.547498 |  0.743625 |   0.691005 | -2.19452   | 0.830388 |
| NO2Changping     | 19.7499 | 14.345  | 0.56609  |  0.757728 |   0.697133 |  2.01328   | 0.837592 |
| NO2Dingling      | 15.4194 | 10.398  | 0.641813 |  0.803333 |   0.71943  |  0.664967  | 0.875279 |
| NO2Dongsi        | 22.7642 | 16.5306 | 0.528808 |  0.728292 |   0.683174 | -1.26973   | 0.830516 |
| NO2Guanyuan      | 23.143  | 16.8039 | 0.5538   |  0.745676 |   0.692232 | -1.63131   | 0.84062  |
| NO2Gucheng       | 24.0158 | 17.6606 | 0.512888 |  0.722324 |   0.673986 | -3.13942   | 0.826821 |
| NO2Huairou       | 16.0051 | 11.6891 | 0.575592 |  0.766364 |   0.683527 | -2.59572   | 0.850654 |
| NO2Nongzhanguan  | 24.5132 | 17.8606 | 0.523979 |  0.725369 |   0.684795 | -1.63402   | 0.827089 |
| NO2Shunyi        | 22.1805 | 16.2763 | 0.504059 |  0.710086 |   0.64011  |  0.0998107 | 0.813036 |
| NO2Tiantan       | 22.0377 | 15.944  | 0.528369 |  0.727445 |   0.687572 |  0.374124  | 0.821607 |
| NO2Wanliu        | 23.9586 | 17.5088 | 0.582652 |  0.766579 |   0.722409 | -2.55328   | 0.854066 |
| NO2Wanshouxigong | 22.9309 | 16.6265 | 0.552761 |  0.745966 |   0.696465 | -2.08638   | 0.840681 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/batch_multioutput_NO2_Aotizhongxin.gif)




<p align="center">SO2 Forecasting (batch multioutput)</p>

<div align="center"> 

|                  |     RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|---------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| SO2Aotizhongxin  | 10.3621  | 6.21548 | 0.513416 |  0.719196 |   0.695816 | -0.901187 | 0.817718 |
| SO2Changping     |  8.65794 | 5.15567 | 0.38594  |  0.657099 |   0.65265  | -1.32078  | 0.789422 |
| SO2Dingling      |  6.77391 | 4.31437 | 0.497911 |  0.706544 |   0.64617  | -0.271726 | 0.812133 |
| SO2Dongsi        | 10.5926  | 6.61472 | 0.498049 |  0.708834 |   0.70102  | -0.969764 | 0.803609 |
| SO2Guanyuan      | 10.7147  | 6.28781 | 0.499664 |  0.707969 |   0.681172 | -0.593462 | 0.805511 |
| SO2Gucheng       | 10.9762  | 5.6904  | 0.477582 |  0.692269 |   0.717258 | -0.604405 | 0.793348 |
| SO2Huairou       |  7.25072 | 4.31517 | 0.363808 |  0.642347 |   0.589305 | -1.06886  | 0.781827 |
| SO2Nongzhanguan  | 10.7242  | 6.71102 | 0.491009 |  0.704713 |   0.674785 | -1.0759   | 0.807733 |
| SO2Shunyi        |  9.9512  | 5.67377 | 0.434045 |  0.659238 |   0.64419  |  0.308949 | 0.764954 |
| SO2Tiantan       |  9.55825 | 5.74398 | 0.365096 |  0.609331 |   0.576468 | -0.44668  | 0.736441 |
| SO2Wanliu        |  9.80261 | 6.12519 | 0.542722 |  0.740816 |   0.722037 | -1.08491  | 0.836709 |
| SO2Wanshouxigong | 11.1168  | 6.37038 | 0.471446 |  0.687115 |   0.672057 | -0.385236 | 0.789992 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/batch_multioutput_SO2_Aotizhongxin.gif)





<p align="center">CO Forecasting (batch multioutput)</p>

<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| COAotizhongxin  | 816.869 | 476.075 | 0.662412 |  0.817947 |   0.712057 |  86.0312   | 0.883947 |
| COChangping     | 688.245 | 399.13  | 0.648168 |  0.806506 |   0.711531 |  30.8801   | 0.879147 |
| CODingling      | 560.495 | 313.584 | 0.676566 |  0.823833 |   0.764111 |  -4.1774   | 0.890707 |
| CODongsi        | 791.117 | 467.638 | 0.610651 |  0.781534 |   0.701147 |   2.5923   | 0.86484  |
| COGuanyuan      | 729.81  | 428.388 | 0.647329 |  0.804659 |   0.711804 |  11.1129   | 0.8824   |
| COGucheng       | 712.771 | 427.272 | 0.679977 |  0.824717 |   0.712186 | -16.2379   | 0.897177 |
| COHuairou       | 533.622 | 319.243 | 0.705577 |  0.840776 |   0.732445 |  -4.69532  | 0.904189 |
| CONongzhanguan  | 816.473 | 479.94  | 0.633905 |  0.796777 |   0.705469 |  35.6447   | 0.875135 |
| COShunyi        | 790.388 | 474.563 | 0.640576 |  0.804715 |   0.686902 |  25.4474   | 0.8699   |
| COTiantan       | 751.132 | 444.217 | 0.647982 |  0.805609 |   0.695569 |  12.791    | 0.879941 |
| COWanliu        | 767.625 | 454.926 | 0.65542  |  0.810183 |   0.698761 |  -0.774151 | 0.891208 |
| COWanshouxigong | 767.899 | 463.84  | 0.646474 |  0.80428  |   0.702443 | -12.2222   | 0.880827 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/batch_multioutput_CO_Aotizhongxin.gif)





