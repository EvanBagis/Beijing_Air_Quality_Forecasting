# Beijing_Air_Quality_Forecasting
## Introduction
### Conceptual framework

### Results
<p align="center">O3 Forecasting (incremental recursive)</p>

<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |     MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|--------:|---------:|
| O3_Aotizhongxin | 36.8965 | 26.206  | 0.589671 |  0.769434 |   0.727027 | 1.67756 | 0.864245 |
| O3_Changping    | 36.489  | 25.5166 | 0.550848 |  0.744649 |   0.72921  | 1.5507  | 0.847123 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/O3/station=O3_Aotizhongxin.gif)



<p align="center">PM10 Forecasting (incremental recursive)</p>

<div align="center"> 

|                   |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:------------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| PM10_Aotizhongxin | 81.7281 | 56.392  | 0.265638 |  0.550185 |   0.550286 | -3.02448 | 0.721973 |
| PM10_Changping    | 70.9678 | 47.3576 | 0.286312 |  0.561449 |   0.568515 | -2.07087 | 0.726262 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM10/station=PM10_Aotizhongxin.gif)


<p align="center">PM2.5 Forecasting (incremental recursive)</p>

<div align="center"> 

|                    |    RMSE |     MAE |       r2 |   Pearson |   Spearman |       MBE |       IA |
|:-------------------|--------:|--------:|---------:|----------:|-----------:|----------:|---------:|
| PM2.5_Aotizhongxin | 67.3144 | 44.3056 | 0.330909 |  0.601158 |   0.576775 | -0.428074 | 0.760379 |
| PM2.5_Changping    | 58.0815 | 37.5036 | 0.356913 |  0.626477 |   0.615474 | -1.09951  | 0.780996 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/PM2.5/station=PM2.5_Aotizhongxin.gif)


<p align="center">NO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |    RMSE |     MAE |      r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|--------:|--------:|--------:|----------:|-----------:|----------:|---------:|
| NO2_Aotizhongxin | 31.1846 | 23.3236 | 0.28985 |  0.558611 |   0.542429 | -0.926497 | 0.724208 |
| NO2_Changping    | 24.287  | 18.0132 | 0.32906 |  0.591602 |   0.554678 | -0.82965  | 0.748695 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/station=NO2_Aotizhongxin.gif)
<div align="center"> 

|                  |    RMSE |     MAE |      r2 |   Pearson |   Spearman |       MBE |       IA |
|:-----------------|--------:|--------:|--------:|----------:|-----------:|----------:|---------:|
| NO2_Aotizhongxin | 31.1846 | 23.3236 | 0.28985 |  0.558611 |   0.542429 | -0.926497 | 0.724208 |
| NO2_Changping    | 24.287  | 18.0132 | 0.32906 |  0.591602 |   0.554678 | -0.82965  | 0.748695 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/NO2/station=NO2_Aotizhongxin.gif)



<p align="center">SO2 Forecasting (incremental recursive)</p>

<div align="center"> 

|                  |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:-----------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| SO2_Aotizhongxin | 16.845  | 9.5642  | 0.455382 |  0.683697 |   0.737945 | 0.688624 | 0.806793 |
| SO2_Changping    | 14.9766 | 8.30125 | 0.496441 |  0.710752 |   0.716355 | 0.645894 | 0.824948 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/SO2/station=SO2_Aotizhongxin.gif)


<p align="center">CO Forecasting (incremental recursive)</p>

<div align="center"> 

|                 |    RMSE |     MAE |       r2 |   Pearson |   Spearman |      MBE |       IA |
|:----------------|--------:|--------:|---------:|----------:|-----------:|---------:|---------:|
| CO_Aotizhongxin | 966.063 | 598.284 | 0.395307 |  0.641384 |   0.566211 | 19.2822  | 0.780875 |
| CO_Changping    | 886.218 | 531.083 | 0.382025 |  0.636212 |   0.59414  | -3.46301 | 0.779179 |

</div> 

![](https://github.com/EvanBagis/Beijing_Air_Quality_Forecasting/blob/master/gifs/CO/station=CO_Aotizhongxin.gif)


### TODO

- define the spliting timestamps
- regular forecasting 1 (single station, only lags, reccursive)
- regular forecasting 2 (single station, all other covariates)
- advanced forecasting 1 (STCV forecasting)
- advanced forecasting 2 (multiple stations, multiple forecasting steps, multioutput)