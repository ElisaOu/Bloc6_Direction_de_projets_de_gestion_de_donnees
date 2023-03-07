# Bloc N° 6 Direction de projets de gestion de données
This project is a sprint for the demoday at Jedha Fullstack Bootcamp held on January 17th 2023 [Link to the demoday](https://youtu.be/cRNy1-rTXYg?t=2917).

# Prédire la consommation électrique: WATT a job!

[Slides used for the demoday](https://docs.google.com/presentation/d/1V10sNomsMMYLlvwJbftaKjHNslNxmAU7R3Xtqs5fT3c/edit#slide=id.ga5178bf3d4_2_0)

[Watt-a-job app](https://watt-a-job-app.herokuapp.com/)

[link to watt-a-job app in case it has been disconnected](https://share.vidyard.com/watch/L1Xucxqe1gNMHyHyLa5wDm?)

# About

5 people in the team, and a great subject to work on!

We have led our project around 3 main parts (data collection, Machine Learning and deployment).

To learn more about how the project was managed, please go the video link above

Here below the content of files with code, to help you navigate in the files:

## 0- Data collection and master file
- 0_0_weather: API request
- 0_1_prices: oil (RBRTEd.xls), electricity (ten00117_linear.csv) and gas (prix_gaz_naturel.csv) source data files of prices
- 0_2_conso_elec: source data file of electricity consumption
- 0_Create_master_dataset: merge of all datasets to create a single master file

## 1- Machine learning models
- 1_0_supervised_ml
  - 0-linear_regression_lasso: Linear regression using all features
  - 0bis-linear_regression_lasso_without_lags: linear regression excluding lags and windows
  - 1-Random_Forest: Random forest using all features
  - 1bis-Random_forest_without_lags: Random forest excluding lags and windows
  - 2-SGD: SGD using all features
  - 2bis-SGD_without_lag: SGD excluding lags and windows
  - 3-stack: stack excluding lags and windows
  - 4-Vote: vote excluding lags and windows
- 1-1_time_series
## 2- Deployment
- 2-1_API
- 2-2_Streamlit



Happy reading!
