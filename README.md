# Beijing_Air_Quality_Forecasting
## Introduction

This repository implements two (2) different forecasting frameworks. The frameworks are tested on the [Beijing Air Quality Dataset](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data).

- **Approach 1: Incremental recursive forecasting** uses the [river](https://riverml.xyz/0.21.0/) python library to implement an incremental forecasting model that aims to forecast 12 hours in the future. The model accepts 24 lag features from the time series that will be forecasted. The approach is a recursive one where the model initially accepts the last 24 observations to predict the future value one step ahead. The prediction becomes the last value of the input instance to predict the future value 2 steps ahead and so on.



- **Approach 2: Batch multioutput forecasting** uses sklearn type models to perform multioutput forecasting. In this approach, the model accepts lagged features from multiple time series (each one corresponding to a specific station for this problem) and forecasts the following hours for all the time series simultaneously. The advantage of this approach is that the model not only learns from it's lags but also learns from the correlations between the other time series as well.





### Conceptual framework

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/frameworks_imgs/incremental_recursive_forecasting.png)


![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/frameworks_imgs/batch_multioutput_forecasting.png)

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



<p align="center">PM10 Forecasting (batch multioutput)</p>



<p align="center">PM2.5 Forecasting (batch multioutput)</p>



<p align="center">NO2 Forecasting (batch multioutput)</p>



<p align="center">SO2 Forecasting (batch multioutput)</p>

<div align="center"> 

|               |     RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:--------------|---------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| Aotizhongxin  |  9.41717 | 5.94078 | 0.598084 |  0.786951 |   0.773936 | -2.13404  | 0.860245 |
| Changping     |  8.21391 | 5.30421 | 0.447296 |  0.73594  |   0.718247 | -2.93525  | 0.83223  |
| Dingling      |  6.3289  | 4.17461 | 0.5617   |  0.762602 |   0.694864 | -1.27574  | 0.85426  |
| Dongsi        |  9.57258 | 6.28033 | 0.590012 |  0.782443 |   0.774283 | -2.13226  | 0.8533   |
| Guanyuan      |  9.71964 | 5.94648 | 0.588246 |  0.777132 |   0.769666 | -1.83237  | 0.852689 |
| Gucheng       | 10.3407  | 5.51595 | 0.5363   |  0.743397 |   0.770872 | -1.91283  | 0.834494 |
| Huairou       |  6.96704 | 4.44275 | 0.412914 |  0.724626 |   0.667835 | -2.33098  | 0.830356 |
| Nongzhanguan  |  9.57699 | 6.32369 | 0.594042 |  0.78743  |   0.768046 | -2.42188  | 0.861904 |
| Shunyi        |  8.7439  | 5.15299 | 0.563004 |  0.752531 |   0.734346 | -0.741619 | 0.840321 |
| Tiantan       |  8.89813 | 5.54211 | 0.449727 |  0.693034 |   0.673742 | -1.91445  | 0.802268 |
| Wanliu        |  8.9188  | 6.00794 | 0.621416 |  0.811395 |   0.80012  | -2.77723  | 0.879214 |
| Wanshouxigong | 10.0654  | 6.03403 | 0.566665 |  0.761953 |   0.766499 | -1.79577  | 0.844541 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/batch_multioutput_SO2_Aotizhongxin.gif)


<p align="center">CO Forecasting (batch multioutput)</p>

<div align="center"> 

|               |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:--------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| Aotizhongxin  | 836.6   | 470.507 | 0.645866 |  0.806733 |   0.763815 |  39.0379 | 0.875146 |
| Changping     | 738.13  | 410.45  | 0.595305 |  0.772848 |   0.757123 | -27.5401 | 0.865606 |
| Dingling      | 603.645 | 325.837 | 0.624838 |  0.790922 |   0.764384 | -25.6389 | 0.873291 |
| Dongsi        | 785.527 | 464.478 | 0.616083 |  0.786025 |   0.745663 | -44.8515 | 0.867234 |
| Guanyuan      | 771.561 | 433.473 | 0.605799 |  0.778612 |   0.754091 | -25.5299 | 0.865749 |
| Gucheng       | 768.117 | 437.182 | 0.628331 |  0.793596 |   0.75354  | -45.7525 | 0.877386 |
| Huairou       | 579.815 | 327.663 | 0.652362 |  0.809028 |   0.774038 | -35.1585 | 0.882299 |
| Nongzhanguan  | 833.002 | 474.947 | 0.618897 |  0.786934 |   0.76179  | -19.7366 | 0.869267 |
| Shunyi        | 814.919 | 476.588 | 0.617902 |  0.7899   |   0.739969 | -19.1054 | 0.859381 |
| Tiantan       | 782.744 | 447.724 | 0.617708 |  0.786853 |   0.755076 | -40.0306 | 0.86792  |
| Wanliu        | 800.674 | 454.828 | 0.625068 |  0.792178 |   0.75146  | -39.3074 | 0.880093 |
| Wanshouxigong | 778.814 | 469.63  | 0.636317 |  0.799902 |   0.755187 | -72.4079 | 0.876594 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/batch_multioutput_CO_Aotizhongxin.gif)



### TODO

- define the spliting timestamps
- regular forecasting 1 (single station, only lags, reccursive)
- regular forecasting 2 (single station, all other covariates)
- advanced forecasting 1 (STCV forecasting)
- advanced forecasting 2 (multiple stations, multiple forecasting steps, multioutput)