# Beijing_Air_Quality_Forecasting
## Introduction

This repository implements teo (3) different forecasting frameworks. The frameworks are tested on the [Beijing Air Quality Dataset](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data).

- **Approach 1: Incremental recursive forecasting** uses the river python library to implement an incremental forecasting model that aims to forecast 12 hours in the future. The model accepts 24 lag features from the time series that will be forecasted. The approach is a recursive one where the model initially accepts the last 24 observations to predict the future value one step ahead. The prediction becomes the last value of the input instance to predict the future value 2 steps ahead and so on. The model is implemented with the [river](https://riverml.xyz/0.21.0/) package.

- **Batch recursive forecasting**



- **Batch multioutput forecasting**





### Conceptual framework






### Results
<p align="center">O3 Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|--------:|---------:|
| O3_Aotizhongxin  | 37.2926 | 26.0634 | 0.580813 |  0.767332 |   0.725385 | 1.54928 | 0.867765 |
| O3_Changping     | 37.2639 | 25.82   | 0.531569 |  0.736825 |   0.717908 | 1.16114 | 0.847615 |
| O3_Dingling      | 42.4422 | 27.7365 | 0.590547 |  0.778291 |   0.714402 | 1.00072 | 0.875868 |
| O3_Dongsi        | 43.5108 | 26.0964 | 0.450383 |  0.685029 |   0.727775 | 2.23128 | 0.810735 |
| O3_Guanyuan      | 37.8856 | 26.3388 | 0.56273  |  0.756244 |   0.723974 | 1.55226 | 0.860735 |
| O3_Gucheng       | 36.7106 | 25.9657 | 0.602942 |  0.78107  |   0.721255 | 1.9712  | 0.876157 |
| O3_Huairou       | 38.4224 | 26.8581 | 0.550955 |  0.750594 |   0.698576 | 1.95355 | 0.857386 |
| O3_Nongzhanguan  | 38.2415 | 27.238  | 0.571042 |  0.76149  |   0.705387 | 1.69256 | 0.863666 |
| O3_Shunyi        | 37.5229 | 26.3415 | 0.532797 |  0.736631 |   0.680223 | 1.72882 | 0.84755  |
| O3_Tiantan       | 42.6512 | 27.9689 | 0.508904 |  0.722789 |   0.710817 | 1.60687 | 0.838449 |
| O3_Wanliu        | 35.4547 | 24.212  | 0.576317 |  0.764719 |   0.699465 | 1.67322 | 0.866211 |
| O3_Wanshouxigong | 36.8785 | 26.0998 | 0.584091 |  0.769595 |   0.721341 | 1.52191 | 0.868985 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/incremental recursive O3_Aotizhongxin.gif)




<p align="center">PM10 Forecasting (incremental recursive)</p>

<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| PM10_Aotizhongxin  | 84.8484 | 58.0001 | 0.208493 |  0.52876  |   0.53427  | -3.15336 | 0.716223 |
| PM10_Changping     | 73.8563 | 48.8643 | 0.227034 |  0.540253 |   0.547664 | -2.36222 | 0.7214   |
| PM10_Dingling      | 69.8128 | 45.5864 | 0.243429 |  0.558551 |   0.553931 | -2.54191 | 0.737221 |
| PM10_Dongsi        | 87.026  | 59.5741 | 0.214284 |  0.52884  |   0.511728 | -3.21358 | 0.713904 |
| PM10_Guanyuan      | 83.1785 | 57.0067 | 0.191209 |  0.516584 |   0.507274 | -3.69235 | 0.707711 |
| PM10_Gucheng       | 88.4208 | 62.4609 | 0.180024 |  0.496769 |   0.484002 | -4.05399 | 0.690914 |
| PM10_Huairou       | 75.1911 | 49.9608 | 0.219837 |  0.532665 |   0.547989 | -1.7549  | 0.716834 |
| PM10_Nongzhanguan  | 85.1352 | 58.4747 | 0.216752 |  0.52916  |   0.511797 | -2.36542 | 0.714223 |
| PM10_Shunyi        | 81.1966 | 54.6948 | 0.217995 |  0.523713 |   0.529963 | -1.49972 | 0.706658 |
| PM10_Tiantan       | 80.5486 | 55.3241 | 0.206613 |  0.518276 |   0.50125  | -2.61189 | 0.704961 |
| PM10_Wanliu        | 82.7469 | 57.1799 | 0.218619 |  0.542593 |   0.519999 | -4.8261  | 0.7278   |
| PM10_Wanshouxigong | 88.2194 | 60.7918 | 0.201042 |  0.514538 |   0.484502 | -2.8851  | 0.703938 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/incremental recursive PM10_Aotizhongxin.gif)




<p align="center">PM2.5 Forecasting (incremental recursive)</p>

<div align="center"> 

|                     |    RMSE |     MAE |       r2 |   Pearson |   Spearman |        MBE |       IA |
|:--------------------|--------:|--------:|---------:|----------:|-----------:|-----------:|---------:|
| PM2.5_Aotizhongxin  | 70.5705 | 45.4768 | 0.264615 |  0.575129 |   0.56759  | -0.884923  | 0.750771 |
| PM2.5_Changping     | 60.6511 | 38.389  | 0.298753 |  0.608273 |   0.606474 | -1.83955   | 0.774641 |
| PM2.5_Dingling      | 61.3019 | 38.1351 | 0.328828 |  0.628521 |   0.604914 | -1.17287   | 0.787714 |
| PM2.5_Dongsi        | 74.0451 | 48.6503 | 0.264529 |  0.571531 |   0.551357 | -1.46869   | 0.746852 |
| PM2.5_Guanyuan      | 69.0452 | 45.0745 | 0.278921 |  0.5875   |   0.560025 | -1.83562   | 0.759874 |
| PM2.5_Gucheng       | 69.1932 | 45.2245 | 0.308901 |  0.600766 |   0.558445 | -0.819572  | 0.766212 |
| PM2.5_Huairou       | 60.5294 | 38.346  | 0.277289 |  0.59203  |   0.599341 | -1.62169   | 0.763133 |
| PM2.5_Nongzhanguan  | 74.3062 | 48.5555 | 0.270333 |  0.572537 |   0.554079 | -0.0876712 | 0.746632 |
| PM2.5_Shunyi        | 68.9549 | 45.0852 | 0.294588 |  0.589975 |   0.565498 | -0.166875  | 0.758274 |
| PM2.5_Tiantan       | 69.247  | 45.8418 | 0.271561 |  0.577127 |   0.551569 | -0.981861  | 0.751592 |
| PM2.5_Wanliu        | 67.8309 | 43.7782 | 0.318736 |  0.612865 |   0.586164 | -1.92238   | 0.776467 |
| PM2.5_Wanshouxigong | 74.3531 | 48.5015 | 0.26339  |  0.56782  |   0.538682 | -0.522217  | 0.743766 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/incremental recursive PM2.5_Aotizhongxin.gif)




<p align="center">NO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| NO2_Aotizhongxin  | 32.1402 | 23.834  | 0.24566  |  0.543479 |   0.527637 | -0.838969 | 0.725801 |
| NO2_Changping     | 25.2256 | 18.6075 | 0.276202 |  0.566981 |   0.526763 | -0.74235  | 0.740022 |
| NO2_Dingling      | 21.6506 | 14.3372 | 0.32332  |  0.61206  |   0.562815 | -0.476287 | 0.775466 |
| NO2_Dongsi        | 29.7603 | 21.8094 | 0.254994 |  0.556854 |   0.533432 | -1.03003  | 0.737949 |
| NO2_Guanyuan      | 30.5643 | 22.5363 | 0.246508 |  0.556432 |   0.535726 | -1.55319  | 0.738516 |
| NO2_Gucheng       | 32.8889 | 24.6184 | 0.189728 |  0.512663 |   0.475695 | -1.11494  | 0.711579 |
| NO2_Huairou       | 22.1836 | 15.4131 | 0.288623 |  0.586366 |   0.588083 | -0.806725 | 0.75657  |
| NO2_Nongzhanguan  | 32.073  | 24.0664 | 0.226855 |  0.532609 |   0.503358 | -1.03677  | 0.72048  |
| NO2_Shunyi        | 27.2231 | 19.9532 | 0.258704 |  0.552892 |   0.51279  | -0.406913 | 0.733085 |
| NO2_Tiantan       | 27.5522 | 20.572  | 0.258563 |  0.55472  |   0.527737 | -1.15421  | 0.732978 |
| NO2_Wanliu        | 31.3144 | 23.1851 | 0.32951  |  0.612353 |   0.58637  | -1.53243  | 0.775101 |
| NO2_Wanshouxigong | 30.9517 | 22.8474 | 0.264488 |  0.569695 |   0.543399 | -1.60543  | 0.747852 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/incremental recursive NO2_Aotizhongxin.gif)
<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| NO2_Aotizhongxin  | 32.1402 | 23.834  | 0.24566  |  0.543479 |   0.527637 | -0.838969 | 0.725801 |
| NO2_Changping     | 25.2256 | 18.6075 | 0.276202 |  0.566981 |   0.526763 | -0.74235  | 0.740022 |
| NO2_Dingling      | 21.6506 | 14.3372 | 0.32332  |  0.61206  |   0.562815 | -0.476287 | 0.775466 |
| NO2_Dongsi        | 29.7603 | 21.8094 | 0.254994 |  0.556854 |   0.533432 | -1.03003  | 0.737949 |
| NO2_Guanyuan      | 30.5643 | 22.5363 | 0.246508 |  0.556432 |   0.535726 | -1.55319  | 0.738516 |
| NO2_Gucheng       | 32.8889 | 24.6184 | 0.189728 |  0.512663 |   0.475695 | -1.11494  | 0.711579 |
| NO2_Huairou       | 22.1836 | 15.4131 | 0.288623 |  0.586366 |   0.588083 | -0.806725 | 0.75657  |
| NO2_Nongzhanguan  | 32.073  | 24.0664 | 0.226855 |  0.532609 |   0.503358 | -1.03677  | 0.72048  |
| NO2_Shunyi        | 27.2231 | 19.9532 | 0.258704 |  0.552892 |   0.51279  | -0.406913 | 0.733085 |
| NO2_Tiantan       | 27.5522 | 20.572  | 0.258563 |  0.55472  |   0.527737 | -1.15421  | 0.732978 |
| NO2_Wanliu        | 31.3144 | 23.1851 | 0.32951  |  0.612353 |   0.58637  | -1.53243  | 0.775101 |
| NO2_Wanshouxigong | 30.9517 | 22.8474 | 0.264488 |  0.569695 |   0.543399 | -1.60543  | 0.747852 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/incremental recursive NO2_Aotizhongxin.gif)




<p align="center">SO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                   |    RMSE |      MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:------------------|--------:|---------:|---------:|----------:|-----------:|---------:|---------:|
| SO2_Aotizhongxin  | 17.5957 |  9.94094 | 0.405764 |  0.660785 |   0.727234 | 0.50315  | 0.79737  |
| SO2_Changping     | 15.488  |  8.53688 | 0.461465 |  0.693633 |   0.70123  | 0.52312  | 0.818145 |
| SO2_Dingling      | 12.5547 |  7.10407 | 0.35079  |  0.619855 |   0.633161 | 0.426143 | 0.769131 |
| SO2_Dongsi        | 17.7219 | 10.5564  | 0.405262 |  0.661194 |   0.682633 | 0.569823 | 0.799868 |
| SO2_Guanyuan      | 18.2275 | 10.2529  | 0.406012 |  0.66597  |   0.695198 | 0.316552 | 0.804158 |
| SO2_Gucheng       | 21.3597 |  8.73324 | 0.375979 |  0.650819 |   0.773658 | 0.404314 | 0.788993 |
| SO2_Huairou       | 14.9549 |  7.57749 | 0.375687 |  0.635847 |   0.646182 | 0.697864 | 0.776559 |
| SO2_Nongzhanguan  | 18.7322 | 10.9286  | 0.411181 |  0.668457 |   0.682571 | 0.43214  | 0.80588  |
| SO2_Shunyi        | 16.1294 |  8.8399  | 0.320221 |  0.598675 |   0.626344 | 0.874689 | 0.752368 |
| SO2_Tiantan       | 16.7737 |  9.18497 | 0.331436 |  0.604356 |   0.631442 | 0.78808  | 0.754049 |
| SO2_Wanliu        | 16.2063 |  9.31157 | 0.492537 |  0.716731 |   0.762933 | 0.26166  | 0.835994 |
| SO2_Wanshouxigong | 18.4314 | 10.1786  | 0.423608 |  0.672614 |   0.724283 | 0.556321 | 0.806141 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/incremental recursive SO2_Aotizhongxin.gif)




<p align="center">CO Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |     RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|---------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| CO_Aotizhongxin  |  996.087 | 608.716 | 0.357137 |  0.627091 |   0.555932 |  14.7712  | 0.778376 |
| CO_Changping     |  927.816 | 547.219 | 0.322649 |  0.611661 |   0.580772 | -10.8803  | 0.7691   |
| CO_Dingling      |  729.551 | 425.373 | 0.339916 |  0.62302  |   0.609657 |   8.79241 | 0.778737 |
| CO_Dongsi        |  971.439 | 595.987 | 0.346132 |  0.619248 |   0.549353 |   3.31989 | 0.775302 |
| CO_Guanyuan      |  958.623 | 594.581 | 0.310562 |  0.598481 |   0.531333 |  -9.9627  | 0.761523 |
| CO_Gucheng       |  960.27  | 589.213 | 0.396981 |  0.665008 |   0.58467  | -37.5254  | 0.80828  |
| CO_Huairou       |  793.658 | 477.928 | 0.213718 |  0.549488 |   0.547558 | -10.4776  | 0.7303   |
| CO_Nongzhanguan  | 1051.09  | 657.388 | 0.304189 |  0.591534 |   0.520793 |   3.71418 | 0.755517 |
| CO_Shunyi        | 1017.39  | 620.916 | 0.245915 |  0.557097 |   0.523942 |   7.34218 | 0.733372 |
| CO_Tiantan       |  982.117 | 619.672 | 0.312672 |  0.601139 |   0.516291 |  -3.59658 | 0.764394 |
| CO_Wanliu        | 1017.03  | 619.789 | 0.356805 |  0.632845 |   0.571347 | -10.8251  | 0.784974 |
| CO_Wanshouxigong | 1013.11  | 644.306 | 0.331338 |  0.612256 |   0.530534 |   2.19124 | 0.771517 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/incremental recursive CO_Aotizhongxin.gif)



### TODO

- define the spliting timestamps
- regular forecasting 1 (single station, only lags, reccursive)
- regular forecasting 2 (single station, all other covariates)
- advanced forecasting 1 (STCV forecasting)
- advanced forecasting 2 (multiple stations, multiple forecasting steps, multioutput)