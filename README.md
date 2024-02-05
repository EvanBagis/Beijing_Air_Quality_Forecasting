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









<p align="center">PM10 Forecasting (incremental recursive)</p>








<p align="center">PM2.5 Forecasting (incremental recursive)</p>









<p align="center">NO2 Forecasting (incremental recursive)</p>









<p align="center">SO2 Forecasting (incremental recursive)</p>











<p align="center">CO Forecasting (incremental recursive)</p>





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





