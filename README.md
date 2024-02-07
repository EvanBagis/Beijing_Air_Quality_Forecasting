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
| O3Aotizhongxin  | 35.2617 | 24.506  | 0.660216 |  0.824381 |   0.786806 |  8.41672  | 0.892309 |
| O3Changping     | 29.7449 | 20.7395 | 0.680367 |  0.831563 |   0.814587 | -2.25969  | 0.908155 |
| O3Dingling      | 41.6612 | 24.5485 | 0.70459  |  0.850388 |   0.822309 |  5.85501  | 0.895998 |
| O3Dongsi        | 32.1009 | 22.0671 | 0.649719 |  0.811187 |   0.788954 |  1.61985  | 0.895804 |
| O3Guanyuan      | 33.704  | 23.356  | 0.664763 |  0.820313 |   0.796415 |  4.20157  | 0.898031 |
| O3Gucheng       | 33.3041 | 23.1008 | 0.682374 |  0.831498 |   0.8041   |  5.50921  | 0.900997 |
| O3Huairou       | 31.9299 | 21.9582 | 0.659444 |  0.817238 |   0.796153 |  0.968759 | 0.899437 |
| O3Nongzhanguan  | 32.9024 | 22.8748 | 0.68231  |  0.83111  |   0.794066 |  4.09802  | 0.905125 |
| O3Shunyi        | 34.2874 | 24.0327 | 0.603258 |  0.784896 |   0.697309 | -0.859631 | 0.881919 |
| O3Tiantan       | 35.9048 | 25.0292 | 0.637801 |  0.804239 |   0.780445 |  3.81281  | 0.889081 |
| O3Wanliu        | 34.468  | 23.657  | 0.649129 |  0.817293 |   0.769339 |  7.95523  | 0.88561  |
| O3Wanshouxigong | 32.1566 | 22.5799 | 0.687283 |  0.834043 |   0.798968 |  4.76228  | 0.905115 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/batch_multioutput_O3_Aotizhongxin.gif)


<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| O3Aotizhongxin  | 35.4226 | 25.2276 | 0.657109 |  0.839418 |   0.800552 |  11.1071  | 0.879749 |
| O3Changping     | 31.2187 | 22.8872 | 0.647909 |  0.833263 |   0.816021 | -10.889   | 0.896764 |
| O3Dingling      | 57.691  | 28.4171 | 0.433529 |  0.667697 |   0.806722 |   3.93329 | 0.734443 |
| O3Dongsi        | 34.4327 | 24.0423 | 0.596983 |  0.792514 |   0.797515 |  -8.10707 | 0.878941 |
| O3Guanyuan      | 32.2049 | 23.2965 | 0.693923 |  0.833835 |   0.804405 |  -1.84436 | 0.90138  |
| O3Gucheng       | 33.0828 | 24.4396 | 0.68658  |  0.832822 |   0.794327 |  -2.14159 | 0.892172 |
| O3Huairou       | 34.2668 | 25.3693 | 0.607769 |  0.807287 |   0.762149 | -11.4378  | 0.875968 |
| O3Nongzhanguan  | 31.7454 | 22.9007 | 0.70426  |  0.839865 |   0.796633 |  -1.94659 | 0.90712  |
| O3Shunyi        | 35.7838 | 25.6835 | 0.567874 |  0.772654 |   0.6827   |  -8.31363 | 0.866258 |
| O3Tiantan       | 34.3234 | 25.2734 | 0.669005 |  0.820697 |   0.790788 |  -3.98679 | 0.892592 |
| O3Wanliu        | 34.3716 | 24.0312 | 0.651088 |  0.825415 |   0.779614 |   7.58841 | 0.874629 |
| O3Wanshouxigong | 31.5151 | 22.8295 | 0.699634 |  0.836776 |   0.80374  |  -1.08743 | 0.903896 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/batch_multioutput_O3_Aotizhongxin.gif)






<p align="center">PM10 Forecasting (batch multioutput)</p>

<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM10Aotizhongxin  | 61.4241 | 38.5876 | 0.586866 |  0.768935 |   0.76885  |  -6.28316  | 0.855116 |
| PM10Changping     | 54.8978 | 33.5923 | 0.567636 |  0.756003 |   0.747718 |  -5.21418  | 0.846712 |
| PM10Dingling      | 51.5208 | 30.6331 | 0.580096 |  0.761928 |   0.76064  |  -1.09705  | 0.855233 |
| PM10Dongsi        | 65.2339 | 39.2796 | 0.599888 |  0.776478 |   0.778858 |  -0.26708  | 0.852722 |
| PM10Guanyuan      | 61.2347 | 37.5628 | 0.596254 |  0.773924 |   0.77691  |   0.704351 | 0.851955 |
| PM10Gucheng       | 66.4571 | 43.0653 | 0.556737 |  0.746974 |   0.742701 |  -2.39683  | 0.836277 |
| PM10Huairou       | 52.8871 | 33.8033 | 0.598612 |  0.777455 |   0.762984 |  -6.293    | 0.86483  |
| PM10Nongzhanguan  | 60.6224 | 38.4001 | 0.598342 |  0.775844 |   0.771787 |  -5.08036  | 0.857153 |
| PM10Shunyi        | 59.5244 | 37.0919 | 0.580595 |  0.764176 |   0.765344 |  -5.25373  | 0.851308 |
| PM10Tiantan       | 60.5961 | 37.0908 | 0.579994 |  0.763541 |   0.763602 |  -2.31308  | 0.843577 |
| PM10Wanliu        | 57.5988 | 37.4801 | 0.589762 |  0.779765 |   0.764414 | -12.0352   | 0.86417  |
| PM10Wanshouxigong | 61.9946 | 39.1165 | 0.589171 |  0.77009  |   0.760514 |  -4.23904  | 0.850007 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/batch_multioutput_PM10_Aotizhongxin.gif)


<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM10Aotizhongxin  | 64.675  | 40.583  | 0.541978 |  0.739301 |   0.743891 |  -1.99338  | 0.820753 |
| PM10Changping     | 57.4068 | 34.1665 | 0.52721  |  0.726976 |   0.740173 |  -1.09637  | 0.817456 |
| PM10Dingling      | 53.899  | 31.2652 | 0.540435 |  0.738912 |   0.761907 |   5.02532  | 0.82499  |
| PM10Dongsi        | 71.9931 | 43.1334 | 0.512676 |  0.732279 |   0.742381 |   8.74302  | 0.792271 |
| PM10Guanyuan      | 66.4083 | 40.9607 | 0.525148 |  0.737655 |   0.74294  |   6.82905  | 0.801688 |
| PM10Gucheng       | 70.6441 | 46.0299 | 0.499124 |  0.713397 |   0.706981 |   2.73496  | 0.788709 |
| PM10Huairou       | 55.2878 | 35.4843 | 0.561345 |  0.752657 |   0.749156 |  -3.38615  | 0.83284  |
| PM10Nongzhanguan  | 64.3005 | 40.4816 | 0.548123 |  0.744268 |   0.748715 |  -1.42393  | 0.821824 |
| PM10Shunyi        | 63.8391 | 39.7905 | 0.51759  |  0.721584 |   0.738037 |   0.916176 | 0.807306 |
| PM10Tiantan       | 64.9067 | 39.3714 | 0.518113 |  0.728017 |   0.738019 |   1.03072  | 0.797257 |
| PM10Wanliu        | 60.9629 | 39.9394 | 0.540443 |  0.745059 |   0.731727 | -10.5779   | 0.830586 |
| PM10Wanshouxigong | 65.7965 | 41.3974 | 0.537238 |  0.737811 |   0.732774 |  -2.89695  | 0.81508  |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/batch_multioutput_PM10_Aotizhongxin.gif)







<p align="center">PM2.5 Forecasting (batch multioutput)</p>

<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM2.5Aotizhongxin  | 49.5535 | 29.3318 | 0.657663 |  0.81191  |   0.805205 | -0.552089  | 0.883405 |
| PM2.5Changping     | 41.2171 | 24.8764 | 0.634595 |  0.799568 |   0.779583 | -4.1621    | 0.88357  |
| PM2.5Dingling      | 42.8327 | 24.9587 | 0.654079 |  0.810226 |   0.790057 | -2.97541   | 0.890597 |
| PM2.5Dongsi        | 53.4885 | 31.1821 | 0.642623 |  0.803103 |   0.797092 |  2.30355   | 0.876234 |
| PM2.5Guanyuan      | 48.1925 | 28.5873 | 0.671232 |  0.820502 |   0.806556 |  0.417151  | 0.888752 |
| PM2.5Gucheng       | 49.4518 | 29.4955 | 0.675461 |  0.823766 |   0.8003   | -0.0728441 | 0.889367 |
| PM2.5Huairou       | 38.9088 | 23.7147 | 0.699683 |  0.837202 |   0.810785 | -2.24146   | 0.90426  |
| PM2.5Nongzhanguan  | 51.8149 | 30.8632 | 0.648083 |  0.805147 |   0.79715  | -0.388642  | 0.882214 |
| PM2.5Shunyi        | 50.4626 | 30.0651 | 0.64938  |  0.807112 |   0.801818 |  0.414303  | 0.878488 |
| PM2.5Tiantan       | 49.6259 | 29.1761 | 0.644495 |  0.803297 |   0.80008  | -0.846999  | 0.878801 |
| PM2.5Wanliu        | 46.5413 | 27.688  | 0.669918 |  0.81966  |   0.800627 | -3.54381   | 0.894184 |
| PM2.5Wanshouxigong | 53.8945 | 31.3631 | 0.638342 |  0.800841 |   0.788564 |  0.366607  | 0.872287 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/batch_multioutput_PM2.5_Aotizhongxin.gif)


<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| PM2.5Aotizhongxin  | 52.0521 | 30.4077 | 0.62227  |  0.792757 |   0.795718 |  1.77722  | 0.86218  |
| PM2.5Changping     | 42.8862 | 24.687  | 0.604402 |  0.779936 |   0.784    | -3.14087  | 0.87174  |
| PM2.5Dingling      | 45.8823 | 24.3575 | 0.603067 |  0.77676  |   0.803384 |  1.10033  | 0.862323 |
| PM2.5Dongsi        | 56.3187 | 32.4635 | 0.603802 |  0.782837 |   0.786024 |  4.9308   | 0.853036 |
| PM2.5Guanyuan      | 50.7888 | 29.403  | 0.634855 |  0.802342 |   0.798233 |  3.7319   | 0.867641 |
| PM2.5Gucheng       | 53.0791 | 30.9344 | 0.626106 |  0.800281 |   0.791375 |  3.52152  | 0.859276 |
| PM2.5Huairou       | 41.2612 | 24.6902 | 0.66227  |  0.816093 |   0.807077 |  0.113745 | 0.882899 |
| PM2.5Nongzhanguan  | 53.9941 | 31.7941 | 0.617859 |  0.787742 |   0.789948 |  1.49914  | 0.863469 |
| PM2.5Shunyi        | 54.2905 | 31.976  | 0.594169 |  0.776423 |   0.783345 |  4.2033   | 0.847287 |
| PM2.5Tiantan       | 52.0401 | 29.8631 | 0.609065 |  0.783112 |   0.793058 |  1.35262  | 0.857156 |
| PM2.5Wanliu        | 48.2174 | 28.3699 | 0.645715 |  0.805914 |   0.797949 | -4.49447  | 0.88048  |
| PM2.5Wanshouxigong | 56.4312 | 32.4061 | 0.603495 |  0.781641 |   0.778828 |  2.02716  | 0.85124  |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/batch_multioutput_PM2.5_Aotizhongxin.gif)






<p align="center">NO2 Forecasting (batch multioutput)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| NO2Aotizhongxin  | 24.9278 | 18.2533 | 0.56291  |  0.756269 |   0.717786 | -3.18468  | 0.839955 |
| NO2Changping     | 19.5136 | 14.0642 | 0.576407 |  0.762553 |   0.714327 |  1.29335  | 0.84247  |
| NO2Dingling      | 15.4884 | 10.4595 | 0.638604 |  0.800335 |   0.702126 |  0.436178 | 0.87518  |
| NO2Dongsi        | 22.4132 | 16.2242 | 0.543225 |  0.739199 |   0.707919 | -1.84669  | 0.837849 |
| NO2Guanyuan      | 22.8483 | 16.4462 | 0.565093 |  0.754555 |   0.713303 | -2.2587   | 0.847078 |
| NO2Gucheng       | 23.7928 | 17.3845 | 0.521893 |  0.730641 |   0.695662 | -3.66363  | 0.832511 |
| NO2Huairou       | 15.7508 | 11.4581 | 0.588974 |  0.777259 |   0.697767 | -2.98597  | 0.858138 |
| NO2Nongzhanguan  | 24.178  | 17.5553 | 0.536909 |  0.736983 |   0.712623 | -2.78397  | 0.835447 |
| NO2Shunyi        | 21.6113 | 15.886  | 0.529187 |  0.727895 |   0.667143 | -0.798556 | 0.82821  |
| NO2Tiantan       | 21.6852 | 15.6071 | 0.543335 |  0.737521 |   0.707693 |  0.128883 | 0.829657 |
| NO2Wanliu        | 23.5532 | 16.9978 | 0.596655 |  0.77725  |   0.74679  | -3.16406  | 0.861532 |
| NO2Wanshouxigong | 22.6235 | 16.3222 | 0.564672 |  0.75709  |   0.722407 | -3.16024  | 0.848626 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/batch_multioutput_NO2_Aotizhongxin.gif)


<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| NO2Aotizhongxin  | 27.2186 | 20.7047 | 0.478886 |  0.703456 |   0.653235 | -1.90143  | 0.77493  |
| NO2Changping     | 21.544  | 15.7843 | 0.483676 |  0.724476 |   0.639911 |  4.78537  | 0.784615 |
| NO2Dingling      | 16.5578 | 11.0932 | 0.586973 |  0.781128 |   0.704735 |  2.3889   | 0.839969 |
| NO2Dongsi        | 23.1838 | 16.9907 | 0.511277 |  0.718353 |   0.681105 |  0.520846 | 0.803781 |
| NO2Guanyuan      | 23.8551 | 17.7606 | 0.52592  |  0.731604 |   0.673055 | -1.11442  | 0.808528 |
| NO2Gucheng       | 24.1785 | 18.0526 | 0.506265 |  0.720422 |   0.679052 | -3.55379  | 0.809648 |
| NO2Huairou       | 16.9989 | 13.0036 | 0.521252 |  0.742474 |   0.667412 | -3.71377  | 0.812776 |
| NO2Nongzhanguan  | 25.2063 | 18.7737 | 0.496679 |  0.707153 |   0.672312 | -0.345394 | 0.796899 |
| NO2Shunyi        | 23.1676 | 17.2996 | 0.458939 |  0.697436 |   0.62224  |  3.09676  | 0.760511 |
| NO2Tiantan       | 22.9524 | 16.8835 | 0.488404 |  0.712332 |   0.675749 |  2.36819  | 0.780622 |
| NO2Wanliu        | 26.0686 | 20.0526 | 0.505904 |  0.730916 |   0.694228 | -4.39511  | 0.795632 |
| NO2Wanshouxigong | 23.5135 | 17.2261 | 0.529747 |  0.730826 |   0.687277 | -1.47147  | 0.818494 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/batch_multioutput_NO2_Aotizhongxin.gif)







<p align="center">SO2 Forecasting (batch multioutput)</p>

<div align="center"> 

|                  |     RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|---------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| SO2Aotizhongxin  | 10.6021  | 6.68948 | 0.490612 |  0.734577 |   0.716849 | -2.53585  | 0.841457 |
| SO2Changping     |  9.56167 | 6.13736 | 0.251057 |  0.67575  |   0.710959 | -2.8828   | 0.801992 |
| SO2Dingling      |  7.34383 | 4.95772 | 0.409871 |  0.703701 |   0.663719 | -1.42528  | 0.830538 |
| SO2Dongsi        | 10.8175  | 6.99826 | 0.476506 |  0.724551 |   0.733824 | -2.66314  | 0.833364 |
| SO2Guanyuan      | 10.968   | 6.78712 | 0.475736 |  0.720758 |   0.710812 | -2.45819  | 0.831877 |
| SO2Gucheng       | 11.1397  | 5.84913 | 0.461906 |  0.698929 |   0.759264 | -1.49421  | 0.818036 |
| SO2Huairou       |  8.57427 | 5.69098 | 0.110349 |  0.637594 |   0.604099 | -2.95929  | 0.774403 |
| SO2Nongzhanguan  | 11.2326  | 7.42861 | 0.441601 |  0.721683 |   0.723726 | -3.1604   | 0.832965 |
| SO2Shunyi        |  9.8409  | 5.86093 | 0.446522 |  0.676768 |   0.677877 | -0.486069 | 0.801606 |
| SO2Tiantan       | 10.012   | 6.50674 | 0.303385 |  0.631648 |   0.631726 | -2.30904  | 0.775886 |
| SO2Wanliu        | 10.0817  | 6.43075 | 0.516313 |  0.754552 |   0.754858 | -2.60071  | 0.854484 |
| SO2Wanshouxigong | 11.305   | 6.84543 | 0.4534   |  0.703381 |   0.726278 | -2.12324  | 0.822012 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/batch_multioutput_SO2_Aotizhongxin.gif)


<div align="center"> 

|                  |     RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|---------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| SO2Aotizhongxin  | 10.5567  | 6.242   | 0.494966 |  0.709714 |   0.725545 | -1.26525  | 0.815555 |
| SO2Changping     |  9.09494 | 5.75417 | 0.322389 |  0.658246 |   0.676473 | -2.81689  | 0.783347 |
| SO2Dingling      |  6.91759 | 4.53387 | 0.476386 |  0.694153 |   0.633918 | -0.580053 | 0.806454 |
| SO2Dongsi        | 10.5434  | 6.59247 | 0.5027   |  0.719887 |   0.740367 | -1.82087  | 0.819507 |
| SO2Guanyuan      | 10.7953  | 6.29625 | 0.492111 |  0.707091 |   0.712868 | -1.24925  | 0.812208 |
| SO2Gucheng       | 13.0363  | 5.74604 | 0.263081 |  0.577021 |   0.772393 | -0.592804 | 0.734487 |
| SO2Huairou       |  7.70609 | 4.72287 | 0.281389 |  0.642457 |   0.635849 | -2.1212   | 0.780624 |
| SO2Nongzhanguan  | 10.6487  | 6.59717 | 0.49815  |  0.717827 |   0.720983 | -1.68306  | 0.825056 |
| SO2Shunyi        | 10.0172  | 5.75588 | 0.426515 |  0.654673 |   0.656088 |  0.41268  | 0.752152 |
| SO2Tiantan       | 10.471   | 6.40765 | 0.238045 |  0.56171  |   0.591422 | -2.07053  | 0.720224 |
| SO2Wanliu        |  9.88257 | 6.71018 | 0.535232 |  0.75216  |   0.759192 | -2.50576  | 0.830969 |
| SO2Wanshouxigong | 11.0073  | 6.13021 | 0.481811 |  0.697839 |   0.745976 | -0.907208 | 0.806317 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/batch_multioutput_SO2_Aotizhongxin.gif)








<p align="center">CO Forecasting (batch multioutput)</p>

<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| COAotizhongxin  | 795.218 | 462.133 | 0.680071 |  0.83231  |   0.727821 |  89.5121  | 0.887508 |
| COChangping     | 688.009 | 401.648 | 0.648409 |  0.810325 |   0.721248 |  34.6882  | 0.873332 |
| CODingling      | 567.211 | 319.052 | 0.668768 |  0.822046 |   0.764742 | -17.3843  | 0.883149 |
| CODongsi        | 772.144 | 454.44  | 0.629102 |  0.794673 |   0.72088  |  -7.10725 | 0.868422 |
| COGuanyuan      | 719.088 | 422.382 | 0.657616 |  0.812856 |   0.719419 |   3.12685 | 0.881207 |
| COGucheng       | 704.327 | 416.66  | 0.687514 |  0.830697 |   0.730232 | -19.9298  | 0.895479 |
| COHuairou       | 530.861 | 312.039 | 0.708615 |  0.845162 |   0.758012 | -11.0362  | 0.901596 |
| CONongzhanguan  | 797.848 | 470.22  | 0.650417 |  0.808991 |   0.723506 |  30.3876  | 0.877193 |
| COShunyi        | 776.123 | 462.635 | 0.653433 |  0.816042 |   0.718451 |  17.0667  | 0.87228  |
| COTiantan       | 750.375 | 439.581 | 0.64869  |  0.809055 |   0.715213 |  19.1482  | 0.87462  |
| COWanliu        | 743.62  | 448.3   | 0.676633 |  0.82302  |   0.698364 |  10.2989  | 0.893438 |
| COWanshouxigong | 756.44  | 454.788 | 0.656946 |  0.813092 |   0.719947 |  -9.4424  | 0.879816 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/batch_multioutput_CO_Aotizhongxin.gif)


<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| COAotizhongxin  | 959.344 | 532.544 | 0.534381 |  0.776708 |   0.688587 | 195.192  | 0.793085 |
| COChangping     | 796.324 | 429.967 | 0.528991 |  0.738183 |   0.683486 |  81.1315 | 0.805376 |
| CODingling      | 674.881 | 341.115 | 0.531081 |  0.749758 |   0.743378 |  79.9529 | 0.797534 |
| CODongsi        | 873.531 | 509.961 | 0.525305 |  0.735696 |   0.675097 |  14.4213 | 0.798439 |
| COGuanyuan      | 820.436 | 463.824 | 0.554303 |  0.755026 |   0.68186  |  41.1509 | 0.817278 |
| COGucheng       | 793.133 | 465.261 | 0.603746 |  0.786465 |   0.687233 | -17.036  | 0.845585 |
| COHuairou       | 661.221 | 369.864 | 0.547939 |  0.755129 |   0.702596 |  15.903  | 0.808124 |
| CONongzhanguan  | 899.621 | 513.619 | 0.555543 |  0.760563 |   0.694422 |  65.3917 | 0.814373 |
| COShunyi        | 931.919 | 538.334 | 0.500332 |  0.736242 |   0.657308 |  63.027  | 0.767748 |
| COTiantan       | 854.227 | 479.97  | 0.544719 |  0.752109 |   0.686026 |  38.5393 | 0.807976 |
| COWanliu        | 849.722 | 496.229 | 0.577772 |  0.763338 |   0.648926 |  31.124  | 0.840533 |
| COWanshouxigong | 858.225 | 503.984 | 0.558413 |  0.756496 |   0.686213 | -17.1623 | 0.820464 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/batch_multioutput_CO_Aotizhongxin.gif)



# Conclusions






